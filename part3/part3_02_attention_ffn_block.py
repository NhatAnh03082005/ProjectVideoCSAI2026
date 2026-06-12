import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part302AttentionFFNBlock(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Helpers for audio playback
        def play_audio(path):
            resolved = resolve_audio_path(path)
            if os.path.exists(resolved):
                self.add_sound(resolved)
            else:
                print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path} (đã phân giải thành {resolved})")

        audio = "voice_part3/p3_02.mp3"
        play_audio(audio)

        # Precise speech timestamps from -5% rate audio file
        t_speech = [
            0.10,   # S1: Intro (0.10s)
            6.56,   # S2: Two components (6.56s)
            9.98,   # S3: Self-attention (9.98s)
            13.29,  # S4: Self-attention role (13.29s)
            20.26,  # S5: Example sentence (20.26s)
            28.89,  # S6: Reading analogy (28.89s)
            33.72,  # S7: Selective reading (33.72s)
            38.30,  # S8: Focus on relevant words (38.30s)
            43.66,  # S9: Feed-Forward (43.66s)
            48.31,  # S10: Feed-Forward role & Pulse (48.31s)
            56.88,  # S11: Intuition recap (Where to look vs What to do) (56.88s)
            65.61,  # S12: Multi-block intro (65.61s)
            70.56,  # S13: Stacking block demo (70.56s)
            76.08,  # S14: Deep context representation (76.08s)
            81.96,  # S15: LLM scaling advantages (81.96s)
            88.97   # End of speech / Transition out (88.97s)
        ]

        self.current_time = 0.0

        def wait_until(target_time):
            diff = target_time - self.current_time
            if diff > 0.01:
                self.wait(diff)
                self.current_time = target_time
            elif diff < -0.05:
                print(f"[WARNING] Animation runtime exceeded target time {target_time}s by {-diff:.3f}s")

        def play_anim(*anims, run_time=1.0, **kwargs):
            self.play(*anims, run_time=run_time, **kwargs)
            self.current_time += run_time

        # ----------------------------------------------------
        # VISUAL HEADER DEFINITIONS
        # ----------------------------------------------------
        title = T("Inside a Transformer Block", size=42, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.35)

        subtitle = T("Self-Attention + Feed-Forward Network", size=22, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.2)

        # ----------------------------------------------------
        # SINGLE BLOCK CONTAINER & COMPONENTS
        # ----------------------------------------------------
        block = RoundedRectangle(
            width=9.6,
            height=3.4,
            corner_radius=0.25,
            stroke_color=BLUE,
            fill_color="#111827",
            fill_opacity=0.96
        ).shift(DOWN * 0.25)

        block_label = T(
            "Transformer Block",
            size=24,
            color=BLUE,
            weight=BOLD
        ).move_to(block.get_top() + DOWN * 0.35)

        attn_box = RoundedRectangle(
            width=3.4,
            height=1.35,
            corner_radius=0.18,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).shift(LEFT * 2.3 + DOWN * 0.15)

        attn_text = T(
            "Self-Attention\nfind relevant tokens",
            size=21,
            color=YELLOW,
            weight=BOLD
        ).move_to(attn_box)

        ffn_box = RoundedRectangle(
            width=3.4,
            height=1.35,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        ).shift(RIGHT * 2.3 + DOWN * 0.15)

        ffn_text = T(
            "Feed-Forward\ntransform features",
            size=21,
            color=GREEN,
            weight=BOLD
        ).move_to(ffn_box)

        arrow = Arrow(attn_box.get_right(), ffn_box.get_left(), buff=0.18, color=WHITE)

        # ----------------------------------------------------
        # ANIMATIONS EXECUTION
        # ----------------------------------------------------

        # --- SEGMENT 1: INTRO (0.10s to 6.56s) ---
        wait_until(t_speech[0])
        play_anim(Write(title), run_time=1.0)
        play_anim(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        play_anim(FadeIn(block), FadeIn(block_label), run_time=1.2)
        wait_until(t_speech[1])

        # --- SEGMENT 2: TWO COMPONENTS (6.56s to 9.98s) ---
        play_anim(Indicate(block, color=BLUE, scale_factor=1.02), run_time=1.0)
        wait_until(t_speech[2])

        # --- SEGMENT 3: SELF-ATTENTION INTRO (9.98s to 13.29s) ---
        play_anim(FadeIn(attn_box, shift=UP * 0.2), FadeIn(attn_text), run_time=1.0)
        wait_until(t_speech[3])

        # --- SEGMENT 4: SELF-ATTENTION ROLE (13.29s to 20.26s) ---
        play_anim(Flash(attn_box, color=YELLOW, flash_radius=1.8), run_time=0.8)
        wait_until(t_speech[4])

        # --- SEGMENT 5: EXAMPLE SENTENCE & ATTENTION LINES (20.26s to 28.89s) ---
        sentence_title = T(
            "Ví dụ: Hà Nội là thủ đô của Việt Nam",
            size=24,
            color=MUTED
        ).to_edge(DOWN, buff=1.2)

        words = ["Hà Nội", "là", "thủ đô", "của", "Việt Nam"]
        word_group = VGroup()
        for w in words:
            word = T(w, size=23, color=WHITE)
            word_group.add(word)
        word_group.arrange(RIGHT, buff=0.35, aligned_edge=DOWN).to_edge(DOWN, buff=0.55)
        # Precise baseline alignment using the bottom of the first character of each word
        ref_y = word_group[0][0].get_bottom()[1]
        for w_obj in word_group:
            dy = ref_y - w_obj[0].get_bottom()[1]
            w_obj.shift(UP * dy)

        play_anim(FadeIn(sentence_title, shift=UP * 0.2), run_time=0.8)
        play_anim(
            LaggedStart(
                *[FadeIn(w, shift=UP * 0.12) for w in word_group],
                lag_ratio=0.15
            ),
            run_time=1.5
        )

        target = word_group[2]
        line1 = Line(word_group[0].get_top(), target.get_top(), color=YELLOW, stroke_width=3).set_opacity(0.8)
        line2 = Line(word_group[4].get_top(), target.get_top(), color=YELLOW, stroke_width=3).set_opacity(0.8)

        play_anim(
            Indicate(target, color=YELLOW, scale_factor=1.15),
            run_time=0.8
        )
        play_anim(Create(line1), Create(line2), run_time=1.0)
        play_anim(
            Indicate(word_group[0], color=YELLOW, scale_factor=1.1),
            Indicate(word_group[4], color=YELLOW, scale_factor=1.1),
            run_time=1.0
        )
        wait_until(t_speech[5])

        # --- SEGMENT 6: READING ANALOGY (28.89s to 33.72s) ---
        new_title = T("Trực quan: Giống như con người đọc tài liệu", size=24, color=YELLOW).to_edge(DOWN, buff=1.2)
        play_anim(
            FadeOut(line1), FadeOut(line2),
            Transform(sentence_title, new_title),
            run_time=1.0
        )
        wait_until(t_speech[6])

        # --- SEGMENT 7: SELECTIVE READING (33.72s to 38.30s) ---
        play_anim(
            word_group[1].animate.set_opacity(0.25),
            word_group[3].animate.set_opacity(0.25),
            run_time=1.0
        )
        wait_until(t_speech[7])

        # --- SEGMENT 8: FOCUS ON RELEVANT WORDS (38.30s to 43.66s) ---
        play_anim(
            Indicate(word_group[0], color=YELLOW, scale_factor=1.1),
            Indicate(word_group[2], color=YELLOW, scale_factor=1.1),
            Indicate(word_group[4], color=YELLOW, scale_factor=1.1),
            run_time=1.2
        )
        wait_until(t_speech[8])

        # --- SEGMENT 9: FEED-FORWARD INTRO (43.66s to 48.31s) ---
        # Clear bottom texts to avoid overlap with subsequent elements
        play_anim(
            FadeOut(sentence_title),
            FadeOut(word_group),
            FadeIn(ffn_box, shift=UP * 0.2),
            FadeIn(ffn_text),
            GrowArrow(arrow),
            run_time=1.2
        )
        wait_until(t_speech[9])

        # --- SEGMENT 10: FEED-FORWARD ROLE & PULSE (48.31s to 56.88s) ---
        pulse = RoundedRectangle(
            width=0.8, height=0.8, corner_radius=0.1,
            stroke_color=YELLOW, stroke_width=2,
            fill_color=YELLOW, fill_opacity=0.4
        ).move_to(attn_box.get_center())

        play_anim(FadeIn(pulse), run_time=0.3)
        play_anim(pulse.animate.move_to(ffn_box.get_center()), run_time=0.8)
        play_anim(FadeOut(pulse), run_time=0.3)
        play_anim(Flash(ffn_box, color=GREEN, flash_radius=1.8), run_time=0.8)
        wait_until(t_speech[10])

        # --- SEGMENT 11: COMPARATIVE INTUITION (56.88s to 65.61s) ---
        attn_note = T("Nên nhìn vào đâu?\n(Lấy thông tin ngữ cảnh)", size=20, color=YELLOW, weight=BOLD)
        attn_note.next_to(attn_box, DOWN, buff=0.4)

        ffn_note = T("Xử lý sâu hơn thế nào?\n(Biến đổi đặc trưng)", size=20, color=GREEN, weight=BOLD)
        ffn_note.next_to(ffn_box, DOWN, buff=0.4)

        play_anim(Write(attn_note), Write(ffn_note), run_time=1.5)
        wait_until(t_speech[11])

        # --- SEGMENT 12: MULTI-BLOCK INTRO (65.61s to 70.56s) ---
        old_components = VGroup(
            block, block_label, attn_box, attn_text, ffn_box, ffn_text,
            arrow, attn_note, ffn_note
        )
        play_anim(FadeOut(old_components), run_time=1.0)
        wait_until(t_speech[12])

        # --- SEGMENT 13: STACKING BLOCK DEMO (70.56s to 76.08s) ---
        stack_group = VGroup()
        block_colors = [BLUE, PURPLE, ORANGE, GREEN, YELLOW]
        block_labels_text = ["Block 1", "Block 2", "Block 3", "...", "Block N"]
        for col, text_lbl in zip(block_colors, block_labels_text):
            slab = RoundedRectangle(
                width=6.0, height=0.48, corner_radius=0.1,
                stroke_color=col, stroke_width=1.5,
                fill_color=col, fill_opacity=FILL_SOFT
            )
            lbl = T(text_lbl, size=18, color=col, weight=BOLD).move_to(slab)
            stack_group.add(VGroup(slab, lbl))
        stack_group.arrange(UP, buff=0.12).shift(DOWN * 0.4)

        play_anim(
            LaggedStart(
                *[FadeIn(slab, shift=UP * 0.2) for slab in stack_group],
                lag_ratio=0.15
            ),
            run_time=2.0
        )
        wait_until(t_speech[13])

        # --- SEGMENT 14: DEEP CONTEXT REPRESENTATION (76.08s to 81.96s) ---
        flow_arrow = Arrow(
            stack_group.get_bottom() + LEFT * 2.2,
            stack_group.get_top() + LEFT * 2.2,
            color=YELLOW,
            buff=0.1
        )
        context_note = T("Biểu diễn ngữ cảnh ngày càng sâu và phức tạp", size=22, color=YELLOW, weight=BOLD)
        context_note.to_edge(DOWN, buff=0.35)

        play_anim(GrowArrow(flow_arrow), run_time=0.8)
        play_anim(FadeIn(context_note, shift=UP * 0.25), run_time=0.8)
        wait_until(t_speech[14])

        # --- SEGMENT 15: LLM SCALING ADVANTAGES (81.96s to 88.97s) ---
        play_anim(
            stack_group.animate.shift(LEFT * 2.8),
            flow_arrow.animate.shift(LEFT * 2.8),
            FadeOut(context_note),
            run_time=1.0
        )

        card1 = RoundedRectangle(width=4.8, height=0.7, corner_radius=0.12, stroke_color=GREEN, fill_color=GREEN, fill_opacity=FILL_SOFT)
        lbl1 = T("1. Hiểu ngữ cảnh dài", size=18, color=GREEN, weight=BOLD).move_to(card1)
        item1 = VGroup(card1, lbl1)

        card2 = RoundedRectangle(width=4.8, height=0.7, corner_radius=0.12, stroke_color=BLUE, fill_color=BLUE, fill_opacity=FILL_SOFT)
        lbl2 = T("2. Khả năng suy luận tốt", size=18, color=BLUE, weight=BOLD).move_to(card2)
        item2 = VGroup(card2, lbl2)

        card3 = RoundedRectangle(width=4.8, height=0.7, corner_radius=0.12, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=FILL_SOFT)
        lbl3 = T("3. Sinh câu trả lời tự nhiên", size=18, color=YELLOW, weight=BOLD).move_to(card3)
        item3 = VGroup(card3, lbl3)

        capabilities = VGroup(item1, item2, item3).arrange(DOWN, buff=0.25).shift(RIGHT * 2.8 + DOWN * 0.4)

        play_anim(
            LaggedStart(
                *[FadeIn(item, shift=LEFT * 0.2) for item in capabilities],
                lag_ratio=0.2
            ),
            run_time=1.8
        )
        wait_until(t_speech[15])

        # --- TRANSITION OUT (88.97s to 90.0s) ---
        play_anim(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(stack_group),
            FadeOut(flow_arrow),
            FadeOut(capabilities),
            run_time=1.0
        )
        self.wait(0.05)
