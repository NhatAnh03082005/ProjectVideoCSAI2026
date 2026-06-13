# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# PHẦN 2.6 - RECURRENT UNIT VÀ ALTERNATIVE ARCHITECTURES
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_02_06_recurrent.py SceneP3RecurrentUnit
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
    title = Text(text, font_size=38, color=WHITE, font=FONT)
    fit_text(title, 11.4)
    title.to_edge(UP, buff=0.28)
    return title


def make_box(text, color, width=3.0, height=0.8, font_size=21, fill_opacity=0.13):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.2,
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
    fit_text(label, width - 0.28, height - 0.16)
    label.move_to(box.get_center())
    return VGroup(box, label)


def small_token(text, color=BLUE, width=0.75, height=0.42, font_size=15):
    return make_box(
        text,
        color=color,
        width=width,
        height=height,
        font_size=font_size,
        fill_opacity=0.16,
    )


class SceneP3RecurrentUnit(Scene):
    def construct(self):
        self.camera.background_color = BG

        active_mobs = []
        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"

        def audio_path(filename):
            return str(voice_dir / filename)

        def play_segment(filename, fallback_duration, visual_func):
            nonlocal active_mobs

            # Xóa visual cũ trước khi bật audio mới.
            # Như vậy voice mới sẽ không chạy trước visual mới.
            old_mobs = [m for m in active_mobs if m is not None]
            if old_mobs:
                self.play(
                    *[FadeOut(m) for m in old_mobs],
                    run_time=0.10,
                )
                active_mobs = []

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

        def clear_active(play_timed, run_time=0.18):
            nonlocal active_mobs
            valid = [m for m in active_mobs if m is not None]
            if valid:
                play_timed(*[FadeOut(m) for m in valid], run_time=run_time)
            active_mobs = []

        def set_active(*mobs):
            nonlocal active_mobs
            active_mobs = [m for m in mobs if m is not None]

        def section_title(text, color=WHITE, font_size=27):
            t = Text(text, font_size=font_size, color=color, font=FONT)
            fit_text(t, 10.9)
            t.next_to(title, DOWN, buff=0.42)
            return t

        title = make_title("Recurrent Unit và Alternative Architectures")

        # =====================================================
        # CẢNH 1 - INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            model_boxes = VGroup(
                make_box("RWKV", GREEN, width=2.05, height=0.72, font_size=24),
                make_box("RetNet", BLUE, width=2.05, height=0.72, font_size=24),
                make_box(
                    "State-space\nmodels",
                    PURPLE,
                    width=2.55,
                    height=0.84,
                    font_size=20,
                ),
            )
            model_boxes.arrange(RIGHT, buff=0.45)
            model_boxes.move_to(UP * 0.28)

            goal = make_box(
                "Giảm phụ thuộc vào attention toàn cục\nkhi xử lý sequence dài",
                YELLOW,
                width=7.20,
                height=0.92,
                font_size=22,
                fill_opacity=0.10,
            )
            goal.next_to(model_boxes, DOWN, buff=0.55)

            play(Write(title), run_time=0.55)

            wait_to(0.34)
            play(
                LaggedStart(
                    *[FadeIn(b, shift=UP) for b in model_boxes],
                    lag_ratio=0.14,
                ),
                run_time=0.66,
            )

            wait_to(0.72)
            play(FadeIn(goal, shift=UP), run_time=0.35)

            set_active(model_boxes, goal)

        play_segment(
            "p3_02_06_01_intro.mp3",
            fallback_duration=14.0,
            visual_func=visual_intro,
        )

        # =====================================================
        # CẢNH 2 - TRANSFORMER ATTENTION
        # =====================================================
        def visual_transformer_attention(wait_to, play, duration):
            clear_active(play)

            st = section_title(
                "Transformer: token mới nhìn lại nhiều token bằng attention",
                color=BLUE,
                font_size=25,
            )

            tokens = VGroup()
            for i in range(7):
                lab = f"t{i + 1}" if i < 6 else "tL"
                tokens.add(
                    small_token(
                        lab,
                        color=MUTED,
                        width=0.64,
                        height=0.38,
                        font_size=14,
                    )
                )
            tokens.arrange(RIGHT, buff=0.18)
            tokens.move_to(LEFT * 2.35 + DOWN * 0.30)

            new_tok = small_token(
                "new",
                color=BLUE,
                width=0.90,
                height=0.44,
                font_size=15,
            )
            new_tok.move_to(LEFT * 2.35 + UP * 1.05)

            attn_lines = VGroup()
            for tok in tokens:
                attn_lines.add(
                    Line(
                        new_tok.get_bottom(),
                        tok.get_top(),
                        color=BLUE,
                        stroke_width=2.0,
                    )
                )

            left_note = make_box(
                "Token mới kết nối\nvới nhiều token cũ",
                BLUE,
                width=4.20,
                height=0.76,
                font_size=19,
                fill_opacity=0.10,
            )
            left_note.move_to(LEFT * 2.35 + DOWN * 1.45)

            map_title = make_box(
                "Attention map lớn",
                RED,
                width=3.10,
                height=0.52,
                font_size=18,
                fill_opacity=0.10,
            )
            map_title.move_to(RIGHT * 3.05 + UP * 1.18)

            grid = VGroup()
            n = 7
            for r in range(n):
                for c in range(n):
                    color = RED if (r + c) % 3 == 0 else MUTED
                    op = 0.30 if color == RED else 0.13
                    sq = Square(
                        side_length=0.235,
                        stroke_color=color,
                        stroke_width=0.9,
                        fill_color=color,
                        fill_opacity=op,
                    )
                    grid.add(sq)

            grid.arrange_in_grid(rows=n, cols=n, buff=0.03)
            grid.move_to(RIGHT * 3.05 + DOWN * 0.18)

            cost = make_box(
                "Memory + Compute\ntăng khi chuỗi dài",
                RED,
                width=3.55,
                height=0.68,
                font_size=18,
                fill_opacity=0.10,
            )
            cost.move_to(RIGHT * 3.05 + DOWN * 1.72)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.25)

            wait_to(0.16)
            play(FadeIn(new_tok, shift=UP), FadeIn(tokens, shift=UP), run_time=0.38)

            wait_to(0.32)
            play(
                LaggedStart(
                    *[Create(line) for line in attn_lines],
                    lag_ratio=0.07,
                ),
                run_time=0.65,
            )

            wait_to(0.48)
            play(FadeIn(left_note, shift=UP), run_time=0.28)

            wait_to(0.64)
            play(FadeIn(map_title, shift=UP), run_time=0.25)

            wait_to(0.72)
            play(FadeIn(grid, scale=0.95), run_time=0.50)

            wait_to(0.86)
            play(FadeIn(cost, shift=UP), run_time=0.32)

            set_active(st, tokens, new_tok, attn_lines, left_note, map_title, grid, cost)

        play_segment(
            "p3_02_06_02_transformer_attention.mp3",
            fallback_duration=18.0,
            visual_func=visual_transformer_attention,
        )

        # =====================================================
        # CẢNH 3 - RECURRENT / STATE UPDATE
        # =====================================================
        def visual_recurrent_state(wait_to, play, duration):
            clear_active(play)

            st = section_title(
                "Recurrent / State-space: cập nhật trạng thái nén",
                color=GREEN,
                font_size=27,
            )

            trail = VGroup()
            for i, lab in enumerate(["h0", "h1", "h2", "h3"]):
                color = GREEN if i > 0 else MUTED
                trail.add(
                    make_box(
                        lab,
                        color,
                        width=0.72,
                        height=0.42,
                        font_size=15,
                        fill_opacity=0.12,
                    )
                )
            trail.arrange(RIGHT, buff=0.26)
            trail.move_to(UP * 1.30)

            trail_arrows = VGroup()
            for i in range(3):
                trail_arrows.add(
                    Arrow(
                        trail[i].get_right(),
                        trail[i + 1].get_left(),
                        color=MUTED,
                        stroke_width=1.8,
                        buff=0.04,
                    )
                )

            state_old = make_box(
                "State cũ\nh_{t-1}",
                PURPLE,
                width=2.20,
                height=0.82,
                font_size=21,
                fill_opacity=0.12,
            )
            state_old.move_to(LEFT * 3.70 + UP * 0.25)

            token = make_box(
                "Token mới\nx_t",
                BLUE,
                width=2.20,
                height=0.82,
                font_size=21,
                fill_opacity=0.12,
            )
            token.move_to(LEFT * 3.70 + DOWN * 0.80)

            recurrent = make_box(
                "Recurrent Unit\nupdate",
                GREEN,
                width=3.05,
                height=1.00,
                font_size=23,
                fill_opacity=0.12,
            )
            recurrent.move_to(LEFT * 0.10 + DOWN * 0.30)

            state_new = make_box(
                "State mới\nh_t",
                YELLOW,
                width=2.20,
                height=0.82,
                font_size=21,
                fill_opacity=0.12,
            )
            state_new.move_to(RIGHT * 3.55 + DOWN * 0.30)

            arr1 = Arrow(
                state_old.get_right(),
                recurrent.get_left() + UP * 0.20,
                color=MUTED,
                stroke_width=2.5,
                buff=0.14,
            )
            arr2 = Arrow(
                token.get_right(),
                recurrent.get_left() + DOWN * 0.20,
                color=MUTED,
                stroke_width=2.5,
                buff=0.14,
            )
            arr3 = Arrow(
                recurrent.get_right(),
                state_new.get_left(),
                color=YELLOW,
                stroke_width=3,
                buff=0.14,
            )

            note1 = make_box(
                "Không lưu toàn bộ quan hệ giữa các token",
                RED,
                width=5.60,
                height=0.58,
                font_size=19,
                fill_opacity=0.08,
            )
            note1.move_to(DOWN * 1.60)

            note2 = make_box(
                "State vector được cập nhật tuần tự theo thời gian",
                GREEN,
                width=6.70,
                height=0.58,
                font_size=19,
                fill_opacity=0.08,
            )
            note2.move_to(DOWN * 2.30)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.22)

            # Voice nói recurrent/state-space xử lý khác
            wait_to(0.14)
            play(FadeIn(note1, shift=UP), run_time=0.24)

            # Voice nói mô hình duy trì trạng thái nén
            wait_to(0.28)
            play(FadeIn(state_old, shift=RIGHT), run_time=0.28)

            # Voice nói token mới đi vào
            wait_to(0.38)
            play(FadeIn(token, shift=RIGHT), run_time=0.28)

            # Voice nói state cũ và token mới đi vào recurrent unit
            wait_to(0.50)
            play(
                FadeIn(recurrent, shift=UP),
                Create(arr1),
                Create(arr2),
                run_time=0.42,
            )

            # Voice nói tạo state mới
            wait_to(0.62)
            play(FadeIn(state_new, shift=LEFT), Create(arr3), run_time=0.35)

            # Voice bắt đầu nói chuỗi h0, h1, h2, h3
            wait_to(0.72)
            play(FadeIn(trail, shift=UP), run_time=0.24)

            wait_to(0.76)
            play(
                LaggedStart(
                    *[Create(a) for a in trail_arrows],
                    lag_ratio=0.10,
                ),
                run_time=0.32,
            )

            wait_to(0.82)
            play(FadeIn(note2, shift=UP), run_time=0.28)

            set_active(
                st,
                trail,
                trail_arrows,
                state_old,
                token,
                recurrent,
                state_new,
                arr1,
                arr2,
                arr3,
                note1,
                note2,
            )

        play_segment(
            "p3_02_06_03_recurrent_state.mp3",
            fallback_duration=22.0,
            visual_func=visual_recurrent_state,
        )

        # =====================================================
        # CẢNH 4 - COST + CAVEAT
        # =====================================================
        def visual_cost_caveat(wait_to, play, duration):
            clear_active(play)

            st = section_title(
                "Chi phí với sequence dài",
                color=YELLOW,
                font_size=29,
            )

            full = make_box(
                "Full attention\nchi phí tăng nhanh",
                RED,
                width=3.45,
                height=0.92,
                font_size=21,
                fill_opacity=0.11,
            )
            full.move_to(LEFT * 3.00 + UP * 0.95)

            rec = make_box(
                "State update\ncó thể tuyến tính hơn",
                GREEN,
                width=3.65,
                height=0.92,
                font_size=21,
                fill_opacity=0.11,
            )
            rec.move_to(RIGHT * 3.00 + UP * 0.95)

            red_bars = VGroup()
            red_heights = [0.28, 0.50, 0.82, 1.22]
            for i, h in enumerate(red_heights):
                bar = Rectangle(
                    width=0.34,
                    height=h,
                    stroke_color=RED,
                    fill_color=RED,
                    fill_opacity=0.60,
                )
                bar.move_to(
                    LEFT * 4.00 + RIGHT * i * 0.72 + DOWN * 1.45 + UP * h / 2
                )
                red_bars.add(bar)

            green_bars = VGroup()
            green_heights = [0.28, 0.45, 0.60, 0.76]
            for i, h in enumerate(green_heights):
                bar = Rectangle(
                    width=0.34,
                    height=h,
                    stroke_color=GREEN,
                    fill_color=GREEN,
                    fill_opacity=0.60,
                )
                bar.move_to(
                    RIGHT * 1.95 + RIGHT * i * 0.72 + DOWN * 1.45 + UP * h / 2
                )
                green_bars.add(bar)

            l_label = Text(
                "Tăng nhanh",
                font_size=18,
                color=RED,
                font=FONT,
            )
            l_label.next_to(red_bars, DOWN, buff=0.18)

            r_label = Text(
                "Tăng đều hơn",
                font_size=18,
                color=GREEN,
                font=FONT,
            )
            r_label.next_to(green_bars, DOWN, buff=0.18)

            caveat = make_box(
                "Không thay thế Transformer\ntrong mọi trường hợp",
                RED,
                width=4.90,
                height=0.82,
                font_size=21,
                fill_opacity=0.11,
            )
            caveat.move_to(DOWN * 2.45)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.25)

            wait_to(0.18)
            play(FadeIn(full, shift=UP), run_time=0.30)

            wait_to(0.34)
            play(
                LaggedStart(
                    *[FadeIn(b, shift=UP) for b in red_bars],
                    lag_ratio=0.10,
                ),
                FadeIn(l_label, shift=UP),
                run_time=0.58,
            )

            wait_to(0.54)
            play(FadeIn(rec, shift=UP), run_time=0.30)

            wait_to(0.66)
            play(
                LaggedStart(
                    *[FadeIn(b, shift=UP) for b in green_bars],
                    lag_ratio=0.10,
                ),
                FadeIn(r_label, shift=UP),
                run_time=0.58,
            )

            wait_to(0.84)
            play(FadeIn(caveat, shift=UP), run_time=0.38)

            set_active(st, full, rec, red_bars, green_bars, l_label, r_label, caveat)

        play_segment(
            "p3_02_06_04_cost_caveat.mp3",
            fallback_duration=18.0,
            visual_func=visual_cost_caveat,
        )

        # =====================================================
        # CẢNH 5 - SUMMARY
        # =====================================================
        def visual_summary(wait_to, play, duration):
            clear_active(play)

            st = section_title(
                "Tóm tắt",
                color=YELLOW,
                font_size=30,
            )

            transformer = make_box(
                "Transformer\nnền tảng chính của nhiều LLM",
                BLUE,
                width=4.55,
                height=0.88,
                font_size=21,
                fill_opacity=0.11,
            )
            transformer.move_to(LEFT * 2.65 + UP * 0.90)

            research = make_box(
                "Recurrent / State-space\nhướng nghiên cứu quan trọng",
                GREEN,
                width=4.75,
                height=0.88,
                font_size=21,
                fill_opacity=0.11,
            )
            research.move_to(RIGHT * 2.55 + UP * 0.90)

            factors_title = Text(
                "Hiệu quả phụ thuộc vào",
                font_size=23,
                color=WHITE,
                font=FONT,
            )
            factors_title.move_to(UP * 0.05)

            factor_boxes = VGroup(
                make_box(
                    "Bài toán",
                    PURPLE,
                    width=1.75,
                    height=0.55,
                    font_size=17,
                    fill_opacity=0.09,
                ),
                make_box(
                    "Dữ liệu",
                    PURPLE,
                    width=1.75,
                    height=0.55,
                    font_size=17,
                    fill_opacity=0.09,
                ),
                make_box(
                    "Phần cứng",
                    PURPLE,
                    width=2.00,
                    height=0.55,
                    font_size=17,
                    fill_opacity=0.09,
                ),
                make_box(
                    "Inference",
                    PURPLE,
                    width=1.90,
                    height=0.55,
                    font_size=17,
                    fill_opacity=0.09,
                ),
            )
            factor_boxes.arrange(RIGHT, buff=0.23)
            factor_boxes.next_to(factors_title, DOWN, buff=0.28)

            final_summary = make_box(
                "Xử lý sequence dài hiệu quả hơn\nnhưng chưa thay thế hoàn toàn Transformer",
                YELLOW,
                width=8.75,
                height=0.90,
                font_size=21,
                fill_opacity=0.10,
            )
            final_summary.move_to(DOWN * 1.85)

            wait_to(0.00)
            play(FadeIn(st, shift=UP), run_time=0.20)

            # Voice nói Transformer vẫn là nền tảng chính
            wait_to(0.07)
            play(FadeIn(transformer, shift=UP), run_time=0.28)

            # Voice nói recurrent/state-space là hướng nghiên cứu
            wait_to(0.22)
            play(FadeIn(research, shift=UP), run_time=0.28)

            # Voice nói hiệu quả phụ thuộc vào
            wait_to(0.38)
            play(FadeIn(factors_title, shift=UP), run_time=0.20)

            wait_to(0.46)
            play(
                LaggedStart(
                    *[FadeIn(b, shift=UP) for b in factor_boxes],
                    lag_ratio=0.08,
                ),
                run_time=0.45,
            )

            # Voice nói vì vậy, ý chính là
            wait_to(0.66)
            play(FadeIn(final_summary, shift=UP), run_time=0.32)

            set_active(st, transformer, research, factors_title, factor_boxes, final_summary)

        play_segment(
            "p3_02_06_05_summary.mp3",
            fallback_duration=24.0,
            visual_func=visual_summary,
        )

        final_mobs = [m for m in active_mobs if m is not None]
        self.play(
            FadeOut(title),
            *[FadeOut(m) for m in final_mobs],
            run_time=0.55,
        )
