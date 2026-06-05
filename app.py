import streamlit as st
from utils.pdf_utils import pdf_to_image, get_page_count
from ocr_engines import tesseract_engine

st.set_page_config(page_title="Local OCR Lab", layout="centered")
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

        st.subheader("Page Preview")
        st.image(image, use_container_width=True)

        with st.spinner("Running Tesseract OCR..."):
            try:
                text = tesseract_engine.run(image)
            except Exception as e:
                st.error(f"OCR failed: {e}")
                st.stop()

        st.subheader("Extracted Text")

        if text.strip():
            st.text_area("OCR Output", text, height=300)
            st.download_button(
                label="Download as .txt",
                data=text,
                file_name=f"ocr_page_{page_number}.txt",
                mime="text/plain",
            )
        else:
            st.warning("No text was extracted. The page may be a photo or the scan quality may be too low.")
