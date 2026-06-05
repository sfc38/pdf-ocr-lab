import streamlit as st
from utils.pdf_utils import pdf_to_image, get_page_count
from utils.image_utils import draw_word_boxes
from ocr_engines import tesseract_engine

st.set_page_config(page_title="Local OCR Lab", layout="wide")
st.title("Local OCR Lab")
st.caption("Extract text from scanned PDFs using local OCR — no external APIs.")

uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.read()

    with st.spinner("Reading PDF..."):
        try:
            total_pages = get_page_count(pdf_bytes)
        except Exception as e:
            st.error(f"Could not read PDF: {e}")
            st.stop()

    st.write(f"Pages found: **{total_pages}**")

    page_number = st.number_input(
        "Select page", min_value=1, max_value=total_pages, value=1, step=1
    )

    if st.button("Run OCR", type="primary"):
        with st.spinner("Converting page to image..."):
            try:
                image = pdf_to_image(pdf_bytes, page_number)
            except Exception as e:
                st.error(f"Could not convert page: {e}")
                st.stop()

        with st.spinner("Running Tesseract OCR..."):
            try:
                words = tesseract_engine.run_with_boxes(image)
            except Exception as e:
                st.error(f"OCR failed: {e}")
                st.stop()

        st.session_state["ocr_image"] = image
        st.session_state["ocr_words"] = words
        st.session_state["ocr_page"] = page_number

if "ocr_words" in st.session_state:
    words = st.session_state["ocr_words"]
    image = st.session_state["ocr_image"]
    page = st.session_state["ocr_page"]

    conf_threshold = st.slider(
        "Confidence threshold",
        min_value=0, max_value=100, value=0,
        help="Show bounding boxes only for words with confidence >= this value. "
             "Tesseract scores 0–100; below ~40 is usually noise.",
    )

    visible_words = words[(words["conf"] >= conf_threshold) & (words["text"].str.strip() != "")]
    text = " ".join(visible_words["text"].tolist())
    word_count = len(visible_words)

    st.caption(f"{word_count} word{'s' if word_count != 1 else ''} above threshold")

    annotated = draw_word_boxes(image, words, conf_threshold)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Page")
        st.image(image, use_container_width=True)
    with col2:
        st.subheader("Detected Words")
        st.image(annotated, use_container_width=True)

    st.subheader("Extracted Text")
    if text.strip():
        st.text_area("OCR Output", text, height=300)
        st.download_button(
            label="Download as .txt",
            data=text,
            file_name=f"ocr_page_{page}.txt",
            mime="text/plain",
        )
    else:
        st.warning("No words found at this confidence level. Try lowering the threshold.")
