# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# PHẦN 2.1 - ARCHITECTURE DESIGN LÀ GÌ?
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_02_01_arch_intro.py SceneP30201ArchitectureIntro
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
    # Chữ tiếng Anh: không truyền font để Manim dùng font mặc định.
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
    width=3.6,
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


class SceneP30201ArchitectureIntro(Scene):
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

        def transformer_block(center=ORIGIN, scale=1.0):
            input_box = make_box_en(
                "Input token representations",
                MUTED,
                width=4.05 * scale,
                height=0.50 * scale,
                font_size=18 * scale,
                fill=0.08,
            )

            attn_box = make_box_en(
                "Self-Attention",
                GREEN,
                width=3.25 * scale,
                height=0.64 * scale,
                font_size=21 * scale,
                fill=0.11,
            )

            ffn_box = make_box_en(
                "Feed-Forward Network",
                ORANGE,
                width=3.65 * scale,
                height=0.64 * scale,
                font_size=20 * scale,
                fill=0.11,
            )

            output_box = make_box_en(
                "Output representations",
                MUTED,
                width=3.85 * scale,
                height=0.50 * scale,
                font_size=18 * scale,
                fill=0.08,
            )

            block = VGroup(input_box, attn_box, ffn_box, output_box)
            block.arrange(DOWN, buff=0.34 * scale)
            block.move_to(center)

            arrows = VGroup()
            for a, b in [(input_box, attn_box), (attn_box, ffn_box), (ffn_box, output_box)]:
                arrows.add(
                    Arrow(
                        a.get_bottom(),
                        b.get_top(),
                        color=MUTED,
                        stroke_width=2.2,
                        buff=0.08,
                    )
                )

            outline = RoundedRectangle(
                width=4.75 * scale,
                height=3.75 * scale,
                corner_radius=0.20 * scale,
                stroke_color=BLUE,
                stroke_width=2.0,
                fill_color=BLUE,
                fill_opacity=0.025,
            )
            outline.move_to(block.get_center())

            return VGroup(outline, block, arrows), input_box, attn_box, ffn_box, output_box, arrows, outline

        title = make_title_en("Architecture Design")
        subtitle = make_subtitle_vi(
            "Tối ưu thiết kế kiến trúc mô hình",
            title,
        )

        # =====================================================
        # CẢNH 1 - INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            vi_box = make_box_vi(
                "Tối ưu thiết kế\nkiến trúc mô hình",
                YELLOW,
                width=5.35,
                height=1.02,
                font_size=25,
                fill=0.11,
            )
            vi_box.move_to(UP * 0.60)

            note = bottom_note_vi(
                "Không chỉ chạy model nhanh hơn, mà thay đổi cách model được thiết kế",
                color=YELLOW,
                font_size=21,
                y=-1.55,
            )

            play(Write(title), run_time=0.50)

            wait_to(0.16)
            play(FadeIn(subtitle, shift=UP), run_time=0.25)

            wait_to(0.42)
            play(FadeIn(vi_box, shift=UP), run_time=0.35)

            wait_to(0.72)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(vi_box, note)

        play_segment(
            "p3_02_01_01_intro.mp3",
            fallback_duration=5.0,
            visual_func=visual_intro,
            clear_before=False,
        )

        # =====================================================
        # CẢNH 2 - CẤU TRÚC BÊN TRONG MODEL
        # =====================================================
        def visual_inside_structure(wait_to, play, duration):
            outer = RoundedRectangle(
                width=7.70,
                height=2.35,
                corner_radius=0.22,
                stroke_color=BLUE,
                stroke_width=2.2,
                fill_color=BLUE,
                fill_opacity=0.05,
            )
            outer.move_to(UP * 0.15)

            model_label = text_en("LLM", font_size=35, color=WHITE)
            model_label.move_to(outer.get_top() + DOWN * 0.45)

            parts = VGroup(
                make_box_en("Attention", GREEN, width=2.15, height=0.58, font_size=19, fill=0.10),
                make_box_en("FFN", ORANGE, width=1.45, height=0.58, font_size=19, fill=0.10),
                make_box_en("Layers", PURPLE, width=1.70, height=0.58, font_size=18, fill=0.10),
                make_box_en("Blocks", YELLOW, width=1.70, height=0.58, font_size=18, fill=0.10),
            )
            parts.arrange(RIGHT, buff=0.26)
            parts.move_to(outer.get_center() + DOWN * 0.25)

            note = bottom_note_vi(
                "Architecture Design nhìn vào các thành phần bên trong mô hình",
                color=YELLOW,
                font_size=21,
                y=-2.05,
            )

            wait_to(0.05)
            play(Create(outer), FadeIn(model_label, shift=UP), run_time=0.42)

            wait_to(0.32)
            play(
                LaggedStart(
                    *[FadeIn(p, shift=UP) for p in parts],
                    lag_ratio=0.12,
                ),
                run_time=0.72,
            )

            wait_to(0.72)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(outer, model_label, parts, note)

        play_segment(
            "p3_02_01_02_inside_structure.mp3",
            fallback_duration=5.0,
            visual_func=visual_inside_structure,
        )

        # =====================================================
        # CẢNH 3 - TRANSFORMER DECODER BLOCK
        # =====================================================
        def visual_transformer_decoder(wait_to, play, duration):
            block_group, input_box, attn_box, ffn_box, output_box, arrows, outline = transformer_block(
                center=DOWN * 0.05,
                scale=1.0,
            )

            block_title = make_box_en(
                "Transformer Decoder Block",
                BLUE,
                width=4.60,
                height=0.60,
                font_size=21,
                fill=0.10,
            )
            block_title.next_to(outline, UP, buff=0.25)

            note = bottom_note_vi(
                "Phần lớn LLM hiện nay vẫn dựa trên Transformer decoder",
                color=YELLOW,
                font_size=21,
                y=-2.28,
            )

            wait_to(0.05)
            play(FadeIn(block_title, shift=UP), run_time=0.30)

            wait_to(0.22)
            play(Create(outline), run_time=0.30)

            wait_to(0.36)
            play(FadeIn(input_box, shift=UP), run_time=0.24)

            wait_to(0.48)
            play(Create(arrows[0]), FadeIn(attn_box, shift=UP), run_time=0.36)

            wait_to(0.60)
            play(Create(arrows[1]), FadeIn(ffn_box, shift=UP), run_time=0.36)

            wait_to(0.72)
            play(Create(arrows[2]), FadeIn(output_box, shift=UP), run_time=0.34)

            wait_to(0.86)
            play(FadeIn(note, shift=UP), run_time=0.28)

            set_active(block_title, outline, input_box, attn_box, ffn_box, output_box, arrows, note)

        play_segment(
            "p3_02_01_03_transformer_decoder.mp3",
            fallback_duration=5.5,
            visual_func=visual_transformer_decoder,
        )

        # =====================================================
        # CẢNH 4 - ATTENTION VÀ FFN
        # =====================================================
        def visual_attention_ffn(wait_to, play, duration):
            block_group, input_box, attn_box, ffn_box, output_box, arrows, outline = transformer_block(
                center=DOWN * 0.15,
                scale=1.0,
            )

            label = text_vi("Hai thành phần quan trọng", font_size=28, color=WHITE)
            fit_text(label, 10.5)
            label.next_to(subtitle, DOWN, buff=0.32)

            attn_note = make_box_vi(
                "Hiểu quan hệ\ngiữa các token",
                GREEN,
                width=3.20,
                height=0.78,
                font_size=19,
                fill=0.09,
            )
            attn_note.move_to(LEFT * 3.55 + DOWN * 0.10)

            ffn_note = make_box_vi(
                "Nhiều tham số\nvà compute",
                ORANGE,
                width=3.05,
                height=0.78,
                font_size=19,
                fill=0.09,
            )
            ffn_note.move_to(RIGHT * 3.55 + DOWN * 0.10)

            a1 = Arrow(attn_note.get_right(), attn_box.get_left(), color=GREEN, stroke_width=2.5, buff=0.14)
            a2 = Arrow(ffn_note.get_left(), ffn_box.get_right(), color=ORANGE, stroke_width=2.5, buff=0.14)

            wait_to(0.03)
            play(FadeIn(label, shift=UP), run_time=0.25)

            wait_to(0.18)
            play(
                FadeIn(outline),
                FadeIn(input_box),
                FadeIn(attn_box),
                FadeIn(ffn_box),
                FadeIn(output_box),
                FadeIn(arrows),
                run_time=0.48,
            )

            wait_to(0.42)
            play(highlight_box(attn_box, GREEN, opacity=0.18, width=3.8), run_time=0.30)

            wait_to(0.55)
            play(FadeIn(attn_note, shift=RIGHT), Create(a1), run_time=0.35)

            wait_to(0.68)
            play(highlight_box(ffn_box, ORANGE, opacity=0.18, width=3.8), run_time=0.30)

            wait_to(0.80)
            play(FadeIn(ffn_note, shift=LEFT), Create(a2), run_time=0.35)

            set_active(label, outline, input_box, attn_box, ffn_box, output_box, arrows, attn_note, ffn_note, a1, a2)

        play_segment(
            "p3_02_01_04_attention_ffn.mp3",
            fallback_duration=7.0,
            visual_func=visual_attention_ffn,
        )

        # =====================================================
        # CẢNH 5 - ATTENTION COST
        # =====================================================
        def visual_attention_cost(wait_to, play, duration):
            title_vi = text_vi("Attention: hiểu quan hệ giữa token", font_size=28, color=GREEN)
            fit_text(title_vi, 10.6)
            title_vi.next_to(subtitle, DOWN, buff=0.34)

            tokens = VGroup()
            for i in range(8):
                tok = make_box_en(
                    f"t{i+1}",
                    BLUE,
                    width=0.58,
                    height=0.44,
                    font_size=15,
                    fill=0.10,
                )
                tokens.add(tok)

            tokens.arrange(RIGHT, buff=0.22)
            tokens.move_to(UP * 0.45)

            connections = VGroup()
            for i in range(len(tokens)):
                for j in range(i + 1, len(tokens)):
                    if (j - i) <= 3:
                        line = Line(
                            tokens[i].get_bottom(),
                            tokens[j].get_bottom(),
                            color=GREEN,
                            stroke_width=1.0,
                        )
                        line.set_opacity(0.22)
                        connections.add(line)

            cost_box = make_box_vi(
                "Chuỗi càng dài\n-> attention càng tốn",
                RED,
                width=4.25,
                height=0.86,
                font_size=21,
                fill=0.10,
            )
            cost_box.move_to(DOWN * 0.95)

            badges = VGroup(
                make_box_en("Memory", RED, width=1.80, height=0.52, font_size=17, fill=0.10),
                make_box_en("Compute", ORANGE, width=1.90, height=0.52, font_size=17, fill=0.10),
            )
            badges.arrange(RIGHT, buff=0.35)
            badges.next_to(cost_box, DOWN, buff=0.30)

            wait_to(0.03)
            play(FadeIn(title_vi, shift=UP), run_time=0.25)

            wait_to(0.20)
            play(
                LaggedStart(*[FadeIn(t, shift=UP) for t in tokens], lag_ratio=0.06),
                run_time=0.60,
            )

            wait_to(0.43)
            play(Create(connections), run_time=0.75)

            wait_to(0.66)
            play(FadeIn(cost_box, shift=UP), run_time=0.35)

            wait_to(0.82)
            play(FadeIn(badges, shift=UP), run_time=0.32)

            wait_to(0.92)
            play(Flash(cost_box[0], color=RED), run_time=0.45)

            set_active(title_vi, tokens, connections, cost_box, badges)

        play_segment(
            "p3_02_01_05_attention_cost.mp3",
            fallback_duration=8.5,
            visual_func=visual_attention_cost,
        )

        # =====================================================
        # CẢNH 6 - FFN COST
        # =====================================================
        def visual_ffn_cost(wait_to, play, duration):
            title_vi = text_vi("FFN: nhiều tham số, chi phí inference lớn", font_size=28, color=ORANGE)
            fit_text(title_vi, 10.6)
            title_vi.next_to(subtitle, DOWN, buff=0.34)

            input_vec = make_box_en("Hidden states", BLUE, width=2.45, height=0.60, font_size=19, fill=0.10)
            ffn = make_box_en("Feed-Forward Network", ORANGE, width=3.85, height=0.78, font_size=21, fill=0.12)
            output_vec = make_box_en("Updated states", BLUE, width=2.35, height=0.60, font_size=19, fill=0.10)

            flow = VGroup(input_vec, ffn, output_vec)
            flow.arrange(RIGHT, buff=0.55)
            flow.move_to(UP * 0.45)

            arrows = VGroup(
                Arrow(input_vec.get_right(), ffn.get_left(), color=MUTED, stroke_width=2.5, buff=0.12),
                Arrow(ffn.get_right(), output_vec.get_left(), color=MUTED, stroke_width=2.5, buff=0.12),
            )

            param_grid = VGroup()
            for i in range(24):
                dot = Square(
                    side_length=0.13,
                    stroke_color=ORANGE,
                    stroke_width=1.0,
                    fill_color=ORANGE,
                    fill_opacity=0.45,
                )
                param_grid.add(dot)

            param_grid.arrange_in_grid(rows=3, cols=8, buff=0.08)
            param_grid.next_to(ffn, DOWN, buff=0.35)

            params_label = make_box_vi(
                "Rất nhiều tham số",
                ORANGE,
                width=3.20,
                height=0.52,
                font_size=19,
                fill=0.09,
            )
            params_label.next_to(param_grid, DOWN, buff=0.20)

            cost = make_box_vi(
                "Đóng góp lớn vào chi phí inference",
                RED,
                width=5.50,
                height=0.62,
                font_size=21,
                fill=0.09,
            )
            cost.move_to(DOWN * 2.02)

            wait_to(0.03)
            play(FadeIn(title_vi, shift=UP), run_time=0.25)

            wait_to(0.22)
            play(FadeIn(input_vec, shift=RIGHT), run_time=0.28)

            wait_to(0.36)
            play(Create(arrows[0]), FadeIn(ffn, shift=UP), run_time=0.38)

            wait_to(0.50)
            play(Create(arrows[1]), FadeIn(output_vec, shift=LEFT), run_time=0.32)

            wait_to(0.64)
            play(FadeIn(param_grid, shift=UP), FadeIn(params_label, shift=UP), run_time=0.45)

            wait_to(0.82)
            play(FadeIn(cost, shift=UP), run_time=0.32)

            wait_to(0.92)
            play(Flash(ffn[0], color=ORANGE), run_time=0.45)

            set_active(title_vi, input_vec, ffn, output_vec, arrows, param_grid, params_label, cost)

        play_segment(
            "p3_02_01_06_ffn_cost.mp3",
            fallback_duration=6.0,
            visual_func=visual_ffn_cost,
        )

        # =====================================================
        # CẢNH 7 - GOAL
        # =====================================================
        def visual_goal(wait_to, play, duration):
            goal_title = text_vi("Mục tiêu của Architecture Design", font_size=29, color=YELLOW)
            fit_text(goal_title, 10.6)
            goal_title.next_to(subtitle, DOWN, buff=0.34)

            left = make_box_vi(
                "Hiệu quả hơn\nngay từ kiến trúc",
                GREEN,
                width=3.90,
                height=1.00,
                font_size=23,
                fill=0.11,
            )

            right = make_box_vi(
                "Vẫn giữ\nnăng lực biểu diễn",
                BLUE,
                width=3.90,
                height=1.00,
                font_size=23,
                fill=0.11,
            )

            pair = VGroup(left, right)
            pair.arrange(RIGHT, buff=0.70)
            pair.move_to(UP * 0.25)

            balance = Arrow(left.get_right(), right.get_left(), color=YELLOW, stroke_width=4, buff=0.18)

            tradeoff = make_box_vi(
                "Tối ưu kiến trúc luôn đi kèm cân bằng giữa chi phí và chất lượng",
                YELLOW,
                width=8.70,
                height=0.72,
                font_size=21,
                fill=0.09,
            )
            tradeoff.move_to(DOWN * 1.35)

            examples = VGroup(
                make_box_en("Attention", GREEN, width=2.15, height=0.52, font_size=18, fill=0.08),
                make_box_en("FFN", ORANGE, width=1.40, height=0.52, font_size=18, fill=0.08),
                make_box_en("Layers", PURPLE, width=1.65, height=0.52, font_size=17, fill=0.08),
            )
            examples.arrange(RIGHT, buff=0.28)
            examples.move_to(DOWN * 2.15)

            wait_to(0.03)
            play(FadeIn(goal_title, shift=UP), run_time=0.25)

            wait_to(0.24)
            play(FadeIn(left, shift=RIGHT), run_time=0.35)

            wait_to(0.46)
            play(GrowArrow(balance), FadeIn(right, shift=LEFT), run_time=0.45)

            wait_to(0.68)
            play(FadeIn(tradeoff, shift=UP), run_time=0.35)

            wait_to(0.84)
            play(FadeIn(examples, shift=UP), run_time=0.35)

            wait_to(0.94)
            play(Flash(left[0], color=GREEN), Flash(right[0], color=BLUE), run_time=0.55)

            set_active(goal_title, left, right, balance, tradeoff, examples)

        play_segment(
            "p3_02_01_07_goal.mp3",
            fallback_duration=8.5,
            visual_func=visual_goal,
        )

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