# utils/effects.py

import numpy as np

# ---------- Vignette Effect ----------
def apply_vignette(frame, strength=0.5):
    h, w = frame.shape[:2]

    # Create coordinate grid
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    xv, yv = np.meshgrid(x, y)

    # Distance from center
    dist = np.sqrt(xv**2 + yv**2)

    # Create mask (smooth falloff)
    mask = 1 - strength * dist
    mask = np.clip(mask, 0, 1)

    # Apply to all channels
    vignette = frame.astype(np.float32)
    for i in range(3):
        vignette[:, :, i] *= mask

    return vignette.astype(np.uint8)


# ---------- Color Grading ----------
def apply_color_grade(frame):
    f = frame.astype(np.float32)

    # Slight brightness boost
    f = f * 1.1

    # Channel tweaks
    f[:, :, 0] *= 1.2  # blue boost
    f[:, :, 1] *= 1.1
    f[:, :, 2] *= 0.85

    return np.clip(f, 0, 255).astype(np.uint8)