import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part201Chatbot(Scene):
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

        audio = "voice_part2/p2_01.mp3"
        play_audio(audio)

        title = T(
            "LLM được triển khai rộng trong thực tế",
            size=36,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "From research demos to real-world AI products",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        self.wait(5.08) # Sentence 1: total 7.08s

        # Sentence 2: total 6.10s
        # Keep title, fade out subtitle to clean up
        self.play(FadeOut(subtitle), run_time=1.0)
        self.wait(5.10)

        # App cards
        chatgpt = RoundedRectangle(
            width=2.4,
            height=1.35,
            corner_radius=0.15,
            stroke_color=GREEN,
            fill_color="#0e1b15",
            fill_opacity=0.85
        )
        chatgpt_text = T("ChatGPT", size=24, color=GREEN, weight=BOLD).move_to(chatgpt)

        claude = RoundedRectangle(
            width=2.4,
            height=1.35,
            corner_radius=0.15,
            stroke_color=ORANGE,
            fill_color="#1d1410",
            fill_opacity=0.85
        )
        claude_text = T("Claude", size=24, color=ORANGE, weight=BOLD).move_to(claude)

        gemini = RoundedRectangle(
            width=2.4,
            height=1.35,
            corner_radius=0.15,
            stroke_color=BLUE,
            fill_color="#0a1424",
            fill_opacity=0.85
        )
        gemini_text = T("Gemini", size=24, color=BLUE, weight=BOLD).move_to(gemini)

        copilot = RoundedRectangle(
            width=2.4,
            height=1.35,
            corner_radius=0.15,
            stroke_color=PURPLE,
            fill_color="#151028",
            fill_opacity=0.85
        )
        copilot_text = T("Copilot", size=24, color=PURPLE, weight=BOLD).move_to(copilot)

        cards = VGroup(
            VGroup(chatgpt, chatgpt_text),
            VGroup(claude, claude_text),
            VGroup(gemini, gemini_text),
            VGroup(copilot, copilot_text)
        ).arrange(RIGHT, buff=0.35).shift(UP * 0.45)

        note = T(
            "LLM is no longer just a research demo.",
            size=25,
            color=YELLOW,
            weight=BOLD
        ).next_to(cards, DOWN, buff=0.55)

        # Sentence 3: total 3.10s
        # Fade in all cards together
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.25) for card in cards],
                lag_ratio=0.12
            ),
            run_time=1.5
        )
        self.wait(1.60)

        # Sentence 4: total 5.64s
        # Show note
        self.play(FadeIn(note, shift=UP), run_time=1.0)
        self.wait(4.64)

        # Chat UI
        chat_box = RoundedRectangle(
            width=8.8,
            height=2.5,
            corner_radius=0.25,
            stroke_color=GREEN,
            fill_color="#111827",
            fill_opacity=1
        ).shift(DOWN * 0.4)

        user_bubble = RoundedRectangle(
            width=5.8,
            height=0.58,
            corner_radius=0.16,
            fill_color="#1f2937",
            fill_opacity=1,
            stroke_width=0
        ).move_to(chat_box.get_center() + UP * 0.48 + RIGHT * 0.75)

        ai_bubble = RoundedRectangle(
            width=6.8,
            height=0.58,
            corner_radius=0.16,
            fill_color="#0f172a",
            fill_opacity=1,
            stroke_color=GREEN,
            stroke_width=1
        ).move_to(chat_box.get_center() + DOWN * 0.42 + LEFT * 0.25)

        user_text = T(
            "User: Explain this topic simply.",
            size=18,
            color=WHITE
        ).move_to(user_bubble)

        ai_text = T(
            "Chatbox: Sure. Here is a clear explanation...",
            size=18,
            color=GREEN
        ).move_to(ai_bubble)

        chat_group = VGroup(chat_box, user_bubble, ai_bubble, user_text, ai_text)

        # Sentence 5: total 7.61s
        # Fade out cards and note, fade in Chat Box, show User prompt
        self.play(
            FadeOut(cards),
            FadeOut(note),
            FadeIn(chat_box),
            run_time=1.0
        )
        self.play(FadeIn(user_bubble), Write(user_text), run_time=1.2)
        self.wait(5.41)

        # Sentence 6: total 3.82s
        # Pause to let user read the user prompt
        self.wait(3.82)

        explanation = T(
            "Behind each response: prompt processing → model inference → token streaming",
            size=21,
            color=MUTED
        ).to_edge(DOWN, buff=0.35)

        # Sentence 7: total 8.62s
        # AI responds and explanation text appears
        self.play(FadeIn(ai_bubble), run_time=0.6)
        self.play(Write(ai_text), run_time=1.4)
        self.play(FadeIn(explanation, shift=UP), run_time=1.0)
        self.wait(5.62)

        # Transition Out (1.0s)
        self.play(
            FadeOut(title),
            FadeOut(chat_group),
            FadeOut(explanation),
            run_time=1.0
        )
        self.wait(0.5)
