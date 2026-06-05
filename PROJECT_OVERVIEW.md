# Project Overview — pdf-ocr-lab

**Last updated:** 2026-06-05 (V1 code written)

## What This Is
A free personal web app that lets a user upload a scanned PDF, choose a page, run OCR locally, and display the extracted text. No paid APIs. All OCR runs inside the app.

Portfolio goal: demonstrate Python, Streamlit, OCR, PDF processing, local ML model hosting, and free deployment skills.

## Current Status
**Phase: V1 code written — needs local test run.**

Next step: install dependencies locally and run `streamlit run app.py` to verify the pipeline works.

## Stack Decided
| Area | Choice | Reason |
|---|---|---|
| Language | Python | Primary language, best OCR library support |
| Web framework | Streamlit | Fast to build, free hosting options |
| OCR engine (v1) | Tesseract via pytesseract | Free, lightweight, good starting point |
| PDF to image | pdf2image + poppler | Standard, free |
| Image handling | Pillow | Standard |
| Hosting | Hugging Face Spaces (primary) | Free, ML-friendly, portfolio-visible |
| Code | GitHub (sfc38) | Personal account |

## What Is Built
- Project folder and documentation (CLAUDE.md, PROJECT_OVERVIEW.md, DESIGN_DECISIONS.md)
- `app.py` — full V1 Streamlit UI (upload → page select → image preview → OCR → text display → .txt download)
- `ocr_engines/tesseract_engine.py` — thin wrapper around pytesseract
- `utils/pdf_utils.py` — PDF to image conversion and page counting
- `utils/image_utils.py` — image serialization helper
- `requirements.txt`, `packages.txt` — dependency files

## What Is Decided
- Use Tesseract for Version 1 (no deep learning models yet).
- Load models lazily (only when user picks an engine), not at startup.
- Version 1 scope: upload → page select → image preview → OCR → text display → .txt download.
- Hosting: try Hugging Face Spaces first; Streamlit Community Cloud as backup.
- Repo name: `pdf-ocr-lab` on GitHub account `sfc38`.

## What Is NOT Decided Yet
- Whether to add a FastAPI backend later (future option, not needed for v1-v3).
- Exact UI layout and styling.
- Whether to add image preprocessing in V1 or wait until V2.
- Multi-language OCR support (Tesseract supports many languages).

## Version Roadmap Summary
| Version | Goal |
|---|---|
| V1 | Tesseract pipeline, local + deployed |
| V2 | EasyOCR, engine selector, side-by-side comparison |
| V3 | PaddleOCR, multi-page, confidence scores, comparison table |
| Future | Optional FastAPI backend, Docker |
