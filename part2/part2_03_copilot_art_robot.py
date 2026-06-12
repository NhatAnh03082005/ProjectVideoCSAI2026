import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part203CopilotArtRobot(Scene):
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

        audio = "voice_part2/p2_03.mp3"
        play_audio(audio)

        title = T(
            "LLM trong công việc, sáng tạo và robotics",
            size=36,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "Personal Copilot • Art Creation • Robotics Control",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        # Define all shapes/panels first
        copilot_box = RoundedRectangle(
            width=3.5,
            height=3.6,
            corner_radius=0.22,
            stroke_color=BLUE,
            fill_color="#0a1424",
            fill_opacity=0.92
        )

        art_box = RoundedRectangle(
            width=3.5,
            height=3.6,
            corner_radius=0.22,
            stroke_color=PURPLE,
            fill_color="#151028",
            fill_opacity=0.92
        )

        robot_box = RoundedRectangle(
            width=3.5,
            height=3.6,
            corner_radius=0.22,
            stroke_color=GREEN,
            fill_color="#102018",
            fill_opacity=0.92
        )

        boxes = VGroup(copilot_box, art_box, robot_box).arrange(RIGHT, buff=0.45).shift(DOWN * 0.25)

        copilot_title = T("Personal\nCopilot", size=24, color=BLUE, weight=BOLD).move_to(copilot_box.get_top() + DOWN * 0.6)
        art_title = T("Art\nCreation", size=24, color=PURPLE, weight=BOLD).move_to(art_box.get_top() + DOWN * 0.6)
        robot_title = T("Robotics\nControl", size=24, color=GREEN, weight=BOLD).move_to(robot_box.get_top() + DOWN * 0.6)

        copilot_items = T(
            "• schedule\n• summarize\n• search\n• decide",
            size=18,
            color=WHITE,
            line_spacing=1.2
        ).move_to(copilot_box.get_center() + DOWN * 0.35)

        # Art icon
        star = Star(
            n=5,
            outer_radius=0.55,
            color=PURPLE,
            fill_color=PURPLE,
            fill_opacity=0.55
        ).move_to(art_box.get_center())

        art_text = T(
            "prompt → idea\nscript → image/video",
            size=17,
            color=WHITE
        ).next_to(star, DOWN, buff=0.35)

        # Robot icon
        robot_head = RoundedRectangle(
            width=1.45,
            height=0.75,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color="#163821",
            fill_opacity=1
        )

        robot_body = RoundedRectangle(
            width=1.8,
            height=1.35,
            corner_radius=0.2,
            stroke_color=GREEN,
            fill_color="#102018",
            fill_opacity=1
        ).next_to(robot_head, DOWN, buff=0.08)

        eye1 = Dot(radius=0.06, color=GREEN).move_to(robot_head.get_center() + LEFT * 0.28)
        eye2 = Dot(radius=0.06, color=GREEN).move_to(robot_head.get_center() + RIGHT * 0.28)

        robot_icon = VGroup(robot_head, robot_body, eye1, eye2).move_to(robot_box.get_center() + UP * 0.05)

        robot_command = T(
            '"Pick up\nthe red block"',
            size=17,
            color=WHITE
        ).next_to(robot_icon, DOWN, buff=0.3)

        # Sentence 1: total 6.74s
        # Title/subtitle and Copilot Box + Title appear
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        self.play(
            FadeIn(copilot_box, shift=UP),
            FadeIn(copilot_title),
            run_time=1.0
        )
        self.wait(3.74)

        # Sentence 2: total 9.46s
        # Copilot items appear
        self.play(FadeIn(copilot_items, shift=UP), run_time=1.2)
        self.wait(8.26)

        # Sentence 3: total 5.84s
        # Art Box + Title appear
        self.play(
            FadeIn(art_box, shift=UP),
            FadeIn(art_title),
            run_time=1.0
        )
        self.wait(4.84)

        # Sentence 4: total 9.13s
        # Art star/text appear and star rotates
        self.play(FadeIn(star), FadeIn(art_text), run_time=1.2)
        self.play(Rotate(star, angle=PI / 5), run_time=1.0)
        self.wait(6.93)

        # Sentence 5: total 3.68s
        # Robot Box + Title appear
        self.play(
            FadeIn(robot_box, shift=UP),
            FadeIn(robot_title),
            run_time=1.0
        )
        self.wait(2.68)

        # Sentence 6: total 7.08s
        # Robot icon/command appear, and bottom note appears
        self.play(FadeIn(robot_icon), FadeIn(robot_command), run_time=1.2)

        note = T(
            "LLM becomes a general interface for many tasks.",
            size=24,
            color=YELLOW,
            weight=BOLD
        ).to_edge(DOWN, buff=0.35)

        self.play(FadeIn(note, shift=UP), run_time=1.0)
        self.wait(4.88)

        # Transition Out (1.0s)
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(boxes),
            FadeOut(copilot_title),
            FadeOut(art_title),
            FadeOut(robot_title),
            FadeOut(copilot_items),
            FadeOut(star),
            FadeOut(art_text),
            FadeOut(robot_icon),
            FadeOut(robot_command),
            FadeOut(note),
            run_time=1.0
        )
        self.wait(0.5)