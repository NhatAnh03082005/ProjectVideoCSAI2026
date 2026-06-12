import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part204DemoToServing(Scene):
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

        audio = "voice_part2/p2_04.mp3"
        play_audio(audio)

        title = T(
            "Từ demo đến sản phẩm thật",
            size=38,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "The problem shifts from intelligence to serving efficiency",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        self.wait(0.73)

        # Compare boxes
        demo_box = RoundedRectangle(
            width=5.1,
            height=3.6,
            corner_radius=0.22,
            stroke_color=BLUE,
            fill_color="#0f172a",
            fill_opacity=0.95
        ).shift(LEFT * 3.0 + DOWN * 0.1)

        product_box = RoundedRectangle(
            width=5.1,
            height=3.6,
            corner_radius=0.22,
            stroke_color=YELLOW,
            fill_color="#1f1608",
            fill_opacity=0.95
        ).shift(RIGHT * 3.0 + DOWN * 0.1)

        demo_title = T(
            "Demo / Lab",
            size=26,
            color=BLUE,
            weight=BOLD
        ).move_to(demo_box.get_top() + DOWN * 0.45)

        product_title = T(
            "Real Product",
            size=26,
            color=YELLOW,
            weight=BOLD
        ).move_to(product_box.get_top() + DOWN * 0.45)

        demo_items = VGroup(
            T("• one user", size=21, color=WHITE),
            T("• one request", size=21, color=WHITE),
            T("• slow response is acceptable", size=21, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(demo_box.get_center() + DOWN * 0.25)

        product_items = VGroup(
            T("• many concurrent users", size=21, color=WHITE),
            T("• different prompt lengths", size=21, color=WHITE),
            T("• fast and stable serving", size=21, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(product_box.get_center() + DOWN * 0.25)

        # Sentence 2: total 7.26s
        self.play(FadeIn(demo_box), FadeIn(demo_title), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(i, shift=RIGHT * 0.15) for i in demo_items], lag_ratio=0.25),
            run_time=1.5
        )
        self.wait(4.76)

        # Sentence 3: total 7.25s
        self.play(FadeIn(product_box), FadeIn(product_title), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(i, shift=RIGHT * 0.15) for i in product_items], lag_ratio=0.25),
            run_time=1.5
        )
        self.wait(4.75)

        # Request variety - sequential fade-in matching Sentence 4, 5, 6
        part1 = T("Different users → different prompts", size=18, color=YELLOW)
        part3 = T(" → different input lengths", size=18, color=YELLOW)
        part5 = T(" → different output lengths", size=18, color=YELLOW)

        request_note = VGroup(part1, part3, part5).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).to_edge(DOWN, buff=0.35)

        # Sentence 4: total 2.95s
        self.play(FadeIn(part1, shift=UP), run_time=0.8)
        self.wait(2.15)

        # Sentence 5: total 2.79s
        self.play(FadeIn(part3, shift=UP), run_time=0.8)
        self.wait(1.99)

        # Sentence 6: total 3.34s
        self.play(FadeIn(part5, shift=UP), run_time=0.8)
        self.wait(2.54)

        # Shift visual
        # Sentence 7: total 4.88s (including transition and shift label + intelligence box)
        self.play(
            FadeOut(demo_box),
            FadeOut(demo_title),
            FadeOut(demo_items),
            FadeOut(product_box),
            FadeOut(product_title),
            FadeOut(product_items),
            FadeOut(request_note),
            run_time=1.0
        )

        shift_label = T(
            "The focus shifts...",
            size=30,
            color=MUTED,
            weight=BOLD
        ).next_to(subtitle, DOWN, buff=0.8)

        intelligence_box = RoundedRectangle(
            width=4.7,
            height=1.4,
            corner_radius=0.22,
            stroke_color=PURPLE,
            fill_color="#171127",
            fill_opacity=0.95
        ).shift(LEFT * 3.0 + DOWN * 0.3)

        intelligence_text = T(
            "Model Intelligence",
            size=26,
            color=PURPLE,
            weight=BOLD
        ).move_to(intelligence_box)

        serving_box = RoundedRectangle(
            width=4.9,
            height=1.4,
            corner_radius=0.22,
            stroke_color=GREEN,
            fill_color="#102018",
            fill_opacity=0.95
        ).shift(RIGHT * 3.0 + DOWN * 0.3)

        serving_text = T(
            "Serving Efficiency",
            size=26,
            color=GREEN,
            weight=BOLD
        ).move_to(serving_box)

        arrow = Arrow(
            intelligence_box.get_right(),
            serving_box.get_left(),
            buff=0.25,
            color=YELLOW
        )

        final_note = T(
            "LLM Serving becomes a core engineering problem.",
            size=26,
            color=YELLOW,
            weight=BOLD
        ).next_to(VGroup(intelligence_box, serving_box), DOWN, buff=0.6)

        self.play(FadeIn(shift_label), run_time=0.8)
        self.play(FadeIn(intelligence_box), FadeIn(intelligence_text), run_time=1.0)
        self.wait(2.08)

        # Sentence 8: total 4.28s
        self.play(GrowArrow(arrow), run_time=1.2)
        self.play(FadeIn(serving_box), FadeIn(serving_text), run_time=1.0)
        self.wait(2.08)

        # Sentence 9: total 6.08s
        self.play(FadeIn(final_note, shift=UP), run_time=1.0)
        self.wait(5.08)

        # Sentence 10: total 7.86s
        self.wait(7.86)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(shift_label),
            FadeOut(intelligence_box),
            FadeOut(intelligence_text),
            FadeOut(serving_box),
            FadeOut(serving_text),
            FadeOut(arrow),
            FadeOut(final_note),
            run_time=1.0
        )
        self.wait(0.5)