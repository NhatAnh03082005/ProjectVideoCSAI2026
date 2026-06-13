# -*- coding: utf-8 -*-

from manim import *
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.visual_utils import *


class SceneP3ArchitectureIntro(Scene):
    def construct(self):
        self.camera.background_color = BG

        ROOT = Path(__file__).resolve().parents[1]
        audio_rel = "voice/p3_02_01_arch_intro.mp3"
        audio_path = ROOT / "voice" / "p3_02_01_arch_intro.mp3"

        play_audio(self, audio_rel)
        visual_time = 0

        # =====================================================
        # HELPERS
        # =====================================================
        def get_audio_duration(path, fallback=52.0):
            try:
                from mutagen.mp3 import MP3
                return float(MP3(str(path)).info.length)
            except Exception:
                return fallback

        audio_len = get_audio_duration(audio_path, fallback=52.0)

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

        def clear(*mobjects, run_time=0.28):
            if not mobjects:
                return
            play_timed(*[FadeOut(mob) for mob in mobjects], run_time=run_time)

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

        def block_box(text, color, width=3.6, height=0.72, font_size=21):
            return model_box(
                text,
                color,
                width=width,
                height=height,
                font_size=font_size,
            )

        # =====================================================
        # HEADER
        # Voice:
        # Nhóm thứ hai là Architecture Design...
        # =====================================================
        title = safe_text(
            "Architecture Design",
            font_size=40,
            color=WHITE,
            max_width=11,
        )
        title.to_edge(UP, buff=0.38)

        subtitle = safe_text(
            "Tối ưu thiết kế kiến trúc mô hình",
            font_size=25,
            color=BLUE,
            max_width=11,
        )
        subtitle.next_to(title, DOWN, buff=0.20)

        intro_box = model_box(
            "Architecture Design\n= tối ưu cấu trúc bên trong model",
            YELLOW,
            width=5.55,
            height=1.05,
            font_size=23,
        )
        intro_box.move_to(UP * 0.30)

        intro_note = bottom_note(
            "Không chỉ đổi cách sinh token, mà tối ưu bản thân kiến trúc model",
            color=YELLOW,
        )

        play_timed(Write(title), run_time=0.60)

        pause_to(at(0.04))

        play_timed(FadeIn(subtitle, shift=UP), run_time=0.38)

        pause_to(at(0.08))

        play_timed(FadeIn(intro_box, scale=0.96), run_time=0.45)

        pause_to(at(0.14))

        play_timed(FadeIn(intro_note, shift=UP), run_time=0.35)

        pause_to(at(0.20))

        clear(intro_box, intro_note, run_time=0.25)

        # =====================================================
        # CẢNH 1 - SO SÁNH DECODING VÀ ARCHITECTURE
        # Voice:
        # Nếu Decoding Algorithms tập trung vào cách model sinh token,
        # thì Architecture Design tập trung vào cấu trúc bên trong model.
        # =====================================================
        compare_title = section_title(
            "Decoding vs Architecture",
            color=WHITE,
        )

        decoding_box = model_box(
            "Decoding Algorithms\ncách model sinh token",
            GREEN,
            width=3.75,
            height=1.05,
            font_size=21,
        )

        architecture_box = model_box(
            "Architecture Design\ncấu trúc bên trong model",
            YELLOW,
            width=3.95,
            height=1.05,
            font_size=21,
        )

        decoding_box.move_to(LEFT * 2.55 + UP * 0.25)
        architecture_box.move_to(RIGHT * 2.55 + UP * 0.25)

        decoding_note = safe_text(
            "Tối ưu quá trình chạy từng bước",
            font_size=20,
            color=GREEN,
            max_width=4.0,
        )
        decoding_note.next_to(decoding_box, DOWN, buff=0.28)

        architecture_note = safe_text(
            "Tối ưu hình dạng bên trong model",
            font_size=20,
            color=YELLOW,
            max_width=4.0,
        )
        architecture_note.next_to(architecture_box, DOWN, buff=0.28)

        focus_rect = SurroundingRectangle(
            architecture_box,
            color=YELLOW,
            buff=0.10,
            corner_radius=0.14,
            stroke_width=3,
        )

        pause_to(at(0.22))

        play_timed(Write(compare_title), run_time=0.40)

        pause_to(at(0.27))

        play_timed(
            FadeIn(decoding_box, shift=UP),
            FadeIn(decoding_note, shift=UP),
            run_time=0.45,
        )

        pause_to(at(0.34))

        play_timed(
            FadeIn(architecture_box, shift=UP),
            FadeIn(architecture_note, shift=UP),
            run_time=0.45,
        )

        pause_to(at(0.40))

        play_timed(Create(focus_rect), run_time=0.35)

        pause_to(at(0.46))

        clear(
            compare_title,
            decoding_box,
            architecture_box,
            decoding_note,
            architecture_note,
            focus_rect,
            run_time=0.25,
        )

        # =====================================================
        # CẢNH 2 - TRANSFORMER DECODER BLOCK
        # Voice:
        # Phần lớn LLM hiện nay vẫn dựa trên Transformer decoder.
        # =====================================================
        block_title = section_title(
            "Transformer decoder block đơn giản",
            color=WHITE,
        )

        input_box = block_box(
            "Input token\nrepresentations",
            MUTED,
            width=3.55,
            height=0.72,
            font_size=18,
        )

        attn_box = block_box(
            "Self-Attention",
            BLUE,
            width=3.55,
            height=0.72,
            font_size=22,
        )

        ffn_box = block_box(
            "Feed-Forward Network\nFFN",
            PURPLE,
            width=3.55,
            height=0.82,
            font_size=20,
        )

        output_box = block_box(
            "Output\nrepresentations",
            MUTED,
            width=3.55,
            height=0.72,
            font_size=18,
        )

        block = VGroup(input_box, attn_box, ffn_box, output_box)
        block.arrange(DOWN, buff=0.18)
        block.move_to(LEFT * 2.75 + DOWN * 0.10)

        arrow1 = Arrow(input_box.get_bottom(), attn_box.get_top(), color=MUTED, buff=0.05)
        arrow2 = Arrow(attn_box.get_bottom(), ffn_box.get_top(), color=MUTED, buff=0.05)
        arrow3 = Arrow(ffn_box.get_bottom(), output_box.get_top(), color=MUTED, buff=0.05)
        block_arrows = VGroup(arrow1, arrow2, arrow3)

        transformer_note = model_box(
            "Phần lớn LLM hiện nay\nvẫn dựa trên Transformer decoder",
            BLUE,
            width=4.25,
            height=1.05,
            font_size=21,
        )
        transformer_note.move_to(RIGHT * 2.55 + UP * 0.55)

        pause_to(at(0.47))

        play_timed(Write(block_title), run_time=0.40)

        pause_to(at(0.52))

        play_timed(
            FadeIn(block, shift=UP),
            LaggedStart(
                Create(arrow1),
                Create(arrow2),
                Create(arrow3),
                lag_ratio=0.15,
            ),
            run_time=0.80,
        )

        pause_to(at(0.58))

        play_timed(FadeIn(transformer_note, shift=LEFT), run_time=0.45)

        # =====================================================
        # CẢNH 3 - ATTENTION VÀ FFN LÀ HAI THÀNH PHẦN QUAN TRỌNG
        # Voice:
        # Trong Transformer, hai thành phần rất quan trọng là attention và FFN.
        # =====================================================
        key_title = safe_text(
            "Hai thành phần quan trọng",
            font_size=26,
            color=YELLOW,
            max_width=5.0,
        )
        key_title.move_to(RIGHT * 2.55 + UP * 1.35)

        attn_tag = model_box(
            "Attention",
            BLUE,
            width=2.75,
            height=0.65,
            font_size=23,
        )
        ffn_tag = model_box(
            "FFN",
            PURPLE,
            width=2.75,
            height=0.65,
            font_size=23,
        )

        attn_tag.move_to(RIGHT * 2.55 + UP * 0.40)
        ffn_tag.move_to(RIGHT * 2.55 + DOWN * 0.45)

        attn_highlight = SurroundingRectangle(
            attn_box,
            color=BLUE,
            buff=0.08,
            corner_radius=0.12,
            stroke_width=3,
        )

        ffn_highlight = SurroundingRectangle(
            ffn_box,
            color=PURPLE,
            buff=0.08,
            corner_radius=0.12,
            stroke_width=3,
        )

        pause_to(at(0.63))

        play_timed(
            FadeOut(transformer_note),
            FadeIn(key_title, shift=UP),
            Create(attn_highlight),
            FadeIn(attn_tag, shift=LEFT),
            run_time=0.45,
        )

        pause_to(at(0.69))

        play_timed(
            Create(ffn_highlight),
            FadeIn(ffn_tag, shift=LEFT),
            run_time=0.45,
        )

        # =====================================================
        # CẢNH 4 - ATTENTION
        # Voice:
        # Attention giúp mô hình hiểu quan hệ giữa các token.
        # Nhưng khi chuỗi dài, attention tốn bộ nhớ và tính toán.
        # =====================================================
        token_row = VGroup(
            token_box("t1", color=BLUE, width=0.62, height=0.42, font_size=16),
            token_box("t2", color=BLUE, width=0.62, height=0.42, font_size=16),
            token_box("t3", color=BLUE, width=0.62, height=0.42, font_size=16),
            token_box("t4", color=BLUE, width=0.62, height=0.42, font_size=16),
            token_box("t5", color=BLUE, width=0.62, height=0.42, font_size=16),
        )
        token_row.arrange(RIGHT, buff=0.12)
        token_row.move_to(RIGHT * 2.55 + UP * 0.10)

        relation_lines = VGroup()
        for i in range(len(token_row)):
            for j in range(i):
                relation_lines.add(
                    Line(
                        token_row[i].get_top(),
                        token_row[j].get_top(),
                        color=BLUE,
                        stroke_width=1.4,
                    ).set_opacity(0.60)
                )

        attention_note = bottom_note(
            "Attention hiểu quan hệ giữa các token",
            color=BLUE,
        )

        attention_cost = bottom_note(
            "Chuỗi càng dài -> attention càng tốn memory và compute",
            color=RED,
        )

        long_context_warning = model_box(
            "Long sequence\nmemory + compute tăng",
            RED,
            width=3.35,
            height=0.88,
            font_size=21,
        )
        long_context_warning.move_to(RIGHT * 2.55 + DOWN * 1.05)

        pause_to(at(0.72))

        play_timed(
            FadeOut(key_title),
            FadeOut(attn_tag),
            FadeOut(ffn_tag),
            FadeIn(token_row, shift=UP),
            Create(relation_lines),
            FadeIn(attention_note, shift=UP),
            run_time=0.65,
        )

        pause_to(at(0.80))

        play_timed(
            FadeOut(attention_note),
            FadeIn(long_context_warning, shift=UP),
            FadeIn(attention_cost, shift=UP),
            run_time=0.45,
        )

        # =====================================================
        # CẢNH 5 - FFN
        # Voice:
        # FFN chứa rất nhiều tham số và đóng góp lớn vào chi phí inference.
        # =====================================================
        param_dots = VGroup()
        for row in range(4):
            for col in range(8):
                dot = Dot(
                    radius=0.035,
                    color=PURPLE,
                )
                dot.move_to(RIGHT * 1.55 + RIGHT * col * 0.18 + DOWN * row * 0.18)
                param_dots.add(dot)

        param_box = model_box(
            "FFN\nnhiều tham số",
            PURPLE,
            width=2.75,
            height=0.82,
            font_size=22,
        )
        param_box.move_to(RIGHT * 2.55 + UP * 0.65)

        ffn_cost = bottom_note(
            "FFN đóng góp lớn vào chi phí inference",
            color=PURPLE,
        )

        pause_to(at(0.84))

        play_timed(
            FadeOut(token_row),
            FadeOut(relation_lines),
            FadeOut(long_context_warning),
            FadeOut(attention_cost),
            FadeOut(attn_highlight),
            Create(ffn_highlight.copy()),
            FadeIn(param_box, shift=UP),
            LaggedStart(
                *[FadeIn(dot, scale=0.7) for dot in param_dots],
                lag_ratio=0.01,
            ),
            FadeIn(ffn_cost, shift=UP),
            run_time=0.75,
        )

        # =====================================================
        # CẢNH 6 - KẾT LUẬN
        # Voice:
        # Architecture Design làm model hiệu quả hơn ngay từ kiến trúc,
        # nhưng vẫn giữ năng lực biểu diễn tốt.
        # =====================================================
        final_box = model_box(
            "Mục tiêu Architecture Design",
            YELLOW,
            width=4.30,
            height=0.70,
            font_size=24,
        )
        final_box.move_to(UP * 0.80)

        efficiency = model_box(
            "Hiệu quả hơn\nngay từ kiến trúc",
            GREEN,
            width=3.10,
            height=0.95,
            font_size=21,
        )

        quality = model_box(
            "Giữ năng lực\nbiểu diễn tốt",
            BLUE,
            width=3.10,
            height=0.95,
            font_size=21,
        )

        final_pair = VGroup(efficiency, quality)
        final_pair.arrange(RIGHT, buff=0.55)
        final_pair.move_to(DOWN * 0.25)

        final_note = bottom_note(
            "Tối ưu cấu trúc model để giảm chi phí, nhưng không làm mất quá nhiều chất lượng",
            color=YELLOW,
        )

        pause_to(at(0.91))

        clear(
            block_title,
            block,
            block_arrows,
            ffn_highlight,
            param_box,
            param_dots,
            ffn_cost,
            run_time=0.25,
        )

        play_timed(
            FadeIn(final_box, shift=UP),
            run_time=0.35,
        )

        pause_to(at(0.94))

        play_timed(
            FadeIn(efficiency, shift=UP),
            FadeIn(quality, shift=UP),
            run_time=0.45,
        )

        pause_to(at(0.97))

        play_timed(FadeIn(final_note, shift=UP), run_time=0.35)

        wait_audio(self, audio_rel, visual_time)

        play_timed(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(final_box),
            FadeOut(final_pair),
            FadeOut(final_note),
            run_time=0.55,
        )