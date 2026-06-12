import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part501TokenByToken(Scene):
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

        audio = "voice_part5/p5_01.mp3"
        play_audio(audio)

        # 0.00s - 8.00s: Title & Subtitle
        title = T(
            "Autoregressive Decoding",
            size=42,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "LLM không sinh cả câu trả lời một lần — nó sinh từng token",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Prompt box
        prompt_box = RoundedRectangle(
            width=9.8,
            height=1.15,
            corner_radius=0.18,
            stroke_color=BLUE,
            fill_color="#0a1424",
            fill_opacity=0.92
        ).shift(UP * 1.6)

        prompt_text = T(
            'Prompt: "Thủ đô của Việt Nam là"',
            size=27,
            color=WHITE,
            weight=BOLD
        ).move_to(prompt_box)

        # Token stream title
        stream_title = T(
            "Output appears token by token",
            size=26,
            color=YELLOW,
            weight=BOLD
        ).shift(UP * 0.4)

        # Tokens
        tokens = [
            ("Token 1", "Hà", GREEN),
            ("Token 2", "Nội", GREEN),
            ("Token 3", ".", GREEN),
        ]

        token_cards = VGroup()

        for label, value, color in tokens:
            card = RoundedRectangle(
                width=2.2,
                height=1.35,
                corner_radius=0.18,
                stroke_color=color,
                fill_color=color,
                fill_opacity=FILL_SOFT
            )

            label_t = T(label, size=18, color=MUTED)
            value_t = T(value, size=34, color=color, weight=BOLD)

            group_text = VGroup(label_t, value_t).arrange(DOWN, buff=0.12)
            group_text.move_to(card)

            token_cards.add(VGroup(card, group_text))

        token_cards.arrange(RIGHT, buff=0.65).shift(DOWN * 0.6)

        # Align first and second cards value texts baseline
        align_texts_to_baseline(token_cards[0][1][1], token_cards[1][1][1])

        arrows = VGroup()
        for i in range(len(token_cards) - 1):
            arrows.add(
                Arrow(
                    token_cards[i].get_right(),
                    token_cards[i + 1].get_left(),
                    buff=0.16,
                    color=YELLOW
                )
            )

        # Final sentence
        prompt_lbl = T("Thủ đô của Việt Nam là", size=26, color=WHITE)
        tok1_lbl = T(" Hà", size=26, color=GREEN, weight=BOLD)
        tok2_lbl = T(" Nội", size=26, color=GREEN, weight=BOLD)
        tok3_lbl = T(".", size=26, color=GREEN, weight=BOLD)

        final_sentence = VGroup(prompt_lbl, tok1_lbl, tok2_lbl, tok3_lbl)
        final_sentence.arrange(RIGHT, buff=0.06)
        align_texts_to_baseline(prompt_lbl, tok1_lbl, tok2_lbl, tok3_lbl)
        final_sentence.to_edge(DOWN, buff=0.55)

        note = T(
            "A long answer = many repeated decoding steps",
            size=23,
            color=YELLOW,
            weight=BOLD
        ).next_to(final_sentence, UP, buff=0.35)

        # 13.00s: Prompt box & Prompt text
        wait_until(13.00)
        self.play(FadeIn(prompt_box), Write(prompt_text), run_time=1.4)
        curr_time += 1.4

        # 17.50s: Output Stream Title
        wait_until(17.50)
        self.play(FadeIn(stream_title, shift=UP), run_time=0.8)
        curr_time += 0.8

        # 27.20s: Token 1 (Hà) appears
        wait_until(27.20)
        self.play(
            FadeIn(token_cards[0], shift=UP * 0.2),
            FadeIn(prompt_lbl, shift=UP * 0.15),
            FadeIn(tok1_lbl, shift=UP * 0.15),
            run_time=1.0
        )
        curr_time += 1.0

        # 34.20s: Arrow 1 grows
        wait_until(34.20)
        self.play(GrowArrow(arrows[0]), run_time=0.8)
        curr_time += 0.8

        # 38.00s: Token 2 (Nội) appears
        wait_until(38.00)
        self.play(
            FadeIn(token_cards[1], shift=UP * 0.2),
            FadeIn(tok2_lbl, shift=UP * 0.15),
            run_time=1.0
        )
        curr_time += 1.0

        # 41.65s: Token 3 (.) appears
        wait_until(41.65)
        self.play(
            GrowArrow(arrows[1]),
            FadeIn(token_cards[2], shift=UP * 0.2),
            FadeIn(tok3_lbl, shift=UP * 0.15),
            run_time=1.0
        )
        curr_time += 1.0

        # 44.40s - 49.30s: Highlight final sentence (user's view)
        wait_until(44.40)
        self.play(
            final_sentence.animate.scale(1.08),
            run_time=0.6
        )
        self.play(
            final_sentence.animate.scale(1 / 1.08),
            run_time=0.6
        )
        curr_time += 1.2

        # 49.30s - 54.30s: Highlight cards individually (system steps)
        wait_until(49.30)
        # Highlight card 1
        self.play(
            token_cards[0].animate.scale(1.15).set_stroke(width=4),
            run_time=0.5
        )
        self.play(
            token_cards[0].animate.scale(1 / 1.15).set_stroke(width=2),
            run_time=0.5
        )
        curr_time += 1.0

        # Highlight card 2
        self.play(
            token_cards[1].animate.scale(1.15).set_stroke(width=4),
            run_time=0.5
        )
        self.play(
            token_cards[1].animate.scale(1 / 1.15).set_stroke(width=2),
            run_time=0.5
        )
        curr_time += 1.0

        # Highlight card 3
        self.play(
            token_cards[2].animate.scale(1.15).set_stroke(width=4),
            run_time=0.5
        )
        self.play(
            token_cards[2].animate.scale(1 / 1.15).set_stroke(width=2),
            run_time=0.5
        )
        curr_time += 1.0

        # 54.30s: Show Note (repeated steps)
        wait_until(54.30)
        self.play(FadeIn(note, shift=UP), run_time=1.0)
        curr_time += 1.0

        # Wait until audio finishes
        wait_audio(audio, visual_time=curr_time)
        curr_time = audio_duration(audio)

        # Visual pause at the end (2.5 seconds)
        self.wait(2.5)
        curr_time += 2.5

        # Fade out everything at the very end
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(prompt_box),
            FadeOut(prompt_text),
            FadeOut(stream_title),
            FadeOut(token_cards),
            FadeOut(arrows),
            FadeOut(final_sentence),
            FadeOut(note),
            run_time=1.2
        )
        curr_time += 1.2