from PIL import Image, ImageDraw
import pandas as pd
import io


def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def draw_word_boxes(image: Image.Image, words: pd.DataFrame, conf_threshold: int) -> Image.Image:
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    visible = words[(words["conf"] >= conf_threshold) & (words["text"].str.strip() != "")]
    for _, row in visible.iterrows():
        x, y, w, h = row["left"], row["top"], row["width"], row["height"]
        draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
    return annotated
