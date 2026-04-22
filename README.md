# 🎮 Gesture UI (OpenCV + MediaPipe)

A real-time gesture-controlled interface built using computer vision.
Control a UI carousel with hand movements, lock interactions with a fist, and trigger a **hologram-style overlay** using gestures.

---

## 🎥 Demo

[Watch Demo](https://youtu.be/maI_ni-SWso)

## 🚀 Features

* ✋ **Gesture-Based Control**

  * Swipe left/right to navigate between heroes
  * Fist gesture to lock/unlock interaction
  * Pinch gesture to trigger hologram-style overlay (rendered using PNG animation sequences)

* 🌀 **Smooth Carousel UI**

  * Center-focused scaling
  * Responsive and stable gesture tracking

* 🔒 **Lock System**

  * Prevents accidental swipes
  * Controlled via fist gesture with cooldown

* 🧠 **Real-Time Processing**

  * Built using MediaPipe hand tracking
  * Optimized for smooth webcam interaction

* 🎨 **Custom UI**

  * Futuristic font (Orbitron)
  * Clean layout with right-aligned labels

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV**
* **MediaPipe**
* **NumPy**
* **Pillow (PIL)**

---

## 📦 Project Structure

```
project/
│
├── assets/
│   ├── batman.png
│   ├── superman.png
│   ├── wonderwoman.png
│   ├── flash.png
│   └── holo/
│       ├── batman/
│       ├── superman/
│       ├── wonderwoman/
│       └── flash/
│
├── main.py
├── README.md
└── .gitignore
```

---

## ⚙️ How to Run

1. Clone the repo:

```bash
git clone https://github.com/parthipkrishna1/gesture-ui.git
cd YOUR_REPO
```

2. Install dependencies:

```bash
pip install opencv-python mediapipe numpy pillow
```

3. Run the project:

```bash
python main.py
```

---

## 🧪 Debug Mode

The project includes optional debug overlays to visualize interaction zones.

Uncomment the following block in the code to enable:

```python
# ---------- DEBUG ZONES (comment out to disable) ----------
cv2.rectangle(frame, (0, swipe_top), (w, swipe_bottom), (255, 0, 0), 2)

cv2.putText(frame, "LOCK ZONE", (10, swipe_top - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

cv2.rectangle(frame, (0, holo_zone), (w, h), (0, 255, 0), 2)

cv2.putText(frame, "PINCH ZONE", (10, holo_zone - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.putText(frame, "SWIPE ZONE", (10, swipe_bottom + 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
```

> ⚠️ Debug overlays are disabled by default. Enable only for development.

---

## 🎮 Controls

| Gesture  | Action                         |
| -------- | ------------------------------ |
| 👉 Swipe | Change selected hero           |
| ✊ Fist   | Lock / Unlock UI               |
| 🤏 Pinch | Trigger hologram-style overlay |

> 🤏 Pinch = thumb and index finger brought together

---

## 🧠 Note on “Hologram”

The “hologram” in this project is a **stylized animated overlay rendered in real time**, not a true volumetric or AR-anchored hologram.

---

## 🎨 Assets & Credits

* 3D / hologram assets sourced from Sketchfab

* Batman | MultiVersus
* Model by: **[King_45]**
* Link: **[https://sketchfab.com/3d-models/batman-multiversus-b6a84cca73f647ba8c86df799dd3eef3]**

* Superman | MultiVersus
* Model by: **[King_45]**
* Link: **[https://sketchfab.com/3d-models/superman-multiversus-339ed9e6d8ff438fa82de22ecc314cf1]**

* Wonder Woman - DC
* Model by: **[Chechorams16]**
* Link: **[https://sketchfab.com/3d-models/wonder-woman-dc-40cc3dc3bfd44ddbad459aac4272d040]**

* The Flash
* Model by: **[Dmitry]**
* Link: **[https://sketchfab.com/3d-models/the-flash-7a9c912929674ef88ed18de3575a0903]**

All rights belong to the original creators.
Assets are used for educational / non-commercial purposes.

---

## 💡 Notes

* Works best in good lighting conditions
* Keep your hand clearly visible to the camera
* Gesture detection is tuned for stability over sensitivity

---

## 🚀 Future Improvements

* Gesture-based selection (click)
* Sound feedback on interaction
* Improved hologram effects (glow, scanlines, distortion)
* Depth-based AR-style enhancements

---

## 📌 License

This project is for educational and experimental purposes.

---

