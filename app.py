import time
import streamlit as st
from utils.pdf_utils import pdf_to_image, get_page_count
from utils.image_utils import draw_word_boxes
from ocr_engines import tesseract_engine, easyocr_engine

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
        [72, 150, 200, 300],
        index=2,
        format_func=lambda x: {
            72:  "72  — fast preview",
            150: "150 — balanced",
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

col_m1, col_m2 = st.columns([1, 5])
col_m1.metric("Conversion time", f"{st.session_state['conversion_time']:.2f}s")
st.image(
    st.session_state["page_image"],
    caption=f"Page {st.session_state['ocr_page']} · {dpi} DPI",
    use_container_width=True,
)

# ── 3. OCR ───────────────────────────────────────────────────────
st.header("3 · Run OCR")

col_engine, col_run = st.columns([4, 1])
with col_engine:
    engine_choice = st.selectbox(
        "Engine",
        ["Tesseract", "EasyOCR", "Both (Compare)"],
        help=(
            "**Tesseract** — fast, rule-based, good on clean scans.\n\n"
            "**EasyOCR** — deep learning, slower but handles difficult scans better. "
            "Model downloads on first use (~100 MB)."
        ),
    )
with col_run:
    st.write("")
    run_clicked = st.button("Run OCR", type="primary", use_container_width=True)

conf_threshold = st.slider(
    "Confidence threshold",
    min_value=0, max_value=100, value=0,
    help="Filter words below this confidence score. 0 = show everything Tesseract/EasyOCR detected.",
)

if run_clicked:
    image = st.session_state["page_image"]
    engines_to_run = (
        ["Tesseract", "EasyOCR"] if engine_choice == "Both (Compare)" else [engine_choice]
    )
    results = {}
    for eng in engines_to_run:
        with st.spinner(f"Running {eng}..."):
            t0 = time.perf_counter()
            try:
                words = (
                    tesseract_engine.run_with_boxes(image)
                    if eng == "Tesseract"
                    else easyocr_engine.run_with_boxes(image)
                )
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


if len(results) == 1:
    name, data = next(iter(results.items()))
    words     = data["words"]
    text      = _text(words, conf_threshold)
    n_words   = len(_visible(words, conf_threshold))
    annotated = draw_word_boxes(image, words, conf_threshold)

    col_m1, col_m2, _ = st.columns([1, 1, 4])
    col_m1.metric("OCR time", f"{data['time']:.2f}s")
    col_m2.metric("Words found", n_words)

    col_img, col_text = st.columns(2)
    col_img.subheader(f"{name} — detected words")
    col_img.image(annotated, use_container_width=True)

    col_text.subheader("Extracted Text")
    col_text.text_area("", text, height=420, label_visibility="collapsed", key="text_single")
    if text.strip():
        col_text.download_button(
            "Download .txt",
            data=text,
            file_name=f"ocr_{name.lower()}_page_{page}.txt",
            mime="text/plain",
        )
    else:
        col_text.warning("No words at this confidence level — try lowering the threshold.")

else:
    names = list(results.keys())

    # Metrics
    col_t_time, col_t_words, col_e_time, col_e_words = st.columns(4)
    metric_cols = [
        (col_t_time, col_t_words),
        (col_e_time, col_e_words),
    ]
    for (col_time, col_words), name in zip(metric_cols, names):
        data    = results[name]
        n_words = len(_visible(data["words"], conf_threshold))
        col_time.metric(f"{name} — OCR time", f"{data['time']:.2f}s")
        col_words.metric(f"{name} — Words", n_words)

    # Annotated images
    col_left, col_right = st.columns(2)
    for col, name in zip([col_left, col_right], names):
        annotated = draw_word_boxes(image, results[name]["words"], conf_threshold)
        col.subheader(f"{name} — detected words")
        col.image(annotated, use_container_width=True)

    # Extracted texts
    st.subheader("Extracted Text")
    col_left, col_right = st.columns(2)
    for col, name in zip([col_left, col_right], names):
        words = results[name]["words"]
        text  = _text(words, conf_threshold)
        col.text_area(name, text, height=300, key=f"text_{name}")
        if text.strip():
            col.download_button(
                f"Download {name} .txt",
                data=text,
                file_name=f"ocr_{name.lower()}_page_{page}.txt",
                mime="text/plain",
                key=f"dl_{name}",
            )
        else:
            col.warning("No words at this confidence level.")
