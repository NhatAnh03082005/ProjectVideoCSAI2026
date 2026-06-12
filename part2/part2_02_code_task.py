import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part202CodeTask(Scene):
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

        audio = "voice_part2/p2_02.mp3"
        play_audio(audio)

        title = T(
            "LLM không chỉ là chatbot",
            size=38,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "Code generation và task automation",
            size=23,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.1)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        self.wait(2.47) # Sentence 1: total 4.37s

        # Code generation window
        code_window = RoundedRectangle(
            width=9.2,
            height=3.0,
            corner_radius=0.2,
            stroke_color=PURPLE,
            fill_color="#0f172a",
            fill_opacity=0.95
        ).shift(UP * 0.25)

        code_title = T(
            "Code Generation",
            size=24,
            color=PURPLE,
            weight=BOLD
        ).next_to(code_window, UP, buff=0.2)

        code_lines = VGroup(
            T("def summarize_document(text):", size=20, color=BLUE),
            T("    # LLM suggests the next lines", size=20, color=MUTED),
            T("    summary = model.generate(text)", size=20, color=GREEN),
            T("    return summary", size=20, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        code_lines.move_to(code_window.get_center() + LEFT * 0.7)

        # Sentence 2: total 4.22s
        # Fade in code window
        self.play(FadeIn(code_window), FadeIn(code_title), run_time=1.0)
        self.wait(3.22)

        # Sentence 3: total 8.95s
        # Write code lines
        self.play(
            LaggedStart(
                *[Write(line) for line in code_lines],
                lag_ratio=0.25
            ),
            run_time=2.8
        )
        self.wait(6.15)

        # Workflow automation
        workflow_title = T(
            "Task Automation",
            size=24,
            color=YELLOW,
            weight=BOLD
        ).shift(DOWN * 1.7)

        step_names = ["Read email", "Extract info", "Create report", "Send summary"]
        step_groups = VGroup()

        for name in step_names:
            box = RoundedRectangle(
                width=2.1,
                height=0.75,
                corner_radius=0.15,
                stroke_color=YELLOW,
                fill_color="#1f2937",
                fill_opacity=1
            )
            text = T(name, size=17, color=WHITE).move_to(box)
            step_groups.add(VGroup(box, text))

        step_groups.arrange(RIGHT, buff=0.35).next_to(workflow_title, DOWN, buff=0.35)

        arrows = VGroup()
        for i in range(len(step_groups) - 1):
            arrows.add(
                Arrow(
                    step_groups[i].get_right(),
                    step_groups[i + 1].get_left(),
                    buff=0.1,
                    color=YELLOW
                )
            )

        # Sentence 4: total 5.47s
        # Fade in workflow title
        self.play(FadeIn(workflow_title), run_time=0.7)
        self.wait(4.77)

        # Sentence 5: total 8.38s
        # Fade in step boxes and arrows
        self.play(
            LaggedStart(
                *[FadeIn(step, shift=UP * 0.15) for step in step_groups],
                lag_ratio=0.2
            ),
            run_time=1.6
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
            run_time=1.2
        )
        self.wait(5.58)

        key = T(
            "Real products require fast and stable responses.",
            size=24,
            color=YELLOW,
            weight=BOLD
        ).to_edge(DOWN, buff=0.35)

        # Sentence 6: total 7.58s
        # Fade in key note
        self.play(FadeIn(key, shift=UP), run_time=1.0)
        self.wait(6.58)

        # Transition Out (1.0s)
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(code_window),
            FadeOut(code_title),
            FadeOut(code_lines),
            FadeOut(workflow_title),
            FadeOut(step_groups),
            FadeOut(arrows),
            FadeOut(key),
            run_time=1.0
        )
        self.wait(0.5)