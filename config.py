# config.py

# ---------- Global Colors ----------
COLOR_PRIMARY = (255, 180, 0)   # main neon blue
COLOR_ACCENT  = (255, 220, 100) # brighter highlight
COLOR_LOCK    = (255, 120, 0)   # slightly deeper blue

# ---------- Hero Names ----------
heroes = ["Batman", "Superman", "WonderWoman", "Flash"]

# ---------- Hero Color Themes (BGR) ----------
hero_colors = [
    {  # Batman
        "primary": (200, 150, 50),
        "accent":  (255, 200, 80),
        "lock":    (120, 80, 30)
    },
    {  # Superman
        "primary": (255, 100, 50),
        "accent":  (255, 150, 80),
        "lock":    (150, 60, 30)
    },
    {  # WonderWoman
        "primary": (255, 200, 0),
        "accent":  (255, 220, 100),
        "lock":    (150, 120, 0)
    },
    {  # Flash
        "primary": (255, 255, 0),
        "accent":  (255, 200, 0),
        "lock":    (180, 120, 0)
    }
]