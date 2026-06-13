from manim import *
from mutagen.mp3 import MP3
import os

# ============================================================
# STYLE CHUNG CHO PHẦN 3
# ============================================================

config.background_color = "#0f172a"

BG = "#0f172a"
WHITE = "#e5e7eb"
MUTED = "#94a3b8"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"

VI_FONT = "Arial"
FONT = None

_MANIM_TEXT = Text


def has_vietnamese(text):
    vietnamese_chars = (
        "ăâđêôơư"
        "áàảãạấầẩẫậắằẳẵặ"
        "éèẻẽẹếềểễệ"
        "íìỉĩị"
        "óòỏõọốồổỗộớờởỡợ"
        "úùủũụứừửữự"
        "ýỳỷỹỵ"
    )
    lowered = str(text).lower()
    return any(ch in lowered for ch in vietnamese_chars)


def Text(text, *args, font=None, **kwargs):
    if font is None:
        if has_vietnamese(text):
            kwargs["font"] = VI_FONT
    else:
        kwargs["font"] = font
    return _MANIM_TEXT(text, *args, **kwargs)


# ============================================================
# AUDIO HELPERS
# ============================================================

def audio_duration(path):
    if not os.path.exists(path):
        print(f"[WARNING] Không tìm thấy audio: {path}")
        return 0
    return MP3(path).info.length


def play_audio(scene, path):
    if os.path.exists(path):
        scene.add_sound(path)
    else:
        print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path}")


def wait_audio(scene, path, visual_time):
    duration = audio_duration(path)
    remaining = duration - visual_time
    if remaining > 0:
        scene.wait(remaining)


# ============================================================
# TEXT HELPERS
# ============================================================

def make_title(text):
    title = Text(text, font=FONT, font_size=42, color=WHITE)
    title.to_edge(UP, buff=0.35)
    return title


def make_subtitle(text, title):
    subtitle = Text(text, font=FONT, font_size=23, color=BLUE)
    subtitle.next_to(title, DOWN, buff=0.22)
    return subtitle


def make_caption(text):
    caption = Text(text, font=FONT, font_size=23, color=MUTED)
    caption.to_edge(DOWN, buff=0.35)
    caption.scale_to_fit_width(11)
    return caption


def safe_text(text, font_size=24, color=WHITE, max_width=6):
    t = Text(text, font=FONT, font_size=font_size, color=color)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


# ============================================================
# VISUAL BLOCK HELPERS
# ============================================================

def model_box(text, color=BLUE, width=3.0, height=0.9, font_size=23):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.14
    )

    label = Text(text, font=FONT, font_size=font_size, color=WHITE)
    if label.width > width - 0.25:
        label.scale_to_fit_width(width - 0.25)
    if label.height > height - 0.18:
        label.scale_to_fit_height(height - 0.18)
    label.move_to(box.get_center())

    return VGroup(box, label)


def token_box(text, color=BLUE, width=0.8, height=0.55, font_size=22):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.18
    )

    label = Text(text, font=FONT, font_size=font_size, color=WHITE)
    label.move_to(box.get_center())

    return VGroup(box, label)


def small_label(text, color=MUTED):
    return Text(text, font=FONT, font_size=20, color=color)
