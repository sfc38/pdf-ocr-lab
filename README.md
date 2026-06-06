---
title: Pdf Ocr Lab
colorFrom: pink
colorTo: purple
sdk: docker
pinned: false
---

# Local OCR Lab

A web app that extracts text from scanned PDF pages using locally hosted OCR engines — no external APIs, no paid services. All processing happens inside the container.

**Live demo:** [huggingface.co/spaces/sfc38/pdf-ocr-lab](https://huggingface.co/spaces/sfc38/pdf-ocr-lab)

---

## Features

- Upload a scanned PDF and select a page
- Control image quality with DPI selector (72 / 150 / 180 / 200 / 300)
- Run OCR with any of 4 engines — or all at once for side-by-side comparison
- Bounding box overlay showing detected words / regions
- Confidence threshold slider — filter noise without re-running OCR
- Separate timing for model load vs OCR inference
- Download extracted text as `.txt`
- **Comparison metrics**
  - Jaccard word overlap matrix between engines (no reference needed)
  - CER and WER per engine when you paste reference text

---

## OCR engines

| Engine | Type | License | Box level |
|---|---|---|---|
| Tesseract | Rule-based | Apache 2.0 | Word |
| EasyOCR | Deep learning | Apache 2.0 | Detection region |
| PaddleOCR v5 | Deep learning | Apache 2.0 | Detection region |
| DocTR | Deep learning | Apache 2.0 | Word |

All engines are free for commercial use.

---

## Tech stack

| Area | Tool |
|---|---|
| Language | Python |
| Web framework | Streamlit |
| PDF to image | pdf2image + Poppler |
| Image annotation | Pillow |
| Metrics | CER / WER / Jaccard (no external lib) |
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
sudo apt install tesseract-ocr poppler-utils libgl1 libglib2.0-0 libgomp1

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

> Note: deep learning engines (EasyOCR, PaddleOCR, DocTR) require Python ≤ 3.12 locally. The Docker image uses Python 3.11.

---

## Limitations

- Deep learning engines take 20–60 s per page on CPU; model weights (~100–200 MB each) download on first use
- Free HF Spaces tier is CPU-only
- OCR accuracy depends on scan quality — higher DPI generally helps
- Large PDFs are processed one page at a time
