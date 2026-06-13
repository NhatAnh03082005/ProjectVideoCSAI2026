# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# PHẦN 3 - INTRO: ALGORITHMIC INNOVATIONS
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_00_intro.py SceneP3Intro
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


def audio_duration(path, fallback=8.0):
    if not os.path.exists(path):
        print("[WARNING] Không tìm thấy audio:", path)
        return fallback
    try:
        return MP3(path).info.length
    except Exception:
        return fallback


def fit_text(mob, width, height=None):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    if height is not None and mob.height > height:
        mob.scale_to_fit_height(height)
    return mob


def text_vi(text, font_size=24, color=WHITE, line_spacing=0.85):
    return Text(
        text,
        font=VI_FONT,
        font_size=font_size,
        color=color,
        line_spacing=line_spacing,
    )


def text_en(text, font_size=24, color=WHITE, line_spacing=0.85):
    # Không truyền font để Manim dùng font mặc định cho chữ tiếng Anh.
    return Text(
        text,
        font_size=font_size,
        color=color,
        line_spacing=line_spacing,
    )


def make_box_vi(text, color, width=3.0, height=0.78, font_size=21, fill=0.12):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.2,
        fill_color=color,
        fill_opacity=fill,
    )

    label = text_vi(text, font_size=font_size, color=WHITE)
    fit_text(label, width - 0.28, height - 0.16)
    label.move_to(box.get_center())

    return VGroup(box, label)


def make_box_en(text, color, width=3.0, height=0.78, font_size=21, fill=0.12):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.2,
        fill_color=color,
        fill_opacity=fill,
    )

    label = text_en(text, font_size=font_size, color=WHITE)
    fit_text(label, width - 0.28, height - 0.16)
    label.move_to(box.get_center())

    return VGroup(box, label)


def make_mixed_card(
    heading_en,
    desc_vi,
    color,
    width=3.5,
    height=1.05,
    heading_size=22,
    desc_size=18,
    fill=0.11,
):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.2,
        fill_color=color,
        fill_opacity=fill,
    )

    heading = text_en(heading_en, font_size=heading_size, color=WHITE)
    desc = text_vi(desc_vi, font_size=desc_size, color=MUTED)

    fit_text(heading, width - 0.34, height * 0.42)
    fit_text(desc, width - 0.34, height * 0.38)

    group = VGroup(heading, desc).arrange(DOWN, buff=0.07)
    group.move_to(box.get_center())

    return VGroup(box, group)


def mixed_title(english, vietnamese, en_size=42, vi_size=30):
    en = text_en(english, font_size=en_size, color=WHITE)
    vi = text_vi(vietnamese, font_size=vi_size, color=BLUE)
    title = VGroup(en, vi).arrange(DOWN, buff=0.08)
    fit_text(title, 11.0)
    title.to_edge(UP, buff=0.35)
    return title


class SceneP3Intro(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"
        active_mobs = []

        def get_audio_path(filename):
            return str(voice_dir / filename)

        def clear_active_before_audio(run_time=0.12):
            nonlocal active_mobs
            mobs = [m for m in active_mobs if m is not None]
            if mobs:
                self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
            active_mobs = []

        def set_active(*mobs):
            nonlocal active_mobs
            active_mobs = [m for m in mobs if m is not None]

        def play_segment(filename, fallback_duration, visual_func, clear_before=True):
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

        # =====================================================
        # CẢNH 1 - HOOK
        # =====================================================
        def visual_hook(wait_to, play, duration):
            title = mixed_title("LLM Serving", "trong thực tế", en_size=42, vi_size=30)

            main_box = make_box_vi(
                "Không đơn giản\nchỉ là chạy một model lớn",
                BLUE,
                width=5.80,
                height=1.08,
                font_size=25,
                fill=0.12,
            )
            main_box.move_to(UP * 0.82)

            note = text_vi(
                "Khi phục vụ một mô hình ngôn ngữ lớn,\nhệ thống gặp rất nhiều thách thức.",
                font_size=27,
                color=YELLOW,
                line_spacing=0.92,
            )
            fit_text(note, 10.8)
            note.move_to(DOWN * 0.85)

            play(Write(title), run_time=0.55)

            wait_to(0.20)
            play(FadeIn(main_box, shift=UP), run_time=0.35)

            wait_to(0.55)
            play(FadeIn(note, shift=UP), run_time=0.45)

            set_active(title, main_box, note)

        play_segment(
            "p3_00_01_hook.mp3",
            fallback_duration=8.0,
            visual_func=visual_hook,
            clear_before=False,
        )

        # =====================================================
        # CẢNH 2 - CÂU HỎI
        # =====================================================
        def visual_question(wait_to, play, duration):
            title = text_vi("Câu hỏi tiếp theo", font_size=34, color=WHITE)
            title.to_edge(UP, buff=0.55)

            question = text_vi(
                "Làm sao để tối ưu\nquá trình phục vụ mô hình ngôn ngữ lớn?",
                font_size=34,
                color=YELLOW,
                line_spacing=0.88,
            )
            fit_text(question, 10.2)
            question.move_to(ORIGIN + DOWN * 0.05)

            question_box = RoundedRectangle(
                width=10.85,
                height=1.80,
                corner_radius=0.18,
                stroke_color=YELLOW,
                stroke_width=2.4,
                fill_color=YELLOW,
                fill_opacity=0.08,
            )
            question_box.move_to(question.get_center())

            wait_to(0.02)
            play(FadeIn(title, shift=UP), run_time=0.30)

            wait_to(0.22)
            play(Create(question_box), Write(question), run_time=0.85)

            wait_to(0.72)
            play(Flash(question_box, color=YELLOW), run_time=0.55)

            set_active(title, question_box, question)

        play_segment(
            "p3_00_02_question.mp3",
            fallback_duration=5.0,
            visual_func=visual_question,
        )

        # =====================================================
        # CẢNH 3 - HAI NHÓM TỐI ƯU
        # =====================================================
        def visual_two_groups(wait_to, play, duration):
            title = text_vi("Hai nhóm tối ưu lớn", font_size=36, color=WHITE)
            title.to_edge(UP, buff=0.42)

            root_box = make_box_en(
                "LLM Serving Optimization",
                BLUE,
                width=5.35,
                height=0.76,
                font_size=22,
                fill=0.12,
            )
            root_box.move_to(UP * 1.15)

            algo = make_mixed_card(
                "Algorithmic Innovations",
                "cải tiến thuật toán\nhoặc thiết kế mô hình",
                GREEN,
                width=4.35,
                height=1.28,
                heading_size=21,
                desc_size=18,
            )
            system = make_mixed_card(
                "System Optimizations",
                "tối ưu cách chạy\ntrên phần cứng thật",
                PURPLE,
                width=4.35,
                height=1.28,
                heading_size=21,
                desc_size=18,
            )

            algo.move_to(LEFT * 2.75 + DOWN * 0.35)
            system.move_to(RIGHT * 2.75 + DOWN * 0.35)

            line_algo = Line(root_box.get_bottom(), algo.get_top(), color=MUTED, stroke_width=2.0)
            line_system = Line(root_box.get_bottom(), system.get_top(), color=MUTED, stroke_width=2.0)
            lines = VGroup(line_algo, line_system)

            note = text_vi(
                "Một nhóm thay đổi mô hình, một nhóm tối ưu hệ thống chạy mô hình.",
                font_size=21,
                color=YELLOW,
            )
            fit_text(note, 10.8)
            note.move_to(DOWN * 2.18)

            wait_to(0.02)
            play(FadeIn(title, shift=UP), run_time=0.35)

            wait_to(0.16)
            play(FadeIn(root_box, shift=UP), run_time=0.32)

            wait_to(0.40)
            play(Create(lines), run_time=0.28)

            wait_to(0.52)
            play(
                FadeIn(algo, shift=RIGHT),
                FadeIn(system, shift=LEFT),
                run_time=0.48,
            )

            wait_to(0.82)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(title, root_box, lines, algo, system, note)

        play_segment(
            "p3_00_03_two_groups.mp3",
            fallback_duration=15.0,
            visual_func=visual_two_groups,
        )

        # =====================================================
        # CẢNH 4 - FOCUS ALGORITHMIC INNOVATIONS
        # =====================================================
        def visual_algorithmic_focus(wait_to, play, duration):
            title = text_en("Algorithmic Innovations", font_size=40, color=WHITE)
            fit_text(title, 11.0)
            title.to_edge(UP, buff=0.35)

            subtitle = text_vi("Tập trung vào cách mô hình suy luận", font_size=24, color=BLUE)
            subtitle.next_to(title, DOWN, buff=0.16)

            focus_box = make_box_en(
                "Algorithmic Innovations",
                GREEN,
                width=4.75,
                height=0.78,
                font_size=24,
                fill=0.13,
            )
            focus_box.move_to(UP * 0.88)

            left_card = make_mixed_card(
                "Not only GPU speed",
                "Không chỉ hỏi:\nchạy model nhanh hơn trên GPU?",
                RED,
                width=4.70,
                height=1.22,
                heading_size=20,
                desc_size=18,
                fill=0.09,
            )
            left_card.move_to(LEFT * 2.75 + DOWN * 0.55)

            right_card = make_mixed_card(
                "Change inference",
                "Có thể thay đổi cách mô hình suy luận\nđể nhẹ hơn ngay từ đầu không?",
                YELLOW,
                width=5.05,
                height=1.22,
                heading_size=20,
                desc_size=17,
                fill=0.10,
            )
            right_card.move_to(RIGHT * 2.60 + DOWN * 0.55)

            arrow = Arrow(
                left_card.get_right(),
                right_card.get_left(),
                color=YELLOW,
                stroke_width=4,
                buff=0.18,
            )

            wait_to(0.02)
            play(Write(title), run_time=0.45)

            wait_to(0.15)
            play(FadeIn(subtitle, shift=UP), run_time=0.25)

            wait_to(0.28)
            play(FadeIn(focus_box, shift=UP), run_time=0.32)

            wait_to(0.48)
            play(FadeIn(left_card, shift=RIGHT), run_time=0.34)

            wait_to(0.63)
            play(GrowArrow(arrow), run_time=0.26)

            wait_to(0.72)
            play(FadeIn(right_card, shift=LEFT), run_time=0.40)

            wait_to(0.88)
            play(Flash(right_card[0], color=YELLOW), run_time=0.45)

            set_active(title, subtitle, focus_box, left_card, right_card, arrow)

        play_segment(
            "p3_00_04_algorithmic_focus.mp3",
            fallback_duration=18.0,
            visual_func=visual_algorithmic_focus,
        )

        # =====================================================
        # CẢNH 5 - BA NHÓM CHÍNH
        # =====================================================
        def visual_three_groups(wait_to, play, duration):
            title = text_en("Algorithmic Innovations", font_size=39, color=WHITE)
            fit_text(title, 11.0)
            title.to_edge(UP, buff=0.32)

            subtitle = text_vi("Ba nhóm chính", font_size=28, color=GREEN)
            subtitle.next_to(title, DOWN, buff=0.18)

            decoding = make_mixed_card(
                "1. Decoding Algorithms",
                "tối ưu cách mô hình sinh token",
                GREEN,
                width=6.25,
                height=0.88,
                heading_size=22,
                desc_size=18,
                fill=0.10,
            )
            architecture = make_mixed_card(
                "2. Architecture Design",
                "thay đổi kiến trúc bên trong mô hình",
                BLUE,
                width=6.25,
                height=0.88,
                heading_size=22,
                desc_size=18,
                fill=0.10,
            )
            compression = make_mixed_card(
                "3. Model Compression",
                "nén mô hình nhỏ hơn, nhanh hơn, rẻ hơn",
                ORANGE,
                width=6.25,
                height=0.88,
                heading_size=22,
                desc_size=18,
                fill=0.10,
            )

            groups = VGroup(decoding, architecture, compression)
            groups.arrange(DOWN, buff=0.34)
            groups.move_to(DOWN * 0.42)

            wait_to(0.02)
            play(Write(title), run_time=0.45)

            wait_to(0.16)
            play(FadeIn(subtitle, shift=UP), run_time=0.30)

            wait_to(0.34)
            play(FadeIn(decoding, shift=RIGHT), run_time=0.42)
            play(decoding[0].animate.set_stroke(GREEN, width=3.4).set_fill(GREEN, opacity=0.15), run_time=0.18)

            wait_to(0.56)
            play(FadeIn(architecture, shift=RIGHT), run_time=0.42)
            play(architecture[0].animate.set_stroke(BLUE, width=3.4).set_fill(BLUE, opacity=0.15), run_time=0.18)

            wait_to(0.76)
            play(FadeIn(compression, shift=RIGHT), run_time=0.42)
            play(compression[0].animate.set_stroke(ORANGE, width=3.4).set_fill(ORANGE, opacity=0.15), run_time=0.18)

            set_active(title, subtitle, groups)

        play_segment(
            "p3_00_05_three_groups.mp3",
            fallback_duration=17.0,
            visual_func=visual_three_groups,
        )

        # =====================================================
        # CẢNH 6 - MỤC TIÊU CHUNG
        # =====================================================
        def visual_goal(wait_to, play, duration):
            title = text_vi("Mục tiêu chung", font_size=36, color=YELLOW)
            title.to_edge(UP, buff=0.42)

            intro = text_vi(
                "Giảm chi phí suy luận nhưng vẫn giữ chất lượng đầu ra.",
                font_size=24,
                color=WHITE,
            )
            fit_text(intro, 10.7)
            intro.next_to(title, DOWN, buff=0.25)

            goals = VGroup(
                make_box_en("Latency", RED, width=1.75, height=0.58, font_size=19, fill=0.11),
                make_box_en("Compute", ORANGE, width=1.85, height=0.58, font_size=19, fill=0.11),
                make_box_en("Memory", BLUE, width=1.80, height=0.58, font_size=19, fill=0.11),
                make_box_en("Cost", PURPLE, width=1.55, height=0.58, font_size=19, fill=0.11),
                make_box_en("Quality", GREEN, width=1.85, height=0.58, font_size=19, fill=0.11),
            )
            goals.arrange(RIGHT, buff=0.20)
            goals.move_to(DOWN * 0.35)

            arrows = VGroup()
            for i in range(4):
                arrows.add(
                    Arrow(
                        goals[i].get_right(),
                        goals[i + 1].get_left(),
                        color=MUTED,
                        stroke_width=1.8,
                        buff=0.08,
                    )
                )

            note = text_vi(
                "Nhanh hơn, ít tốn tài nguyên hơn, nhưng chất lượng vẫn phải tốt nhất có thể.",
                font_size=22,
                color=YELLOW,
            )
            fit_text(note, 10.8)
            note.move_to(DOWN * 1.55)

            wait_to(0.02)
            play(FadeIn(title, shift=UP), run_time=0.35)

            wait_to(0.18)
            play(FadeIn(intro, shift=UP), run_time=0.35)

            wait_to(0.38)
            play(
                LaggedStart(
                    *[FadeIn(item, shift=UP) for item in goals],
                    lag_ratio=0.10,
                ),
                Create(arrows),
                run_time=0.90,
            )

            wait_to(0.75)
            play(FadeIn(note, shift=UP), run_time=0.35)

            wait_to(0.88)
            play(Flash(goals[-1][0], color=GREEN), run_time=0.55)

            set_active(title, intro, goals, arrows, note)

        play_segment(
            "p3_00_06_goal.mp3",
            fallback_duration=8.5,
            visual_func=visual_goal,
        )

        final_mobs = [m for m in active_mobs if m is not None]
        if final_mobs:
            self.play(*[FadeOut(m) for m in final_mobs], run_time=0.60)
