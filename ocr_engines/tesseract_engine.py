import pytesseract
from PIL import Image


def run(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)
