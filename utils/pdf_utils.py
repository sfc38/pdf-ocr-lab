from pdf2image import convert_from_bytes
from PIL import Image


def pdf_to_image(pdf_bytes: bytes, page_number: int) -> Image.Image:
    images = convert_from_bytes(
        pdf_bytes,
        first_page=page_number,
        last_page=page_number,
    )
    return images[0]


def get_page_count(pdf_bytes: bytes) -> int:
    images = convert_from_bytes(pdf_bytes, dpi=30)  # low DPI just for counting
    return len(images)
