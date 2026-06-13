# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# P3_02_07 - CHỐT PHẦN ARCHITECTURE DESIGN
# Render:
# python -m manim -pql scenes/p3_02_07_arch_summary.py SceneP30207ArchSummary
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


def audio_duration(path, fallback=6.0):
    if not os.path.exists(path):
        print(f"[WARNING] Missing audio: {path}")
        return fallback
    try:
        return MP3(path).info.length
    except Exception:
        return fallback


def fit_text(text_mob, width, height=None):
    if text_mob.width > width:
        text_mob.scale_to_fit_width(width)
    if height is not None and text_mob.height > height:
        text_mob.scale_to_fit_height(height)
    return text_mob


def make_box(text, color, width=4.0, height=0.8, font_size=24, fill_opacity=0.10):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        stroke_color=color,
        stroke_width=2.4,
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
    fit_text(label, width - 0.30, height - 0.14)
    label.move_to(box.get_center())
    return VGroup(box, label)


def make_title(text):
    t = Text(text, font=FONT, font_size=34, color=WHITE)
    fit_text(t, 12.4)
    t.to_edge(UP, buff=0.18)
    return t


def make_subtitle(text, title):
    s = Text(text, font=FONT, font_size=22, color=BLUE)
    fit_text(s, 11.8)
    s.next_to(title, DOWN, buff=0.12)
    return s


class SceneP30207ArchSummary(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"
        full_audio = voice_dir / "p3_02_07_arch_summary.mp3"

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
                delay = max(0, target - local_time)
                if delay > 0:
                    self.wait(delay)
                    local_time += delay

            def play_timed(*animations, run_time=0.30, **kwargs):
                nonlocal local_time
                self.play(*animations, run_time=run_time, **kwargs)
                local_time += run_time

            visual_func(wait_to, play_timed, duration)

            remain = max(0, duration - local_time)
            if remain > 0:
                self.wait(remain)

        # ------------------------------------------------------------
        # LAYOUT TỔNG
        # ------------------------------------------------------------
        title = make_title("Chốt phần Architecture Design")
        subtitle = make_subtitle(
            "Thay đổi kiến trúc để mô hình phục vụ hiệu quả hơn",
            title
        )

        header = make_box(
            "Architecture Design",
            BLUE,
            width=4.2,
            height=0.68,
            font_size=25,
            fill_opacity=0.12,
        )
        header.move_to(UP * 2.15)

        # ------------------------------------------------------------
        # BẢNG ROW
        # ------------------------------------------------------------
        def build_row(name, desc, color, y):
            row_width = 11.4
            row_height = 0.68
            name_col_w = 3.9

            rect = RoundedRectangle(
                width=row_width,
                height=row_height,
                corner_radius=0.12,
                stroke_color=color,
                stroke_width=2.0,
                fill_color=color,
                fill_opacity=0.08,
            )
            rect.move_to([0, y, 0])

            dot = Dot(color=color, radius=0.055)
            dot.move_to(rect.get_left() + RIGHT * 0.28)

            divider_x = rect.get_left()[0] + name_col_w
            divider = Line(
                [divider_x, y - 0.22, 0],
                [divider_x, y + 0.22, 0],
                color=color,
                stroke_width=1.6,
            )
            divider.set_opacity(0.45)

            name_text = Text(
                name,
                font=FONT,
                font_size=20,
                color=color,
            )
            fit_text(name_text, 3.05, 0.34)
            name_text.move_to([rect.get_left()[0] + 1.95, y, 0])

            desc_text = Text(
                desc,
                font=FONT,
                font_size=18,
                color=WHITE,
            )
            fit_text(desc_text, 6.85, 0.34)
            desc_text.move_to([divider_x + 3.55, y, 0])

            return {
                "rect": rect,
                "dot": dot,
                "divider": divider,
                "name": name_text,
                "desc": desc_text,
                "color": color,
                "group": VGroup(rect, dot, divider, name_text, desc_text),
            }

        rows = [
            build_row("Config Downsizing", "giảm kích thước cấu hình model", GREEN, 1.15),
            build_row("Attention Simplification", "giảm chi phí attention khi sequence dài", BLUE, 0.38),
            build_row("MQA / GQA", "giảm KV cache và memory bandwidth", PURPLE, -0.39),
            build_row("MoE", "chỉ kích hoạt một phần expert cần thiết", ORANGE, -1.16),
            build_row("Recurrent / State-space", "hướng nghiên cứu cho long sequence", YELLOW, -1.93),
        ]

        tradeoff = make_box(
            "Hiệu quả lớn, nhưng có trade-off:\nchất lượng, training, hoặc triển khai hệ thống",
            RED,
            width=10.6,
            height=1.00,
            font_size=20,
            fill_opacity=0.10,
        )
        tradeoff.move_to(DOWN * 3.05)

        # ------------------------------------------------------------
        # HELPER CHO MỖI ROW
        # ------------------------------------------------------------
        def show_row(row, wait_to, play, name_ratio=0.08, desc_ratio=0.42, hi_ratio=0.78):
            # hiện phần khung + tên trước
            wait_to(name_ratio)
            play(
                Create(row["rect"]),
                FadeIn(row["dot"], scale=0.8),
                FadeIn(row["name"], shift=RIGHT * 0.15),
                run_time=0.30,
            )

            # hiện phần mô tả đúng lúc voice đọc nội dung mô tả
            wait_to(desc_ratio)
            play(
                Create(row["divider"]),
                FadeIn(row["desc"], shift=RIGHT * 0.15),
                run_time=0.28,
            )

            # highlight nhẹ
            wait_to(hi_ratio)
            play(
                row["rect"].animate.set_stroke(row["color"], width=3.0).set_fill(row["color"], opacity=0.13),
                run_time=0.22,
            )

        # ------------------------------------------------------------
        # SEGMENT 1 - INTRO
        # ------------------------------------------------------------
        def visual_intro(wait_to, play, duration):
            play(Write(title), run_time=0.42)

            wait_to(0.18)
            play(FadeIn(subtitle, shift=UP * 0.10), run_time=0.24)

            wait_to(0.56)
            play(FadeIn(header, shift=UP * 0.15), run_time=0.32)

        play_segment(
            "p3_02_07_01_intro.mp3",
            fallback_duration=5.8,
            visual_func=visual_intro,
        )

        # ------------------------------------------------------------
        # SEGMENT 2 - CONFIG
        # ------------------------------------------------------------
        def visual_config(wait_to, play, duration):
            show_row(
                rows[0],
                wait_to,
                play,
                name_ratio=0.08,
                desc_ratio=0.44,
                hi_ratio=0.80,
            )

        play_segment(
            "p3_02_07_02_config.mp3",
            fallback_duration=4.5,
            visual_func=visual_config,
        )

        # ------------------------------------------------------------
        # SEGMENT 3 - ATTENTION
        # ------------------------------------------------------------
        def visual_attention(wait_to, play, duration):
            show_row(
                rows[1],
                wait_to,
                play,
                name_ratio=0.06,
                desc_ratio=0.38,
                hi_ratio=0.78,
            )

        play_segment(
            "p3_02_07_03_attention.mp3",
            fallback_duration=4.8,
            visual_func=visual_attention,
        )

        # ------------------------------------------------------------
        # SEGMENT 4 - MQA/GQA
        # ------------------------------------------------------------
        def visual_mqa_gqa(wait_to, play, duration):
            show_row(
                rows[2],
                wait_to,
                play,
                name_ratio=0.06,
                desc_ratio=0.34,
                hi_ratio=0.80,
            )

        play_segment(
            "p3_02_07_04_mqa_gqa.mp3",
            fallback_duration=6.0,
            visual_func=visual_mqa_gqa,
        )

        # ------------------------------------------------------------
        # SEGMENT 5 - MoE
        # ------------------------------------------------------------
        def visual_moe(wait_to, play, duration):
            show_row(
                rows[3],
                wait_to,
                play,
                name_ratio=0.05,
                desc_ratio=0.28,
                hi_ratio=0.74,
            )

        play_segment(
            "p3_02_07_05_moe.mp3",
            fallback_duration=7.2,
            visual_func=visual_moe,
        )

        # ------------------------------------------------------------
        # SEGMENT 6 - RECURRENT
        # ------------------------------------------------------------
        def visual_recurrent(wait_to, play, duration):
            show_row(
                rows[4],
                wait_to,
                play,
                name_ratio=0.06,
                desc_ratio=0.40,
                hi_ratio=0.82,
            )

        play_segment(
            "p3_02_07_06_recurrent.mp3",
            fallback_duration=5.0,
            visual_func=visual_recurrent,
        )

        # ------------------------------------------------------------
        # SEGMENT 7 - TRADEOFF
        # ------------------------------------------------------------
        def visual_tradeoff(wait_to, play, duration):
            wait_to(0.10)
            play(
                *[
                    row["rect"].animate.set_fill(row["color"], opacity=0.11)
                    for row in rows
                ],
                run_time=0.24,
            )

            wait_to(0.48)
            play(FadeIn(tradeoff, shift=UP * 0.12), run_time=0.34)

            wait_to(0.82)
            play(
                tradeoff[0].animate.set_stroke(RED, width=3.2),
                run_time=0.24,
            )

        play_segment(
            "p3_02_07_07_tradeoff.mp3",
            fallback_duration=8.0,
            visual_func=visual_tradeoff,
        )

        self.wait(0.2)
