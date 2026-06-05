# pdf-ocr-lab — Claude Code Instructions

## Project Purpose
A free personal web app (Streamlit + Python) to upload scanned PDFs, choose a page, and run OCR locally using downloaded models. No paid OCR APIs. Built as a portfolio project.

## Core Rule: Free Only
Never recommend or add any paid service, API, or SDK (no Google Vision, AWS Textract, Azure OCR, OpenAI, etc.). All OCR must run locally inside the app or on self-hosted infrastructure.

## Session Continuity Files
Every session must maintain two files:

- **PROJECT_OVERVIEW.md** — living document of the current state of the project (stack, decisions made, what's built, what's next). Update it whenever a significant decision is finalized or a feature is completed.
- **DESIGN_DECISIONS.md** — append-only log. Every time we make a design decision (choosing a library, changing architecture, picking hosting, etc.), add a new dated entry. Never delete old entries — they capture why we made past choices.

Always read both files at the start of a session to restore context.

## Tech Stack (current)
- Language: Python
- Web framework: Streamlit
- OCR v1: Tesseract (via pytesseract)
- PDF to image: pdf2image + poppler
- Image handling: Pillow
- Hosting target: Hugging Face Spaces (primary), Streamlit Community Cloud (backup)
- Code: GitHub (personal account: sfc38)

## Project Folder Structure
```
pdf-ocr-lab/
  app.py
  requirements.txt
  packages.txt
  CLAUDE.md
  PROJECT_OVERVIEW.md
  DESIGN_DECISIONS.md

  ocr_engines/
    __init__.py
    tesseract_engine.py
    easyocr_engine.py      (future)
    paddle_engine.py       (future)

  utils/
    __init__.py
    pdf_utils.py
    image_utils.py

  samples/                 (example scanned PDFs)
```

## Development Rules
- Build incrementally: get Version 1 (Tesseract only) fully working before adding more OCR engines.
- Load OCR models lazily (only when user selects them), not at app startup.
- Use `@st.cache_resource` for heavier models (EasyOCR, PaddleOCR) to avoid reload on every click.
- Keep Version 1 simple: upload PDF → select page → show image → run OCR → show text → download .txt.
- Do not add features beyond the current version goal.

## Version Roadmap
- **V1**: Tesseract only — full pipeline works locally and deployed
- **V2**: Add EasyOCR, engine selector, side-by-side comparison, image preprocessing
- **V3**: Add PaddleOCR, confidence scores, multi-page OCR, comparison table

## GitHub
Repo name: `pdf-ocr-lab`
Account: sfc38 (personal)
