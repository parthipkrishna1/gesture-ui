# main.py

import cv2
import mediapipe as mp
import time
import numpy as np

from config import heroes, hero_colors
from utils.effects import apply_vignette, apply_color_grade
from utils.drawing import draw_text
from utils.gestures import is_fist, is_pinch
from utils.assets import load_png, overlay, load_sequence


# ---------- MediaPipe Setup ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

# ---------- Load Assets ----------
icons = [
    load_png("assets/batman.png"),
    load_png("assets/superman.png"),
    load_png("assets/wonderwoman.png"),
    load_png("assets/flash.png"),
]

holograms = [
    load_sequence("assets/holo/batman"),
    load_sequence("assets/holo/superman"),
    load_sequence("assets/holo/wonderwoman"),
    load_sequence("assets/holo/flash"),
]

# ---------- State Variables ----------
selected_index = 0

smooth_x = None
prev_x = None
last_swipe_time = 0
direction = 0

locked = False
lock_cooldown = 0
prev_fist = False

hologram_active = False
prev_pinch = False
frame_idx = 0

# ---------- Fullscreen ----------
cv2.namedWindow("Gesture UI", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Gesture UI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# ---------- Main Loop ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Apply visual effects
    frame = apply_color_grade(frame)
    frame = apply_vignette(frame, strength=0.4)

    h, w, _ = frame.shape

    y_pos = int(h * 0.3)
    swipe_top = y_pos - 80
    swipe_bottom = y_pos + 80

    # ---------- Zones ----------
    swipe_zone = int(h * 0.32)
    holo_zone = int(h * 0.65)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    now = time.time()

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            landmarks = hand_landmarks.landmark

            # ---------- Lock (TOP ONLY) ----------
            fingers_closed = is_fist(landmarks)

            if fingers_closed and not prev_fist and now - lock_cooldown > 1.0 and swipe_top < y < swipe_bottom:
                locked = not locked
                lock_cooldown = now

            prev_fist = fingers_closed

            # ---------- Pinch (BOTTOM ONLY) ----------
            pinch = is_pinch(landmarks)
            in_holo_zone = y > holo_zone

            if pinch and not prev_pinch and in_holo_zone:
                hologram_active = not hologram_active

            prev_pinch = pinch

            # ---------- Swipe (TOP ONLY) ----------
            alpha = 0.6
            smooth_x = x if smooth_x is None else int(alpha * smooth_x + (1 - alpha) * x)

            if swipe_top < y < swipe_bottom:
                if prev_x is not None:
                    dx = smooth_x - prev_x

                    if not locked and abs(dx) > 25 and now - last_swipe_time > 0.25:

                        if dx > 0 and direction != 1:
                            selected_index = (selected_index - 1) % len(heroes)
                            direction = 1
                            hologram_active = False

                        elif dx < 0 and direction != -1:
                            selected_index = (selected_index + 1) % len(heroes)
                            direction = -1
                            hologram_active = False

                        last_swipe_time = now

                    if abs(dx) < 5:
                        direction = 0

                prev_x = smooth_x
            else:
                prev_x = None
                direction = 0

    else:
        smooth_x = None
        prev_x = None
        direction = 0
    '''
    # ---------- DEBUG ZONES (comment out to disable) ----------
    # Swipe Zone (TOP band)
    cv2.rectangle(frame, (0, swipe_top), (w, swipe_bottom), (255, 0, 0), 2)

    # Lock Zone (same as swipe zone - since lock uses swipe band)
    cv2.putText(frame, "LOCK ZONE", (10, swipe_top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Pinch / Hologram Zone (BOTTOM)
    cv2.rectangle(frame, (0, holo_zone), (w, h), (0, 255, 0), 2)
    cv2.putText(frame, "PINCH ZONE", (10, holo_zone - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Optional: label swipe zone too
    cv2.putText(frame, "SWIPE ZONE", (10, swipe_bottom + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    '''

    # ---------- Carousel ----------
    center_x = w // 2

    for offset in [-1, 0, 1]:
        idx = (selected_index + offset) % len(icons)
        icon = icons[idx]

        x_pos = center_x + offset * 120
        scale = 1.3 if offset == 0 else 0.8

        new_w = int(80 * scale)
        new_h = int(80 * scale)

        bgr = cv2.resize(icon[0], (new_w, new_h))
        alpha = icon[1]
        if alpha is not None:
            alpha = cv2.resize(alpha, (new_w, new_h))

        overlay(frame, (bgr, alpha),
                x_pos - new_w // 2,
                y_pos - new_h // 2)

    # ---------- Hologram ----------
    if hologram_active:
        frames = holograms[selected_index]

        if len(frames) > 0:
            holo = cv2.resize(frames[frame_idx], (300, 300))

            x_draw = w // 2 - 150
            float_offset = int(10 * np.sin(time.time() * 2))
            y_draw = h // 2 - 150 + 80 + float_offset

            bgr = holo[:, :, :3].astype(float)
            alpha = holo[:, :, 3] / 255.0

            bgr[:, :, 0] *= 1.2
            bgr[:, :, 1] *= 1.2
            bgr[:, :, 2] *= 0.7
            bgr = np.clip(bgr, 0, 255).astype(np.uint8)

            roi = frame[y_draw:y_draw+300, x_draw:x_draw+300]

            if roi.shape[0] == 300 and roi.shape[1] == 300:
                for c in range(3):
                    roi[:, :, c] = (1 - alpha) * roi[:, :, c] + alpha * bgr[:, :, c]

                frame[y_draw:y_draw+300, x_draw:x_draw+300] = roi

            frame_idx = (frame_idx + 1) % len(frames)

    colors = hero_colors[selected_index]

    # ---------- Text ----------
    
    margin = 20
    font_path = "assets/Orbitron-VariableFont_wght.ttf"

    y_offset = 30

    # Hero name (was 24)
    font_size_main = 14

    # Status text (was 18)
    font_size_small = 12

    frame = draw_text(frame,
                  heroes[selected_index].upper(),
                  (w - margin, h - margin - y_offset),
                  font_path,
                  font_size_main,
                  colors["primary"],
                  align="right")

    if hologram_active:
        y_offset += 30
        frame = draw_text(frame,
                  "HOLOGRAM ACTIVE",
                  (w - margin, h - margin - y_offset),
                  font_path,
                  font_size_small,
                  colors["accent"],
                  align="right")

    if locked:
        y_offset += 30
        frame = draw_text(frame,
                  "LOCKED",
                  (w - margin, h - margin - y_offset),
                  font_path,
                  font_size_small,
                  colors["lock"],
                  align="right")

    cv2.imshow("Gesture UI", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()