import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part404PipelineSummary(Scene):
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

        # Timestamps tracking
        curr_time = 0

        def wait_until(target_time):
            nonlocal curr_time
            wait_duration = target_time - curr_time
            if wait_duration > 0.05:
                self.wait(wait_duration)
                curr_time = target_time

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

        audio = "voice_part4/p4_04.mp3"
        play_audio(audio)

        # ==========================================
        # PHASE 1: TITLE & PIPELINE NODES (0.0s - 13.50s)
        # ==========================================
        title = make_title("LLM Serving Pipeline")
        subtitle = make_subtitle("User Prompt → Tokenizer → Engine → GPU → Output Stream", title)

        self.play(Write(title), run_time=1.1)
        curr_time += 1.1
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Pipeline nodes spec
        node_specs = [
            ("User\nPrompt", BLUE),
            ("Tokenize\nprompt", YELLOW),
            ("LLM\nEngine", PURPLE),
            ("GPU\nCompute", GREEN),
            ("Output\nStream", BLUE),
        ]

        nodes = VGroup()
        for label, color in node_specs:
            box = RoundedRectangle(
                width=1.9,
                height=1.1,
                corner_radius=0.16,
                stroke_color=color,
                fill_color=color,
                fill_opacity=FILL_SOFT
            )
            lines = label.split('\n')
            t1 = T(lines[0], size=14, color=color, weight=BOLD)
            t2 = T(lines[1], size=14, color=color, weight=BOLD)
            text_vg = VGroup(t1, t2).arrange(DOWN, buff=0.06).move_to(box)
            nodes.add(VGroup(box, text_vg))

        nodes.arrange(RIGHT, buff=0.36).shift(UP * 0.75)

        # Baseline align first and second line of nodes labels
        first_lines = []
        second_lines = []
        for n in nodes:
            label_vg = n[1]
            first_lines.append(label_vg[0])
            second_lines.append(label_vg[1])

        align_texts_to_baseline(first_lines[0], *first_lines[1:])
        align_texts_to_baseline(second_lines[0], *second_lines[1:])

        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrows.add(Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.08, color=WHITE, stroke_width=2.2))

        wait_until(3.2)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in nodes], lag_ratio=0.18), run_time=1.8)
        curr_time += 1.8
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.18), run_time=1.0)
        curr_time += 1.0

        # ==========================================
        # PHASE 2: REQUEST FLOW ANIMATION (13.50s - 31.00s)
        # ==========================================
        # Request dot moves through pipeline
        dot = Dot(radius=0.11, color=RED).move_to(nodes[0].get_center())
        dot_label = T("request", size=14, color=RED, weight=BOLD).next_to(nodes[0], UP, buff=0.18)

        wait_until(4.50)
        self.play(FadeIn(dot), FadeIn(dot_label), run_time=0.6)
        curr_time += 0.6

        # Move to Tokenizer
        wait_until(9.00)
        self.play(
            dot.animate.move_to(nodes[1].get_center()),
            dot_label.animate.next_to(nodes[1], UP, buff=0.18),
            run_time=0.8
        )
        curr_time += 0.8

        # Move to Engine
        wait_until(13.50)
        self.play(
            dot.animate.move_to(nodes[2].get_center()),
            dot_label.animate.next_to(nodes[2], UP, buff=0.18),
            run_time=0.8
        )
        curr_time += 0.8

        # Move to GPU
        wait_until(17.50)
        self.play(
            dot.animate.move_to(nodes[3].get_center()),
            dot_label.animate.next_to(nodes[3], UP, buff=0.18),
            run_time=0.8
        )
        curr_time += 0.8

        # Move to Output Stream & Trigger token stream display
        wait_until(22.00)
        self.play(
            dot.animate.move_to(nodes[4].get_center()),
            dot_label.animate.next_to(nodes[4], UP, buff=0.18),
            run_time=0.8
        )
        curr_time += 0.8

        # Token stream output
        tokens = ["This", "is", "LLM", "Serving", "..."]
        token_group = VGroup()
        for tok in tokens:
            token = T(tok, size=22, color=GREEN, weight=BOLD)
            token_group.add(token)

        token_group.arrange(RIGHT, buff=0.25).shift(DOWN * 1.8)

        # Baseline align token stream items
        align_texts_to_baseline(token_group[0], *token_group[1:])

        stream_label = T("stream output token-by-token", size=18, color=GREEN).next_to(token_group, UP, buff=0.22)

        self.play(FadeIn(stream_label, shift=UP), run_time=0.8)
        curr_time += 0.8
        self.play(
            LaggedStart(*[FadeIn(tok, shift=UP * 0.15) for tok in token_group], lag_ratio=0.25),
            run_time=2.0
        )
        curr_time += 2.0

        # ==========================================
        # PHASE 3: SUMMARY CARD (31.00s - 58.85s)
        # ==========================================
        wait_until(31.00)
        # Fade out pipeline and stream elements to avoid overlap
        self.play(
            FadeOut(nodes),
            FadeOut(arrows),
            FadeOut(dot),
            FadeOut(dot_label),
            FadeOut(token_group),
            FadeOut(stream_label),
            FadeOut(subtitle),
            run_time=1.5
        )
        curr_time += 1.5

        # Centered Summary Card
        summary_box = RoundedRectangle(
            width=9.0,
            height=2.0,
            corner_radius=0.18,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).move_to(ORIGIN)

        # Serving Components (to show during "Còn sơ ving bao gồm...")
        serving_title = T("SERVING INCLUDES:", size=18, color=YELLOW, weight=BOLD)
        serving_title.move_to(summary_box.get_top() + DOWN * 0.35)

        serving_labels = ["Tokenization", "Scheduling", "Memory Mgmt", "Streaming", "Latency Control"]
        serving_colors = [BLUE, YELLOW, PURPLE, GREEN, RED]
        serving_items = VGroup()
        for text, color in zip(serving_labels, serving_colors):
            box = RoundedRectangle(
                width=1.45,
                height=0.65,
                corner_radius=0.1,
                stroke_color=color,
                fill_color=color,
                fill_opacity=FILL_SOFT
            )
            lbl = T(text, size=10, color=color, weight=BOLD)
            item = VGroup(box, lbl).move_to(ORIGIN)
            serving_items.add(item)
        serving_items.arrange(RIGHT, buff=0.16).move_to(summary_box.get_center() + DOWN * 0.15)

        # Roles summary (to show after serving components fade out)
        summary_title = T("LLM SYSTEM ROLES:", size=19, color=YELLOW, weight=BOLD)
        summary_t1 = T("• Training: Creates the model", size=17, color=WHITE)
        summary_t2 = T("• Inference: Uses the model", size=17, color=WHITE)
        summary_t3 = T("• Serving: Turns inference into a service", size=17, color=WHITE)

        summary_content = VGroup(summary_title, summary_t1, summary_t2, summary_t3).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if summary_content.width > 8.0:
            summary_content.scale_to_fit_width(8.0)
        summary_content.move_to(summary_box)

        # 33.50s - 42.60s: Show Serving components
        wait_until(33.50)
        self.play(
            FadeIn(summary_box),
            FadeIn(serving_title),
            run_time=1.2
        )
        curr_time += 1.2

        # Show Tokenization at 35.20s
        wait_until(35.20)
        self.play(FadeIn(serving_items[0], shift=UP * 0.15), run_time=0.6)
        curr_time += 0.6

        # Show Scheduling at 36.50s
        wait_until(36.50)
        self.play(FadeIn(serving_items[1], shift=UP * 0.15), run_time=0.6)
        curr_time += 0.6

        # Show Memory Management at 37.80s
        wait_until(37.80)
        self.play(FadeIn(serving_items[2], shift=UP * 0.15), run_time=0.6)
        curr_time += 0.6

        # Show Streaming at 39.50s
        wait_until(39.50)
        self.play(FadeIn(serving_items[3], shift=UP * 0.15), run_time=0.6)
        curr_time += 0.6

        # Show Latency Control at 41.00s
        wait_until(41.00)
        self.play(FadeIn(serving_items[4], shift=UP * 0.15), run_time=0.6)
        curr_time += 0.6

        # Fade out all serving components at 42.60s
        wait_until(42.60)
        self.play(
            FadeOut(serving_title),
            FadeOut(serving_items),
            run_time=0.8
        )
        curr_time += 0.8

        # 45.51s - 53.28s: Show Roles Card sequentially
        # Show Title & Training bullet point at 45.51s
        wait_until(45.51)
        self.play(
            FadeIn(summary_title),
            FadeIn(summary_t1, shift=RIGHT * 0.2),
            run_time=0.8
        )
        curr_time += 0.8

        # Show Inference bullet point at 47.50s
        wait_until(47.50)
        self.play(FadeIn(summary_t2, shift=RIGHT * 0.2), run_time=0.8)
        curr_time += 0.8

        # Show Serving bullet point at 49.30s
        wait_until(49.30)
        self.play(FadeIn(summary_t3, shift=RIGHT * 0.2), run_time=0.8)
        curr_time += 0.8

        # Wait until audio finishes
        wait_audio(audio, visual_time=curr_time)
        curr_time = audio_duration(audio)

        # Visual pause at the end (2.5 seconds)
        self.wait(2.5)
        curr_time += 2.5

        # Fade out everything at the very end
        self.play(
            FadeOut(title),
            FadeOut(summary_box),
            FadeOut(summary_content),
            run_time=1.2
        )
        curr_time += 1.2