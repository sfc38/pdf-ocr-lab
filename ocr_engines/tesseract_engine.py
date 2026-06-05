import pytesseract
import pandas as pd
from PIL import Image


def preload() -> None:
    pass  # Tesseract is a CLI binary — no model to load into memory


def run(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)


def run_with_boxes(image: Image.Image) -> pd.DataFrame:
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    df = pd.DataFrame(data)
    # level 5 = word-level bounding boxes
    return df[df["level"] == 5].reset_index(drop=True)
