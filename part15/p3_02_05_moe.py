# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
import os

# ============================================================
# PHẦN 2.5 - CONDITIONAL COMPUTING VÀ MOE
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_02_05_moe.py SceneP3MoE
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
DIM = "#334155"
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


def audio_duration(path, fallback=10.0):
    if not os.path.exists(path):
        print(f"[WARNING] Không tìm thấy audio: {path}")
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


def make_title(text):
    title = Text(text, font_size=40, color=WHITE, font=FONT)
    fit_text(title, 11.2)
    title.to_edge(UP, buff=0.32)
    return title


def make_subtitle(text, title):
    subtitle = Text(text, font_size=23, color=BLUE, font=FONT)
    fit_text(subtitle, 10.8)
    subtitle.next_to(title, DOWN, buff=0.16)
    return subtitle


def make_box(text, color, width=2.8, height=0.78, font_size=21, fill_opacity=0.13):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.3,
        fill_color=color,
        fill_opacity=fill_opacity,
    )

    label = Text(
        text,
        font_size=font_size,
        color=WHITE,
        font=FONT,
        line_spacing=0.82,
    )
    fit_text(label, width - 0.24, height - 0.16)
    label.move_to(box.get_center())
    return VGroup(box, label)


def token_box(text, color=BLUE, width=1.7, height=0.55, font_size=18):
    return make_box(
        text,
        color=color,
        width=width,
        height=height,
        font_size=font_size,
        fill_opacity=0.15,
    )


class SceneP3MoE(Scene):
    def construct(self):
        self.camera.background_color = BG

        active_mobs = []

        def audio_path(filename):
            return os.path.join("voice", filename)

        def play_segment(filename, fallback_duration, visual_func):
            path = audio_path(filename)
            duration = audio_duration(path, fallback=fallback_duration)

            if os.path.exists(path):
                self.add_sound(path)
            else:
                print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path}")

            local_time = 0.0

            def wait_to(ratio):
                nonlocal local_time
                target = duration * ratio
                delay = max(0, target - local_time)
                if delay > 0:
                    self.wait(delay)
                    local_time += delay

            def play_timed(*animations, run_time=0.35, **kwargs):
                nonlocal local_time
                self.play(*animations, run_time=run_time, **kwargs)
                local_time += run_time

            visual_func(wait_to, play_timed, duration)

            remain = max(0, duration - local_time)
            if remain > 0:
                self.wait(remain)

        def clear_active(play_timed, run_time=0.16):
            nonlocal active_mobs
            valid = [m for m in active_mobs if m is not None]
            if valid:
                play_timed(*[FadeOut(m) for m in valid], run_time=run_time)
            active_mobs = []

        def set_active(*mobs):
            nonlocal active_mobs
            active_mobs = [m for m in mobs if m is not None]

        def section_title(text, subtitle, color=WHITE, font_size=28):
            t = Text(text, font_size=font_size, color=color, font=FONT)
            fit_text(t, 10.8)
            t.next_to(subtitle, DOWN, buff=0.30)
            return t

        def bottom_note(text, color=YELLOW, font_size=21, y=-2.30):
            note = Text(text, font_size=font_size, color=color, font=FONT)
            fit_text(note, 11.0)
            note.move_to(DOWN * abs(y))
            return note

        def expert_box(name, color, width=2.35, height=0.56, font_size=19, opacity=0.13):
            return make_box(
                name,
                color=color,
                width=width,
                height=height,
                font_size=font_size,
                fill_opacity=opacity,
            )

        title = make_title("Conditional Computing")
        subtitle = make_subtitle("Mỗi token chỉ kích hoạt phần cần thiết", title)

        # =====================================================
        # 1) INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            dense_box = make_box(
                "Dense model\nmọi token dùng toàn bộ mạng",
                RED,
                width=3.75,
                height=1.00,
                font_size=21,
            )
            dense_box.move_to(LEFT * 2.75 + UP * 0.05)

            conditional_box = make_box(
                "Conditional computing\nchỉ kích hoạt phần cần thiết",
                GREEN,
                width=3.95,
                height=1.00,
                font_size=21,
            )
            conditional_box.move_to(RIGHT * 2.75 + UP * 0.05)

            arrow = Arrow(
                dense_box.get_right(),
                conditional_box.get_left(),
                color=YELLOW,
                stroke_width=4,
                buff=0.18,
            )

            note = bottom_note(
                "Không phải mọi token đều cần dùng toàn bộ mô hình",
                color=YELLOW,
                font_size=21,
            )

            play(Write(title), run_time=0.48)

            wait_to(0.06)
            play(FadeIn(subtitle, shift=UP), run_time=0.24)

            wait_to(0.24)
            play(FadeIn(dense_box, shift=UP), run_time=0.32)

            wait_to(0.50)
            play(
                Create(arrow),
                FadeIn(conditional_box, shift=UP),
                run_time=0.38,
            )

            wait_to(0.76)
            play(FadeIn(note, shift=UP), run_time=0.28)

            set_active(dense_box, conditional_box, arrow, note)

        play_segment(
            "p3_02_05_01_intro.mp3",
            fallback_duration=14.0,
            visual_func=visual_intro,
        )

        # =====================================================
        # 2) ROUTER SELECT EXPERTS
        # =====================================================
        def visual_router(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            moe_title = section_title(
                "MoE: Router chọn expert cho từng token",
                subtitle,
                color=WHITE,
                font_size=27,
            )

            token = token_box(
                "Token\nrepresentation",
                BLUE,
                width=2.40,
                height=0.72,
                font_size=19,
            )
            token.move_to(LEFT * 4.15 + UP * 0.65)

            router = make_box(
                "Router",
                YELLOW,
                width=1.85,
                height=0.70,
                font_size=23,
            )
            router.move_to(LEFT * 1.55 + UP * 0.65)

            token_to_router = Arrow(
                token.get_right(),
                router.get_left(),
                color=YELLOW,
                stroke_width=3,
                buff=0.15,
            )

            experts = VGroup()
            ys = [1.25, 0.62, -0.01, -0.64, -1.27]

            for i, y in enumerate(ys, start=1):
                if i in [2, 4]:
                    color = GREEN
                    opacity = 0.17
                else:
                    color = MUTED
                    opacity = 0.05

                expert = expert_box(
                    f"Expert {i}",
                    color=color,
                    width=2.35,
                    height=0.52,
                    font_size=19,
                    opacity=opacity,
                )
                expert.move_to(RIGHT * 2.65 + UP * y)

                if i not in [2, 4]:
                    expert.set_opacity(0.35)

                experts.add(expert)

            arrows = VGroup()
            for i, expert in enumerate(experts, start=1):
                color = GREEN if i in [2, 4] else MUTED
                stroke = 3.2 if i in [2, 4] else 1.4

                arr = Arrow(
                    router.get_right(),
                    expert.get_left(),
                    color=color,
                    stroke_width=stroke,
                    buff=0.12,
                    max_tip_length_to_length_ratio=0.12,
                )

                if i not in [2, 4]:
                    arr.set_opacity(0.25)

                arrows.add(arr)

            selected_2 = Text(
                "selected",
                font_size=17,
                color=GREEN,
                font=FONT,
            )
            selected_2.next_to(experts[1], RIGHT, buff=0.18)

            selected_4 = Text(
                "selected",
                font_size=17,
                color=GREEN,
                font=FONT,
            )
            selected_4.next_to(experts[3], RIGHT, buff=0.18)

            dim_note = bottom_note(
                "Expert không được chọn thì không cần chạy cho token này",
                color=GREEN,
                font_size=21,
            )

            wait_to(0.02)
            play(FadeIn(moe_title, shift=UP), run_time=0.25)

            wait_to(0.12)
            play(FadeIn(token, shift=RIGHT), run_time=0.32)

            wait_to(0.26)
            play(
                FadeIn(router, shift=RIGHT),
                Create(token_to_router),
                run_time=0.36,
            )

            wait_to(0.42)
            play(
                LaggedStart(
                    *[FadeIn(ex, shift=LEFT) for ex in experts],
                    lag_ratio=0.08,
                ),
                run_time=0.65,
            )

            wait_to(0.62)
            play(
                Create(arrows),
                FadeIn(selected_2, shift=LEFT),
                FadeIn(selected_4, shift=LEFT),
                run_time=0.55,
            )

            wait_to(0.82)
            play(FadeIn(dim_note, shift=UP), run_time=0.28)

            set_active(
                moe_title,
                token,
                router,
                token_to_router,
                experts,
                arrows,
                selected_2,
                selected_4,
                dim_note,
            )

        play_segment(
            "p3_02_05_02_router.mp3",
            fallback_duration=24.0,
            visual_func=visual_router,
        )

        # =====================================================
        # 3) TOTAL PARAMS VS ACTIVE PARAMS
        # =====================================================
        def visual_params(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            params_title = section_title(
                "Total parameters lớn, active parameters nhỏ",
                subtitle,
                color=YELLOW,
                font_size=27,
            )

            total_box = make_box(
                "Total parameters\nrất lớn",
                RED,
                width=3.35,
                height=1.02,
                font_size=23,
            )
            total_box.move_to(LEFT * 3.00 + UP * 0.35)

            active_box = make_box(
                "Active parameters\nper token: nhỏ",
                GREEN,
                width=3.35,
                height=1.02,
                font_size=23,
            )
            active_box.move_to(RIGHT * 3.00 + UP * 0.35)

            total_bar_frame = RoundedRectangle(
                width=4.25,
                height=0.46,
                corner_radius=0.08,
                stroke_color=RED,
                stroke_width=2,
                fill_color=RED,
                fill_opacity=0.08,
            )
            total_bar_frame.move_to(LEFT * 3.00 + DOWN * 0.78)

            total_bar = Rectangle(
                width=4.00,
                height=0.28,
                stroke_color=RED,
                fill_color=RED,
                fill_opacity=0.65,
            )
            total_bar.move_to(total_bar_frame.get_center())

            active_bar_frame = RoundedRectangle(
                width=4.25,
                height=0.46,
                corner_radius=0.08,
                stroke_color=GREEN,
                stroke_width=2,
                fill_color=GREEN,
                fill_opacity=0.08,
            )
            active_bar_frame.move_to(RIGHT * 3.00 + DOWN * 0.78)

            active_bar = Rectangle(
                width=1.10,
                height=0.28,
                stroke_color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.70,
            )
            active_bar.move_to(active_bar_frame.get_center())
            active_bar.align_to(active_bar_frame, LEFT)
            active_bar.shift(RIGHT * 0.16)

            capacity_note = bottom_note(
                "Tăng capacity mà không tăng tương ứng chi phí mỗi token",
                color=YELLOW,
                font_size=21,
            )

            wait_to(0.02)
            play(FadeIn(params_title, shift=UP), run_time=0.25)

            wait_to(0.18)
            play(
                FadeIn(total_box, shift=UP),
                Create(total_bar_frame),
                FadeIn(total_bar, shift=RIGHT),
                run_time=0.45,
            )

            wait_to(0.45)
            play(
                FadeIn(active_box, shift=UP),
                Create(active_bar_frame),
                FadeIn(active_bar, shift=RIGHT),
                run_time=0.45,
            )

            wait_to(0.70)
            play(FadeIn(capacity_note, shift=UP), run_time=0.32)

            set_active(
                params_title,
                total_box,
                active_box,
                total_bar_frame,
                total_bar,
                active_bar_frame,
                active_bar,
                capacity_note,
            )

        play_segment(
            "p3_02_05_03_params.mp3",
            fallback_duration=16.0,
            visual_func=visual_params,
        )

        # =====================================================
        # 4) BUILDING ANALOGY + CAVEAT
        # =====================================================
        def visual_analogy(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            analogy_title = section_title(
                "Ví dụ trực quan: tòa nhà nhiều phòng",
                subtitle,
                color=ORANGE,
                font_size=27,
            )

            building = RoundedRectangle(
                width=3.85,
                height=2.35,
                corner_radius=0.12,
                stroke_color=WHITE,
                stroke_width=2.0,
                fill_color=WHITE,
                fill_opacity=0.04,
            )
            building.move_to(LEFT * 2.90 + DOWN * 0.02)

            building_label = Text(
                "Model có nhiều phòng chuyên môn",
                font_size=18,
                color=WHITE,
                font=FONT,
            )
            fit_text(building_label, 4.05)
            building_label.next_to(building, UP, buff=0.16)

            rooms = VGroup()
            room_names = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5", "Room 6"]

            for idx, name in enumerate(room_names):
                color = GREEN if idx in [1, 4] else MUTED
                fill = 0.18 if idx in [1, 4] else 0.04

                room = make_box(
                    name,
                    color=color,
                    width=1.18,
                    height=0.52,
                    font_size=15,
                    fill_opacity=fill,
                )

                if idx not in [1, 4]:
                    room.set_opacity(0.40)

                rooms.add(room)

            rooms.arrange_in_grid(rows=3, cols=2, buff=0.22)
            rooms.move_to(building.get_center())

            token = token_box(
                "token",
                BLUE,
                width=1.22,
                height=0.48,
                font_size=17,
            )
            token.move_to(RIGHT * 2.95 + UP * 0.95)

            router = make_box(
                "router",
                YELLOW,
                width=1.45,
                height=0.55,
                font_size=18,
            )
            router.move_to(RIGHT * 2.95 + UP * 0.22)

            pick_arrow = Arrow(
                token.get_bottom(),
                router.get_top(),
                color=YELLOW,
                buff=0.12,
                stroke_width=3,
            )

            to_room_2 = Arrow(
                router.get_left(),
                rooms[1].get_right(),
                color=GREEN,
                buff=0.16,
                stroke_width=3,
            )

            to_room_5 = Arrow(
                router.get_left(),
                rooms[4].get_right(),
                color=GREEN,
                buff=0.16,
                stroke_width=3,
            )

            caveat = make_box(
                "Lưu ý\nExpert không có nhãn cố định\nnhư toán, code, văn bản",
                RED,
                width=4.55,
                height=1.10,
                font_size=18,
            )
            caveat.move_to(RIGHT * 2.85 + DOWN * 0.95)

            learned_note = bottom_note(
                "Expert và router đều được học trong quá trình huấn luyện",
                color=YELLOW,
                font_size=21,
            )

            wait_to(0.02)
            play(FadeIn(analogy_title, shift=UP), run_time=0.25)

            wait_to(0.16)
            play(
                Create(building),
                FadeIn(building_label, shift=UP),
                FadeIn(rooms, shift=UP),
                run_time=0.55,
            )

            wait_to(0.38)
            play(
                FadeIn(token, shift=UP),
                FadeIn(router, shift=UP),
                Create(pick_arrow),
                run_time=0.42,
            )

            wait_to(0.50)
            play(
                Create(to_room_2),
                Create(to_room_5),
                run_time=0.40,
            )

            wait_to(0.66)
            play(FadeIn(caveat, shift=UP), run_time=0.38)

            wait_to(0.84)
            play(FadeIn(learned_note, shift=UP), run_time=0.26)

            set_active(
                analogy_title,
                building,
                building_label,
                rooms,
                token,
                router,
                pick_arrow,
                to_room_2,
                to_room_5,
                caveat,
                learned_note,
            )

        play_segment(
            "p3_02_05_04_analogy.mp3",
            fallback_duration=24.0,
            visual_func=visual_analogy,
        )

        # =====================================================
        # 5) SERVING CHALLENGES
        # =====================================================
        def visual_serving(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            serving_title = section_title(
                "Serving MoE khó hơn model dense",
                subtitle,
                color=RED,
                font_size=28,
            )

            dense = make_box(
                "Dense model\nluồng xử lý đều hơn",
                BLUE,
                width=3.25,
                height=0.92,
                font_size=21,
            )
            dense.move_to(LEFT * 3.10 + UP * 0.95)

            moe = make_box(
                "MoE serving\nphụ thuộc router + expert",
                RED,
                width=3.55,
                height=0.92,
                font_size=21,
            )
            moe.move_to(RIGHT * 2.85 + UP * 0.95)

            compare_arrow = Arrow(
                dense.get_right(),
                moe.get_left(),
                color=RED,
                buff=0.15,
                stroke_width=3.5,
            )

            issue1 = make_box(
                "1. Router\nchọn expert tốt",
                YELLOW,
                width=3.05,
                height=0.88,
                font_size=20,
            )

            issue2 = make_box(
                "2. Load balance\ntránh expert bottleneck",
                RED,
                width=3.35,
                height=0.88,
                font_size=20,
            )

            issue3 = make_box(
                "3. Communication\ngiữa nhiều GPU",
                PURPLE,
                width=3.15,
                height=0.88,
                font_size=20,
            )

            issues = VGroup(issue1, issue2, issue3)
            issues.arrange(RIGHT, buff=0.40)
            issues.move_to(DOWN * 0.55)

            gpu_note = bottom_note(
                "Token có thể phải được gửi tới expert nằm trên GPU khác",
                color=YELLOW,
                font_size=21,
            )

            wait_to(0.02)
            play(FadeIn(serving_title, shift=UP), run_time=0.25)

            wait_to(0.18)
            play(
                FadeIn(dense, shift=UP),
                Create(compare_arrow),
                FadeIn(moe, shift=UP),
                run_time=0.48,
            )

            wait_to(0.40)
            play(FadeIn(issue1, shift=UP), run_time=0.30)

            wait_to(0.56)
            play(FadeIn(issue2, shift=UP), run_time=0.30)

            wait_to(0.72)
            play(
                FadeIn(issue3, shift=UP),
                FadeIn(gpu_note, shift=UP),
                run_time=0.36,
            )

            set_active(
                serving_title,
                dense,
                moe,
                compare_arrow,
                issues,
                gpu_note,
            )

        play_segment(
            "p3_02_05_05_serving.mp3",
            fallback_duration=17.0,
            visual_func=visual_serving,
        )

        # =====================================================
        # 6) SUMMARY
        # =====================================================
        def visual_summary(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            summary_title = section_title(
                "Tóm tắt MoE",
                subtitle,
                color=YELLOW,
                font_size=29,
            )

            many_experts = make_box(
                "Nhiều expert\ncapacity lớn hơn",
                GREEN,
                width=3.00,
                height=0.90,
                font_size=21,
            )

            active_subset = make_box(
                "Mỗi token\nchỉ kích hoạt một phần",
                BLUE,
                width=3.20,
                height=0.90,
                font_size=21,
            )

            hard_serving = make_box(
                "Serving\nkhó tối ưu hơn",
                RED,
                width=3.00,
                height=0.90,
                font_size=21,
            )

            chain = VGroup(many_experts, active_subset, hard_serving)
            chain.arrange(RIGHT, buff=0.50)
            chain.move_to(UP * 0.25)

            arr1 = Arrow(
                many_experts.get_right(),
                active_subset.get_left(),
                color=MUTED,
                buff=0.12,
                stroke_width=2.5,
            )

            arr2 = Arrow(
                active_subset.get_right(),
                hard_serving.get_left(),
                color=MUTED,
                buff=0.12,
                stroke_width=2.5,
            )

            final_note = bottom_note(
                "MoE: tăng dung lượng mô hình, đổi lại hệ thống serving phức tạp hơn",
                color=YELLOW,
                font_size=21,
            )

            wait_to(0.02)
            play(FadeIn(summary_title, shift=UP), run_time=0.25)

            wait_to(0.20)
            play(FadeIn(many_experts, shift=UP), run_time=0.30)

            wait_to(0.40)
            play(
                Create(arr1),
                FadeIn(active_subset, shift=UP),
                run_time=0.32,
            )

            wait_to(0.62)
            play(
                Create(arr2),
                FadeIn(hard_serving, shift=UP),
                run_time=0.32,
            )

            wait_to(0.78)
            play(FadeIn(final_note, shift=UP), run_time=0.28)

            set_active(
                summary_title,
                chain,
                arr1,
                arr2,
                final_note,
            )

        play_segment(
            "p3_02_05_06_summary.mp3",
            fallback_duration=12.0,
            visual_func=visual_summary,
        )

        final_mobs = [m for m in active_mobs if m is not None]
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            *[FadeOut(m) for m in final_mobs],
            run_time=0.50,
        )
