# utils/drawing.py

from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ---------- Hologram Text Drawing ----------
def draw_text(frame, text, pos, font_path, size, color, align="left"):
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, size)

    # Measure text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]

    x, y = pos

    # Alignment handling
    if align == "right":
        x -= text_w
    elif align == "center":
        x -= text_w // 2

    # ---------- HOLOGRAM EFFECT COLORS ----------
    outer_glow = (120, 40, 0)
    inner_glow = (255, 140, 0)
    core = (255, 255, 200)

    # Outer glow layer
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outer_glow)

    # Inner glow layer
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=inner_glow)

    # Core text (sharp)
    draw.text((x, y), text, font=font, fill=core)

    return np.array(img_pil)