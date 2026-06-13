# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# CHỐT PHẦN MODEL COMPRESSION
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_03_04_compression_summary.py SceneP30304CompressionSummary
# ============================================================

config.background_color = "#0f172a"

BG = "#0f172a"
WHITE = "#e5e7eb"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
MUTED = "#94a3b8"
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


def audio_duration(path, fallback=5.0):
    if not os.path.exists(path):
        print("[WARNING] Không tìm thấy audio:", path)
        return fallback
    try:
        return MP3(path).info.length
    except Exception:
        return fallback


def fit_text(text, width, height=None):
    if text.width > width:
        text.scale_to_fit_width(width)
    if height is not None and text.height > height:
        text.scale_to_fit_height(height)
    return text


def make_box(text, color, width=2.8, height=0.78, font_size=21, fill=0.13):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.3,
        fill_color=color,
        fill_opacity=fill,
    )

    label = Text(
        text,
        font=FONT,
        font_size=font_size,
        color=WHITE,
        line_spacing=0.82,
    )
    fit_text(label, width - 0.28, height - 0.16)
    label.move_to(box.get_center())

    return VGroup(box, label)


def make_title(text):
    title = Text(text, font=FONT, font_size=38, color=WHITE)
    fit_text(title, 11.2)
    title.to_edge(UP, buff=0.28)
    return title


def make_subtitle(text, title):
    subtitle = Text(text, font=FONT, font_size=23, color=BLUE)
    fit_text(subtitle, 10.8)
    subtitle.next_to(title, DOWN, buff=0.14)
    return subtitle


class SceneP30304CompressionSummary(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"
        active_mobs = []

        def get_audio_path(filename):
            return str(voice_dir / filename)

        def set_active(*mobs):
            nonlocal active_mobs
            active_mobs = [m for m in mobs if m is not None]

        def play_segment(filename, fallback_duration, visual_func):
            audio_path = get_audio_path(filename)
            duration = audio_duration(audio_path, fallback=fallback_duration)

            if os.path.exists(audio_path):
                self.add_sound(audio_path)
            else:
                print("[WARNING] Bỏ qua audio vì không tìm thấy:", audio_path)

            local_time = 0.0

            def wait_to(ratio):
                nonlocal local_time
                target = duration * ratio
                delay = max(0, target - local_time)
                if delay > 0:
                    self.wait(delay)
                    local_time += delay

            def play_func(*animations, run_time=0.35, **kwargs):
                nonlocal local_time
                self.play(*animations, run_time=run_time, **kwargs)
                local_time += run_time

            visual_func(wait_to, play_func, duration)

            remain = max(0, duration - local_time)
            if remain > 0:
                self.wait(remain)

        def highlight_box(box_group, color, opacity=0.18, width=3.5):
            return box_group[0].animate.set_stroke(color, width=width).set_fill(color, opacity=opacity)

        def dim_box(box_group, color, opacity=0.08, width=2.0):
            return box_group[0].animate.set_stroke(color, width=width).set_fill(color, opacity=opacity)

        # =====================================================
        # HEADER
        # =====================================================
        title = make_title("Chốt phần Model Compression")
        subtitle = make_subtitle(
            "Nén mô hình để giảm chi phí inference",
            title,
        )

        header = make_box(
            "Model Compression",
            BLUE,
            width=4.50,
            height=0.70,
            font_size=25,
            fill=0.13,
        )
        header.move_to(UP * 1.45)

        kd_box = make_box(
            "Knowledge Distillation\nmodel nhỏ học theo model lớn",
            GREEN,
            width=6.70,
            height=0.88,
            font_size=21,
            fill=0.09,
        )
        kd_box.move_to(UP * 0.28)

        pruning_box = make_box(
            "Network Pruning\ncắt phần ít quan trọng",
            PURPLE,
            width=6.70,
            height=0.88,
            font_size=21,
            fill=0.09,
        )
        pruning_box.move_to(DOWN * 0.82)

        tree_x = -4.05

        connector = Line(
            header.get_bottom() + DOWN * 0.04,
            [tree_x, header.get_bottom()[1] - 0.04, 0],
            color=MUTED,
            stroke_width=2.0,
        )
        connector.set_opacity(0.38)

        vline = Line(
            [tree_x, header.get_bottom()[1] - 0.04, 0],
            [tree_x, pruning_box.get_center()[1], 0],
            color=MUTED,
            stroke_width=2.0,
        )
        vline.set_opacity(0.38)

        branch1 = Line(
            [tree_x, kd_box.get_center()[1], 0],
            kd_box.get_left() + LEFT * 0.08,
            color=MUTED,
            stroke_width=2.0,
        )
        branch1.set_opacity(0.38)

        branch2 = Line(
            [tree_x, pruning_box.get_center()[1], 0],
            pruning_box.get_left() + LEFT * 0.08,
            color=MUTED,
            stroke_width=2.0,
        )
        branch2.set_opacity(0.38)

        tradeoff = make_box(
            "Trade-off: tốc độ  |  bộ nhớ  |  chất lượng",
            RED,
            width=7.80,
            height=0.78,
            font_size=22,
            fill=0.10,
        )
        tradeoff.move_to(DOWN * 2.10)

        # =====================================================
        # SEGMENT 1 - INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            play(Write(title), run_time=0.50)

            wait_to(0.14)
            play(FadeIn(subtitle, shift=UP), run_time=0.25)

            wait_to(0.38)
            play(FadeIn(header, shift=UP), run_time=0.32)

            wait_to(0.62)
            play(
                Create(connector),
                Create(vline),
                run_time=0.32,
            )

            set_active(header, connector, vline)

        play_segment(
            "p3_03_04_01_intro.mp3",
            fallback_duration=5.5,
            visual_func=visual_intro,
        )

        # =====================================================
        # SEGMENT 2 - KNOWLEDGE DISTILLATION
        # =====================================================
        def visual_distillation(wait_to, play, duration):
            wait_to(0.08)
            play(
                Create(branch1),
                FadeIn(kd_box, shift=RIGHT),
                run_time=0.40,
            )

            wait_to(0.55)
            play(highlight_box(kd_box, GREEN), run_time=0.24)

            wait_to(0.84)
            play(dim_box(kd_box, GREEN), run_time=0.20)

            set_active(header, connector, vline, branch1, kd_box)

        play_segment(
            "p3_03_04_02_distillation.mp3",
            fallback_duration=4.8,
            visual_func=visual_distillation,
        )

        # =====================================================
        # SEGMENT 3 - NETWORK PRUNING
        # =====================================================
        def visual_pruning(wait_to, play, duration):
            wait_to(0.08)
            play(
                Create(branch2),
                FadeIn(pruning_box, shift=RIGHT),
                run_time=0.40,
            )

            wait_to(0.55)
            play(highlight_box(pruning_box, PURPLE), run_time=0.24)

            wait_to(0.84)
            play(dim_box(pruning_box, PURPLE), run_time=0.20)

            set_active(header, connector, vline, branch1, branch2, kd_box, pruning_box)

        play_segment(
            "p3_03_04_03_pruning.mp3",
            fallback_duration=4.8,
            visual_func=visual_pruning,
        )

        # =====================================================
        # SEGMENT 4 - TRADE-OFF
        # =====================================================
        def visual_tradeoff(wait_to, play, duration):
            wait_to(0.08)
            play(
                highlight_box(kd_box, GREEN, opacity=0.13, width=2.6),
                highlight_box(pruning_box, PURPLE, opacity=0.13, width=2.6),
                run_time=0.28,
            )

            wait_to(0.35)
            play(FadeIn(tradeoff, shift=UP), run_time=0.38)

            wait_to(0.72)
            play(Flash(tradeoff[0], color=RED), run_time=0.55)

            set_active(
                header,
                connector,
                vline,
                branch1,
                branch2,
                kd_box,
                pruning_box,
                tradeoff,
            )

        play_segment(
            "p3_03_04_04_tradeoff.mp3",
            fallback_duration=6.0,
            visual_func=visual_tradeoff,
        )

        # =====================================================
        # END
        # =====================================================
        final_mobs = [m for m in active_mobs if m is not None]
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            *[FadeOut(m) for m in final_mobs],
            run_time=0.50,
        )
