---
title: Pdf Ocr Lab
colorFrom: pink
colorTo: purple
sdk: docker
pinned: false
---

# Local OCR Lab

A web app that extracts text from scanned PDF pages using locally hosted OCR engines — no external APIs, no paid services.

**Live demo:** [huggingface.co/spaces/sfc38/pdf-ocr-lab](https://huggingface.co/spaces/sfc38/pdf-ocr-lab)

---

## What it does

- Upload a scanned PDF and select a page
- Control image quality with DPI selector (72–300)
- Run OCR with any of 4 engines — or all at once for side-by-side comparison
- Visualise detected words/regions with bounding boxes
- Tune a confidence threshold to filter noise
- Download extracted text as `.txt`
- Compare engines with Jaccard word overlap (no reference needed) or CER/WER (paste reference text)

---

## OCR engines

| Engine | Type | License | Box level |
|---|---|---|---|
| Tesseract | Rule-based | Apache 2.0 | Word |
| EasyOCR | Deep learning | Apache 2.0 | Detection region |
| PaddleOCR v5 | Deep learning | Apache 2.0 | Detection region |
| DocTR | Deep learning | Apache 2.0 | Word |

All engines run locally inside the container. No data leaves the app.

---

## Tech stack

| Area | Tool |
|---|---|
| Language | Python |
| Web framework | Streamlit |
| PDF to image | pdf2image + Poppler |
| Image annotation | Pillow |
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

---

## Limitations

- Deep learning engines (EasyOCR, PaddleOCR, DocTR) take 20–60 s per page on CPU
- Model weights (~100–200 MB per engine) download on first use and are cached after that
- Free HF Spaces tier is CPU-only — GPU would be ~10× faster
- OCR accuracy depends on scan quality; higher DPI generally helps
- Large PDFs processed one page at a time
