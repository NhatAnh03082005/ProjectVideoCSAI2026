# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# PHẦN 1.5 - CASCADE INFERENCE
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_01_05_cascade.py SceneP30105CascadeInference
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
    # English: dùng font mặc định của Manim
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
    width=3.4,
    height=1.0,
    heading_size=21,
    desc_size=17,
    fill=0.10,
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

    fit_text(heading, width - 0.30, height * 0.40)
    fit_text(desc, width - 0.30, height * 0.42)

    group = VGroup(heading, desc).arrange(DOWN, buff=0.06)
    group.move_to(box.get_center())

    return VGroup(box, group)


def make_title_en(text):
    title = text_en(text, font_size=40, color=WHITE)
    fit_text(title, 11.0)
    title.to_edge(UP, buff=0.30)
    return title


def make_subtitle_vi(text, title):
    subtitle = text_vi(text, font_size=23, color=BLUE)
    fit_text(subtitle, 10.8)
    subtitle.next_to(title, DOWN, buff=0.13)
    return subtitle


def bottom_note_vi(text, color=YELLOW, font_size=21, y=-2.18):
    note = text_vi(text, font_size=font_size, color=color)
    fit_text(note, 10.8)
    note.move_to(DOWN * abs(y))
    return note


def highlight_box(box_group, color, opacity=0.17, width=3.4):
    return box_group[0].animate.set_stroke(color, width=width).set_fill(
        color, opacity=opacity
    )


def dim_box(box_group, color, opacity=0.08, width=2.0):
    return box_group[0].animate.set_stroke(color, width=width).set_fill(
        color, opacity=opacity
    )


def check_mark(center, color=GREEN, scale=0.65):
    mark = Text("✓", font_size=46, color=color)
    mark.scale(scale)
    mark.move_to(center)
    return mark


def cross_mark(center, color=RED, scale=0.65):
    mark = Text("✕", font_size=46, color=color)
    mark.scale(scale)
    mark.move_to(center)
    return mark


class SceneP30105CascadeInference(Scene):
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

        title = make_title_en("Cascade Inference")
        subtitle = make_subtitle_vi(
            "Suy luận theo tầng: request dễ dùng model nhỏ",
            title,
        )

        # =====================================================
        # CẢNH 1 - INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            vi_box = make_box_vi(
                "Suy luận theo tầng",
                YELLOW,
                width=4.55,
                height=0.76,
                font_size=25,
                fill=0.11,
            )
            vi_box.move_to(UP * 0.68)

            small = make_box_en(
                "Small Model",
                GREEN,
                width=2.55,
                height=0.56,
                font_size=19,
                fill=0.10,
            )

            medium = make_box_en(
                "Medium Model",
                BLUE,
                width=2.75,
                height=0.56,
                font_size=19,
                fill=0.10,
            )

            large = make_box_en(
                "Large Model",
                RED,
                width=2.65,
                height=0.56,
                font_size=19,
                fill=0.10,
            )

            stack = VGroup(small, medium, large)
            stack.arrange(DOWN, buff=0.22)
            stack.move_to(DOWN * 0.85)

            note = bottom_note_vi(
                "Không phải request nào cũng cần model lớn nhất",
                color=YELLOW,
                font_size=21,
                y=-2.20,
            )

            play(Write(title), run_time=0.50)

            wait_to(0.14)
            play(FadeIn(subtitle, shift=UP), run_time=0.25)

            wait_to(0.40)
            play(FadeIn(vi_box, shift=UP), run_time=0.35)

            wait_to(0.62)
            play(
                LaggedStart(
                    FadeIn(small, shift=UP),
                    FadeIn(medium, shift=UP),
                    FadeIn(large, shift=UP),
                    lag_ratio=0.16,
                ),
                run_time=0.65,
            )

            wait_to(0.82)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(vi_box, stack, note)

        play_segment(
            "p3_01_05_01_intro.mp3",
            fallback_duration=5.0,
            visual_func=visual_intro,
            clear_before=False,
        )

        # =====================================================
        # CẢNH 2 - ROUTER PHÂN NHÁNH
        # =====================================================
        def visual_multi_model(wait_to, play, duration):
            request = make_box_en(
                "User request",
                YELLOW,
                width=2.35,
                height=0.58,
                font_size=19,
                fill=0.10,
            )
            request.move_to(LEFT * 5.20 + UP * 0.20)

            router = make_box_en(
                "Router",
                BLUE,
                width=1.95,
                height=0.68,
                font_size=22,
                fill=0.13,
            )
            router.move_to(LEFT * 2.65 + UP * 0.20)

            easy_label = make_box_en(
                "Easy",
                GREEN,
                width=1.32,
                height=0.42,
                font_size=16,
                fill=0.09,
            )

            medium_label = make_box_en(
                "Medium",
                BLUE,
                width=1.62,
                height=0.42,
                font_size=16,
                fill=0.09,
            )

            hard_label = make_box_en(
                "Hard",
                RED,
                width=1.32,
                height=0.42,
                font_size=16,
                fill=0.09,
            )

            labels = VGroup(easy_label, medium_label, hard_label)
            labels.arrange(DOWN, buff=0.58)
            labels.move_to(RIGHT * 0.25 + UP * 0.20)

            small = make_mixed_card(
                "Small Model",
                "nhanh, rẻ",
                GREEN,
                width=2.75,
                height=0.76,
                heading_size=19,
                desc_size=15,
            )

            medium = make_mixed_card(
                "Medium Model",
                "cân bằng",
                BLUE,
                width=2.90,
                height=0.76,
                heading_size=19,
                desc_size=15,
            )

            large = make_mixed_card(
                "Large Model",
                "chất lượng cao",
                RED,
                width=2.75,
                height=0.76,
                heading_size=19,
                desc_size=15,
            )

            models = VGroup(small, medium, large)
            models.arrange(DOWN, buff=0.38)
            models.move_to(RIGHT * 4.25 + UP * 0.20)

            a0 = Arrow(
                request.get_right(),
                router.get_left(),
                color=YELLOW,
                stroke_width=2.6,
                buff=0.14,
            )

            # Tách thành hai chặng để label không đè lên arrow:
            # Router -> Easy/Medium/Hard -> Model
            arrows_left = VGroup(
                Arrow(router.get_right(), easy_label.get_left(), color=GREEN, stroke_width=2.4, buff=0.12),
                Arrow(router.get_right(), medium_label.get_left(), color=BLUE, stroke_width=2.4, buff=0.12),
                Arrow(router.get_right(), hard_label.get_left(), color=RED, stroke_width=2.4, buff=0.12),
            )

            arrows_right = VGroup(
                Arrow(easy_label.get_right(), small.get_left(), color=GREEN, stroke_width=2.4, buff=0.12),
                Arrow(medium_label.get_right(), medium.get_left(), color=BLUE, stroke_width=2.4, buff=0.12),
                Arrow(hard_label.get_right(), large.get_left(), color=RED, stroke_width=2.4, buff=0.12),
            )

            note = bottom_note_vi(
                "Router chọn model phù hợp theo độ khó của request",
                color=YELLOW,
                font_size=21,
                y=-2.20,
            )

            wait_to(0.03)
            play(FadeIn(request, shift=RIGHT), run_time=0.30)

            wait_to(0.22)
            play(Create(a0), FadeIn(router, shift=RIGHT), run_time=0.35)

            wait_to(0.42)
            play(
                LaggedStart(
                    Create(arrows_left[0]),
                    FadeIn(easy_label, shift=UP),
                    Create(arrows_right[0]),
                    FadeIn(small, shift=LEFT),
                    Create(arrows_left[1]),
                    FadeIn(medium_label, shift=UP),
                    Create(arrows_right[1]),
                    FadeIn(medium, shift=LEFT),
                    Create(arrows_left[2]),
                    FadeIn(hard_label, shift=UP),
                    Create(arrows_right[2]),
                    FadeIn(large, shift=LEFT),
                    lag_ratio=0.08,
                ),
                run_time=1.10,
            )

            wait_to(0.82)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(
                request,
                router,
                a0,
                labels,
                models,
                arrows_left,
                arrows_right,
                note,
            )

        play_segment(
            "p3_01_05_02_multi_model.mp3",
            fallback_duration=7.0,
            visual_func=visual_multi_model,
        )

        # =====================================================
        # CẢNH 3 - EASY / MEDIUM / HARD
        # =====================================================
        def visual_easy_medium_hard(wait_to, play, duration):
            router = make_box_en(
                "Router",
                BLUE,
                width=2.15,
                height=0.72,
                font_size=23,
                fill=0.13,
            )
            router.move_to(LEFT * 3.85 + UP * 0.20)

            easy = make_mixed_card(
                "Easy",
                "câu dễ",
                GREEN,
                width=2.15,
                height=0.70,
                heading_size=20,
                desc_size=16,
            )

            medium = make_mixed_card(
                "Medium",
                "câu trung bình",
                BLUE,
                width=2.35,
                height=0.70,
                heading_size=20,
                desc_size=16,
            )

            hard = make_mixed_card(
                "Hard",
                "câu khó",
                RED,
                width=2.15,
                height=0.70,
                heading_size=20,
                desc_size=16,
            )

            small_model = make_box_en(
                "Small Model",
                GREEN,
                width=2.55,
                height=0.62,
                font_size=19,
                fill=0.10,
            )

            medium_model = make_box_en(
                "Medium Model",
                BLUE,
                width=2.75,
                height=0.62,
                font_size=19,
                fill=0.10,
            )

            large_model = make_box_en(
                "Large Model",
                RED,
                width=2.55,
                height=0.62,
                font_size=19,
                fill=0.10,
            )

            rows = VGroup(
                VGroup(easy, small_model).arrange(RIGHT, buff=1.05),
                VGroup(medium, medium_model).arrange(RIGHT, buff=0.82),
                VGroup(hard, large_model).arrange(RIGHT, buff=1.05),
            )
            rows.arrange(DOWN, buff=0.35)
            rows.move_to(RIGHT * 1.15 + DOWN * 0.05)

            arrows = VGroup()
            for level, model, color in [
                (easy, small_model, GREEN),
                (medium, medium_model, BLUE),
                (hard, large_model, RED),
            ]:
                arrows.add(
                    Arrow(
                        level.get_right(),
                        model.get_left(),
                        color=color,
                        stroke_width=2.8,
                        buff=0.15,
                    )
                )

            router_arrows = VGroup(
                Arrow(router.get_right(), easy.get_left(), color=GREEN, stroke_width=2.2, buff=0.15),
                Arrow(router.get_right(), medium.get_left(), color=BLUE, stroke_width=2.2, buff=0.15),
                Arrow(router.get_right(), hard.get_left(), color=RED, stroke_width=2.2, buff=0.15),
            )

            note = bottom_note_vi(
                "Cấp độ khó quyết định model nào được dùng",
                color=YELLOW,
                font_size=21,
                y=-2.20,
            )

            wait_to(0.02)
            play(FadeIn(router, shift=RIGHT), run_time=0.30)

            wait_to(0.18)
            play(
                Create(router_arrows[0]),
                FadeIn(easy, shift=RIGHT),
                Create(arrows[0]),
                FadeIn(small_model, shift=LEFT),
                run_time=0.45,
            )
            play(highlight_box(small_model, GREEN), run_time=0.18)

            wait_to(0.42)
            play(
                Create(router_arrows[1]),
                FadeIn(medium, shift=RIGHT),
                Create(arrows[1]),
                FadeIn(medium_model, shift=LEFT),
                run_time=0.45,
            )
            play(highlight_box(medium_model, BLUE), run_time=0.18)

            wait_to(0.66)
            play(
                Create(router_arrows[2]),
                FadeIn(hard, shift=RIGHT),
                Create(arrows[2]),
                FadeIn(large_model, shift=LEFT),
                run_time=0.45,
            )
            play(highlight_box(large_model, RED), run_time=0.18)

            wait_to(0.84)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(router, rows, arrows, router_arrows, note)

        play_segment(
            "p3_01_05_03_easy_medium_hard.mp3",
            fallback_duration=8.0,
            visual_func=visual_easy_medium_hard,
        )

        # =====================================================
        # CẢNH 4 - VÍ DỤ REQUEST
        # =====================================================
        def visual_examples(wait_to, play, duration):
            title_vi = text_vi(
                "Ví dụ request đi vào model phù hợp",
                font_size=28,
                color=WHITE,
            )
            fit_text(title_vi, 10.6)
            title_vi.next_to(subtitle, DOWN, buff=0.34)

            router = make_box_en(
                "Router",
                BLUE,
                width=1.80,
                height=0.62,
                font_size=21,
                fill=0.12,
            )
            router.move_to(ORIGIN + DOWN * 0.08)

            small_model = make_box_en(
                "Small Model",
                GREEN,
                width=2.30,
                height=0.54,
                font_size=18,
                fill=0.10,
            )

            medium_model = make_box_en(
                "Medium Model",
                BLUE,
                width=2.48,
                height=0.54,
                font_size=18,
                fill=0.10,
            )

            large_model = make_box_en(
                "Large Model",
                RED,
                width=2.30,
                height=0.54,
                font_size=18,
                fill=0.10,
            )

            models = VGroup(small_model, medium_model, large_model)
            models.arrange(DOWN, buff=0.30)
            models.move_to(RIGHT * 4.20 + DOWN * 0.08)

            greeting = make_box_vi(
                "Chào bạn!",
                GREEN,
                width=2.35,
                height=0.54,
                font_size=19,
                fill=0.09,
            )

            email = make_box_vi(
                "Viết email ngắn",
                BLUE,
                width=2.70,
                height=0.54,
                font_size=18,
                fill=0.09,
            )

            document = make_box_vi(
                "Phân tích tài liệu\nkỹ thuật dài",
                RED,
                width=2.95,
                height=0.78,
                font_size=17,
                fill=0.09,
            )

            requests = VGroup(greeting, email, document)
            requests.arrange(DOWN, buff=0.25)
            requests.move_to(LEFT * 4.15 + DOWN * 0.08)

            in_arrows = VGroup(
                Arrow(greeting.get_right(), router.get_left(), color=GREEN, stroke_width=2.3, buff=0.12),
                Arrow(email.get_right(), router.get_left(), color=BLUE, stroke_width=2.3, buff=0.12),
                Arrow(document.get_right(), router.get_left(), color=RED, stroke_width=2.3, buff=0.12),
            )

            out_arrows = VGroup(
                Arrow(router.get_right(), small_model.get_left(), color=GREEN, stroke_width=2.3, buff=0.12),
                Arrow(router.get_right(), medium_model.get_left(), color=BLUE, stroke_width=2.3, buff=0.12),
                Arrow(router.get_right(), large_model.get_left(), color=RED, stroke_width=2.3, buff=0.12),
            )

            note = bottom_note_vi(
                "Câu càng khó thì càng cần model mạnh hơn",
                color=YELLOW,
                font_size=21,
                y=-2.20,
            )

            wait_to(0.02)
            play(FadeIn(title_vi, shift=UP), run_time=0.24)

            wait_to(0.12)
            play(FadeIn(router, scale=0.95), FadeIn(models, shift=LEFT), run_time=0.38)

            wait_to(0.26)
            play(FadeIn(greeting, shift=RIGHT), Create(in_arrows[0]), Create(out_arrows[0]), run_time=0.45)
            play(highlight_box(small_model, GREEN), run_time=0.20)
            play(dim_box(small_model, GREEN), run_time=0.14)

            wait_to(0.48)
            play(FadeIn(email, shift=RIGHT), Create(in_arrows[1]), Create(out_arrows[1]), run_time=0.45)
            play(highlight_box(medium_model, BLUE), run_time=0.20)
            play(dim_box(medium_model, BLUE), run_time=0.14)

            wait_to(0.70)
            play(FadeIn(document, shift=RIGHT), Create(in_arrows[2]), Create(out_arrows[2]), run_time=0.48)
            play(highlight_box(large_model, RED), run_time=0.22)

            wait_to(0.88)
            play(FadeIn(note, shift=UP), run_time=0.28)

            set_active(title_vi, router, models, requests, in_arrows, out_arrows, note)

        play_segment(
            "p3_01_05_04_examples.mp3",
            fallback_duration=11.0,
            visual_func=visual_examples,
        )

        # =====================================================
        # CẢNH 5 - TIẾT KIỆM CHI PHÍ
        # =====================================================
        def visual_cost(wait_to, play, duration):
            title_vi = text_vi(
                "Tiết kiệm chi phí inference",
                font_size=30,
                color=GREEN,
            )
            fit_text(title_vi, 10.6)
            title_vi.next_to(subtitle, DOWN, buff=0.34)

            small = make_mixed_card(
                "Small Model",
                "dùng thường xuyên",
                GREEN,
                width=3.00,
                height=0.80,
                heading_size=20,
                desc_size=16,
            )

            medium = make_mixed_card(
                "Medium Model",
                "dùng khi cần",
                BLUE,
                width=3.00,
                height=0.80,
                heading_size=20,
                desc_size=16,
            )

            large = make_mixed_card(
                "Large Model",
                "chỉ dùng khi thật sự cần",
                RED,
                width=3.20,
                height=0.80,
                heading_size=20,
                desc_size=15,
            )

            models = VGroup(small, medium, large)
            models.arrange(RIGHT, buff=0.40)
            models.move_to(UP * 0.55)

            cost_bar_bg = RoundedRectangle(
                width=8.6,
                height=0.50,
                corner_radius=0.14,
                stroke_color=MUTED,
                stroke_width=1.6,
                fill_color=MUTED,
                fill_opacity=0.08,
            )
            cost_bar_bg.move_to(DOWN * 0.85)

            cost_fill = Rectangle(
                width=2.25,
                height=0.28,
                stroke_color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.70,
            )
            cost_fill.move_to(cost_bar_bg.get_left() + RIGHT * (cost_fill.width / 2))

            cost_label = text_vi("Chi phí trung bình giảm", font_size=22, color=YELLOW)
            cost_label.next_to(cost_bar_bg, UP, buff=0.18)

            large_note = make_box_vi(
                "Large Model không chạy cho mọi request",
                RED,
                width=6.45,
                height=0.60,
                font_size=21,
                fill=0.09,
            )
            large_note.move_to(DOWN * 1.70)

            wait_to(0.02)
            play(FadeIn(title_vi, shift=UP), run_time=0.28)

            wait_to(0.20)
            play(
                LaggedStart(
                    FadeIn(small, shift=UP),
                    FadeIn(medium, shift=UP),
                    FadeIn(large, shift=UP),
                    lag_ratio=0.16,
                ),
                run_time=0.65,
            )

            wait_to(0.50)
            play(FadeIn(cost_label, shift=UP), Create(cost_bar_bg), run_time=0.36)

            wait_to(0.66)
            play(GrowFromEdge(cost_fill, LEFT), run_time=0.42)

            wait_to(0.80)
            play(FadeIn(large_note, shift=UP), run_time=0.32)

            wait_to(0.90)
            play(Flash(large[0], color=RED), run_time=0.50)

            set_active(title_vi, models, cost_bar_bg, cost_fill, cost_label, large_note)

        play_segment(
            "p3_01_05_05_cost.mp3",
            fallback_duration=7.0,
            visual_func=visual_cost,
        )

        # =====================================================
        # CẢNH 6 - ROUTER ĐÁNH GIÁ REQUEST
        # =====================================================
        def visual_router(wait_to, play, duration):
            title_vi = text_vi(
                "Router đánh giá độ khó của request",
                font_size=29,
                color=YELLOW,
            )
            fit_text(title_vi, 10.6)
            title_vi.next_to(subtitle, DOWN, buff=0.34)

            router = make_box_en(
                "Router",
                BLUE,
                width=2.35,
                height=0.85,
                font_size=25,
                fill=0.13,
            )
            router.move_to(ORIGIN + UP * 0.20)

            request = make_box_en(
                "Request",
                YELLOW,
                width=2.20,
                height=0.62,
                font_size=21,
                fill=0.10,
            )
            request.move_to(LEFT * 4.10 + UP * 0.20)

            choices = VGroup(
                make_box_en("Easy?", GREEN, width=1.65, height=0.48, font_size=18, fill=0.08),
                make_box_en("Medium?", BLUE, width=2.05, height=0.48, font_size=18, fill=0.08),
                make_box_en("Hard?", RED, width=1.65, height=0.48, font_size=18, fill=0.08),
            )
            choices.arrange(DOWN, buff=0.22)
            choices.move_to(RIGHT * 3.65 + UP * 0.20)

            a_in = Arrow(request.get_right(), router.get_left(), color=YELLOW, stroke_width=3, buff=0.15)

            a_out = VGroup(
                Arrow(router.get_right(), choices[0].get_left(), color=GREEN, stroke_width=2.4, buff=0.12),
                Arrow(router.get_right(), choices[1].get_left(), color=BLUE, stroke_width=2.4, buff=0.12),
                Arrow(router.get_right(), choices[2].get_left(), color=RED, stroke_width=2.4, buff=0.12),
            )

            note = bottom_note_vi(
                "Router là bước quyết định request đi vào model nào",
                color=YELLOW,
                font_size=21,
                y=-2.20,
            )

            wait_to(0.02)
            play(FadeIn(title_vi, shift=UP), run_time=0.25)

            wait_to(0.20)
            play(FadeIn(request, shift=RIGHT), Create(a_in), FadeIn(router, shift=RIGHT), run_time=0.45)

            wait_to(0.52)
            play(
                LaggedStart(
                    Create(a_out[0]),
                    FadeIn(choices[0], shift=LEFT),
                    Create(a_out[1]),
                    FadeIn(choices[1], shift=LEFT),
                    Create(a_out[2]),
                    FadeIn(choices[2], shift=LEFT),
                    lag_ratio=0.13,
                ),
                run_time=0.75,
            )

            wait_to(0.82)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(title_vi, router, request, choices, a_in, a_out, note)

        play_segment(
            "p3_01_05_06_router.mp3",
            fallback_duration=8.5,
            visual_func=visual_router,
        )

        # =====================================================
        # CẢNH 7 - ROUTER ĐÚNG / SAI
        # =====================================================
        def visual_router_risk(wait_to, play, duration):
            title_vi = text_vi(
                "Router chọn đúng hoặc chọn sai",
                font_size=30,
                color=WHITE,
            )
            fit_text(title_vi, 10.6)
            title_vi.next_to(subtitle, DOWN, buff=0.34)

            correct_panel = RoundedRectangle(
                width=5.25,
                height=2.35,
                corner_radius=0.18,
                stroke_color=GREEN,
                stroke_width=2.2,
                fill_color=GREEN,
                fill_opacity=0.06,
            )

            wrong_panel = RoundedRectangle(
                width=5.25,
                height=2.35,
                corner_radius=0.18,
                stroke_color=RED,
                stroke_width=2.2,
                fill_color=RED,
                fill_opacity=0.06,
            )

            panels = VGroup(correct_panel, wrong_panel).arrange(RIGHT, buff=0.45)
            panels.move_to(DOWN * 0.15)

            ok_title = text_vi("Chọn đúng", font_size=23, color=GREEN)
            bad_title = text_vi("Chọn sai", font_size=23, color=RED)
            ok_title.next_to(correct_panel, UP, buff=0.12)
            bad_title.next_to(wrong_panel, UP, buff=0.12)

            hard_req_ok = make_box_vi("Câu khó", RED, width=1.65, height=0.50, font_size=18, fill=0.08)
            large_model = make_box_en("Large Model", RED, width=2.15, height=0.50, font_size=17, fill=0.09)
            quality_ok = make_box_vi("Giữ chất lượng", GREEN, width=2.30, height=0.50, font_size=18, fill=0.08)

            ok_flow = VGroup(hard_req_ok, large_model, quality_ok).arrange(DOWN, buff=0.22)
            ok_flow.move_to(correct_panel.get_center())

            ok_arrows = VGroup(
                Arrow(hard_req_ok.get_bottom(), large_model.get_top(), color=MUTED, stroke_width=2.0, buff=0.07),
                Arrow(large_model.get_bottom(), quality_ok.get_top(), color=MUTED, stroke_width=2.0, buff=0.07),
            )

            hard_req_bad = make_box_vi("Câu khó", RED, width=1.65, height=0.50, font_size=18, fill=0.08)
            small_model = make_box_en("Small Model", GREEN, width=2.15, height=0.50, font_size=17, fill=0.09)
            quality_bad = make_box_vi("Chất lượng giảm", RED, width=2.35, height=0.50, font_size=18, fill=0.08)

            bad_flow = VGroup(hard_req_bad, small_model, quality_bad).arrange(DOWN, buff=0.22)
            bad_flow.move_to(wrong_panel.get_center())

            bad_arrows = VGroup(
                Arrow(hard_req_bad.get_bottom(), small_model.get_top(), color=MUTED, stroke_width=2.0, buff=0.07),
                Arrow(small_model.get_bottom(), quality_bad.get_top(), color=MUTED, stroke_width=2.0, buff=0.07),
            )

            check = check_mark(correct_panel.get_corner(UR) + LEFT * 0.28 + DOWN * 0.28, color=GREEN)
            cross = cross_mark(wrong_panel.get_corner(UR) + LEFT * 0.28 + DOWN * 0.28, color=RED)

            note = bottom_note_vi(
                "Cascade hiệu quả khi router phân loại request đủ tốt",
                color=YELLOW,
                font_size=21,
                y=-2.22,
            )

            wait_to(0.02)
            play(FadeIn(title_vi, shift=UP), run_time=0.25)

            wait_to(0.18)
            play(Create(correct_panel), FadeIn(ok_title, shift=UP), run_time=0.35)

            wait_to(0.32)
            play(FadeIn(ok_flow[0], shift=UP), Create(ok_arrows[0]), FadeIn(ok_flow[1], shift=UP), run_time=0.40)

            wait_to(0.46)
            play(Create(ok_arrows[1]), FadeIn(ok_flow[2], shift=UP), FadeIn(check, scale=0.8), run_time=0.40)

            wait_to(0.60)
            play(Create(wrong_panel), FadeIn(bad_title, shift=UP), run_time=0.30)

            wait_to(0.72)
            play(FadeIn(bad_flow[0], shift=UP), Create(bad_arrows[0]), FadeIn(bad_flow[1], shift=UP), run_time=0.38)

            wait_to(0.84)
            play(Create(bad_arrows[1]), FadeIn(bad_flow[2], shift=UP), FadeIn(cross, scale=0.8), run_time=0.38)

            wait_to(0.94)
            play(FadeIn(note, shift=UP), run_time=0.25)

            set_active(
                title_vi,
                correct_panel,
                wrong_panel,
                ok_title,
                bad_title,
                ok_flow,
                bad_flow,
                ok_arrows,
                bad_arrows,
                check,
                cross,
                note,
            )

        play_segment(
            "p3_01_05_07_router_risk.mp3",
            fallback_duration=11.0,
            visual_func=visual_router_risk,
        )

        # =====================================================
        # CẢNH 8 - TÓM TẮT
        # =====================================================
        def visual_summary(wait_to, play, duration):
            title_vi = text_vi(
                "Cascade Inference tối ưu ở cấp độ request",
                font_size=29,
                color=YELLOW,
            )
            fit_text(title_vi, 10.6)
            title_vi.next_to(subtitle, DOWN, buff=0.34)

            easy = make_mixed_card(
                "Easy request",
                "dùng model nhỏ\nnhanh và rẻ",
                GREEN,
                width=3.60,
                height=1.05,
                heading_size=22,
                desc_size=18,
                fill=0.10,
            )

            hard = make_mixed_card(
                "Hard request",
                "dùng model lớn\ngiữ chất lượng",
                RED,
                width=3.60,
                height=1.05,
                heading_size=22,
                desc_size=18,
                fill=0.10,
            )

            easy.move_to(LEFT * 2.65 + UP * 0.35)
            hard.move_to(RIGHT * 2.65 + UP * 0.35)

            small = make_box_en("Small Model", GREEN, width=2.55, height=0.58, font_size=19, fill=0.10)
            large = make_box_en("Large Model", RED, width=2.55, height=0.58, font_size=19, fill=0.10)

            small.next_to(easy, DOWN, buff=0.45)
            large.next_to(hard, DOWN, buff=0.45)

            a1 = Arrow(easy.get_bottom(), small.get_top(), color=GREEN, stroke_width=3, buff=0.12)
            a2 = Arrow(hard.get_bottom(), large.get_top(), color=RED, stroke_width=3, buff=0.12)

            final = make_box_vi(
                "Mục tiêu: nhanh hơn, rẻ hơn,\nnhưng vẫn giữ chất lượng cho câu khó",
                YELLOW,
                width=7.60,
                height=0.85,
                font_size=21,
                fill=0.09,
            )
            final.move_to(DOWN * 2.22)

            wait_to(0.02)
            play(FadeIn(title_vi, shift=UP), run_time=0.25)

            wait_to(0.22)
            play(FadeIn(easy, shift=RIGHT), Create(a1), FadeIn(small, shift=UP), run_time=0.48)
            play(highlight_box(small, GREEN), run_time=0.20)

            wait_to(0.52)
            play(FadeIn(hard, shift=LEFT), Create(a2), FadeIn(large, shift=UP), run_time=0.48)
            play(highlight_box(large, RED), run_time=0.20)

            wait_to(0.80)
            play(FadeIn(final, shift=UP), run_time=0.35)

            wait_to(0.92)
            play(Flash(final[0], color=YELLOW), run_time=0.50)

            set_active(title_vi, easy, hard, small, large, a1, a2, final)

        play_segment(
            "p3_01_05_08_summary.mp3",
            fallback_duration=9.0,
            visual_func=visual_summary,
        )

        # =====================================================
        # END
        # =====================================================
        final_mobs = [m for m in active_mobs if m is not None]
        if final_mobs:
            self.play(
                FadeOut(title),
                FadeOut(subtitle),
                *[FadeOut(m) for m in final_mobs],
                run_time=0.55,
            )
        else:
            self.play(FadeOut(title), FadeOut(subtitle), run_time=0.55)
