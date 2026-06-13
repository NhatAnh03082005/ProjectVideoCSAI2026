# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# 3.1. Model Compression là gì?
#
# Render:
# python -m manim -pql p3_03_intro.py SceneP30301ModelCompression
# ============================================================

config.background_color = "#0f172a"

BG = "#0f172a"
WHITE = "#e5e7eb"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"
GRAY = "#94a3b8"

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


def audio_duration(path, fallback=4.0):
    if not os.path.exists(path):
        print(f"[WARNING] Missing audio: {path}")
        return fallback
    try:
        return MP3(path).info.length
    except Exception:
        return fallback


def fit_text(text_mob, max_width, max_height=None):
    if text_mob.width > max_width:
        text_mob.scale_to_fit_width(max_width)
    if max_height is not None and text_mob.height > max_height:
        text_mob.scale_to_fit_height(max_height)
    return text_mob


def make_box(text, color, width=3.5, height=1.0, font_size=26, fill_opacity=0.10):
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    label = Text(
        text,
        font=FONT,
        font_size=font_size,
        color=WHITE,
        line_spacing=0.84,
    )
    fit_text(label, width - 0.30, height - 0.18)
    label.move_to(rect.get_center())
    return VGroup(rect, label)


def make_title(text):
    t = Text(text, font=FONT, font_size=34, color=WHITE)
    fit_text(t, 12.2)
    t.to_edge(UP, buff=0.18)
    return t


def make_subtitle(text, title_obj):
    s = Text(text, font=FONT, font_size=22, color=BLUE)
    fit_text(s, 11.5)
    s.next_to(title_obj, DOWN, buff=0.12)
    return s


class SceneP30301ModelCompression(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"
        full_audio = voice_dir / "p3_03_01_model_compression.mp3"

        if full_audio.exists():
            self.add_sound(str(full_audio))
        else:
            print(f"[WARNING] Audio not found: {full_audio}")

        def audio_path(filename):
            return str(voice_dir / filename)

        def play_segment(filename, fallback_duration, visual_func):
            path = audio_path(filename)
            duration = audio_duration(path, fallback=fallback_duration)

            local_time = 0.0

            def wait_to(ratio):
                nonlocal local_time
                target = duration * ratio
                delay = max(0.0, target - local_time)
                if delay > 0:
                    self.wait(delay)
                    local_time += delay

            def play_timed(*animations, run_time=0.30, **kwargs):
                nonlocal local_time
                self.play(*animations, run_time=run_time, **kwargs)
                local_time += run_time

            visual_func(wait_to, play_timed, duration)

            remain = max(0.0, duration - local_time)
            if remain > 0:
                self.wait(remain)

        # ------------------------------------------------------------
        # STATIC HEADER
        # ------------------------------------------------------------
        title = make_title("Model Compression")
        subtitle = make_subtitle(
            "Nén mô hình để inference hiệu quả hơn",
            title
        )

        self.play(Write(title), run_time=0.45)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.28)

        # ------------------------------------------------------------
        # VISUAL ELEMENTS
        # ------------------------------------------------------------
        large_model = make_box(
            "Large Model",
            BLUE,
            width=3.2,
            height=1.1,
            font_size=28,
            fill_opacity=0.12,
        )

        small_model = make_box(
            "Smaller Model",
            GREEN,
            width=3.6,
            height=1.1,
            font_size=28,
            fill_opacity=0.12,
        )

        large_model.move_to(LEFT * 3.3 + UP * 0.4)
        small_model.move_to(RIGHT * 3.3 + UP * 0.4)

        arrow = Arrow(
            start=large_model.get_right() + RIGHT * 0.15,
            end=small_model.get_left() + LEFT * 0.15,
            buff=0.0,
            stroke_width=5,
            color=YELLOW,
        )

        compression_text = Text(
            "compression",
            font=FONT,
            font_size=24,
            color=YELLOW,
        )
        compression_text.next_to(arrow, UP, buff=0.12)

        smaller_box = make_box(
            "Smaller",
            GREEN,
            width=2.3,
            height=0.88,
            font_size=24,
            fill_opacity=0.10,
        )
        lighter_box = make_box(
            "Lighter",
            BLUE,
            width=2.3,
            height=0.88,
            font_size=24,
            fill_opacity=0.10,
        )
        cheaper_box = make_box(
            "Cheaper",
            ORANGE,
            width=2.3,
            height=0.88,
            font_size=24,
            fill_opacity=0.10,
        )

        goal_row = VGroup(smaller_box, lighter_box, cheaper_box).arrange(RIGHT, buff=0.55)
        goal_row.move_to(DOWN * 1.35)

        deploy_note = make_box(
            "Inference nhanh hơn, dễ triển khai hơn",
            YELLOW,
            width=5.8,
            height=0.62,
            font_size=20,
            fill_opacity=0.08,
        )
        deploy_note.move_to(DOWN * 2.34)

        distill_box = make_box(
            "Knowledge Distillation",
            PURPLE,
            width=4.5,
            height=1.0,
            font_size=24,
            fill_opacity=0.10,
        )
        prune_box = make_box(
            "Network Pruning",
            RED,
            width=4.1,
            height=1.0,
            font_size=24,
            fill_opacity=0.10,
        )

        technique_row = VGroup(distill_box, prune_box).arrange(RIGHT, buff=0.8)
        technique_row.move_to(DOWN * 0.35)

        focus_title = Text(
            "Hai kỹ thuật chính",
            font=FONT,
            font_size=30,
            color=WHITE,
        )
        focus_title.move_to(UP * 1.35)

        # ------------------------------------------------------------
        # SEGMENT 1
        # ------------------------------------------------------------
        def visual_intro(wait_to, play, duration):
            wait_to(0.10)
            play(FadeIn(large_model, shift=RIGHT * 0.2), run_time=0.28)

            wait_to(0.42)
            play(GrowArrow(arrow), FadeIn(compression_text, shift=UP * 0.1), run_time=0.30)

            wait_to(0.72)
            play(FadeIn(small_model, shift=LEFT * 0.2), run_time=0.28)

        play_segment(
            "p3_03_01_01_intro.mp3",
            fallback_duration=4.2,
            visual_func=visual_intro,
        )

        # ------------------------------------------------------------
        # SEGMENT 2
        # ------------------------------------------------------------
        def visual_goal(wait_to, play, duration):
            wait_to(0.12)
            play(
                large_model[0].animate.set_fill(BLUE, opacity=0.16),
                small_model[0].animate.set_fill(GREEN, opacity=0.16),
                run_time=0.22,
            )

            wait_to(0.22)
            play(FadeIn(smaller_box, shift=UP * 0.15), run_time=0.24)

            wait_to(0.30)
            play(FadeIn(lighter_box, shift=UP * 0.15), run_time=0.24)

            wait_to(0.38)
            play(FadeIn(cheaper_box, shift=UP * 0.15), run_time=0.24)

            wait_to(0.62)
            play(
                FadeIn(deploy_note, shift=UP * 0.12),
                run_time=0.26,
            )

        play_segment(
            "p3_03_01_02_goal.mp3",
            fallback_duration=5.6,
            visual_func=visual_goal,
        )

        # ------------------------------------------------------------
        # SEGMENT 3
        # ------------------------------------------------------------
        def visual_focus(wait_to, play, duration):
            wait_to(0.05)
            play(
                FadeOut(large_model),
                FadeOut(small_model),
                FadeOut(arrow),
                FadeOut(compression_text),
                FadeOut(goal_row),
                FadeOut(deploy_note),
                run_time=0.28,
            )

            wait_to(0.22)
            play(FadeIn(focus_title, shift=UP * 0.1), run_time=0.24)

            wait_to(0.42)
            play(FadeIn(distill_box, shift=RIGHT * 0.15), run_time=0.28)

            wait_to(0.72)
            play(FadeIn(prune_box, shift=LEFT * 0.15), run_time=0.28)

        play_segment(
            "p3_03_01_04_focus.mp3",
            fallback_duration=5.0,
            visual_func=visual_focus,
        )

        self.wait(0.3)
