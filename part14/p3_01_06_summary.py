# -*- coding: utf-8 -*-

from manim import *
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.visual_utils import *


class SceneP3DecodingAlgorithmsSummary(Scene):
    def construct(self):
        self.camera.background_color = BG

        audio = str(Path(__file__).resolve().parents[1] / "voice" / "p3_01_06_summary.mp3")
        play_audio(self, audio)
        visual_time = 0

        # =====================================================
        # HELPERS
        # =====================================================
        def add_time(duration):
            nonlocal visual_time
            visual_time += duration

        def pause_to(target_time):
            nonlocal visual_time
            delay = max(0, target_time - visual_time)
            if delay > 0:
                self.wait(delay)
                visual_time += delay

        def play_timed(*animations, run_time=0.4, **kwargs):
            self.play(*animations, run_time=run_time, **kwargs)
            add_time(run_time)

        def clear(*mobjects, run_time=0.25):
            if not mobjects:
                return
            play_timed(*[FadeOut(mob) for mob in mobjects], run_time=run_time)

        def get_audio_duration_seconds(path, fallback=52.0):
            try:
                from mutagen.mp3 import MP3
                return float(MP3(path).info.length)
            except Exception:
                return fallback

        audio_len = get_audio_duration_seconds(audio, fallback=52.0)
        audio_len = max(45.0, min(audio_len, 80.0))

        def at(ratio):
            return audio_len * ratio

        def bottom_note(text, font_size=21, color=YELLOW, max_width=10.8):
            note = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=max_width,
            )
            note.move_to(DOWN * 2.35)
            return note

        def section_title(text, color=WHITE, font_size=30):
            t = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=10.8,
            )
            t.next_to(subtitle, DOWN, buff=0.34)
            return t

        def small_card(text, color, width=2.2, height=0.65, font_size=19):
            return model_box(
                text,
                color,
                width=width,
                height=height,
                font_size=font_size,
            )

        def make_row_card(title_text, desc_text, color):
            rect = RoundedRectangle(
                width=8.9,
                height=0.62,
                corner_radius=0.12,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.08,
            )

            icon = RoundedRectangle(
                width=0.34,
                height=0.34,
                corner_radius=0.08,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.34,
            )
            icon.move_to(LEFT * 4.10)

            title_obj = safe_text(
                title_text,
                font_size=20,
                color=color,
                max_width=3.2,
            )
            title_obj.move_to(LEFT * 2.45)

            desc_obj = safe_text(
                desc_text,
                font_size=18,
                color=WHITE,
                max_width=4.55,
            )
            desc_obj.move_to(RIGHT * 1.55)

            return VGroup(rect, icon, title_obj, desc_obj)

        def row_highlight(row, color):
            return SurroundingRectangle(
                row,
                color=color,
                buff=0.045,
                corner_radius=0.12,
                stroke_width=3,
            )

        # =====================================================
        # HEADER
        # =====================================================
        title = safe_text(
            "Decoding Algorithms",
            font_size=40,
            color=WHITE,
            max_width=11,
        )
        title.to_edge(UP, buff=0.38)

        subtitle = safe_text(
            "Tóm tắt các hướng tối ưu quá trình sinh token",
            font_size=24,
            color=BLUE,
            max_width=11,
        )
        subtitle.next_to(title, DOWN, buff=0.20)

        play_timed(Write(title), run_time=0.60)

        pause_to(0.95)

        play_timed(FadeIn(subtitle, shift=UP), run_time=0.38)

        # =====================================================
        # CẢNH 1 - NÚT THẮT
        # Voice:
        # Tóm lại nhóm decoding algorithms...
        # sinh token tuần tự quá chậm.
        # =====================================================
        bottleneck_title = section_title(
            "Nút thắt lớn của LLM generation",
            color=WHITE,
        )

        llm_box = small_card(
            "LLM",
            BLUE,
            width=1.70,
            height=0.70,
            font_size=24,
        )
        llm_box.move_to(LEFT * 3.65 + DOWN * 0.05)

        t1 = token_box("token 1", color=YELLOW, width=1.25, height=0.58, font_size=18)
        t2 = token_box("token 2", color=YELLOW, width=1.25, height=0.58, font_size=18)
        t3 = token_box("token 3", color=YELLOW, width=1.25, height=0.58, font_size=18)
        t4 = token_box("token 4", color=YELLOW, width=1.25, height=0.58, font_size=18)

        tokens = VGroup(t1, t2, t3, t4)
        tokens.arrange(RIGHT, buff=0.28)
        tokens.move_to(RIGHT * 1.05 + DOWN * 0.05)

        arrow0 = Arrow(
            llm_box.get_right(),
            t1.get_left(),
            color=MUTED,
            stroke_width=2.5,
            buff=0.10,
        )
        arrow1 = Arrow(t1.get_right(), t2.get_left(), color=MUTED, stroke_width=2.5, buff=0.10)
        arrow2 = Arrow(t2.get_right(), t3.get_left(), color=MUTED, stroke_width=2.5, buff=0.10)
        arrow3 = Arrow(t3.get_right(), t4.get_left(), color=MUTED, stroke_width=2.5, buff=0.10)

        # slow_note = bottom_note(
        #     "Sinh token tuần tự: token sau phải chờ token trước",
        #     color=RED,
        # )

        pause_to(1.45)

        play_timed(Write(bottleneck_title), run_time=0.42)

        pause_to(3.20)

        play_timed(FadeIn(llm_box, shift=RIGHT), run_time=0.35)

        pause_to(4.35)

        play_timed(Create(arrow0), FadeIn(t1, shift=RIGHT), run_time=0.35)

        pause_to(5.30)

        play_timed(Create(arrow1), FadeIn(t2, shift=RIGHT), run_time=0.35)

        pause_to(6.15)

        play_timed(Create(arrow2), FadeIn(t3, shift=RIGHT), run_time=0.35)

        pause_to(7.00)

        play_timed(Create(arrow3), FadeIn(t4, shift=RIGHT), run_time=0.35)

        pause_to(at(0.17))

        # play_timed(FadeIn(slow_note, shift=UP), run_time=0.35)

        pause_to(at(0.215))

        clear(
            bottleneck_title,
            llm_box,
            tokens,
            arrow0,
            arrow1,
            arrow2,
            arrow3,
            # slow_note,
            run_time=0.22,
        )

        # =====================================================
        # CẢNH 2 - BẢNG DECODING ALGORITHMS
        # Voice:
        # Có thể tóm tắt nhóm này thành bốn hướng chính.
        # =====================================================
        root = model_box(
            "Decoding Algorithms",
            PURPLE,
            width=4.25,
            height=0.62,
            font_size=24,
        )
        root.move_to(UP * 1.18)

        row_non_ar = make_row_card(
            "Non-autoregressive",
            "Sinh song song nhiều token",
            GREEN,
        )

        row_spec = make_row_card(
            "Speculative",
            "Model nhỏ đoán, model lớn kiểm tra và quyết định",
            PURPLE,
        )

        row_early = make_row_card(
            "Early Exiting",
            "Thoát sớm nếu model đủ tự tin",
            BLUE,
        )

        row_cascade = make_row_card(
            "Cascade",
            "Chọn model theo độ khó request",
            RED,
        )

        rows = VGroup(row_non_ar, row_spec, row_early, row_cascade)
        rows.arrange(DOWN, buff=0.16)
        rows.next_to(root, DOWN, buff=0.48)

        down_arrow = Arrow(
            root.get_bottom(),
            rows.get_top(),
            color=MUTED,
            stroke_width=2.3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.12,
        )

        pause_to(at(0.235))

        play_timed(
            FadeIn(root, shift=UP),
            Create(down_arrow),
            run_time=0.40,
        )

        # -----------------------------------------------------
        # Hướng 1 - Non-autoregressive
        # -----------------------------------------------------
        non_ar_highlight = row_highlight(row_non_ar, GREEN)

        pause_to(at(0.300))

        play_timed(
            FadeIn(row_non_ar, shift=RIGHT),
            Create(non_ar_highlight),
            run_time=0.42,
        )

        pause_to(at(0.385))

        play_timed(FadeOut(non_ar_highlight), run_time=0.18)

        # -----------------------------------------------------
        # Hướng 2 - Speculative
        # -----------------------------------------------------
        spec_highlight = row_highlight(row_spec, PURPLE)

        pause_to(at(0.405))

        play_timed(
            FadeIn(row_spec, shift=RIGHT),
            Create(spec_highlight),
            run_time=0.42,
        )

        pause_to(at(0.545))

        play_timed(FadeOut(spec_highlight), run_time=0.18)

        # -----------------------------------------------------
        # Hướng 3 - Early Exiting
        # -----------------------------------------------------
        early_highlight = row_highlight(row_early, BLUE)

        pause_to(at(0.565))

        play_timed(
            FadeIn(row_early, shift=RIGHT),
            Create(early_highlight),
            run_time=0.42,
        )

        pause_to(at(0.650))

        play_timed(FadeOut(early_highlight), run_time=0.18)

        # -----------------------------------------------------
        # Hướng 4 - Cascade
        # -----------------------------------------------------
        cascade_highlight = row_highlight(row_cascade, RED)

        pause_to(at(0.670))

        play_timed(
            FadeIn(row_cascade, shift=RIGHT),
            Create(cascade_highlight),
            run_time=0.42,
        )

        pause_to(at(0.735))

        play_timed(FadeOut(cascade_highlight), run_time=0.18)

        pause_to(at(0.755))

        clear(
            root,
            down_arrow,
            rows,
            run_time=0.25,
        )

        # =====================================================
        # CẢNH 3 - ĐIỂM CHUNG
        # Voice:
        # Điểm chung là các phương pháp này đều muốn giảm thời gian suy luận
        # hoặc giảm chi phí phục vụ mô hình.
        # =====================================================
        common_title = section_title(
            "Điểm chung của các phương pháp",
            color=YELLOW,
        )

        speed_box = small_card(
            "Giảm thời gian\nsuy luận",
            GREEN,
            width=3.05,
            height=0.95,
            font_size=21,
        )
        speed_box.move_to(LEFT * 2.65 + UP * 0.25)

        cost_box = small_card(
            "Giảm chi phí\nphục vụ",
            BLUE,
            width=3.05,
            height=0.95,
            font_size=21,
        )
        cost_box.move_to(RIGHT * 2.65 + UP * 0.25)

        common_arrow = DoubleArrow(
            speed_box.get_right(),
            cost_box.get_left(),
            color=MUTED,
            stroke_width=2.4,
            buff=0.10,
        )

        common_note = bottom_note(
            "Giảm thời gian suy luận hoặc giảm chi phí phục vụ mô hình",
            color=YELLOW,
            max_width=11.0,
        )

        pause_to(at(0.770))

        play_timed(Write(common_title), run_time=0.36)

        pause_to(at(0.795))

        play_timed(FadeIn(speed_box, shift=UP), run_time=0.34)

        pause_to(at(0.820))

        play_timed(
            Create(common_arrow),
            FadeIn(cost_box, shift=UP),
            run_time=0.38,
        )

        pause_to(at(0.845))

        play_timed(FadeIn(common_note, shift=UP), run_time=0.34)

        # =====================================================
        # CẢNH 4 - TRADE-OFF
        # Voice:
        # Nhưng luôn phải cân bằng giữa tốc độ, chi phí và chất lượng đầu ra.
        # =====================================================
        tradeoff_title = section_title(
            "Cân bằng cuối cùng",
            color=YELLOW,
        )

        quality_box = small_card(
            "Giữ chất lượng\nđầu ra",
            RED,
            width=3.05,
            height=0.95,
            font_size=21,
        )
        quality_box.move_to(DOWN * 1.05)

        trade_triangle = Polygon(
            speed_box.get_top() + UP * 0.18,
            cost_box.get_top() + UP * 0.18,
            quality_box.get_bottom() + DOWN * 0.18,
            color=YELLOW,
            stroke_width=2.4,
        )
        trade_triangle.set_fill(YELLOW, opacity=0.04)

        balance_note = bottom_note(
            "Cân bằng giữa tốc độ, chi phí và chất lượng đầu ra",
            color=YELLOW,
            max_width=11.0,
        )

        pause_to(at(0.875))

        play_timed(
            FadeOut(common_note),
            ReplacementTransform(common_title, tradeoff_title),
            run_time=0.38,
        )

        pause_to(at(0.900))

        play_timed(
            FadeIn(quality_box, shift=UP),
            Create(trade_triangle),
            run_time=0.50,
        )

        pause_to(at(0.925))

        play_timed(
            FadeIn(balance_note, shift=UP),
            Flash(trade_triangle, color=YELLOW),
            run_time=0.50,
        )

        wait_audio(self, audio, visual_time)

        play_timed(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(tradeoff_title),
            FadeOut(speed_box),
            FadeOut(cost_box),
            FadeOut(quality_box),
            FadeOut(common_arrow),
            FadeOut(trade_triangle),
            FadeOut(balance_note),
            run_time=0.25,
        )