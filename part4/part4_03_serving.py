import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part403Serving(Scene):
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

        audio = "voice_part4/p4_03.mp3"
        play_audio(audio)

        # ==========================================
        # PHASE 1: TITLE & ANALOGY (0.0s - 13.00s)
        # ==========================================
        title = make_title("Serving")
        subtitle = make_subtitle("Tổ chức inference thành dịch vụ thực tế", title)

        self.play(Write(title), run_time=1.1)
        curr_time += 1.1
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Analogy: teach / ask / system
        train_box = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.16, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=FILL_SOFT)
        infer_box = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.16, stroke_color=GREEN, fill_color=GREEN, fill_opacity=FILL_SOFT)
        serve_box = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.16, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=FILL_SOFT)

        train_title = T("Training", size=19, color=PURPLE, weight=BOLD)
        train_sub = T("teach model", size=16, color=WHITE)
        train_text = VGroup(train_title, train_sub).arrange(DOWN, buff=0.08).move_to(train_box)

        infer_title = T("Inference", size=19, color=GREEN, weight=BOLD)
        infer_sub = T("ask model", size=16, color=WHITE)
        infer_text = VGroup(infer_title, infer_sub).arrange(DOWN, buff=0.08).move_to(infer_box)

        serve_title = T("Serving", size=19, color=YELLOW, weight=BOLD)
        serve_sub = T("many users", size=16, color=WHITE)
        serve_text = VGroup(serve_title, serve_sub).arrange(DOWN, buff=0.08).move_to(serve_box)

        analogy = VGroup(
            VGroup(train_box, train_text),
            VGroup(infer_box, infer_text),
            VGroup(serve_box, serve_text)
        ).arrange(RIGHT, buff=0.45).shift(UP * 1.1)

        # Baseline align analogy titles & subtitles
        align_texts_to_baseline(train_title, infer_title, serve_title)
        align_texts_to_baseline(train_sub, infer_sub, serve_sub)

        wait_until(3.5)
        self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in analogy], lag_ratio=0.2), run_time=1.8)
        curr_time += 1.8

        # ==========================================
        # PHASE 2: SYSTEM PIPELINE (13.00s - 31.00s)
        # ==========================================
        system_box = RoundedRectangle(
            width=11.6,
            height=2.3,
            corner_radius=0.25,
            stroke_color=BLUE,
            fill_color="#111827",
            fill_opacity=0.96
        ).shift(DOWN * 1.0)

        system_title = T("LLM SERVING SYSTEM", size=20, color=BLUE, weight=BOLD).move_to(system_box.get_top() + DOWN * 0.35)

        components_data = [
            ("Receive\nrequest", BLUE),
            ("Tokenize\nprompt", YELLOW),
            ("Batching &\nscheduling", ORANGE),
            ("KV cache\nmanagement", PURPLE),
            ("GPU\ninference", GREEN),
            ("Stream\noutput", BLUE),
        ]

        comp_groups = VGroup()
        for name, color in components_data:
            box = RoundedRectangle(
                width=1.65,
                height=1.0,
                corner_radius=0.14,
                stroke_color=color,
                fill_color=color,
                fill_opacity=FILL_SOFT
            )
            lines = name.split('\n')
            t1 = T(lines[0], size=13, color=color, weight=BOLD)
            t2 = T(lines[1], size=13, color=color, weight=BOLD)
            label = VGroup(t1, t2).arrange(DOWN, buff=0.06).move_to(box)
            comp_groups.add(VGroup(box, label))

        comp_groups.arrange(RIGHT, buff=0.18).move_to(system_box.get_center() + DOWN * 0.22)

        # Baseline align first and second line of components labels
        first_lines = []
        second_lines = []
        for cg in comp_groups:
            label_vg = cg[1]
            first_lines.append(label_vg[0])
            second_lines.append(label_vg[1])

        align_texts_to_baseline(first_lines[0], *first_lines[1:])
        align_texts_to_baseline(second_lines[0], *second_lines[1:])

        comp_arrows = VGroup()
        for i in range(len(comp_groups) - 1):
            comp_arrows.add(
                Arrow(comp_groups[i].get_right(), comp_groups[i + 1].get_left(), buff=0.05, color=WHITE, stroke_width=2.0)
            )

        wait_until(13.00)
        self.play(FadeIn(system_box), FadeIn(system_title), run_time=1.0)
        curr_time += 1.0
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in comp_groups], lag_ratio=0.15),
            run_time=1.8
        )
        curr_time += 1.8
        self.play(LaggedStart(*[Create(a) for a in comp_arrows], lag_ratio=0.15), run_time=1.0)
        curr_time += 1.0

        # ==========================================
        # PHASE 3: QUEUE & CONCURRENCY (31.00s - 45.00s)
        # ==========================================
        wait_until(31.00)
        # Fade out analogy and shift pipeline up
        self.play(
            FadeOut(analogy),
            system_box.animate.shift(UP * 1.6),
            system_title.animate.shift(UP * 1.6),
            comp_groups.animate.shift(UP * 1.6),
            comp_arrows.animate.shift(UP * 1.6),
            run_time=1.5
        )
        curr_time += 1.5

        # Many concurrent requests dots
        users = VGroup()
        for row in range(3):
            for col in range(6):
                dot = Circle(radius=0.08, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.8)
                dot.move_to(LEFT * 5.2 + RIGHT * col * 0.28 + DOWN * (1.6 + row * 0.3))
                users.add(dot)

        # Queue visualization
        queue_box = RoundedRectangle(
            width=5.0,
            height=1.5,
            corner_radius=0.15,
            stroke_color=MUTED,
            fill_color="#1e293b",
            fill_opacity=0.4
        ).shift(DOWN * 1.8 + RIGHT * 1.0)

        queue_title = T("Queue: Many concurrent requests", size=13, color=YELLOW, weight=BOLD).move_to(queue_box.get_top() + DOWN * 0.22)

        req_long = Rectangle(width=2.3, height=0.25, fill_color=RED, fill_opacity=FILL_STRONG, stroke_color=RED).next_to(queue_box.get_right(), LEFT, buff=0.2).shift(DOWN * 0.22)
        req_short = Rectangle(width=0.8, height=0.25, fill_color=GREEN, fill_opacity=FILL_STRONG, stroke_color=GREEN).next_to(req_long, LEFT, buff=0.15)
        req_med = Rectangle(width=1.2, height=0.25, fill_color=YELLOW, fill_opacity=FILL_STRONG, stroke_color=YELLOW).next_to(req_short, LEFT, buff=0.15)

        req_label_long = T("Long (GPU busy)", size=12, color=RED, weight=BOLD).next_to(req_long, UP, buff=0.05)
        req_label_short = T("Short (Blocked)", size=12, color=GREEN, weight=BOLD).next_to(req_short, UP, buff=0.05)
        align_texts_to_baseline(req_label_long, req_label_short)

        wait_until(34.50)
        self.play(
            FadeIn(users, shift=RIGHT * 0.2),
            FadeIn(queue_box),
            FadeIn(queue_title),
            run_time=1.5
        )
        curr_time += 1.5

        self.play(
            FadeIn(req_long),
            FadeIn(req_short),
            FadeIn(req_med),
            FadeIn(req_label_long),
            FadeIn(req_label_short),
            run_time=1.5
        )
        curr_time += 1.5

        # Indicate the blocking flow
        arrow_to_queue = Arrow(users.get_right(), queue_box.get_left(), buff=0.12, color=YELLOW, stroke_width=2.5)
        arrow_to_gpu = Arrow(queue_box.get_top(), comp_groups[4].get_bottom(), buff=0.12, color=RED, stroke_width=2.5)

        self.play(Create(arrow_to_queue), Create(arrow_to_gpu), run_time=1.2)
        curr_time += 1.2

        wait_until(41.50)
        self.play(
            Indicate(req_short, color=RED),
            Flash(req_short, color=RED),
            run_time=1.2
        )
        curr_time += 1.2

        # ==========================================
        # PHASE 4: SERVING CARD (45.00s - 61.08s)
        # ==========================================
        wait_until(45.00)
        self.play(
            FadeOut(users),
            FadeOut(queue_box),
            FadeOut(queue_title),
            FadeOut(req_long),
            FadeOut(req_short),
            FadeOut(req_med),
            FadeOut(req_label_long),
            FadeOut(req_label_short),
            FadeOut(arrow_to_queue),
            FadeOut(arrow_to_gpu),
            FadeOut(system_box),
            FadeOut(system_title),
            FadeOut(comp_groups),
            FadeOut(comp_arrows),
            run_time=1.5
        )
        curr_time += 1.5

        # Final Serving Card
        serving_box = RoundedRectangle(
            width=9.0,
            height=2.3,
            corner_radius=0.18,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).move_to(ORIGIN)

        serving_title = T("KEY LLM SERVING TECHNIQUES:", size=19, color=YELLOW, weight=BOLD)
        serving_t1 = T("• Continuous Batching", size=17, color=WHITE)
        serving_t2 = T("• Smart Scheduling", size=17, color=WHITE)
        serving_t3 = T("• KV Cache Management (PagedAttention)", size=17, color=WHITE)
        serving_t4 = T("• Latency & Throughput Optimization", size=17, color=WHITE)

        serving_content = VGroup(serving_title, serving_t1, serving_t2, serving_t3, serving_t4).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        if serving_content.width > 8.0:
            serving_content.scale_to_fit_width(8.0)
        serving_content.move_to(serving_box)

        self.play(
            FadeIn(serving_box),
            FadeIn(serving_content),
            run_time=1.5
        )
        curr_time += 1.5

        # Wait until audio finishes
        wait_audio(audio, visual_time=curr_time)
        curr_time = audio_duration(audio)

        # Fade out everything at the very end
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(serving_box),
            FadeOut(serving_content),
            run_time=1.2
        )
        curr_time += 1.2