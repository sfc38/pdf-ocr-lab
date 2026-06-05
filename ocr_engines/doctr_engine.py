import io
import os
os.environ.setdefault("USE_TORCH", "1")  # prefer torch backend; doctr auto-detects if only one is available

import pandas as pd
import streamlit as st
from PIL import Image


@st.cache_resource(show_spinner=False)
def _get_model():
    from doctr.models import ocr_predictor  # deferred — heavy dependency
    return ocr_predictor(pretrained=True)


def preload() -> None:
    _get_model()


def run_with_boxes(image: Image.Image) -> pd.DataFrame:
    from doctr.io import DocumentFile

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    model = _get_model()
    doc = DocumentFile.from_images([img_bytes])
    result = model(doc)

    w, h = image.width, image.height
    rows = []
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    (x_min, y_min), (x_max, y_max) = word.geometry
                    rows.append({
                        "text": word.value,
                        "conf": round(float(word.confidence) * 100, 1),
                        "left": int(x_min * w),
                        "top": int(y_min * h),
                        "width": int((x_max - x_min) * w),
                        "height": int((y_max - y_min) * h),
                    })

    return pd.DataFrame(rows, columns=["text", "conf", "left", "top", "width", "height"])
