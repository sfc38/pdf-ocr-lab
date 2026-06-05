import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from utils.image_utils import split_to_word_boxes


@st.cache_resource(show_spinner=False)
def _get_ocr():
    from paddleocr import PaddleOCR  # deferred — heavy dependency
    return PaddleOCR(use_angle_cls=True, lang="en", show_log=False)


def preload() -> None:
    _get_ocr()


def run_with_boxes(image: Image.Image) -> pd.DataFrame:
    ocr = _get_ocr()
    result = ocr.ocr(np.array(image), cls=True)

    rows = []
    detections = result[0] if result and result[0] else []
    for line in detections:
        if line is None:
            continue
        bbox, (text, conf) = line[0], line[1]
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        rows.append({
            "text": text,
            "conf": round(float(conf) * 100, 1),
            "left": int(min(xs)),
            "top": int(min(ys)),
            "width": int(max(xs) - min(xs)),
            "height": int(max(ys) - min(ys)),
        })

    df = pd.DataFrame(rows, columns=["text", "conf", "left", "top", "width", "height"])
    return split_to_word_boxes(df)
