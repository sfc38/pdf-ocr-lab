# Design Decisions Log — pdf-ocr-lab

This is an append-only log. Each entry records a decision, why it was made, and any alternatives that were considered. Never delete entries.

---

## 2026-06-05 — Project Kickoff

**Decision:** Start with Tesseract OCR for Version 1, not a deep learning model.

**Why:** Tesseract is free, lightweight, easy to install as a system package, and the simplest way to prove the full PDF → image → OCR → text pipeline works end-to-end. Deep learning models (EasyOCR, PaddleOCR) are heavier and harder to deploy on free hosting — no point fighting that until the pipeline is validated.

**Alternatives considered:** Starting with EasyOCR directly (rejected — too heavy for a first version).

---

## 2026-06-05 — Stack Selection

**Decision:** Python + Streamlit + Hugging Face Spaces.

**Why:** Streamlit is the fastest way to build a functional web UI in Python. Hugging Face Spaces is the best free hosting for ML-adjacent projects — better support for system packages (`packages.txt`) and heavier models than Streamlit Community Cloud. Personal GitHub account `sfc38` for code storage.

**Alternatives considered:**
- FastAPI backend: deferred to future, not needed for v1-v3.
- Streamlit Community Cloud: kept as backup; may struggle with system-level dependencies.
- Render Free: option for FastAPI backend later, not now.

---

## 2026-06-05 — Lazy Model Loading

**Decision:** Load OCR models only when the user selects them, not at app startup.

**Why:** Loading all engines at startup would make the app slow or crash on free CPU hosting. Using `@st.cache_resource` for heavier models prevents reloading on every button click while still deferring the initial load.

---

## 2026-06-05 — Free-Only Constraint

**Decision:** The project will never use paid OCR APIs or paid hosting.

**Why:** This is a personal portfolio project. The explicit goal is to demonstrate that a fully functional OCR app can be built and hosted for free using open-source tools. Paid services (Google Vision, AWS Textract, Azure OCR, OpenAI) are permanently off the table.

---

## 2026-06-05 — Docker for Deployment

**Decision:** Use a Dockerfile for Hugging Face Spaces deployment (and local portability).

**Why:** HF Spaces dropped native Streamlit support — Docker is now required for all Streamlit apps there. The Dockerfile also solves cross-platform local dev: it bundles `tesseract-ocr` and `poppler-utils` so anyone on Mac, Linux, or Windows can run the app without manually installing system packages.

**Alternatives considered:** Streamlit Community Cloud (no Docker needed, but limited system package support for heavier models in V2/V3). Kept as a backup option.

---
