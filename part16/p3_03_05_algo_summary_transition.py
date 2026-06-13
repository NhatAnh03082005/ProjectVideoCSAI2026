# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# TỔNG KẾT ALGORITHMIC INNOVATIONS VÀ CHUYỂN Ý
# Render:
# python -m manim -pql scenes/p3_03_05_algo_summary_transition.py SceneP30305AlgorithmicSummaryTransition
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


def audio_duration(path, fallback=8.0):
    if not os.path.exists(path):
        print("[WARNING] Không tìm thấy audio:", path)
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


def make_box(text, color, width=3.0, height=0.70, font_size=20, fill=0.12):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=2.2,
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
    fit_text(label, width - 0.24, height - 0.12)
    label.move_to(box.get_center())

    return VGroup(box, label)


def make_title(text):
    title = Text(text, font=FONT, font_size=36, color=WHITE)
    fit_text(title, 11.5)
    title.to_edge(UP, buff=0.24)
    return title


def make_subtitle(text, title):
    subtitle = Text(text, font=FONT, font_size=22, color=BLUE)
    fit_text(subtitle, 10.8)
    subtitle.next_to(title, DOWN, buff=0.12)
    return subtitle


class SceneP30305AlgorithmicSummaryTransition(Scene):
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

        def clear_active_before_audio(run_time=0.12):
            nonlocal active_mobs
            mobs = [m for m in active_mobs if m is not None]
            if mobs:
                self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
            active_mobs = []

        def play_segment(filename, fallback_duration, visual_func, clear_before=False):
            if clear_before:
                clear_active_before_audio(run_time=0.12)

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

        def highlight(box_group, color, opacity=0.17, width=3.2):
            return box_group[0].animate.set_stroke(color, width=width).set_fill(
                color, opacity=opacity
            )

        def dim(box_group, color, opacity=0.07, width=1.8):
            return box_group[0].animate.set_stroke(color, width=width).set_fill(
                color, opacity=opacity
            )

        # =====================================================
        # HEADER
        # =====================================================
        title = make_title("Tổng kết Algorithmic Innovations")
        subtitle = make_subtitle(
            "Ba nhóm tối ưu ở mức thuật toán và mô hình",
            title,
        )

        root_box = make_box(
            "Algorithmic Innovations",
            BLUE,
            width=4.65,
            height=0.58,
            font_size=22,
            fill=0.13,
        )
        root_box.move_to(UP * 2.08)

        # =====================================================
        # MAP ELEMENTS
        # =====================================================
        def group_header(text, color, x):
            b = make_box(
                text,
                color,
                width=3.70,
                height=0.46,
                font_size=17,
                fill=0.11,
            )
            b.move_to(RIGHT * x + UP * 1.20)
            return b

        def item_box(text, color, x, y):
            b = make_box(
                text,
                color,
                width=3.60,
                height=0.34,
                font_size=13,
                fill=0.055,
            )
            b.move_to(RIGHT * x + UP * y)
            return b

        decoding_header = group_header("Decoding Algorithms", GREEN, -4.15)
        arch_header = group_header("Architecture Design", PURPLE, 0.0)
        comp_header = group_header("Model Compression", YELLOW, 4.15)

        decoding_items = VGroup(
            item_box("Non-autoregressive Decoding", GREEN, -4.15, 0.67),
            item_box("Speculative Decoding", GREEN, -4.15, 0.27),
            item_box("Early Exiting", GREEN, -4.15, -0.13),
            item_box("Cascade Inference", GREEN, -4.15, -0.53),
        )

        arch_items = VGroup(
            item_box("Config Downsizing", PURPLE, 0.0, 0.67),
            item_box("Attention Simplification", PURPLE, 0.0, 0.27),
            item_box("MQA / GQA", PURPLE, 0.0, -0.13),
            item_box("MoE", PURPLE, 0.0, -0.53),
            item_box("Recurrent / State-space", PURPLE, 0.0, -0.93),
        )

        comp_items = VGroup(
            item_box("Knowledge Distillation", YELLOW, 4.15, 0.67),
            item_box("Network Pruning", YELLOW, 4.15, 0.27),
        )

        headers = VGroup(decoding_header, arch_header, comp_header)

        branch_lines = VGroup()
        for h in headers:
            line = Line(
                root_box.get_bottom(),
                h.get_top(),
                color=MUTED,
                stroke_width=1.8,
            )
            line.set_opacity(0.40)
            branch_lines.add(line)

        common_box = make_box(
            "Điểm chung: can thiệp vào thuật toán hoặc model để giảm chi phí inference",
            RED,
            width=10.60,
            height=0.62,
            font_size=19,
            fill=0.10,
        )
        common_box.move_to(DOWN * 2.25)

        # =====================================================
        # SEGMENT 1 - INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            play(Write(title), run_time=0.50)

            wait_to(0.12)
            play(FadeIn(subtitle, shift=UP), run_time=0.24)

            wait_to(0.34)
            play(FadeIn(root_box, shift=UP), run_time=0.32)

            wait_to(0.58)
            play(
                LaggedStart(
                    *[Create(line) for line in branch_lines],
                    lag_ratio=0.10,
                ),
                run_time=0.45,
            )

            wait_to(0.72)
            play(
                LaggedStart(
                    FadeIn(decoding_header, shift=UP),
                    FadeIn(arch_header, shift=UP),
                    FadeIn(comp_header, shift=UP),
                    lag_ratio=0.12,
                ),
                run_time=0.55,
            )

            set_active(root_box, branch_lines, headers)

        play_segment(
            "p3_03_05_01_intro.mp3",
            fallback_duration=5.5,
            visual_func=visual_intro,
            clear_before=False,
        )

        # =====================================================
        # SEGMENT 2 - DECODING
        # =====================================================
        def visual_decoding(wait_to, play, duration):
            wait_to(0.04)
            play(highlight(decoding_header, GREEN), run_time=0.24)

            ratios = [0.34, 0.48, 0.62, 0.76]
            for idx, ratio in enumerate(ratios):
                wait_to(ratio)
                play(FadeIn(decoding_items[idx], shift=UP), run_time=0.25)

            wait_to(0.90)
            play(dim(decoding_header, GREEN), run_time=0.18)

            set_active(root_box, branch_lines, headers, decoding_items)

        play_segment(
            "p3_03_05_02_decoding.mp3",
            fallback_duration=12.0,
            visual_func=visual_decoding,
        )

        # =====================================================
        # SEGMENT 3 - ARCHITECTURE
        # =====================================================
        def visual_architecture(wait_to, play, duration):
            wait_to(0.04)
            play(highlight(arch_header, PURPLE), run_time=0.24)

            ratios = [0.26, 0.38, 0.50, 0.62, 0.76]
            for idx, ratio in enumerate(ratios):
                wait_to(ratio)
                play(FadeIn(arch_items[idx], shift=UP), run_time=0.23)

            wait_to(0.90)
            play(dim(arch_header, PURPLE), run_time=0.18)

            set_active(root_box, branch_lines, headers, decoding_items, arch_items)

        play_segment(
            "p3_03_05_03_architecture.mp3",
            fallback_duration=14.0,
            visual_func=visual_architecture,
        )

        # =====================================================
        # SEGMENT 4 - MODEL COMPRESSION
        # =====================================================
        def visual_compression(wait_to, play, duration):
            wait_to(0.04)
            play(highlight(comp_header, YELLOW), run_time=0.24)

            wait_to(0.42)
            play(FadeIn(comp_items[0], shift=UP), run_time=0.26)

            wait_to(0.64)
            play(FadeIn(comp_items[1], shift=UP), run_time=0.26)

            wait_to(0.86)
            play(dim(comp_header, YELLOW), run_time=0.18)

            set_active(
                root_box,
                branch_lines,
                headers,
                decoding_items,
                arch_items,
                comp_items,
            )

        play_segment(
            "p3_03_05_04_compression.mp3",
            fallback_duration=8.5,
            visual_func=visual_compression,
        )

        # =====================================================
        # SEGMENT 5 - COMMON IDEA
        # =====================================================
        def visual_common(wait_to, play, duration):
            wait_to(0.12)
            play(
                highlight(decoding_header, GREEN, opacity=0.11, width=2.4),
                highlight(arch_header, PURPLE, opacity=0.11, width=2.4),
                highlight(comp_header, YELLOW, opacity=0.11, width=2.4),
                run_time=0.35,
            )

            wait_to(0.48)
            play(FadeIn(common_box, shift=UP), run_time=0.38)

            wait_to(0.78)
            play(Flash(common_box[0], color=RED), run_time=0.50)

            set_active(
                root_box,
                branch_lines,
                headers,
                decoding_items,
                arch_items,
                comp_items,
                common_box,
            )

        play_segment(
            "p3_03_05_05_common.mp3",
            fallback_duration=7.0,
            visual_func=visual_common,
        )

        # =====================================================
        # SEGMENT 6 - SIMPLE IMAGE
        # =====================================================
        def visual_simple_image(wait_to, play, duration):
            simple_title = Text(
                "Một hình ảnh đơn giản",
                font=FONT,
                font_size=29,
                color=WHITE,
            )
            fit_text(simple_title, 10.5)
            simple_title.next_to(subtitle, DOWN, buff=0.35)

            card1 = make_box(
                "Decoding Algorithms\nđổi cách sinh từng token",
                GREEN,
                width=4.00,
                height=0.96,
                font_size=21,
                fill=0.11,
            )

            card2 = make_box(
                "Architecture Design\nđổi cấu trúc bên trong model",
                PURPLE,
                width=4.20,
                height=0.96,
                font_size=21,
                fill=0.11,
            )

            card3 = make_box(
                "Model Compression\nlàm model nhỏ và nhẹ hơn",
                YELLOW,
                width=4.15,
                height=0.96,
                font_size=21,
                fill=0.11,
            )

            cards = VGroup(card1, card2, card3)
            cards.arrange(DOWN, buff=0.35)
            cards.move_to(DOWN * 0.05)

            wait_to(0.02)
            play(FadeIn(simple_title, shift=UP), run_time=0.25)

            wait_to(0.22)
            play(FadeIn(card1, shift=RIGHT), run_time=0.34)

            wait_to(0.46)
            play(FadeIn(card2, shift=RIGHT), run_time=0.34)

            wait_to(0.70)
            play(FadeIn(card3, shift=RIGHT), run_time=0.34)

            set_active(simple_title, cards)

        play_segment(
            "p3_03_05_06_simple_image.mp3",
            fallback_duration=11.0,
            visual_func=visual_simple_image,
            clear_before=True,
        )

        # =====================================================
        # SEGMENT 7 - NEED SYSTEM OPTIMIZATION
        # =====================================================
        def visual_need_system(wait_to, play, duration):
            warn = make_box(
                "Chỉ tối ưu thuật toán là chưa đủ",
                RED,
                width=6.40,
                height=0.72,
                font_size=24,
                fill=0.11,
            )
            warn.move_to(UP * 1.35)

            center = make_box(
                "LLM trong hệ thống thật",
                BLUE,
                width=4.20,
                height=0.70,
                font_size=23,
                fill=0.12,
            )
            center.move_to(UP * 0.40)

            gpu = make_box("GPU", GREEN, width=1.65, height=0.56, font_size=19, fill=0.10)
            devices = make_box("Multi-device", PURPLE, width=2.25, height=0.56, font_size=18, fill=0.10)
            memory = make_box("Memory", YELLOW, width=1.90, height=0.56, font_size=18, fill=0.10)
            schedule = make_box("Request scheduling", ORANGE, width=2.75, height=0.56, font_size=17, fill=0.10)
            kernel = make_box("Kernel", RED, width=1.80, height=0.56, font_size=18, fill=0.10)

            row1 = VGroup(gpu, devices, memory)
            row1.arrange(RIGHT, buff=0.35)
            row1.move_to(DOWN * 0.70)

            row2 = VGroup(schedule, kernel)
            row2.arrange(RIGHT, buff=0.45)
            row2.move_to(DOWN * 1.45)

            items = VGroup(gpu, devices, memory, schedule, kernel)

            wait_to(0.04)
            play(FadeIn(warn, shift=UP), run_time=0.34)

            wait_to(0.26)
            play(FadeIn(center, shift=UP), run_time=0.30)

            ratios = [0.42, 0.54, 0.66, 0.76, 0.86]
            for obj, ratio in zip(items, ratios):
                wait_to(ratio)
                play(FadeIn(obj, shift=UP), run_time=0.22)

            set_active(warn, center, row1, row2)

        play_segment(
            "p3_03_05_07_need_system.mp3",
            fallback_duration=13.0,
            visual_func=visual_need_system,
            clear_before=True,
        )

        # =====================================================
        # SEGMENT 8 - NEXT
        # =====================================================
        def visual_next(wait_to, play, duration):
            current = make_box(
                "Algorithmic Innovations",
                BLUE,
                width=4.20,
                height=0.80,
                font_size=23,
                fill=0.11,
            )
            current.move_to(LEFT * 3.25 + UP * 0.10)

            next_box = make_box(
                "Next:\nSystem Optimizations",
                GREEN,
                width=4.40,
                height=0.96,
                font_size=24,
                fill=0.12,
            )
            next_box.move_to(RIGHT * 3.25 + UP * 0.10)

            arrow = Arrow(
                current.get_right(),
                next_box.get_left(),
                color=YELLOW,
                stroke_width=5,
                buff=0.22,
            )

            note = Text(
                "Từ tối ưu thuật toán -> tối ưu hệ thống chạy trên phần cứng thật",
                font=FONT,
                font_size=22,
                color=YELLOW,
            )
            fit_text(note, 11.0)
            note.move_to(DOWN * 1.45)

            wait_to(0.04)
            play(FadeIn(current, shift=RIGHT), run_time=0.30)

            wait_to(0.28)
            play(GrowArrow(arrow), run_time=0.32)

            wait_to(0.50)
            play(FadeIn(next_box, shift=LEFT), run_time=0.36)

            wait_to(0.76)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(current, arrow, next_box, note)

        play_segment(
            "p3_03_05_08_next.mp3",
            fallback_duration=4.5,
            visual_func=visual_next,
            clear_before=True,
        )

        # =====================================================
        # END
        # =====================================================
        final_mobs = [m for m in active_mobs if m is not None]
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            *[FadeOut(m) for m in final_mobs],
            run_time=0.55,
        )
