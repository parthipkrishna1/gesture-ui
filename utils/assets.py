# utils/assets.py

import cv2
import glob

# ---------- Load PNG with Alpha ----------
def load_png(path, size=(80, 80)):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, size)

    if img.shape[2] == 3:
        return img, None

    return img[:, :, :3], img[:, :, 3]


# ---------- Overlay PNG ----------
def overlay(frame, icon, x, y):
    bgr, alpha = icon
    h, w, _ = bgr.shape

    if y < 0 or x < 0 or y + h > frame.shape[0] or x + w > frame.shape[1]:
        return

    roi = frame[y:y+h, x:x+w]

    if alpha is None:
        frame[y:y+h, x:x+w] = bgr
        return

    alpha = alpha / 255.0

    for c in range(3):
        roi[:, :, c] = (1 - alpha) * roi[:, :, c] + alpha * bgr[:, :, c]

    frame[y:y+h, x:x+w] = roi


# ---------- Load Hologram Sequence ----------
def load_sequence(folder):
    files = sorted(glob.glob(folder + "/*.png"))
    frames = []

    for f in files:
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        if img is not None:
            frames.append(img)

    return frames