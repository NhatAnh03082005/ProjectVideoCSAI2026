# -*- coding: utf-8 -*-

from manim import *
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.visual_utils import *


class SceneP3ConfigDownsizing(Scene):
    def construct(self):
        self.camera.background_color = BG

        ROOT = Path(__file__).resolve().parents[1]
        audio = "voice/p3_02_02_config_downsizing.mp3"
        audio_path = ROOT / "voice" / "p3_02_02_config_downsizing.mp3"

        play_audio(self, audio)
        visual_time = 0.0

        # =====================================================
        # HELPERS
        # =====================================================
        def get_audio_duration(path, fallback=68.0):
            try:
                from mutagen.mp3 import MP3
                return float(MP3(str(path)).info.length)
            except Exception:
                return fallback

        audio_len = get_audio_duration(audio_path, fallback=68.0)

        def at(ratio):
            return audio_len * ratio

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

        def clear_group(mobs, run_time=0.14):
            valid = [m for m in mobs if m is not None]
            if not valid:
                return
            play_timed(*[FadeOut(m) for m in valid], run_time=run_time)

        def section_title(text, color=WHITE, font_size=28):
            t = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=10.8,
            )
            t.next_to(subtitle, DOWN, buff=0.30)
            return t

        def small_card(text, color, width=2.4, height=0.68, font_size=20):
            return model_box(
                text,
                color,
                width=width,
                height=height,
                font_size=font_size,
            )

        def highlight(mob, color):
            return SurroundingRectangle(
                mob,
                color=color,
                buff=0.07,
                corner_radius=0.12,
                stroke_width=3,
            )

        def config_row(name, before, after, color, y):
            name_text = safe_text(
                name,
                font_size=19,
                color=color,
                max_width=3.2,
            )
            name_text.move_to(LEFT * 3.15 + UP * y)

            before_box = model_box(
                before,
                RED,
                width=1.55,
                height=0.46,
                font_size=18,
            )
            before_box.move_to(LEFT * 0.05 + UP * y)

            arrow = Arrow(
                RIGHT * 0.78 + UP * y,
                RIGHT * 1.55 + UP * y,
                color=MUTED,
                stroke_width=2.2,
                buff=0.08,
                max_tip_length_to_length_ratio=0.14,
            )

            after_box = model_box(
                after,
                GREEN,
                width=1.75,
                height=0.46,
                font_size=18,
            )
            after_box.move_to(RIGHT * 2.65 + UP * y)

            return VGroup(name_text, before_box, arrow, after_box)

        # =====================================================
        # 1) INTRO
        # =====================================================
        title = safe_text(
            "Configuration Downsizing",
            font_size=38,
            color=WHITE,
            max_width=11,
        )
        title.to_edge(UP, buff=0.45)

        subtitle = safe_text(
            "Giảm cấu hình mô hình",
            font_size=24,
            color=BLUE,
            max_width=11,
        )
        subtitle.next_to(title, DOWN, buff=0.18)

        intro_center = model_box(
            "Làm model nhỏ hơn\nngay từ cấu hình ban đầu",
            YELLOW,
            width=5.45,
            height=0.98,
            font_size=23,
        )
        intro_center.move_to(UP * 0.10)

        play_timed(Write(title), run_time=0.40)

        pause_to(at(0.025))
        play_timed(FadeIn(subtitle, shift=UP), run_time=0.22)

        pause_to(at(0.055))
        play_timed(FadeIn(intro_center, scale=0.96), run_time=0.28)

        pause_to(at(0.120))
        clear_group([intro_center], run_time=0.14)

        # =====================================================
        # 2) MODEL LỚN THU NHỎ
        # =====================================================
        shrink_title = section_title(
            "Model lớn -> model nhỏ hơn",
            color=WHITE,
        )

        big_model = model_box(
            "Large Model\nnặng, tốn tài nguyên",
            RED,
            width=3.40,
            height=1.05,
            font_size=21,
        )
        big_model.move_to(LEFT * 2.95 + UP * 0.20)

        small_model = model_box(
            "Smaller Model\nnhẹ hơn",
            GREEN,
            width=2.80,
            height=0.88,
            font_size=21,
        )
        small_model.move_to(RIGHT * 2.95 + UP * 0.20)

        shrink_arrow = Arrow(
            big_model.get_right(),
            small_model.get_left(),
            color=YELLOW,
            stroke_width=4,
            buff=0.18,
        )

        pause_to(at(0.128))
        play_timed(Write(shrink_title), run_time=0.22)

        pause_to(at(0.145))
        play_timed(FadeIn(big_model, shift=RIGHT), run_time=0.22)

        pause_to(at(0.170))
        play_timed(
            Create(shrink_arrow),
            FadeIn(small_model, shift=LEFT),
            run_time=0.28,
        )

        pause_to(at(0.210))
        clear_group(
            [shrink_title, big_model, small_model, shrink_arrow],
            run_time=0.14,
        )

        # =====================================================
        # 3) BẢNG GIẢM CẤU HÌNH
        # =====================================================
        table_title = section_title(
            "Các cấu hình có thể giảm",
            color=YELLOW,
        )

        component_header = safe_text(
            "Thành phần",
            font_size=20,
            color=WHITE,
            max_width=2.8,
        )
        component_header.move_to(LEFT * 3.15 + UP * 1.12)

        before_header = safe_text(
            "Trước",
            font_size=20,
            color=RED,
            max_width=2.0,
        )
        before_header.move_to(LEFT * 0.05 + UP * 1.12)

        after_header = safe_text(
            "Sau khi giảm",
            font_size=20,
            color=GREEN,
            max_width=2.6,
        )
        after_header.move_to(RIGHT * 2.65 + UP * 1.12)

        header_line = Line(
            LEFT * 4.25 + UP * 0.84,
            RIGHT * 3.75 + UP * 0.84,
            color=MUTED,
            stroke_width=2,
        )

        row_layers = config_row("Số layer", "80", "40", BLUE, 0.55)
        row_hidden = config_row("Hidden dimension", "8192", "4096", GREEN, 0.05)
        row_heads = config_row("Attention heads", "64", "32", PURPLE, -0.45)
        row_ffn = config_row("FFN size", "lớn", "nhỏ hơn", YELLOW, -0.95)
        row_vocab = config_row("Vocabulary size", "lớn", "nhỏ hơn", RED, -1.45)

        pause_to(at(0.218))
        play_timed(Write(table_title), run_time=0.20)

        pause_to(at(0.232))
        play_timed(
            FadeIn(component_header, shift=UP),
            FadeIn(before_header, shift=UP),
            FadeIn(after_header, shift=UP),
            Create(header_line),
            run_time=0.22,
        )

        pause_to(at(0.255))
        h_layers = highlight(row_layers, BLUE)
        play_timed(
            FadeIn(row_layers, shift=RIGHT),
            Create(h_layers),
            run_time=0.23,
        )

        pause_to(at(0.305))
        h_hidden = highlight(row_hidden, GREEN)
        play_timed(
            FadeOut(h_layers),
            FadeIn(row_hidden, shift=RIGHT),
            Create(h_hidden),
            run_time=0.23,
        )

        pause_to(at(0.350))
        h_heads = highlight(row_heads, PURPLE)
        play_timed(
            FadeOut(h_hidden),
            FadeIn(row_heads, shift=RIGHT),
            Create(h_heads),
            run_time=0.23,
        )

        pause_to(at(0.390))
        h_ffn = highlight(row_ffn, YELLOW)
        play_timed(
            FadeOut(h_heads),
            FadeIn(row_ffn, shift=RIGHT),
            Create(h_ffn),
            run_time=0.21,
        )

        pause_to(at(0.420))
        h_vocab = highlight(row_vocab, RED)
        play_timed(
            FadeOut(h_ffn),
            FadeIn(row_vocab, shift=RIGHT),
            Create(h_vocab),
            run_time=0.21,
        )

        pause_to(at(0.460))
        clear_group(
            [
                table_title,
                component_header,
                before_header,
                after_header,
                header_line,
                row_layers,
                row_hidden,
                row_heads,
                row_ffn,
                row_vocab,
                h_vocab,
            ],
            run_time=0.14,
        )

        # =====================================================
        # 4) LỢI ÍCH
        # Voice: Khi giảm các cấu hình này...
        # =====================================================
        benefit_title = section_title(
            "Lợi ích khi giảm cấu hình",
            color=GREEN,
        )

        smaller_box = model_box(
            "Model nhỏ hơn",
            GREEN,
            width=2.90,
            height=0.80,
            font_size=22,
        )
        memory_box = model_box(
            "Ít bộ nhớ hơn",
            BLUE,
            width=2.90,
            height=0.80,
            font_size=22,
        )
        faster_box = model_box(
            "Inference nhanh hơn",
            YELLOW,
            width=3.15,
            height=0.80,
            font_size=21,
        )

        benefit_group = VGroup(smaller_box, memory_box, faster_box)
        benefit_group.arrange(RIGHT, buff=0.45)
        benefit_group.move_to(UP * 0.08)

        benefit_arrow_1 = Arrow(
            smaller_box.get_right(),
            memory_box.get_left(),
            color=MUTED,
            stroke_width=2.4,
            buff=0.08,
        )
        benefit_arrow_2 = Arrow(
            memory_box.get_right(),
            faster_box.get_left(),
            color=MUTED,
            stroke_width=2.4,
            buff=0.08,
        )

        pause_to(at(0.468))
        play_timed(
            Write(benefit_title),
            FadeIn(smaller_box, shift=UP),
            FadeIn(memory_box, shift=UP),
            FadeIn(faster_box, shift=UP),
            Create(benefit_arrow_1),
            Create(benefit_arrow_2),
            run_time=0.32,
        )

        pause_to(at(0.545))
        clear_group(
            [
                benefit_title,
                benefit_group,
                benefit_arrow_1,
                benefit_arrow_2,
            ],
            run_time=0.14,
        )

        # =====================================================
        # 5) TRADE-OFF
        # Voice: Nhưng đây cũng là cách dễ làm giảm chất lượng nhất.
        # =====================================================
        trade_title = section_title(
            "Trade-off: dễ giảm chất lượng",
            color=RED,
        )

        fast_box = model_box(
            "Chạy nhanh hơn",
            GREEN,
            width=3.05,
            height=0.88,
            font_size=22,
        )
        quality_drop_box = model_box(
            "Chất lượng\ncó thể giảm",
            RED,
            width=3.05,
            height=0.88,
            font_size=22,
        )

        fast_box.move_to(LEFT * 2.35 + UP * 0.10)
        quality_drop_box.move_to(RIGHT * 2.35 + UP * 0.10)

        trade_arrow = DoubleArrow(
            fast_box.get_right(),
            quality_drop_box.get_left(),
            color=MUTED,
            stroke_width=2.4,
            buff=0.10,
        )

        pause_to(at(0.553))
        play_timed(
            Write(trade_title),
            FadeIn(fast_box, shift=UP),
            FadeIn(quality_drop_box, shift=UP),
            Create(trade_arrow),
            run_time=0.28,
        )

        pause_to(at(0.592))
        clear_group(
            [trade_title, fast_box, quality_drop_box, trade_arrow],
            run_time=0.14,
        )

        # =====================================================
        # 6) LÝ DO
        # Voice: Lý do là layer, hidden size, attention head và FFN size...
        # =====================================================
        reason_title = section_title(
            "Vì sao chất lượng có thể giảm?",
            color=YELLOW,
        )

        capability = model_box(
            "Năng lực biểu diễn\ncủa mô hình",
            YELLOW,
            width=3.40,
            height=0.95,
            font_size=22,
        )
        capability.move_to(DOWN * 0.02)

        r_layers = small_card("Layers", BLUE, width=1.85, height=0.58, font_size=19)
        r_hidden = small_card("Hidden size", GREEN, width=2.15, height=0.58, font_size=19)
        r_heads = small_card("Attention heads", PURPLE, width=2.45, height=0.58, font_size=18)
        r_ffn = small_card("FFN size", RED, width=1.85, height=0.58, font_size=19)

        r_layers.move_to(LEFT * 4.0 + UP * 0.88)
        r_hidden.move_to(RIGHT * 4.0 + UP * 0.88)
        r_heads.move_to(LEFT * 4.0 + DOWN * 0.88)
        r_ffn.move_to(RIGHT * 4.0 + DOWN * 0.88)

        reason_cards = VGroup(r_layers, r_hidden, r_heads, r_ffn)

        reason_arrows = VGroup(
            Arrow(r_layers.get_right(), capability.get_left(), color=MUTED, buff=0.10),
            Arrow(r_hidden.get_left(), capability.get_right(), color=MUTED, buff=0.10),
            Arrow(r_heads.get_right(), capability.get_left(), color=MUTED, buff=0.10),
            Arrow(r_ffn.get_left(), capability.get_right(), color=MUTED, buff=0.10),
        )

        pause_to(at(0.600))
        play_timed(
            Write(reason_title),
            FadeIn(capability, scale=0.96),
            FadeIn(reason_cards, shift=UP),
            Create(reason_arrows),
            run_time=0.34,
        )

        pause_to(at(0.675))
        clear_group(
            [
                reason_title,
                capability,
                reason_cards,
                reason_arrows,
            ],
            run_time=0.14,
        )

        # =====================================================
        # 7) GIẢM QUÁ MẠNH
        # Voice: Nếu giảm quá mạnh...
        # =====================================================
        over_title = section_title(
            "Giảm quá mạnh -> rủi ro",
            color=RED,
        )

        normal_model = model_box(
            "Model đủ lớn",
            BLUE,
            width=3.0,
            height=0.82,
            font_size=22,
        )
        tiny_model = model_box(
            "Model quá nhỏ",
            RED,
            width=2.45,
            height=0.72,
            font_size=21,
        )

        normal_model.move_to(LEFT * 2.65 + UP * 0.35)
        tiny_model.move_to(RIGHT * 2.65 + UP * 0.35)

        reduce_arrow = Arrow(
            normal_model.get_right(),
            tiny_model.get_left(),
            color=RED,
            stroke_width=4,
            buff=0.20,
        )

        context_box = model_box(
            "Khó hiểu\nngữ cảnh phức tạp",
            RED,
            width=3.20,
            height=0.90,
            font_size=20,
        )
        reasoning_box = model_box(
            "Suy luận kém hơn",
            RED,
            width=3.20,
            height=0.72,
            font_size=21,
        )

        risk_group = VGroup(context_box, reasoning_box)
        risk_group.arrange(RIGHT, buff=0.45)
        risk_group.move_to(DOWN * 0.95)

        pause_to(at(0.684))
        play_timed(
            Write(over_title),
            FadeIn(normal_model, shift=RIGHT),
            Create(reduce_arrow),
            FadeIn(tiny_model, shift=LEFT),
            FadeIn(risk_group, shift=UP),
            run_time=0.34,
        )

        pause_to(at(0.748))
        clear_group(
            [
                over_title,
                normal_model,
                tiny_model,
                reduce_arrow,
                risk_group,
            ],
            run_time=0.14,
        )

        # =====================================================
        # 8) TÓM TẮT + FINE-TUNING / DISTILLATION
        # Voice: Vì vậy Configuration Downsizing là...
        # =====================================================
        final_title = section_title(
            "Tóm tắt Configuration Downsizing",
            color=YELLOW,
        )

        shrink_box = model_box(
            "Giảm kích thước\nmodel",
            GREEN,
            width=2.85,
            height=0.86,
            font_size=20,
        )

        fast_summary = model_box(
            "Chạy nhanh hơn",
            GREEN,
            width=2.55,
            height=0.76,
            font_size=21,
        )

        risk_summary = model_box(
            "Rủi ro giảm\nnăng lực model",
            RED,
            width=2.95,
            height=0.86,
            font_size=20,
        )

        summary_row = VGroup(shrink_box, fast_summary, risk_summary)
        summary_row.arrange(RIGHT, buff=0.35)
        summary_row.move_to(UP * 0.55)

        summary_arrow_1 = Arrow(
            shrink_box.get_right(),
            fast_summary.get_left(),
            color=MUTED,
            stroke_width=2.2,
            buff=0.08,
        )
        summary_arrow_2 = Arrow(
            fast_summary.get_right(),
            risk_summary.get_left(),
            color=MUTED,
            stroke_width=2.2,
            buff=0.08,
        )

        ft_box = model_box(
            "Fine-tuning",
            BLUE,
            width=2.55,
            height=0.68,
            font_size=21,
        )
        distill_box = model_box(
            "Distillation",
            PURPLE,
            width=2.55,
            height=0.68,
            font_size=21,
        )

        support_group = VGroup(ft_box, distill_box)
        support_group.arrange(RIGHT, buff=0.55)
        support_group.move_to(DOWN * 0.82)

        support_note = safe_text(
            "Kết hợp fine-tuning hoặc distillation để giữ chất lượng tốt hơn",
            font_size=20,
            color=YELLOW,
            max_width=11,
        )
        support_note.move_to(DOWN * 2.35)

        pause_to(at(0.756))
        play_timed(
            Write(final_title),
            FadeIn(shrink_box, shift=UP),
            Create(summary_arrow_1),
            FadeIn(fast_summary, shift=UP),
            Create(summary_arrow_2),
            FadeIn(risk_summary, shift=UP),
            run_time=0.34,
        )

        pause_to(at(0.875))
        play_timed(
            FadeIn(support_group, shift=UP),
            FadeIn(support_note, shift=UP),
            run_time=0.30,
        )

        wait_audio(self, audio, visual_time)

        play_timed(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(final_title),
            FadeOut(summary_row),
            FadeOut(summary_arrow_1),
            FadeOut(summary_arrow_2),
            FadeOut(support_group),
            FadeOut(support_note),
            run_time=0.45,
        )