import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part504LatencyThroughput(Scene):
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

        audio = "voice_part5/p5_04.mp3"
        play_audio(audio)

        # 0.00s - 8.50s: Title & Subtitle + Intro Card
        title = T(
            "Why is LLM inference hard to speed up?",
            size=38,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "Sequential decoding creates latency and throughput bottlenecks",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        intro_box = RoundedRectangle(
            width=8.8,
            height=1.4,
            corner_radius=0.18,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color="#1a1c23",
            fill_opacity=0.9
        ).shift(UP * 0.2)
        intro_text = T("Sequential Decoding: Token-by-Token", size=24, color=YELLOW, weight=BOLD).move_to(intro_box)
        intro_group = VGroup(intro_box, intro_text)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8
        self.play(FadeIn(intro_group, shift=UP * 0.15), run_time=1.0)
        curr_time += 1.0

        # 8.50s - 15.00s: Single Request Timeline
        timeline_title = T(
            "Single Request: 1 Answer = 100+ Sequential Steps",
            size=25,
            color=YELLOW,
            weight=BOLD
        ).shift(UP * 1.6)

        steps = VGroup()
        labels = ["t1", "t2", "t3", "t4", "t5", "...", "t98", "t99", "t100"]
        for lbl in labels:
            if lbl == "...":
                box = RoundedRectangle(
                    width=0.6,
                    height=0.75,
                    corner_radius=0.14,
                    stroke_color=MUTED,
                    stroke_width=1.5,
                    fill_color="#1a1c23",
                    fill_opacity=0.9
                )
                text = T("...", size=20, color=MUTED, weight=BOLD).move_to(box)
                steps.add(VGroup(box, text))
            else:
                box = RoundedRectangle(
                    width=0.9,
                    height=0.75,
                    corner_radius=0.14,
                    stroke_color=GREEN,
                    stroke_width=2,
                    fill_color=GREEN,
                    fill_opacity=FILL_SOFT
                )
                text = T(lbl, size=19, color=GREEN, weight=BOLD).move_to(box)
                steps.add(VGroup(box, text))
        steps.arrange(RIGHT, buff=0.22).shift(UP * 0.7)

        arrows = VGroup()
        for i in range(len(steps) - 1):
            arrows.add(Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.04, color=YELLOW, stroke_width=2.5))

        wait_until(8.50)
        self.play(
            FadeOut(intro_group),
            FadeIn(timeline_title),
            FadeIn(steps[0], shift=UP * 0.1),
            run_time=1.0
        )
        curr_time += 1.0

        for i in range(1, 9):
            self.play(
                GrowArrow(arrows[i - 1]),
                FadeIn(steps[i], shift=UP * 0.1),
                run_time=0.4
            )
            curr_time += 0.4

        # 15.00s - 22.50s: Display operations within each step
        inner_steps_box = RoundedRectangle(
            width=11.8,
            height=1.2,
            corner_radius=0.18,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color="#1a1c23",
            fill_opacity=0.9
        ).shift(DOWN * 0.5)

        inner_title = T("Operations within each decode step:", size=16, color=YELLOW).next_to(inner_steps_box.get_top(), DOWN, buff=0.12)

        op1 = T("Read Context", size=15, color=WHITE, weight=BOLD)
        op2 = T("Attention", size=15, color=WHITE, weight=BOLD)
        op3 = T("KV Cache", size=15, color=WHITE, weight=BOLD)
        op4 = T("Logits", size=15, color=WHITE, weight=BOLD)
        op5 = T("Next Token", size=15, color=GREEN, weight=BOLD)

        arr1 = T(" ──> ", size=14, color=YELLOW)
        arr2 = T(" ──> ", size=14, color=YELLOW)
        arr3 = T(" ──> ", size=14, color=YELLOW)
        arr4 = T(" ──> ", size=14, color=YELLOW)

        op_group = VGroup(op1, arr1, op2, arr2, op3, arr3, op4, arr4, op5).arrange(RIGHT, buff=0.08)
        op_group.next_to(inner_title, DOWN, buff=0.15)
        align_texts_to_baseline(op1, op2, op3, op4, op5)

        inner_steps_group = VGroup(inner_steps_box, inner_title, op_group)

        wait_until(15.00)
        self.play(
            FadeIn(inner_steps_box),
            FadeIn(inner_title),
            FadeIn(op1, shift=UP * 0.1),
            run_time=0.8
        )
        curr_time += 0.8

        wait_until(16.60)
        self.play(
            Write(arr1),
            FadeIn(op2, shift=UP * 0.1),
            run_time=0.6
        )
        curr_time += 0.6

        wait_until(18.20)
        self.play(
            Write(arr2),
            FadeIn(op3, shift=UP * 0.1),
            run_time=0.6
        )
        curr_time += 0.6

        wait_until(19.80)
        self.play(
            Write(arr3),
            FadeIn(op4, shift=UP * 0.1),
            run_time=0.6
        )
        curr_time += 0.6

        wait_until(21.40)
        self.play(
            Write(arr4),
            FadeIn(op5, shift=UP * 0.1),
            run_time=0.6
        )
        curr_time += 0.6

        # 22.50s - 33.50s: Highlight user latency
        latency_box = RoundedRectangle(
            width=11.8,
            height=1.2,
            corner_radius=0.18,
            stroke_color=RED,
            stroke_width=2.5,
            fill_color="#1a0c0c",
            fill_opacity=0.9
        ).shift(DOWN * 0.7)

        latency_text1 = T("User Latency Bottleneck: High Time-per-Token", size=18, color=RED, weight=BOLD)
        latency_text2 = T("User must wait for each token to be sequentially generated and streamed.", size=16, color=WHITE)

        latency_text_group = VGroup(latency_text1, latency_text2).arrange(DOWN, buff=0.12).move_to(latency_box)
        latency_group = VGroup(latency_box, latency_text_group)

        wait_until(22.50)
        self.play(
            FadeOut(inner_steps_group),
            FadeIn(latency_group, shift=UP * 0.15),
            run_time=1.0
        )
        curr_time += 1.0

        # 33.50s - 43.50s: Transition to Multi-User Serving
        multi_title = T(
            "Multi-User Serving: Multiple Parallel Decode Streams",
            size=25,
            color=YELLOW,
            weight=BOLD
        ).shift(UP * 1.6)

        gpu_box = RoundedRectangle(
            width=2.8,
            height=1.6,
            corner_radius=0.18,
            stroke_color=GREEN,
            stroke_width=2.5,
            fill_color="#102018",
            fill_opacity=0.95
        ).shift(RIGHT * 3.8 + UP * 0.1)
        gpu_text = T("GPU ENGINE", size=22, color=GREEN, weight=BOLD).move_to(gpu_box)
        gpu_group = VGroup(gpu_box, gpu_text)

        userA_label = T("User A (Long)", size=16, color=BLUE, weight=BOLD).move_to(LEFT * 4.8 + UP * 1.0)
        userB_label = T("User B (Short)", size=16, color=BLUE, weight=BOLD).move_to(LEFT * 4.8 + UP * 0.1)
        userC_label = T("User C (Medium)", size=16, color=BLUE, weight=BOLD).move_to(LEFT * 4.8 + DOWN * 0.8)

        def make_queue(num_tokens, start_pos, color=BLUE):
            queue = VGroup()
            for j in range(num_tokens):
                box = RoundedRectangle(
                    width=0.45,
                    height=0.4,
                    corner_radius=0.08,
                    stroke_color=color,
                    stroke_width=1.5,
                    fill_color=color,
                    fill_opacity=FILL_SOFT
                )
                label = T("t", size=13, color=color, weight=BOLD).move_to(box)
                queue.add(VGroup(box, label))
            queue.arrange(RIGHT, buff=0.08).next_to(start_pos, RIGHT, buff=0.25)
            return queue

        queueA = make_queue(6, userA_label, BLUE)
        queueB = make_queue(3, userB_label, BLUE)
        queueC = make_queue(4, userC_label, BLUE)

        lineA = Line(queueA.get_right(), gpu_box.get_left(), color=BLUE, stroke_width=1.5)
        lineB = Line(queueB.get_right(), gpu_box.get_left(), color=BLUE, stroke_width=1.5)
        lineC = Line(queueC.get_right(), gpu_box.get_left(), color=BLUE, stroke_width=1.5)
        lines = VGroup(lineA, lineB, lineC)

        wait_until(33.50)
        self.play(
            FadeOut(timeline_title),
            FadeOut(steps),
            FadeOut(arrows),
            FadeOut(latency_group),
            FadeIn(multi_title),
            FadeIn(gpu_group),
            FadeIn(userA_label),
            FadeIn(userB_label),
            FadeIn(userC_label),
            run_time=1.2
        )
        curr_time += 1.2

        wait_until(35.00)
        self.play(
            LaggedStart(
                FadeIn(queueA, shift=RIGHT * 0.2),
                FadeIn(queueB, shift=RIGHT * 0.2),
                FadeIn(queueC, shift=RIGHT * 0.2),
                lag_ratio=0.2
            ),
            LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1),
            run_time=1.5
        )
        curr_time += 1.5

        # 43.50s - 49.50s: Animate Queue Completion (User B finishes, User A grows)
        finished_label = T("✓ Done (GPU Released)", size=14, color=GREEN, weight=BOLD).next_to(userB_label, RIGHT, buff=0.4)

        extra1 = VGroup(
            RoundedRectangle(width=0.45, height=0.4, corner_radius=0.08, stroke_color=RED, stroke_width=1.5, fill_color=RED, fill_opacity=FILL_SOFT),
            T("t7", size=13, color=RED, weight=BOLD)
        )
        extra1[1].move_to(extra1[0])

        extra2 = VGroup(
            RoundedRectangle(width=0.45, height=0.4, corner_radius=0.08, stroke_color=RED, stroke_width=1.5, fill_color=RED, fill_opacity=FILL_SOFT),
            T("t8", size=13, color=RED, weight=BOLD)
        )
        extra2[1].move_to(extra2[0])

        extra_group = VGroup(extra1, extra2).arrange(RIGHT, buff=0.08).next_to(queueA, RIGHT, buff=0.08)
        new_lineA = Line(extra_group.get_right(), gpu_box.get_left(), color=BLUE, stroke_width=1.5)

        wait_until(43.50)
        self.play(
            Flash(queueB, color=GREEN, run_time=0.8),
            FadeOut(queueB, run_time=0.8),
            FadeOut(lineB, run_time=0.8),
            FadeIn(finished_label, shift=RIGHT * 0.1, run_time=1.0),
            FadeIn(extra_group, shift=RIGHT * 0.1, run_time=1.0),
            ReplacementTransform(lineA, new_lineA, run_time=1.0)
        )
        curr_time += 1.0

        # 49.50s - 58.50s: Optimization solutions
        s1 = RoundedRectangle(width=2.5, height=1.2, corner_radius=0.12, stroke_color=BLUE, fill_color="#1e293b", fill_opacity=0.9)
        s1_text = T("Continuous\nBatching", size=13, color=BLUE, weight=BOLD).move_to(s1)
        card1 = VGroup(s1, s1_text)

        s2 = RoundedRectangle(width=2.5, height=1.2, corner_radius=0.12, stroke_color=YELLOW, fill_color="#1e293b", fill_opacity=0.9)
        s2_text = T("Request\nScheduling", size=13, color=YELLOW, weight=BOLD).move_to(s2)
        card2 = VGroup(s2, s2_text)

        s3 = RoundedRectangle(width=2.5, height=1.2, corner_radius=0.12, stroke_color=PURPLE, fill_color="#1e293b", fill_opacity=0.9)
        s3_text = T("KV Cache\nManagement", size=13, color=PURPLE, weight=BOLD).move_to(s3)
        card3 = VGroup(s3, s3_text)

        s4 = RoundedRectangle(width=2.5, height=1.2, corner_radius=0.12, stroke_color=GREEN, fill_color="#1e293b", fill_opacity=0.9)
        s4_text = T("Kernel\nOptimization", size=13, color=GREEN, weight=BOLD).move_to(s4)
        card4 = VGroup(s4, s4_text)

        solutions = VGroup(card1, card2, card3, card4).arrange(RIGHT, buff=0.35).shift(DOWN * 2.0)

        wait_until(48.80)
        self.play(FadeIn(card1, shift=UP * 0.1), run_time=0.7)
        curr_time += 0.7

        wait_until(50.50)
        self.play(FadeIn(card2, shift=UP * 0.1), run_time=0.7)
        curr_time += 0.7

        wait_until(52.20)
        self.play(FadeIn(card3, shift=UP * 0.1), run_time=0.7)
        curr_time += 0.7

        wait_until(54.00)
        self.play(FadeIn(card4, shift=UP * 0.1), run_time=0.7)
        curr_time += 0.7

        # 58.50s - 64.80s: Summary & Conclusion
        conclusion_box = RoundedRectangle(
            width=11.8,
            height=1.2,
            corner_radius=0.18,
            stroke_color=RED,
            stroke_width=2.5,
            fill_color="#1a0c0c",
            fill_opacity=0.9
        ).shift(DOWN * 0.2)

        conclusion_text1 = T("Core Challenge: Sequential Dependency", size=20, color=RED, weight=BOLD)
        conclusion_text2 = T("Autoregressive generation cannot be parallelized, making Latency vs. Throughput key.", size=16, color=WHITE)

        conclusion_text_group = VGroup(conclusion_text1, conclusion_text2).arrange(DOWN, buff=0.12).move_to(conclusion_box)
        conclusion_group = VGroup(conclusion_box, conclusion_text_group)

        wait_until(58.50)
        self.play(
            FadeOut(multi_title),
            FadeOut(userA_label),
            FadeOut(userB_label),
            FadeOut(userC_label),
            FadeOut(queueA),
            FadeOut(extra_group),
            FadeOut(finished_label),
            FadeOut(queueC),
            FadeOut(new_lineA),
            FadeOut(lineC),
            FadeOut(gpu_group),
            FadeOut(solutions),
            FadeIn(conclusion_group, shift=UP * 0.15),
            run_time=1.2
        )
        curr_time += 1.2

        # Wait until audio finishes
        wait_audio(audio, visual_time=curr_time)
        curr_time = audio_duration(audio)

        # 2.5 seconds visual pause at the end
        self.wait(2.5)
        curr_time += 2.5

        # Fade out everything
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(multi_title),
            FadeOut(conclusion_group),
            run_time=1.2
        )
        curr_time += 1.2