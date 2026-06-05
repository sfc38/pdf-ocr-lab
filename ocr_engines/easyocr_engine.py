import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image


@st.cache_resource(show_spinner="Loading EasyOCR model (first run only)...")
def _get_reader():
    import easyocr  # deferred — not available on Python 3.13+
    return easyocr.Reader(["en"], gpu=False)


def run_with_boxes(image: Image.Image) -> pd.DataFrame:
    reader = _get_reader()
    results = reader.readtext(np.array(image))

    rows = []
    for bbox, text, conf in results:
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        rows.append({
            "text": text,
            "conf": round(conf * 100, 1),
            "left": int(min(xs)),
            "top": int(min(ys)),
            "width": int(max(xs) - min(xs)),
            "height": int(max(ys) - min(ys)),
        })

    return pd.DataFrame(rows, columns=["text", "conf", "left", "top", "width", "height"])
