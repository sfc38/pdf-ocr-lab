import logging
import os
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# Must be set before paddle is imported — disables oneDNN (MKL-DNN) which hits an
# unimplemented ConvertPirAttribute2RuntimeAttribute path on HF Spaces CPU hardware.
os.environ.setdefault("FLAGS_use_mkldnn", "0")

# suppress the verbose PaddleOCR/PaddlePaddle console output
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("paddle").setLevel(logging.ERROR)


@st.cache_resource(show_spinner=False)
def _get_ocr():
    from paddleocr import PaddleOCR  # deferred — heavy dependency
    return PaddleOCR(lang="en", enable_mkldnn=False)


def preload() -> None:
    _get_ocr()


def run_with_boxes(image: Image.Image) -> pd.DataFrame:
    ocr = _get_ocr()
    result = ocr.ocr(np.array(image))

    rows = []
    detections = result[0] if result and result[0] else []
    for line in detections:
        if line is None:
            continue
        bbox = line[0]
        text_info = line[1]
        if not isinstance(text_info, (list, tuple)) or len(text_info) < 2:
            continue
        text = str(text_info[0])
        conf = float(text_info[1])
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
