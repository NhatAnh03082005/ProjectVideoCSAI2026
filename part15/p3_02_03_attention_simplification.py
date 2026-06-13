# -*- coding: utf-8 -*-

from manim import *
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.visual_utils import *


class SceneP3AttentionSimplification(Scene):
    def construct(self):
        self.camera.background_color = BG

        ROOT = Path(__file__).resolve().parents[1]
        audio = "voice/p3_02_03_attention_simplification.mp3"
        audio_path = ROOT / "voice" / "p3_02_03_attention_simplification.mp3"

        play_audio(self, audio)
        visual_time = 0.0

        # =====================================================
        # HELPERS
        # =====================================================
        def get_audio_duration(path, fallback=95.0):
            try:
                from mutagen.mp3 import MP3
                return float(MP3(str(path)).info.length)
            except Exception:
                return fallback

        audio_len = get_audio_duration(audio_path, fallback=95.0)

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

        def play_timed(*animations, run_time=0.30, **kwargs):
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

        def bottom_note(text, color=YELLOW, font_size=20, max_width=11.0):
            note = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=max_width,
            )
            note.move_to(DOWN * 2.35)
            return note

        def method_note(text, color=YELLOW, font_size=20, max_width=11.0):
            note = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=max_width,
            )
            note.move_to(DOWN * 1.65)
            return note

        def small_box(text, color, width=2.6, height=0.72, font_size=20):
            return model_box(
                text,
                color,
                width=width,
                height=height,
                font_size=font_size,
            )

        def make_token_row(count=8, color=BLUE, y=0.0):
            tokens = VGroup()
            for i in range(1, count + 1):
                tok = token_box(
                    f"t{i}",
                    color=color,
                    width=0.66,
                    height=0.44,
                    font_size=16,
                )
                tokens.add(tok)
            tokens.arrange(RIGHT, buff=0.14)
            tokens.move_to(UP * y)
            return tokens

        def selected_attention_lines(tokens, focus_idx=5, color=BLUE):
            lines = VGroup()
            for j in [0, 2, 4]:
                start = tokens[focus_idx].get_top() + UP * 0.08
                end = tokens[j].get_top() + UP * 0.08
                arc = ArcBetweenPoints(
                    start,
                    end,
                    angle=PI / 3,
                    color=color,
                    stroke_width=2.0,
                )
                arc.set_opacity(0.85)
                lines.add(arc)
            return lines

        def full_attention_lines(tokens, color=BLUE):
            lines = VGroup()
            for i in range(1, len(tokens)):
                for j in range(i):
                    start = tokens[i].get_top() + UP * 0.06
                    end = tokens[j].get_top() + UP * 0.06
                    arc = ArcBetweenPoints(
                        start,
                        end,
                        angle=PI / 4,
                        color=color,
                        stroke_width=1.15,
                    )
                    arc.set_opacity(0.42)
                    lines.add(arc)
            return lines

        def local_attention_lines(tokens, color=GREEN):
            lines = VGroup()
            focus = 4
            for j in [3, 5]:
                start = tokens[focus].get_top() + UP * 0.06
                end = tokens[j].get_top() + UP * 0.06
                arc = ArcBetweenPoints(
                    start,
                    end,
                    angle=PI / 2.2,
                    color=color,
                    stroke_width=2.4,
                )
                arc.set_opacity(0.95)
                lines.add(arc)
            return lines

        def sliding_window_lines(tokens, window=2, color=BLUE):
            lines = VGroup()
            focus = 5
            for j in range(focus - window, focus + 1):
                if j == focus:
                    continue
                start = tokens[focus].get_top() + UP * 0.06
                end = tokens[j].get_top() + UP * 0.06
                arc = ArcBetweenPoints(
                    start,
                    end,
                    angle=PI / 2.4,
                    color=color,
                    stroke_width=2.2,
                )
                arc.set_opacity(0.90)
                lines.add(arc)
            return lines

        def sparse_lines(tokens, color=PURPLE):
            pairs = [
                (7, 0),
                (6, 3),
                (5, 1),
                (4, 2),
            ]
            lines = VGroup()
            for i, j in pairs:
                start = tokens[i].get_top() + UP * 0.06
                end = tokens[j].get_top() + UP * 0.06
                arc = ArcBetweenPoints(
                    start,
                    end,
                    angle=PI / 3.2,
                    color=color,
                    stroke_width=2.0,
                )
                arc.set_opacity(0.86)
                lines.add(arc)
            return lines

        # =====================================================
        # 1) HEADER
        # =====================================================
        title = safe_text(
            "Attention Simplification",
            font_size=39,
            color=WHITE,
            max_width=11,
        )
        title.to_edge(UP, buff=0.36)

        subtitle = safe_text(
            "Làm cơ chế attention nhẹ hơn",
            font_size=24,
            color=BLUE,
            max_width=11,
        )
        subtitle.next_to(title, DOWN, buff=0.18)

        play_timed(Write(title), run_time=0.42)

        pause_to(at(0.020))
        play_timed(FadeIn(subtitle, shift=UP), run_time=0.24)

        # =====================================================
        # 2) SELF-ATTENTION
        # =====================================================
        attn_title = section_title(
            "Self-attention: token nhìn các token khác",
            color=WHITE,
        )

        tokens_intro = make_token_row(count=8, color=BLUE, y=0.15)

        focus_rect = SurroundingRectangle(
            tokens_intro[5],
            color=YELLOW,
            buff=0.07,
            corner_radius=0.08,
            stroke_width=3,
        )

        look_lines = selected_attention_lines(tokens_intro, focus_idx=5, color=BLUE)

        pause_to(at(0.040))
        play_timed(
            Write(attn_title),
            FadeIn(tokens_intro, shift=UP),
            run_time=0.32,
        )

        pause_to(at(0.075))
        play_timed(
            Create(focus_rect),
            Create(look_lines),
            run_time=0.34,
        )

        pause_to(at(0.150))
        clear_group(
            [attn_title, tokens_intro, focus_rect, look_lines],
            run_time=0.14,
        )

        # =====================================================
        # 3) FULL ATTENTION COST
        # =====================================================
        full_title = section_title(
            "Full attention: nhiều quan hệ giữa token",
            color=YELLOW,
        )

        tokens_full = make_token_row(count=8, color=BLUE, y=0.10)
        full_lines = full_attention_lines(tokens_full, color=BLUE)

        cost_box = model_box(
            "Chi phí tăng nhanh\nO(n^2)",
            RED,
            width=3.25,
            height=0.90,
            font_size=22,
        )
        cost_box.move_to(LEFT * 2.15 + DOWN * 1.20)

        four_x_box = model_box(
            "Chuỗi dài 2x\nquan hệ ~4x",
            RED,
            width=3.25,
            height=0.92,
            font_size=21,
        )
        four_x_box.move_to(RIGHT * 2.15 + DOWN * 1.20)

        pause_to(at(0.158))
        play_timed(
            Write(full_title),
            FadeIn(tokens_full, shift=UP),
            run_time=0.30,
        )

        pause_to(at(0.190))
        play_timed(
            Create(full_lines),
            FadeIn(cost_box, shift=UP),
            run_time=0.38,
        )

        pause_to(at(0.245))
        play_timed(
            FadeIn(four_x_box, shift=UP),
            run_time=0.26,
        )

        pause_to(at(0.302))
        clear_group(
            [full_title, tokens_full, full_lines, cost_box, four_x_box],
            run_time=0.14,
        )

        # =====================================================
        # 4) LONG CONTEXT BOTTLENECK
        # =====================================================
        bottleneck_title = section_title(
            "Long context -> attention bottleneck",
            color=RED,
        )

        short_prompt = small_box(
            "Prompt ngắn\nít token",
            GREEN,
            width=2.65,
            height=0.90,
            font_size=21,
        )
        long_context = small_box(
            "Long context\nvài chục nghìn token",
            RED,
            width=3.55,
            height=0.95,
            font_size=21,
        )

        short_prompt.move_to(LEFT * 2.75 + UP * 0.20)
        long_context.move_to(RIGHT * 2.65 + UP * 0.20)

        bottleneck_arrow = Arrow(
            short_prompt.get_right(),
            long_context.get_left(),
            color=RED,
            stroke_width=4,
            buff=0.20,
        )

        bottleneck_label = model_box(
            "Attention\nrất nặng",
            RED,
            width=2.55,
            height=0.85,
            font_size=21,
        )
        bottleneck_label.move_to(DOWN * 1.10)

        pause_to(at(0.310))
        play_timed(
            Write(bottleneck_title),
            FadeIn(short_prompt, shift=UP),
            run_time=0.26,
        )

        pause_to(at(0.336))
        play_timed(
            Create(bottleneck_arrow),
            FadeIn(long_context, shift=LEFT),
            FadeIn(bottleneck_label, shift=UP),
            run_time=0.32,
        )

        pause_to(at(0.378))
        clear_group(
            [bottleneck_title, short_prompt, long_context, bottleneck_arrow, bottleneck_label],
            run_time=0.14,
        )

        # =====================================================
        # 5) PREFILL AND DECODE PHASE
        # =====================================================
        phase_title = section_title(
            "LLM serving: prefill và decode",
            color=WHITE,
        )

        prefill_box = model_box(
            "Prefill phase\nxử lý toàn bộ prompt",
            BLUE,
            width=3.45,
            height=0.95,
            font_size=21,
        )
        decode_box = model_box(
            "Decode phase\nsinh từng token mới",
            GREEN,
            width=3.45,
            height=0.95,
            font_size=21,
        )

        prefill_box.move_to(LEFT * 2.65 + UP * 0.55)
        decode_box.move_to(RIGHT * 2.65 + UP * 0.55)

        matrix = VGroup()
        for r in range(5):
            for c in range(5):
                sq = Square(side_length=0.16, color=BLUE, stroke_width=1.4)
                sq.set_fill(BLUE, opacity=0.15 if c <= r else 0.04)
                sq.move_to(LEFT * 2.65 + DOWN * 0.60 + RIGHT * c * 0.18 + DOWN * r * 0.18)
                matrix.add(sq)

        matrix_label = safe_text(
            "ma trận quan hệ lớn",
            font_size=18,
            color=BLUE,
            max_width=3.0,
        )
        matrix_label.next_to(matrix, DOWN, buff=0.18)

        kv_cache = VGroup()
        for i in range(6):
            cell = Rectangle(width=0.42, height=0.34, color=GREEN, stroke_width=2)
            cell.set_fill(GREEN, opacity=0.13)
            cell.move_to(RIGHT * 1.65 + DOWN * 0.55 + RIGHT * i * 0.48)
            kv_cache.add(cell)

        new_token = token_box(
            "new",
            color=YELLOW,
            width=0.72,
            height=0.42,
            font_size=15,
        )
        new_token.move_to(RIGHT * 4.85 + DOWN * 0.55)

        kv_arrow = Arrow(
            new_token.get_left(),
            kv_cache.get_right(),
            color=YELLOW,
            buff=0.08,
            stroke_width=3,
        )

        kv_label = safe_text(
            "đọc KV cache",
            font_size=18,
            color=GREEN,
            max_width=3.0,
        )
        kv_label.next_to(kv_cache, DOWN, buff=0.22)

        phase_note = bottom_note(
            "Context càng dài -> đọc KV cache càng tốn memory bandwidth",
            color=YELLOW,
            font_size=20,
        )

        pause_to(at(0.386))
        play_timed(
            Write(phase_title),
            FadeIn(prefill_box, shift=UP),
            FadeIn(matrix, scale=0.96),
            FadeIn(matrix_label, shift=UP),
            run_time=0.36,
        )

        pause_to(at(0.455))
        play_timed(
            FadeIn(decode_box, shift=UP),
            FadeIn(kv_cache, shift=UP),
            FadeIn(new_token, shift=LEFT),
            Create(kv_arrow),
            FadeIn(kv_label, shift=UP),
            run_time=0.38,
        )

        pause_to(at(0.520))
        play_timed(
            FadeIn(phase_note, shift=UP),
            run_time=0.23,
        )

        pause_to(at(0.575))
        clear_group(
            [
                phase_title,
                prefill_box,
                decode_box,
                matrix,
                matrix_label,
                kv_cache,
                new_token,
                kv_arrow,
                kv_label,
                phase_note,
            ],
            run_time=0.14,
        )

        # =====================================================
        # 6) COMMON IDEA
        # =====================================================
        idea_title = section_title(
            "Ý tưởng chung",
            color=YELLOW,
        )

        all_box = model_box(
            "Không cần nhìn\ntất cả token",
            YELLOW,
            width=3.20,
            height=0.92,
            font_size=22,
        )
        important_box = model_box(
            "Chỉ giữ phần\nngữ cảnh quan trọng",
            GREEN,
            width=3.45,
            height=0.92,
            font_size=21,
        )

        all_box.move_to(LEFT * 2.35 + UP * 0.15)
        important_box.move_to(RIGHT * 2.35 + UP * 0.15)

        idea_arrow = Arrow(
            all_box.get_right(),
            important_box.get_left(),
            color=GREEN,
            stroke_width=4,
            buff=0.18,
        )

        pause_to(at(0.586))
        play_timed(
            Write(idea_title),
            FadeIn(all_box, shift=UP),
            Create(idea_arrow),
            FadeIn(important_box, shift=LEFT),
            run_time=0.32,
        )

        pause_to(at(0.648))
        clear_group(
            [idea_title, all_box, important_box, idea_arrow],
            run_time=0.14,
        )

        # =====================================================
        # 7) LOCAL ATTENTION
        # =====================================================
        local_title = section_title(
            "Local attention",
            color=GREEN,
        )

        local_tokens = make_token_row(count=8, color=GREEN, y=0.08)
        local_lines = local_attention_lines(local_tokens, color=GREEN)

        local_focus = SurroundingRectangle(
            VGroup(local_tokens[3], local_tokens[4], local_tokens[5]),
            color=YELLOW,
            buff=0.10,
            corner_radius=0.08,
            stroke_width=3,
        )

        local_note = method_note(
            "Token chỉ nhìn các token gần nó",
            color=GREEN,
            font_size=20,
        )

        pause_to(at(0.656))
        play_timed(
            Write(local_title),
            FadeIn(local_tokens, shift=UP),
            Create(local_lines),
            Create(local_focus),
            FadeIn(local_note, shift=UP),
            run_time=0.34,
        )

        pause_to(at(0.700))
        clear_group(
            [local_title, local_tokens, local_lines, local_focus, local_note],
            run_time=0.14,
        )

        # =====================================================
        # 8) SLIDING WINDOW ATTENTION
        # =====================================================
        window_title = section_title(
            "Sliding window attention",
            color=BLUE,
        )

        window_tokens = make_token_row(count=8, color=BLUE, y=0.08)
        window_lines = sliding_window_lines(window_tokens, window=2, color=BLUE)

        window_rect = SurroundingRectangle(
            VGroup(window_tokens[3], window_tokens[4], window_tokens[5]),
            color=YELLOW,
            buff=0.10,
            corner_radius=0.08,
            stroke_width=3,
        )

        window_note = method_note(
            "Token chỉ nhìn một cửa sổ ngữ cảnh gần nhất",
            color=BLUE,
            font_size=20,
        )

        pause_to(at(0.710))
        play_timed(
            Write(window_title),
            FadeIn(window_tokens, shift=UP),
            Create(window_rect),
            Create(window_lines),
            FadeIn(window_note, shift=UP),
            run_time=0.34,
        )

        pause_to(at(0.748))
        clear_group(
            [window_title, window_tokens, window_lines, window_rect, window_note],
            run_time=0.14,
        )

        # =====================================================
        # 9) SPARSE ATTENTION
        # =====================================================
        sparse_title = section_title(
            "Sparse attention",
            color=PURPLE,
        )

        sparse_tokens = make_token_row(count=8, color=PURPLE, y=0.08)
        sparse_lines_group = sparse_lines(sparse_tokens, color=PURPLE)

        sparse_note = method_note(
            "Chỉ giữ một số kết nối quan trọng",
            color=PURPLE,
            font_size=20,
        )

        pause_to(at(0.758))
        play_timed(
            Write(sparse_title),
            FadeIn(sparse_tokens, shift=UP),
            Create(sparse_lines_group),
            FadeIn(sparse_note, shift=UP),
            run_time=0.34,
        )

        pause_to(at(0.795))
        clear_group(
            [sparse_title, sparse_tokens, sparse_lines_group, sparse_note],
            run_time=0.14,
        )

        # =====================================================
        # 10) CONTEXT COMPRESSION
        # =====================================================
        compress_title = section_title(
            "Context compression",
            color=YELLOW,
        )

        comp_tokens = make_token_row(count=8, color=BLUE, y=0.65)

        summary_1 = token_box("S1", color=YELLOW, width=0.72, height=0.48, font_size=17)
        summary_2 = token_box("S2", color=YELLOW, width=0.72, height=0.48, font_size=17)
        summary_3 = token_box("S3", color=YELLOW, width=0.72, height=0.48, font_size=17)

        summaries = VGroup(summary_1, summary_2, summary_3)
        summaries.arrange(RIGHT, buff=0.52)
        summaries.move_to(DOWN * 0.25)

        comp_arrows = VGroup(
            Arrow(
                VGroup(comp_tokens[0], comp_tokens[1], comp_tokens[2]).get_bottom(),
                summary_1.get_top(),
                color=YELLOW,
                buff=0.10,
                stroke_width=3,
            ),
            Arrow(
                VGroup(comp_tokens[3], comp_tokens[4], comp_tokens[5]).get_bottom(),
                summary_2.get_top(),
                color=YELLOW,
                buff=0.10,
                stroke_width=3,
            ),
            Arrow(
                VGroup(comp_tokens[6], comp_tokens[7]).get_bottom(),
                summary_3.get_top(),
                color=YELLOW,
                buff=0.10,
                stroke_width=3,
            ),
        )

        comp_note = method_note(
            "Nén hoặc rút gọn ngữ cảnh để giảm số token cần xử lý",
            color=YELLOW,
            font_size=20,
        )

        pause_to(at(0.803))
        play_timed(
            Write(compress_title),
            FadeIn(comp_tokens, shift=UP),
            Create(comp_arrows),
            FadeIn(summaries, shift=UP),
            FadeIn(comp_note, shift=UP),
            run_time=0.34,
        )

        # Chuyển sang mục tiêu sớm hơn để không bị voice đi trước.
        pause_to(at(0.835))
        clear_group(
            [compress_title, comp_tokens, comp_arrows, summaries, comp_note],
            run_time=0.14,
        )

        # =====================================================
        # 11) GOAL
        # =====================================================
        goal_title = section_title(
            "Mục tiêu",
            color=GREEN,
        )

        compute_box = small_box(
            "Giảm\ncomputation",
            GREEN,
            width=2.55,
            height=0.90,
            font_size=21,
        )
        memory_box = small_box(
            "Giảm\nmemory",
            BLUE,
            width=2.45,
            height=0.90,
            font_size=21,
        )
        long_box = small_box(
            "Hỗ trợ\nlong context",
            YELLOW,
            width=2.65,
            height=0.90,
            font_size=21,
        )

        goal_group = VGroup(compute_box, memory_box, long_box)
        goal_group.arrange(RIGHT, buff=0.50)
        goal_group.move_to(UP * 0.05)

        pause_to(at(0.842))
        play_timed(
            Write(goal_title),
            FadeIn(compute_box, shift=UP),
            FadeIn(memory_box, shift=UP),
            FadeIn(long_box, shift=UP),
            run_time=0.32,
        )

        pause_to(at(0.878))
        clear_group(
            [goal_title, goal_group],
            run_time=0.14,
        )

        # =====================================================
        # 12) TRADE-OFF
        # =====================================================
        trade_title = section_title(
            "Trade-off",
            color=RED,
            font_size=28,
        )

        remove_box = model_box(
            "Bỏ bớt ngữ cảnh\nkhông khéo",
            RED,
            width=3.30,
            height=0.92,
            font_size=21,
        )
        lose_box = model_box(
            "Mất thông tin\nquan trọng",
            YELLOW,
            width=3.20,
            height=0.92,
            font_size=21,
        )

        remove_box.move_to(LEFT * 2.40 + UP * 0.10)
        lose_box.move_to(RIGHT * 2.40 + UP * 0.10)

        trade_arrow = Arrow(
            remove_box.get_right(),
            lose_box.get_left(),
            color=RED,
            stroke_width=4,
            buff=0.18,
        )

        pause_to(at(0.886))
        play_timed(
            Write(trade_title),
            FadeIn(remove_box, shift=UP),
            Create(trade_arrow),
            FadeIn(lose_box, shift=LEFT),
            run_time=0.34,
        )

        pause_to(at(0.925))
        clear_group(
            [trade_title, remove_box, lose_box, trade_arrow],
            run_time=0.14,
        )

        # =====================================================
        # 13) FINAL TAKEAWAY
        # =====================================================
        final_title = section_title(
            "Attention simplification",
            color=YELLOW,
        )

        cut_box = model_box(
            "Cắt bớt attention",
            RED,
            width=3.10,
            height=0.75,
            font_size=21,
        )
        keep_box = model_box(
            "Giữ ngữ cảnh\nquan trọng nhất",
            GREEN,
            width=3.35,
            height=0.90,
            font_size=21,
        )

        cut_box.move_to(LEFT * 2.45 + UP * 0.05)
        keep_box.move_to(RIGHT * 2.45 + UP * 0.05)

        final_arrow = Arrow(
            cut_box.get_right(),
            keep_box.get_left(),
            color=YELLOW,
            stroke_width=4,
            buff=0.15,
        )

        final_note = bottom_note(
            "Giảm chi phí nhưng vẫn giữ phần ngữ cảnh quan trọng nhất",
            color=YELLOW,
            font_size=20,
        )

        pause_to(at(0.932))
        play_timed(
            Write(final_title),
            FadeIn(cut_box, shift=UP),
            Create(final_arrow),
            FadeIn(keep_box, shift=LEFT),
            FadeIn(final_note, shift=UP),
            run_time=0.40,
        )

        wait_audio(self, audio, visual_time)

        play_timed(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(final_title),
            FadeOut(cut_box),
            FadeOut(keep_box),
            FadeOut(final_arrow),
            FadeOut(final_note),
            run_time=0.45,
        )