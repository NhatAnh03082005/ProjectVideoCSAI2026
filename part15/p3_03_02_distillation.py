# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# PHẦN 3.2 - KNOWLEDGE DISTILLATION
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_03_02_distillation.py SceneP30302KnowledgeDistillation
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


def audio_duration(path, fallback=10.0):
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
    title = Text(
        text,
        font=FONT,
        font_size=38,
        color=WHITE,
    )
    fit_text(title, 11.2)
    title.to_edge(UP, buff=0.28)
    return title


def make_subtitle(text, title):
    subtitle = Text(
        text,
        font=FONT,
        font_size=23,
        color=BLUE,
    )
    fit_text(subtitle, 10.8)
    subtitle.next_to(title, DOWN, buff=0.14)
    return subtitle


class SceneP30302KnowledgeDistillation(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"
        active_mobs = []

        def get_audio_path(filename):
            return str(voice_dir / filename)

        def section_title(text, subtitle, color=WHITE, font_size=28):
            t = Text(text, font=FONT, font_size=font_size, color=color)
            fit_text(t, 10.9)
            t.next_to(subtitle, DOWN, buff=0.30)
            return t

        def bottom_note(text, color=YELLOW, font_size=21, y=-2.32):
            note = Text(text, font=FONT, font_size=font_size, color=color)
            fit_text(note, 10.9)
            note.move_to(DOWN * abs(y))
            return note

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
                clear_active_before_audio(run_time=0.10)

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

        def prob_bar(label, value, color, width=3.55, height=0.34):
            label_text = Text(label, font=FONT, font_size=20, color=WHITE)
            fit_text(label_text, 0.42)

            frame = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.08,
                stroke_color=color,
                stroke_width=1.6,
                fill_color=color,
                fill_opacity=0.06,
            )
            frame.move_to(ORIGIN)

            fill_rect = Rectangle(
                width=max(0.10, width * value),
                height=height * 0.62,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.70,
            )
            fill_rect.move_to(frame.get_left() + RIGHT * (fill_rect.width / 2))

            pct = Text(
                f"{int(value * 100)}%",
                font=FONT,
                font_size=16,
                color=color,
            )

            bar = VGroup(frame, fill_rect)
            row = VGroup(label_text, bar, pct)
            row.arrange(RIGHT, buff=0.18)
            return row

        def person_card(role, desc, color, scale=1.0):
            head = Circle(
                radius=0.26 * scale,
                stroke_color=color,
                stroke_width=2.2,
                fill_color=color,
                fill_opacity=0.18,
            )
            body = RoundedRectangle(
                width=1.25 * scale,
                height=0.82 * scale,
                corner_radius=0.15,
                stroke_color=color,
                stroke_width=2.2,
                fill_color=color,
                fill_opacity=0.12,
            )
            body.next_to(head, DOWN, buff=0.08 * scale)

            role_text = Text(role, font=FONT, font_size=20 * scale, color=color)
            role_text.next_to(body, DOWN, buff=0.12 * scale)

            desc_text = Text(
                desc,
                font=FONT,
                font_size=16 * scale,
                color=WHITE,
                line_spacing=0.80,
            )
            fit_text(desc_text, 2.55 * scale, 0.80 * scale)
            desc_text.next_to(role_text, DOWN, buff=0.10 * scale)

            return VGroup(head, body, role_text, desc_text)

        # =====================================================
        # HEADER
        # =====================================================
        title = make_title("Knowledge Distillation")
        subtitle = make_subtitle(
            "Teacher model lớn dạy student model nhỏ",
            title,
        )

        # =====================================================
        # 1) INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            kd_vi = make_box(
                "Chưng cất tri thức",
                YELLOW,
                width=4.20,
                height=0.86,
                font_size=25,
                fill=0.12,
            )
            kd_vi.move_to(UP * 0.30)

            note = bottom_note(
                "Model lớn truyền kiến thức cho model nhỏ",
                color=YELLOW,
                font_size=22,
                y=-1.45,
            )

            play(Write(title), run_time=0.55)

            wait_to(0.18)
            play(FadeIn(subtitle, shift=UP), run_time=0.25)

            wait_to(0.42)
            play(FadeIn(kd_vi, shift=UP), run_time=0.35)

            wait_to(0.72)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(kd_vi, note)

        play_segment(
            "p3_03_02_01_intro.mp3",
            fallback_duration=5.0,
            visual_func=visual_intro,
            clear_before=False,
        )

        # =====================================================
        # 2) TEACHER -> STUDENT
        # =====================================================
        def visual_teacher_student(wait_to, play, duration):
            teacher = make_box(
                "Teacher Model\nlớn",
                BLUE,
                width=3.05,
                height=1.05,
                font_size=24,
                fill=0.12,
            )
            teacher.move_to(LEFT * 3.35 + UP * 0.35)

            student = make_box(
                "Student Model\nnhỏ hơn",
                GREEN,
                width=3.05,
                height=1.05,
                font_size=24,
                fill=0.12,
            )
            student.move_to(RIGHT * 3.35 + UP * 0.35)

            arrow = Arrow(
                teacher.get_right(),
                student.get_left(),
                color=YELLOW,
                stroke_width=5,
                buff=0.20,
            )

            arrow_label = Text(
                "response / soft label",
                font=FONT,
                font_size=22,
                color=YELLOW,
            )
            fit_text(arrow_label, 4.20)
            arrow_label.next_to(arrow, UP, buff=0.15)

            note = bottom_note(
                "Dùng model lớn để huấn luyện model nhỏ",
                color=GREEN,
                font_size=22,
                y=-1.70,
            )

            wait_to(0.05)
            play(FadeIn(teacher, shift=RIGHT), run_time=0.35)

            wait_to(0.36)
            play(
                GrowArrow(arrow),
                FadeIn(arrow_label, shift=UP),
                run_time=0.35,
            )

            wait_to(0.58)
            play(FadeIn(student, shift=LEFT), run_time=0.35)

            wait_to(0.82)
            play(FadeIn(note, shift=UP), run_time=0.28)

            set_active(teacher, student, arrow, arrow_label, note)

        play_segment(
            "p3_03_02_02_teacher_student.mp3",
            fallback_duration=6.5,
            visual_func=visual_teacher_student,
        )

        # =====================================================
        # 3) HỌC TỪ ĐẦU RA TEACHER
        # =====================================================
        def visual_learn_from_teacher(wait_to, play, duration):
            st = section_title(
                "Student học từ đầu ra của teacher",
                subtitle,
                color=YELLOW,
                font_size=28,
            )

            hard = make_box(
                "Nhãn gốc\nHard label",
                BLUE,
                width=3.10,
                height=0.95,
                font_size=22,
                fill=0.11,
            )
            hard.move_to(LEFT * 3.55 + UP * 0.25)

            teacher_out = make_box(
                "Teacher output\nresponse + soft label",
                PURPLE,
                width=4.05,
                height=1.02,
                font_size=22,
                fill=0.11,
            )
            teacher_out.move_to(RIGHT * 2.75 + UP * 0.25)

            student = make_box(
                "Student",
                GREEN,
                width=2.10,
                height=0.68,
                font_size=22,
                fill=0.12,
            )
            student.move_to(DOWN * 1.18)

            a1 = Arrow(
                hard.get_bottom() + RIGHT * 0.18,
                student.get_left() + UP * 0.12,
                color=BLUE,
                buff=0.15,
                stroke_width=2.4,
            )

            a2 = Arrow(
                teacher_out.get_bottom() + LEFT * 0.20,
                student.get_right() + UP * 0.12,
                color=PURPLE,
                buff=0.15,
                stroke_width=3.0,
            )

            note = bottom_note(
                "Không chỉ học đáp án đúng, mà còn học mức độ tin cậy",
                color=YELLOW,
                font_size=21,
                y=-2.25,
            )

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.16)
            play(FadeIn(hard, shift=RIGHT), run_time=0.32)

            wait_to(0.34)
            play(FadeIn(teacher_out, shift=LEFT), run_time=0.32)

            wait_to(0.58)
            play(
                FadeIn(student, shift=UP),
                Create(a1),
                Create(a2),
                run_time=0.45,
            )

            wait_to(0.78)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(st, hard, teacher_out, student, a1, a2, note)

        play_segment(
            "p3_03_02_03_learn_from_teacher.mp3",
            fallback_duration=11.5,
            visual_func=visual_learn_from_teacher,
        )

        # =====================================================
        # 4) SOFT LABEL EXAMPLE
        # =====================================================
        def visual_soft_label_example(wait_to, play, duration):
            st = section_title(
                "Ví dụ soft label từ teacher",
                subtitle,
                color=PURPLE,
                font_size=28,
            )

            question = make_box(
                "Câu hỏi trắc nghiệm\nĐáp án đúng: A",
                BLUE,
                width=4.05,
                height=0.90,
                font_size=21,
                fill=0.10,
            )
            question.move_to(LEFT * 3.95 + UP * 0.15)

            bars = VGroup(
                prob_bar("A", 0.82, GREEN),
                prob_bar("B", 0.13, YELLOW),
                prob_bar("C", 0.04, ORANGE),
                prob_bar("D", 0.01, RED),
            )
            bars.arrange(DOWN, buff=0.18)
            bars.move_to(RIGHT * 2.30 + DOWN * 0.12)

            teacher_box = make_box(
                "Teacher cho phân phối xác suất",
                PURPLE,
                width=4.60,
                height=0.62,
                font_size=20,
                fill=0.10,
            )
            teacher_box.next_to(bars, UP, buff=0.28)

            note = bottom_note(
                "A rất cao, B hơi hợp lý, C thấp hơn, D gần như sai",
                color=YELLOW,
                font_size=18,
                y=-2.42,
            )

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.16)
            play(FadeIn(question, shift=RIGHT), run_time=0.35)

            wait_to(0.32)
            play(FadeIn(teacher_box, shift=UP), run_time=0.28)

            wait_to(0.46)
            play(FadeIn(bars[0], shift=RIGHT), run_time=0.28)

            wait_to(0.60)
            play(FadeIn(bars[1], shift=RIGHT), run_time=0.28)

            wait_to(0.72)
            play(FadeIn(bars[2], shift=RIGHT), run_time=0.24)

            wait_to(0.82)
            play(FadeIn(bars[3], shift=RIGHT), run_time=0.24)

            wait_to(0.90)
            play(FadeIn(note, shift=UP), run_time=0.26)

            set_active(st, question, teacher_box, bars, note)

        play_segment(
            "p3_03_02_04_soft_label_example.mp3",
            fallback_duration=14.0,
            visual_func=visual_soft_label_example,
        )

        # =====================================================
        # 5) LỢI ÍCH CỦA SOFT LABEL
        # =====================================================
        def visual_soft_label_benefit(wait_to, play, duration):
            st = section_title(
                "Soft label giúp student học tốt hơn",
                subtitle,
                color=GREEN,
                font_size=28,
            )

            hard = make_box(
                "Hard label\nA đúng\nB, C, D sai",
                RED,
                width=3.15,
                height=1.02,
                font_size=20,
                fill=0.09,
            )
            hard.move_to(LEFT * 3.30 + UP * 0.38)

            soft = make_box(
                "Soft label\nA cao, B hơi hợp lý\nC thấp, D gần như sai",
                GREEN,
                width=4.15,
                height=1.15,
                font_size=19,
                fill=0.12,
            )
            soft.move_to(RIGHT * 2.85 + UP * 0.38)

            student = make_box(
                "Student",
                YELLOW,
                width=2.15,
                height=0.70,
                font_size=23,
                fill=0.11,
            )
            student.move_to(DOWN * 1.05)

            hard_arrow = Arrow(
                hard.get_bottom(),
                student.get_left() + UP * 0.12,
                color=RED,
                stroke_width=2.2,
                buff=0.16,
            )

            soft_arrow = Arrow(
                soft.get_bottom(),
                student.get_right() + UP * 0.12,
                color=GREEN,
                stroke_width=3.6,
                buff=0.16,
            )

            note = make_box(
                "Soft label chứa nhiều thông tin hơn\nnên giúp student học cách ra quyết định của teacher",
                GREEN,
                width=7.95,
                height=0.82,
                font_size=20,
                fill=0.09,
            )
            note.move_to(DOWN * 2.18)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.14)
            play(FadeIn(soft, shift=LEFT), run_time=0.32)

            wait_to(0.36)
            play(
                FadeIn(student, shift=UP),
                Create(soft_arrow),
                run_time=0.36,
            )

            wait_to(0.62)
            play(
                FadeIn(hard, shift=RIGHT),
                Create(hard_arrow),
                run_time=0.34,
            )

            wait_to(0.78)
            play(FadeIn(note, shift=UP), run_time=0.34)

            wait_to(0.90)
            play(
                soft[0].animate.set_stroke(GREEN, width=3.5).set_fill(GREEN, opacity=0.16),
                hard[0].animate.set_stroke(RED, width=1.8).set_fill(RED, opacity=0.06),
                run_time=0.28,
            )

            set_active(st, hard, soft, student, hard_arrow, soft_arrow, note)

        play_segment(
            "p3_03_02_05_soft_label_benefit.mp3",
            fallback_duration=9.5,
            visual_func=visual_soft_label_benefit,
        )

        # =====================================================
        # 6) MỤC TIÊU
        # =====================================================
        def visual_goal(wait_to, play, duration):
            st = section_title(
                "Mục tiêu của distillation",
                subtitle,
                color=YELLOW,
                font_size=28,
            )

            small = make_box(
                "Nhỏ hơn",
                GREEN,
                width=2.30,
                height=0.78,
                font_size=24,
                fill=0.11,
            )

            fast = make_box(
                "Chạy nhanh hơn",
                BLUE,
                width=2.70,
                height=0.78,
                font_size=23,
                fill=0.11,
            )

            memory = make_box(
                "Ít bộ nhớ hơn",
                ORANGE,
                width=2.70,
                height=0.78,
                font_size=23,
                fill=0.11,
            )

            goals = VGroup(small, fast, memory)
            goals.arrange(RIGHT, buff=0.42)
            goals.move_to(UP * 0.40)

            keep = make_box(
                "Giữ lại một phần năng lực\ncủa model lớn",
                PURPLE,
                width=5.40,
                height=0.90,
                font_size=22,
                fill=0.10,
            )
            keep.move_to(DOWN * 1.20)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.24)
            play(FadeIn(small, shift=UP), run_time=0.28)

            wait_to(0.40)
            play(FadeIn(fast, shift=UP), run_time=0.28)

            wait_to(0.56)
            play(FadeIn(memory, shift=UP), run_time=0.28)

            wait_to(0.76)
            play(FadeIn(keep, shift=UP), run_time=0.35)

            set_active(st, goals, keep)

        play_segment(
            "p3_03_02_06_goal.mp3",
            fallback_duration=11.0,
            visual_func=visual_goal,
        )

        # =====================================================
        # 7) GIÁO SƯ -> TRỢ GIẢNG
        # =====================================================
        def visual_analogy(wait_to, play, duration):
            st = section_title(
                "Ví dụ trực quan: giáo sư và trợ giảng",
                subtitle,
                color=ORANGE,
                font_size=28,
            )

            professor = person_card(
                "Giáo sư",
                "rất giỏi\nnhưng chậm, tốn kém",
                BLUE,
                scale=1.08,
            )
            professor.move_to(LEFT * 3.40 + UP * 0.20)

            ta = person_card(
                "Trợ giảng",
                "nhỏ hơn\nrẻ hơn",
                GREEN,
                scale=1.00,
            )
            ta.move_to(RIGHT * 3.40 + UP * 0.20)

            arrow = Arrow(
                professor.get_right(),
                ta.get_left(),
                color=YELLOW,
                stroke_width=5,
                buff=0.25,
            )

            arrow_label = Text(
                "bắt chước cách trả lời",
                font=FONT,
                font_size=22,
                color=YELLOW,
            )
            fit_text(arrow_label, 4.5)
            arrow_label.next_to(arrow, UP, buff=0.15)

            # note = bottom_note(
            #     "Student được huấn luyện để bắt chước teacher",
            #     color=YELLOW,
            #     font_size=21,
            #     y=-2.20,
            # )

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.18)
            play(FadeIn(professor, shift=RIGHT), run_time=0.38)

            wait_to(0.50)
            play(GrowArrow(arrow), FadeIn(arrow_label, shift=UP), run_time=0.35)

            wait_to(0.62)
            play(FadeIn(ta, shift=LEFT), run_time=0.38)

            # wait_to(0.82)
            # play(FadeIn(note, shift=UP), run_time=0.28)

            set_active(st, professor, ta, arrow, arrow_label)

        play_segment(
            "p3_03_02_07_analogy.mp3",
            fallback_duration=12.0,
            visual_func=visual_analogy,
        )

        # =====================================================
        # 8) TRADE-OFF + KHI NÀO DÙNG
        # =====================================================
        def visual_tradeoff(wait_to, play, duration):
            st = section_title(
                "Trade-off: chất lượng, tốc độ và chi phí",
                subtitle,
                color=RED,
                font_size=28,
            )

            warning = make_box(
                "Student thường không mạnh hoàn toàn như teacher",
                RED,
                width=7.30,
                height=0.74,
                font_size=21,
                fill=0.10,
            )
            warning.move_to(UP * 0.72)

            quality = make_box(
                "Chất lượng",
                YELLOW,
                width=2.40,
                height=0.74,
                font_size=22,
                fill=0.10,
            )

            speed = make_box(
                "Tốc độ",
                GREEN,
                width=2.10,
                height=0.74,
                font_size=22,
                fill=0.10,
            )

            cost = make_box(
                "Chi phí",
                BLUE,
                width=2.10,
                height=0.74,
                font_size=22,
                fill=0.10,
            )

            trade = VGroup(quality, speed, cost)
            trade.arrange(RIGHT, buff=0.55)
            trade.move_to(DOWN * 0.25)

            deploy = make_box(
                "Knowledge Distillation phù hợp khi tài nguyên hạn chế\nnhưng vẫn cần chất lượng chấp nhận được",
                GREEN,
                width=7.60,
                height=0.92,
                font_size=21,
                fill=0.10,
            )
            deploy.move_to(DOWN * 1.55)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.14)
            play(FadeIn(warning, shift=UP), run_time=0.34)

            wait_to(0.36)
            play(
                LaggedStart(
                    FadeIn(quality, shift=UP),
                    FadeIn(speed, shift=UP),
                    FadeIn(cost, shift=UP),
                    lag_ratio=0.14,
                ),
                run_time=0.66,
            )

            wait_to(0.68)
            play(FadeIn(deploy, shift=UP), run_time=0.40)

            wait_to(0.88)
            play(Flash(deploy[0], color=GREEN), run_time=0.55)

            set_active(st, trade, warning, deploy)

        play_segment(
            "p3_03_02_08_tradeoff.mp3",
            fallback_duration=17.0,
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
