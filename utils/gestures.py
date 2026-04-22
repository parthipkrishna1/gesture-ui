# utils/gestures.py

# ---------- Fist Detection ----------
def is_fist(landmarks):
    palm = landmarks[0]
    ref = landmarks[9]

    dx = ref.x - palm.x
    dy = ref.y - palm.y
    hand_size = (dx**2 + dy**2) ** 0.5

    tips = [8, 12, 16, 20]
    closed = 0

    for tip in tips:
        dx = landmarks[tip].x - palm.x
        dy = landmarks[tip].y - palm.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist < hand_size * 0.9:
            closed += 1

    return closed >= 4


# ---------- Pinch Detection ----------
def is_pinch(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    dx = thumb_tip.x - index_tip.x
    dy = thumb_tip.y - index_tip.y
    dist = (dx**2 + dy**2) ** 0.5

    return dist < 0.05