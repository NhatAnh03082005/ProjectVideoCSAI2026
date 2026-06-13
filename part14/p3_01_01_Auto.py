# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# PHẦN 3.1.1 - DECODING BOTTLENECK
# Render:
# python -m manim -pql scenes/p3_01_01_Auto.py SceneP3DecodingBottleneck
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


# ============================================================
# AUDIO HELPERS
# ============================================================

def audio_duration(path):
    if not os.path.exists(path):
        print(f"[WARNING] Không tìm thấy audio: {path}")
        return 0
    try:
        return MP3(path).info.length
    except Exception:
        return 0


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

def fit_text(mob, width, height=None):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    if height is not None and mob.height > height:
        mob.scale_to_fit_height(height)
    return mob


def text_en(text, font_size=24, color=WHITE, line_spacing=0.85):
    # Chữ tiếng Anh: không truyền font để Manim dùng font mặc định.
    return Text(
        text,
        font_size=font_size,
        color=color,
        line_spacing=line_spacing,
    )


def text_vi(text, font_size=24, color=WHITE, line_spacing=0.85):
    # Chữ tiếng Việt: dùng Arial.
    return Text(
        text,
        font=VI_FONT,
        font_size=font_size,
        color=color,
        line_spacing=line_spacing,
    )


def title_en(text, font_size=42, color=WHITE):
    title = text_en(text, font_size=font_size, color=color)
    fit_text(title, 11.0)
    title.to_edge(UP, buff=0.45)
    return title


def subtitle_vi(text, title, font_size=27, color=BLUE):
    subtitle = text_vi(text, font_size=font_size, color=color)
    fit_text(subtitle, 10.5)
    subtitle.next_to(title, DOWN, buff=0.22)
    return subtitle


def bottom_note_vi(text, font_size=23, color=YELLOW, y=-2.35, max_width=10.5):
    # Đưa caption lên cao hơn mép dưới để không bị thanh điều khiển video che.
    note = text_vi(text, font_size=font_size, color=color)
    fit_text(note, max_width)
    note.move_to(DOWN * abs(y))
    return note


def box_base(color, width, height, fill=0.14, stroke_width=2.0):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        stroke_color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill,
    )


def model_box_vi(text, color=BLUE, width=3.0, height=0.9, font_size=23):
    box = box_base(color, width, height)
    label = text_vi(text, font_size=font_size, color=WHITE)
    fit_text(label, width - 0.25, height - 0.18)
    label.move_to(box.get_center())
    return VGroup(box, label)


def model_box_en(text, color=BLUE, width=3.0, height=0.9, font_size=23):
    box = box_base(color, width, height)
    label = text_en(text, font_size=font_size, color=WHITE)
    fit_text(label, width - 0.25, height - 0.18)
    label.move_to(box.get_center())
    return VGroup(box, label)


def model_box_mixed(
    heading_en,
    desc_vi,
    color=BLUE,
    width=4.8,
    height=1.12,
    heading_size=24,
    desc_size=22,
):
    box = box_base(color, width, height)

    heading = text_en(heading_en, font_size=heading_size, color=WHITE)
    desc = text_vi(desc_vi, font_size=desc_size, color=WHITE)

    fit_text(heading, width - 0.35, height * 0.40)
    fit_text(desc, width - 0.35, height * 0.45)

    group = VGroup(heading, desc).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
    group.move_to(box.get_center())

    return VGroup(box, group)


def token_box_vi(text, color=BLUE, width=0.8, height=0.55, font_size=22):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.18,
    )

    label = text_vi(text, font_size=font_size, color=WHITE)
    fit_text(label, width - 0.12, height - 0.08)
    label.move_to(box.get_center())

    return VGroup(box, label)


def token_box_en(text, color=BLUE, width=0.8, height=0.55, font_size=22):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.18,
    )

    label = text_en(text, font_size=font_size, color=WHITE)
    fit_text(label, width - 0.12, height - 0.08)
    label.move_to(box.get_center())

    return VGroup(box, label)


def mixed_prompt_label():
    left = text_en("Prompt:", font_size=28, color=WHITE)
    right = text_vi('"Thủ đô của Việt Nam là"', font_size=28, color=WHITE)

    group = VGroup(left, right).arrange(RIGHT, buff=0.16)
    fit_text(group, 10.5)

    return group


# ============================================================
# SCENE
# ============================================================

class SceneP3DecodingBottleneck(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        audio = str(root / "voice" / "p3_01_01_bottleneck.mp3")

        play_audio(self, audio)
        visual_time = 0

        # =====================================================
        # HELPER TRONG SCENE
        # =====================================================
        def make_token_vi(text, color=BLUE, width=0.78):
            return token_box_vi(
                text,
                color=color,
                width=width,
                height=0.58,
                font_size=22,
            )

        def make_token_en(text, color=BLUE, width=0.78):
            return token_box_en(
                text,
                color=color,
                width=width,
                height=0.58,
                font_size=21,
            )

        def pause_to(target_time):
            nonlocal visual_time
            delay = max(0, target_time - visual_time)
            if delay > 0:
                self.wait(delay)
                visual_time += delay

        def add_time(duration):
            nonlocal visual_time
            visual_time += duration

        def clear(*mobjects, run_time=0.45):
            nonlocal visual_time
            self.play(
                *[FadeOut(mob) for mob in mobjects],
                run_time=run_time,
            )
            visual_time += run_time

        # =====================================================
        # TITLE
        # =====================================================
        title = title_en("Decoding Algorithms", font_size=42, color=WHITE)
        subtitle = subtitle_vi(
            "Tối ưu cách mô hình sinh token",
            title,
            font_size=27,
            color=BLUE,
        )

        # =====================================================
        # CẢNH 1 - ĐỊNH NGHĨA DECODING
        # =====================================================
        self.play(Write(title), run_time=0.75)
        add_time(0.75)

        self.play(FadeIn(subtitle, shift=UP), run_time=0.55)
        add_time(0.55)

        decode_box = model_box_mixed(
            "Decoding",
            "= tạo câu trả lời từng bước",
            BLUE,
            width=5.35,
            height=1.15,
            heading_size=24,
            desc_size=23,
        )
        decode_box.move_to(UP * 1.05)

        pause_to(2.4)

        self.play(FadeIn(decode_box, scale=0.96), run_time=0.7)
        add_time(0.7)

        prompt_mini = model_box_en(
            "Prompt",
            MUTED,
            width=1.55,
            height=0.65,
            font_size=22,
        )
        prompt_mini.move_to(LEFT * 3.6 + DOWN * 0.25)

        generated_context = VGroup(
            make_token_vi("Thủ", MUTED, width=0.72),
            make_token_vi("đô", MUTED, width=0.72),
            make_token_en("...", MUTED, width=0.72),
            make_token_vi("là", MUTED, width=0.72),
        )
        generated_context.arrange(RIGHT, buff=0.09)
        generated_context.next_to(prompt_mini, RIGHT, buff=0.25)

        predict_box = model_box_vi(
            "Dự đoán\ntoken tiếp theo",
            YELLOW,
            width=2.45,
            height=1.05,
            font_size=21,
        )
        predict_box.move_to(RIGHT * 2.7 + DOWN * 0.25)

        arrow_predict = Arrow(
            generated_context.get_right(),
            predict_box.get_left(),
            color=YELLOW,
            stroke_width=3,
            buff=0.18,
        )

        next_token_1 = make_token_vi("Hà", GREEN, width=0.78)
        next_token_1.next_to(predict_box, DOWN, buff=0.45)

        append_arrow = Arrow(
            next_token_1.get_left(),
            generated_context.get_right() + RIGHT * 0.15,
            color=GREEN,
            stroke_width=3,
            buff=0.1,
        )

        loop_note = bottom_note_vi(
            "Token mới được thêm vào chuỗi,\nrồi tiếp tục dự đoán token kế tiếp",
            font_size=23,
            color=GREEN,
            y=-2.35,
            max_width=9.5,
        )

        next_token_2 = make_token_vi("Nội", GREEN, width=0.85)
        next_token_2.next_to(next_token_1, RIGHT, buff=0.22)

        pause_to(5.0)

        self.play(FadeIn(prompt_mini), FadeIn(generated_context), run_time=0.75)
        add_time(0.75)

        pause_to(7.1)

        self.play(Create(arrow_predict), FadeIn(predict_box, scale=0.96), run_time=0.8)
        add_time(0.8)

        pause_to(9.2)

        self.play(FadeIn(next_token_1, scale=0.85), run_time=0.45)
        add_time(0.45)

        pause_to(10.5)

        self.play(Create(append_arrow), run_time=0.45)
        add_time(0.45)

        self.play(FadeIn(loop_note, shift=UP), run_time=0.65)
        add_time(0.65)

        pause_to(12.8)

        self.play(FadeIn(next_token_2, scale=0.85), run_time=0.45)
        add_time(0.45)

        pause_to(16.4)

        clear(
            decode_box,
            prompt_mini,
            generated_context,
            predict_box,
            arrow_predict,
            next_token_1,
            next_token_2,
            append_arrow,
            loop_note,
            run_time=0.45,
        )

        # =====================================================
        # CẢNH 2 - AUTOREGRESSIVE DECODING
        # =====================================================
        ar_label = text_en(
            "Autoregressive Decoding",
            font_size=31,
            color=GREEN,
        )
        fit_text(ar_label, 10)
        ar_label.next_to(subtitle, DOWN, buff=0.5)

        token_steps = VGroup(
            make_token_en("token 1", GREEN, width=1.15),
            make_token_en("token 2", GREEN, width=1.15),
            make_token_en("token 3", GREEN, width=1.15),
            make_token_en("token 4", GREEN, width=1.15),
        )
        token_steps.arrange(RIGHT, buff=0.42)
        token_steps.move_to(DOWN * 0.25)

        step_arrows = VGroup()
        for i in range(len(token_steps) - 1):
            step_arrows.add(
                Arrow(
                    token_steps[i].get_right(),
                    token_steps[i + 1].get_left(),
                    buff=0.1,
                    color=MUTED,
                    stroke_width=2.5,
                )
            )

        one_by_one = text_vi(
            "Sinh từng token một",
            font_size=26,
            color=YELLOW,
        )
        fit_text(one_by_one, 8)
        one_by_one.next_to(token_steps, DOWN, buff=0.55)

        pause_to(16.9)

        self.play(FadeIn(ar_label, shift=UP), run_time=0.6)
        add_time(0.6)

        pause_to(18.1)

        for i, tok in enumerate(token_steps):
            self.play(FadeIn(tok, scale=0.85), run_time=0.28)
            add_time(0.28)

            if i < len(step_arrows):
                self.play(Create(step_arrows[i]), run_time=0.14)
                add_time(0.14)

        self.play(FadeIn(one_by_one, shift=UP), run_time=0.45)
        add_time(0.45)

        pause_to(23.2)

        clear(
            ar_label,
            token_steps,
            step_arrows,
            one_by_one,
            run_time=0.4,
        )

        # =====================================================
        # CẢNH 3 - VÍ DỤ PROMPT
        # =====================================================
        prompt_label = mixed_prompt_label()
        prompt_label.next_to(subtitle, DOWN, buff=0.5)

        prompt_tokens = VGroup(
            make_token_vi("Thủ", MUTED),
            make_token_vi("đô", MUTED),
            make_token_vi("của", MUTED),
            make_token_vi("Việt", MUTED, width=0.92),
            make_token_vi("Nam", MUTED, width=0.9),
            make_token_vi("là", MUTED),
        )
        prompt_tokens.arrange(RIGHT, buff=0.13)
        prompt_tokens.move_to(UP * 0.35)

        generated_label = text_vi(
            "Mô hình sinh tiếp:",
            font_size=24,
            color=GREEN,
        )
        fit_text(generated_label, 8)
        generated_label.move_to(DOWN * 0.55)

        generated_tokens = VGroup(
            make_token_vi("Hà", GREEN),
            make_token_vi("Nội", GREEN),
            make_token_vi(".", GREEN),
            make_token_en("...", GREEN),
        )
        generated_tokens.arrange(RIGHT, buff=0.22)
        generated_tokens.next_to(generated_label, DOWN, buff=0.35)

        gen_arrows = VGroup()
        for i in range(len(generated_tokens) - 1):
            gen_arrows.add(
                Arrow(
                    generated_tokens[i].get_right(),
                    generated_tokens[i + 1].get_left(),
                    buff=0.08,
                    color=MUTED,
                    stroke_width=2.4,
                )
            )

        context_note = bottom_note_vi(
            "Mỗi token mới dựa trên toàn bộ ngữ cảnh trước đó",
            font_size=24,
            color=BLUE,
            y=-2.38,
            max_width=10.2,
        )

        pause_to(23.7)

        self.play(Write(prompt_label), run_time=0.45)
        add_time(0.45)

        self.play(
            LaggedStart(
                *[FadeIn(tok, shift=UP) for tok in prompt_tokens],
                lag_ratio=0.025,
            ),
            run_time=0.65,
        )
        add_time(0.65)

        pause_to(25.7)

        self.play(FadeIn(generated_label, shift=UP), run_time=0.35)
        add_time(0.35)

        generated_times = [26.7, 27.8, 28.8, 29.6]

        for i, tok in enumerate(generated_tokens):
            pause_to(generated_times[i])

            self.play(FadeIn(tok, scale=0.85), run_time=0.26)
            add_time(0.26)

            if i < len(gen_arrows):
                self.play(Create(gen_arrows[i]), run_time=0.11)
                add_time(0.11)

        pause_to(32.0)

        self.play(FadeIn(context_note, shift=UP), run_time=0.5)
        add_time(0.5)

        pause_to(39.0)

        clear(
            prompt_label,
            prompt_tokens,
            generated_label,
            generated_tokens,
            gen_arrows,
            context_note,
            run_time=0.4,
        )

        # =====================================================
        # CẢNH 4 - ĐIỂM MẠNH VÀ NÚT THẮT TUẦN TỰ
        # =====================================================
        strength_box = model_box_vi(
            "Điểm mạnh\nmạch lạc, đúng ngữ cảnh",
            GREEN,
            width=4.3,
            height=1.25,
            font_size=23,
        )
        strength_box.move_to(LEFT * 3.0 + UP * 0.35)

        bottleneck_box = model_box_vi(
            "Nút thắt\ntính tuần tự rất mạnh",
            RED,
            width=4.3,
            height=1.25,
            font_size=23,
        )
        bottleneck_box.move_to(RIGHT * 3.0 + UP * 0.35)

        compare_arrow = Arrow(
            strength_box.get_right(),
            bottleneck_box.get_left(),
            color=YELLOW,
            stroke_width=3,
        )

        dep_tokens = VGroup(
            make_token_en("8", BLUE),
            make_token_en("9", BLUE),
            make_token_en("10", YELLOW),
        )
        dep_tokens.arrange(RIGHT, buff=0.55)
        dep_tokens.move_to(DOWN * 1.05)

        dep_arrows = VGroup(
            Arrow(
                dep_tokens[0].get_right(),
                dep_tokens[1].get_left(),
                buff=0.1,
                color=MUTED,
            ),
            Arrow(
                dep_tokens[1].get_right(),
                dep_tokens[2].get_left(),
                buff=0.1,
                color=MUTED,
            ),
        )

        dep_note = text_vi(
            "Token 10 phải đợi token 9, token 9 phải đợi token 8",
            font_size=24,
            color=YELLOW,
        )
        fit_text(dep_note, 10.5)
        dep_note.move_to(DOWN * 2.34)

        pause_to(39.4)

        self.play(FadeIn(strength_box, shift=UP), run_time=0.55)
        add_time(0.55)

        pause_to(43.4)

        self.play(
            Create(compare_arrow),
            FadeIn(bottleneck_box, shift=UP),
            run_time=0.65,
        )
        add_time(0.65)

        pause_to(46.3)

        self.play(FadeIn(dep_tokens[0]), run_time=0.22)
        add_time(0.22)

        self.play(
            Create(dep_arrows[0]),
            FadeIn(dep_tokens[1]),
            run_time=0.34,
        )
        add_time(0.34)

        self.play(
            Create(dep_arrows[1]),
            FadeIn(dep_tokens[2]),
            run_time=0.34,
        )
        add_time(0.34)

        self.play(FadeIn(dep_note, shift=UP), run_time=0.55)
        add_time(0.55)

        pause_to(55.0)

        clear(
            strength_box,
            bottleneck_box,
            compare_arrow,
            dep_tokens,
            dep_arrows,
            dep_note,
            run_time=0.4,
        )

        # =====================================================
        # CẢNH 5 - CÂU TRẢ LỜI DÀI THÌ CHẬM
        # =====================================================
        long_answer_title = text_vi(
            "Câu trả lời càng dài...",
            font_size=31,
            color=WHITE,
        )
        fit_text(long_answer_title, 10)
        long_answer_title.next_to(subtitle, DOWN, buff=0.5)

        many_tokens = VGroup()
        for i in range(18):
            color = GREEN if i < 5 else BLUE
            many_tokens.add(make_token_en("", color=color, width=0.36))

        row1 = VGroup(*many_tokens[:9])
        row2 = VGroup(*many_tokens[9:])
        row1.arrange(RIGHT, buff=0.09)
        row2.arrange(RIGHT, buff=0.09)

        token_grid = VGroup(row1, row2)
        token_grid.arrange(DOWN, buff=0.18)
        token_grid.move_to(ORIGIN + DOWN * 0.1)

        slow_label = text_vi(
            "...thì số bước sinh token càng nhiều",
            font_size=26,
            color=YELLOW,
        )
        fit_text(slow_label, 10)
        slow_label.move_to(DOWN * 1.55)

        pause_to(55.5)

        self.play(Write(long_answer_title), run_time=0.5)
        add_time(0.5)

        self.play(
            LaggedStart(
                *[FadeIn(tok, scale=0.8) for tok in many_tokens],
                lag_ratio=0.025,
            ),
            run_time=1.05,
        )
        add_time(1.05)

        self.play(FadeIn(slow_label, shift=UP), run_time=0.5)
        add_time(0.5)

        pause_to(60.0)

        clear(
            long_answer_title,
            token_grid,
            slow_label,
            run_time=0.35,
        )

        # =====================================================
        # CẢNH 6 - CÂU HỎI CHUYỂN Ý
        # =====================================================
        question_box = RoundedRectangle(
            width=11.2,
            height=1.65,
            corner_radius=0.18,
            stroke_color=GREEN,
            stroke_width=2,
            fill_color=GREEN,
            fill_opacity=0.08,
        )
        question_box.move_to(DOWN * 0.15)

        final_question = text_vi(
            "Có cách nào sinh token nhanh hơn,\ntận dụng song song tốt hơn,\nnhưng vẫn giữ chất lượng gần như mô hình gốc?",
            font_size=26,
            color=GREEN,
            line_spacing=0.86,
        )
        fit_text(final_question, 10.5, 1.45)
        final_question.move_to(question_box.get_center())

        pause_to(60.5)

        self.play(
            Create(question_box),
            Write(final_question),
            run_time=0.9,
        )
        add_time(0.9)

        self.play(Flash(question_box, color=GREEN), run_time=0.45)
        add_time(0.45)

        wait_audio(self, audio, visual_time)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(question_box),
            FadeOut(final_question),
            run_time=0.8,
        )