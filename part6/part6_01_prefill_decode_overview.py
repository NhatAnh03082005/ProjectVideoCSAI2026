import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part601PrefillDecodeOverview(Scene):
    def construct(self):
        self.camera.background_color = BG

        def play_audio(path):
            resolved = resolve_audio_path(path)
            if os.path.exists(resolved):
                self.add_sound(resolved)
            else:
                print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path} (đã phân giải thành {resolved})")

        def wait_audio(path, visual_time):
            duration = audio_duration(path)
            remaining = duration - visual_time
            if remaining > 0.05:
                self.wait(remaining)

        def get_first_character(obj):
            while isinstance(obj, VGroup) and not isinstance(obj, Text) and len(obj) > 0:
                obj = obj[0]
            if isinstance(obj, Text) and len(obj) > 0:
                if hasattr(obj, "text") and obj.text:
                    for idx, char in enumerate(obj.text):
                        if char not in ['"', "'", "“", "”", "‘", "’", "(", "[", "{", "•", " "]:
                            if idx < len(obj):
                                return obj[idx]
                return obj[0]
            return obj

        def align_texts_to_baseline(ref_obj, *other_objs):
            ref_char = get_first_character(ref_obj)
            ref_y = ref_char.get_bottom()[1]
            for obj in other_objs:
                char_to_align = get_first_character(obj)
                dy = ref_y - char_to_align.get_bottom()[1]
                obj.shift(UP * dy)

        # Timestamps tracking
        curr_time = 0

        def wait_until(target_time):
            nonlocal curr_time
            wait_duration = target_time - curr_time
            if wait_duration > 0.05:
                self.wait(wait_duration)
                curr_time = target_time

        audio = "voice_part6/p6_01.mp3"
        play_audio(audio)

        # Title & Subtitle (0.00s)
        title = T(
            "Prefill vs Decode",
            size=42,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "An LLM request consists of two primary inference phases",
            size=23,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # 0.00s - 7.70s: Show faded phase boxes to prevent empty screen
        prefill_box = RoundedRectangle(
            width=5.5,
            height=2.3,
            corner_radius=0.22,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_color="#0a1424",
            fill_opacity=0.92
        ).shift(LEFT * 3.35 + UP * 0.8)

        decode_box = RoundedRectangle(
            width=5.5,
            height=2.3,
            corner_radius=0.22,
            stroke_color=GREEN,
            stroke_width=2.5,
            fill_color="#102018",
            fill_opacity=0.92
        ).shift(RIGHT * 3.35 + UP * 0.8)

        prefill_title = T(
            "Prefill / Context Phase",
            size=25,
            color=BLUE,
            weight=BOLD
        ).move_to(prefill_box.get_top() + DOWN * 0.35)

        decode_title = T(
            "Decode / Generation Phase",
            size=25,
            color=GREEN,
            weight=BOLD
        ).move_to(decode_box.get_top() + DOWN * 0.35)

        align_texts_to_baseline(prefill_title, decode_title)

        arrow = Arrow(
            prefill_box.get_right(),
            decode_box.get_left(),
            buff=0.25,
            color=YELLOW,
            stroke_width=3
        )

        arrow_label = T(
            "then",
            size=22,
            color=YELLOW,
            weight=BOLD
        ).next_to(arrow, UP, buff=0.12)

        # Initial faded state
        prefill_box.save_state()
        prefill_box.set_stroke(opacity=0.25)
        prefill_box.set_fill(opacity=0.01)

        decode_box.save_state()
        decode_box.set_stroke(opacity=0.25)
        decode_box.set_fill(opacity=0.01)

        arrow.save_state()
        arrow.set_stroke(opacity=0.25)

        self.play(
            FadeIn(prefill_box),
            FadeIn(decode_box),
            FadeIn(arrow),
            run_time=1.5
        )
        curr_time += 1.5

        # 7.70s - 11.00s: Highlight both boxes and show titles & arrow label
        wait_until(7.70)
        self.play(
            prefill_box.animate.restore(),
            decode_box.animate.restore(),
            arrow.animate.restore(),
            FadeIn(prefill_title),
            FadeIn(decode_title),
            FadeIn(arrow_label),
            run_time=1.2
        )
        curr_time += 1.2

        # 11.00s - 14.35s: Prefill details (op0)
        op0 = T("• Also called Context Phase", size=20, color=WHITE)
        op1 = T("• Read entire prompt", size=20, color=WHITE)
        op2 = T("• Build context representation", size=20, color=WHITE)
        op3 = T("• Initialize KV Cache", size=20, color=WHITE)

        prefill_items = VGroup(op0, op1, op2, op3).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        prefill_items.move_to(prefill_box.get_center() + DOWN * 0.2)

        wait_until(11.00)
        self.play(
            prefill_box.animate.set_stroke(width=4.5),
            FadeIn(op0, shift=RIGHT * 0.15),
            run_time=1.0
        )
        curr_time += 1.0

        # 14.35s - 18.60s: Read entire prompt
        wait_until(14.35)
        self.play(
            FadeIn(op1, shift=RIGHT * 0.15),
            run_time=1.0
        )
        curr_time += 1.0

        # 18.60s - 27.65s: Prompt token parallel processing illustration
        prompt_tokens = VGroup()
        for i in range(6):
            box = RoundedRectangle(
                width=0.55,
                height=0.45,
                corner_radius=0.1,
                stroke_color=BLUE,
                stroke_width=1.5,
                fill_color=BLUE,
                fill_opacity=FILL_SOFT
            )
            text = T(f"p{i+1}", size=14, color=BLUE, weight=BOLD).move_to(box)
            prompt_tokens.add(VGroup(box, text))
        prompt_tokens.arrange(RIGHT, buff=0.12).next_to(prefill_box, DOWN, buff=0.3)

        wait_until(18.60)
        self.play(
            LaggedStart(*[FadeIn(t, scale=0.5) for t in prompt_tokens], lag_ratio=0.08),
            run_time=1.2
        )
        curr_time += 1.2
        self.play(
            Flash(prompt_tokens, color=BLUE, flash_radius=0.8),
            run_time=1.0
        )
        curr_time += 1.0

        # 27.65s - 33.75s: Build representation & KV Cache init
        wait_until(27.65)
        self.play(
            FadeIn(op2, shift=RIGHT * 0.15),
            FadeIn(op3, shift=RIGHT * 0.15),
            run_time=1.2
        )
        curr_time += 1.2

        # 35.40s - 40.90s: Transition and highlight decode phase
        dp1 = T("• Generate token-by-token", size=20, color=WHITE)
        dp2 = T("• Append token to context", size=20, color=WHITE)
        dp3 = T("• Repeat until end token", size=20, color=WHITE)

        decode_items = VGroup(dp1, dp2, dp3).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        decode_items.move_to(decode_box.get_center() + DOWN * 0.15)

        wait_until(35.40)
        # 33.75s - 37.80s: Transition to decode phase
        wait_until(33.75)
        self.play(
            prefill_box.animate.set_stroke(width=2.5),
            decode_box.animate.set_stroke(width=4.5),
            Flash(decode_box, color=GREEN, flash_radius=1.8),
            run_time=1.2
        )
        curr_time += 1.2

        # 37.80s - 41.35s: Show decode definition
        wait_until(37.80)
        self.play(
            FadeIn(dp1, shift=RIGHT * 0.15),
            run_time=1.0
        )
        curr_time += 1.0

        # 41.35s - 49.45s: Animate remaining decode items & token-by-token decoding (t1-t6)
        decode_tokens = VGroup()
        for i in range(6):
            box = RoundedRectangle(
                width=0.55,
                height=0.45,
                corner_radius=0.1,
                stroke_color=GREEN,
                stroke_width=1.5,
                fill_color=GREEN,
                fill_opacity=FILL_SOFT
            )
            text = T(f"t{i+1}", size=14, color=GREEN, weight=BOLD).move_to(box)
            decode_tokens.add(VGroup(box, text))
        decode_tokens.arrange(RIGHT, buff=0.12).next_to(decode_box, DOWN, buff=0.3)

        wait_until(41.35)
        self.play(
            FadeIn(dp2, shift=RIGHT * 0.15),
            FadeIn(dp3, shift=RIGHT * 0.15),
            run_time=1.2
        )
        curr_time += 1.2

        for i in range(6):
            self.play(
                FadeIn(decode_tokens[i], scale=0.5),
                Flash(decode_tokens[i], color=GREEN, flash_radius=0.4),
                run_time=0.5
            )
            curr_time += 0.5

        # 49.30s - 55.70s: Analogy Box (lowered to Y = -2.3 to prevent overlap)
        analogy_box = RoundedRectangle(
            width=11.8,
            height=1.2,
            corner_radius=0.18,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color="#1f1608",
            fill_opacity=0.9
        ).shift(DOWN * 2.3)

        analogy_text = T(
            "Analogy: Prefill = Reading the question  |  Decode = Writing the answer word-by-word",
            size=17,
            color=WHITE,
            weight=BOLD
        ).move_to(analogy_box)

        wait_until(49.45)
        self.play(
            decode_box.animate.set_stroke(width=2.5),
            FadeIn(analogy_box, shift=UP * 0.15),
            Write(analogy_text),
            run_time=1.2
        )
        curr_time += 1.2

        # 55.80s - 58.00s: Fade out analogy & tokens to prevent overlap
        wait_until(55.80)
        self.play(
            FadeOut(analogy_box),
            FadeOut(analogy_text),
            FadeOut(prompt_tokens),
            FadeOut(decode_tokens),
            run_time=1.0
        )
        curr_time += 1.0

        # 58.00s - 68.11s: Bottleneck comparison
        divider = Line(start=[0, -1.3, 0], end=[0, -3.1, 0], color=MUTED, stroke_width=1.5)

        b_prefill_title = T("Prefill Bottleneck:", size=24, color=BLUE, weight=BOLD).move_to(LEFT * 3.35 + DOWN * 1.7)
        b_prefill_desc = T("Compute-bound (Parallel processing)\nLimited by GPU ALU speed", size=18, color=WHITE).next_to(b_prefill_title, DOWN, buff=0.25)
        b_prefill_group = VGroup(b_prefill_title, b_prefill_desc)

        b_decode_title = T("Decode Bottleneck:", size=24, color=GREEN, weight=BOLD).move_to(RIGHT * 3.35 + DOWN * 1.7)
        b_decode_desc = T("Memory-bound (Sequential generation)\nLimited by Memory Bandwidth", size=18, color=WHITE).next_to(b_decode_title, DOWN, buff=0.25)
        b_decode_group = VGroup(b_decode_title, b_decode_desc)

        align_texts_to_baseline(b_prefill_title, b_decode_title)

        wait_until(58.00)
        self.play(
            FadeIn(b_prefill_group, shift=UP * 0.15),
            FadeIn(b_decode_group, shift=UP * 0.15),
            Create(divider),
            run_time=1.2
        )
        curr_time += 1.2

        # Wait until audio finishes
        wait_audio(audio, visual_time=curr_time)
        curr_time = audio_duration(audio)

        # 2.5s visual pause at the end
        self.wait(2.5)
        curr_time += 2.5

        # Fade out everything
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(prefill_box),
            FadeOut(decode_box),
            FadeOut(prefill_title),
            FadeOut(decode_title),
            FadeOut(prefill_items),
            FadeOut(decode_items),
            FadeOut(arrow),
            FadeOut(arrow_label),
            FadeOut(divider),
            FadeOut(b_prefill_group),
            FadeOut(b_decode_group),
            run_time=1.2
        )
        curr_time += 1.2