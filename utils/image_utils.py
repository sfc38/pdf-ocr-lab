from PIL import Image, ImageDraw
import pandas as pd
import io


def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def split_to_word_boxes(df: pd.DataFrame) -> pd.DataFrame:
    """Split phrase-level detections (EasyOCR/PaddleOCR) into word-level boxes
    by dividing the bounding box width proportionally by character count."""
    rows = []
    for _, row in df.iterrows():
        words = str(row["text"]).split()
        if not words:
            continue
        if len(words) == 1:
            rows.append(row.to_dict())
            continue
        total_chars = sum(len(w) for w in words)
        x = int(row["left"])
        for word in words:
            w = max(1, int(row["width"] * len(word) / total_chars))
            rows.append({
                "text": word,
                "conf": float(row["conf"]),
                "left": x,
                "top": int(row["top"]),
                "width": w,
                "height": int(row["height"]),
            })
            x += w
    if not rows:
        return pd.DataFrame(columns=["text", "conf", "left", "top", "width", "height"])
    return pd.DataFrame(rows).reset_index(drop=True)


def draw_word_boxes(image: Image.Image, words: pd.DataFrame, conf_threshold: int) -> Image.Image:
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    visible = words[(words["conf"] >= conf_threshold) & (words["text"].str.strip() != "")]
    for _, row in visible.iterrows():
        x, y, w, h = row["left"], row["top"], row["width"], row["height"]
        draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
    return annotated
