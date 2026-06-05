import time
import streamlit as st
from utils.pdf_utils import pdf_to_image, get_page_count
from utils.image_utils import draw_word_boxes
from ocr_engines import tesseract_engine, easyocr_engine, paddle_engine

st.set_page_config(page_title="Local OCR Lab", layout="wide")
st.title("Local OCR Lab")
st.caption("Extract text from scanned PDFs using locally hosted OCR engines — no external APIs.")

# ── 1. Upload ────────────────────────────────────────────────────
st.header("1 · Upload PDF")
uploaded_file = st.file_uploader("PDF file", type=["pdf"], label_visibility="collapsed")

if not uploaded_file:
    st.stop()

pdf_bytes = uploaded_file.read()
with st.spinner("Reading PDF..."):
    try:
        total_pages = get_page_count(pdf_bytes)
    except Exception as e:
        st.error(f"Could not read PDF: {e}")
        st.stop()

st.success(f"{total_pages} page{'s' if total_pages != 1 else ''} found")

# ── 2. Convert Page ──────────────────────────────────────────────
st.header("2 · Select Page & Convert")

col_page, col_dpi, col_btn = st.columns([2, 2, 1])
with col_page:
    page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
with col_dpi:
    dpi = st.selectbox(
        "DPI",
        [72, 150, 180, 200, 300],
        index=3,
        format_func=lambda x: {
            72:  "72  — fast preview",
            150: "150 — balanced",
            180: "180 — good quality",
            200: "200 — recommended",
            300: "300 — high quality",
        }[x],
    )
with col_btn:
    st.write("")
    convert_clicked = st.button("Convert", type="primary", use_container_width=True)

if convert_clicked:
    t0 = time.perf_counter()
    with st.spinner("Converting page to image..."):
        try:
            image = pdf_to_image(pdf_bytes, page_number, dpi=dpi)
        except Exception as e:
            st.error(f"Could not convert page: {e}")
            st.stop()
    st.session_state.update({
        "page_image": image,
        "conversion_time": time.perf_counter() - t0,
        "ocr_page": page_number,
        "ocr_results": {},
    })

if "page_image" not in st.session_state:
    st.info("Select a page and DPI, then click **Convert**.")
    st.stop()

col_m1, _ = st.columns([1, 5])
col_m1.metric("Conversion time", f"{st.session_state['conversion_time']:.2f}s")
st.image(
    st.session_state["page_image"],
    caption=f"Page {st.session_state['ocr_page']} · {dpi} DPI",
    use_container_width=True,
)

# ── 3. OCR ───────────────────────────────────────────────────────
st.header("3 · Run OCR")

ENGINES = ["Tesseract", "EasyOCR", "PaddleOCR", "Compare All"]
SLOW_ENGINES = {"EasyOCR", "PaddleOCR"}

col_engine, col_run = st.columns([4, 1])
with col_engine:
    engine_choice = st.selectbox(
        "Engine",
        ENGINES,
        help=(
            "**Tesseract** — fast, rule-based, great on clean scans.\n\n"
            "**EasyOCR** — deep learning, better on difficult/handwritten scans. Slow on CPU.\n\n"
            "**PaddleOCR** — deep learning, strong on real-world documents. Slow on CPU.\n\n"
            "**Compare All** — runs all three and shows results side by side."
        ),
    )
with col_run:
    st.write("")
    run_clicked = st.button("Run OCR", type="primary", use_container_width=True)

engines_to_run = (
    ["Tesseract", "EasyOCR", "PaddleOCR"] if engine_choice == "Compare All"
    else [engine_choice]
)

slow_selected = any(e in SLOW_ENGINES for e in engines_to_run)
if slow_selected:
    slow_names = [e for e in engines_to_run if e in SLOW_ENGINES]
    st.info(
        f"**{' and '.join(slow_names)}** run deep learning models on CPU. "
        "Expect **20–60 seconds per page**. "
        "Model weights (~100–200 MB) are downloaded automatically on first use and cached after that."
    )

conf_threshold = st.slider(
    "Confidence threshold",
    min_value=0, max_value=100, value=0,
    help=(
        "Only show words with confidence ≥ this value. "
        "Tesseract scores 0–100. EasyOCR and PaddleOCR tend to score 80–99, "
        "so the slider has the most effect in the upper range for those engines."
    ),
)

if run_clicked:
    image = st.session_state["page_image"]
    results = {}
    for eng in engines_to_run:
        with st.spinner(f"Running {eng}..."):
            t0 = time.perf_counter()
            try:
                if eng == "Tesseract":
                    words = tesseract_engine.run_with_boxes(image)
                elif eng == "EasyOCR":
                    words = easyocr_engine.run_with_boxes(image)
                else:
                    words = paddle_engine.run_with_boxes(image)
            except Exception as e:
                st.error(f"{eng} failed: {e}")
                continue
            results[eng] = {"words": words, "time": time.perf_counter() - t0}
    st.session_state["ocr_results"] = results

# ── 4. Results ───────────────────────────────────────────────────
results = st.session_state.get("ocr_results", {})
if not results:
    st.stop()

st.header("4 · Results")

image = st.session_state["page_image"]
page  = st.session_state["ocr_page"]


def _visible(words, threshold):
    return words[(words["conf"] >= threshold) & (words["text"].str.strip() != "")]

def _text(words, threshold):
    return " ".join(_visible(words, threshold)["text"].tolist())

def _conf_range(words):
    nonempty = words[words["text"].str.strip() != ""]
    if nonempty.empty:
        return None
    return int(nonempty["conf"].min()), int(nonempty["conf"].max())

def render_result(col_img, col_text, name, data, threshold, key_suffix):
    words     = data["words"]
    text      = _text(words, threshold)
    n_words   = len(_visible(words, threshold))
    annotated = draw_word_boxes(image, words, threshold)
    conf_range = _conf_range(words)

    col_img.subheader(name)
    m1, m2 = col_img.columns(2)
    m1.metric("OCR time", f"{data['time']:.2f}s")
    m2.metric("Words", n_words)
    if conf_range:
        col_img.caption(f"Confidence range: {conf_range[0]}–{conf_range[1]}")
    col_img.image(annotated, use_container_width=True)

    col_text.subheader("Extracted Text")
    col_text.text_area("", text, height=420, label_visibility="collapsed", key=f"text_{key_suffix}")
    if text.strip():
        col_text.download_button(
            "Download .txt",
            data=text,
            file_name=f"ocr_{name.lower()}_page_{page}.txt",
            mime="text/plain",
            key=f"dl_{key_suffix}",
        )
    else:
        col_text.warning("No words at this confidence level — try lowering the threshold.")


if len(results) == 1:
    name, data = next(iter(results.items()))
    col_img, col_text = st.columns(2)
    render_result(col_img, col_text, name, data, conf_threshold, name)

else:
    names = list(results.keys())
    n = len(names)
    img_cols  = st.columns(n)
    text_cols = st.columns(n)
    for i, name in enumerate(names):
        render_result(img_cols[i], text_cols[i], name, results[name], conf_threshold, name)
