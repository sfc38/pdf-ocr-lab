---
title: Pdf Ocr Lab
colorFrom: pink
colorTo: purple
sdk: docker
pinned: false
---

# Local OCR Lab

A web app that extracts text from scanned PDF pages using locally hosted OCR engines — no external APIs.

**Live demo:** [huggingface.co/spaces/sfc38/pdf-ocr-lab](https://huggingface.co/spaces/sfc38/pdf-ocr-lab)

---

## What it does

- Upload a scanned PDF
- Select a page
- Preview the page image
- Run OCR and display the extracted text
- Download the result as a `.txt` file

---

## Tech stack

| Area | Tool |
|---|---|
| Language | Python |
| Web framework | Streamlit |
| OCR engine | Tesseract (v1) |
| PDF to image | pdf2image + Poppler |
| Deployment | Hugging Face Spaces (Docker) |

---

## Run locally

### With Docker

```bash
docker build -t pdf-ocr-lab .
docker run -p 8501:7860 pdf-ocr-lab
```

Open http://localhost:8501

### Without Docker (Mac / Linux)

```bash
# Mac
brew install tesseract poppler

# Ubuntu/Debian
sudo apt install tesseract-ocr poppler-utils

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## OCR engines roadmap

- [x] Tesseract
- [ ] EasyOCR
- [ ] PaddleOCR
- [ ] Side-by-side comparison mode

---

## Limitations

- OCR accuracy depends on scan quality
- Free hosting runs on CPU — heavier models will be slower
- Large PDFs are processed one page at a time
