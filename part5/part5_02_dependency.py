import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part502Dependency(Scene):
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

        audio = "voice_part5/p5_02.mp3"
        play_audio(audio)

        # 0.00s - 6.46s: Title & Subtitle
        title = T(
            "Token sau phụ thuộc token trước",
            size=40,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "Next token depends on prompt + all previous generated tokens",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Context rows
        rows_text = [
            ('Step 1', 'Context: "Thủ đô của Việt Nam là"', 'Predict: "Hà"'),
            ('Step 2', 'Context: "Thủ đô của Việt Nam là Hà"', 'Predict: "Nội"'),
            ('Step 3', 'Context: "Thủ đô của Việt Nam là Hà Nội"', 'Predict: "."'),
        ]

        row_groups = VGroup()

        for step, context, pred in rows_text:
            row_box = RoundedRectangle(
                width=11.2,
                height=1.05,
                corner_radius=0.16,
                stroke_color=BLUE,
                fill_color="#111827",
                fill_opacity=0.95
            )

            step_t = T(step, size=22, color=YELLOW, weight=BOLD)
            context_t = T(context, size=20, color=WHITE)
            pred_t = T(pred, size=20, color=GREEN, weight=BOLD)

            row_content = VGroup(step_t, context_t, pred_t)
            row_content.arrange(RIGHT, buff=0.5)
            align_texts_to_baseline(step_t, context_t, pred_t)
            row_content.move_to(row_box)

            row_groups.add(VGroup(row_box, row_content))

        # Shift slightly UP from DOWN * 0.15 to UP * 0.1 to avoid bottom note overlap
        row_groups.arrange(DOWN, buff=0.32).shift(UP * 0.1)

        # Dependency arrows
        dep_arrow1 = CurvedArrow(
            row_groups[0].get_right() + LEFT * 1.35,
            row_groups[1].get_right() + LEFT * 1.35,
            angle=-TAU / 8,
            color=YELLOW
        )

        dep_arrow2 = CurvedArrow(
            row_groups[1].get_right() + LEFT * 1.35,
            row_groups[2].get_right() + LEFT * 1.35,
            angle=-TAU / 8,
            color=YELLOW
        )

        # Prompt card shown initially in the center
        prompt_card_box = RoundedRectangle(
            width=8.5,
            height=1.2,
            corner_radius=0.16,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_color="#1e293b",
            fill_opacity=0.95
        )
        prompt_card_text = T('Prompt: "Thủ đô của Việt Nam là"', size=24, color=WHITE, weight=BOLD)
        prompt_card_text.move_to(prompt_card_box)
        prompt_card = VGroup(prompt_card_box, prompt_card_text)
        prompt_card.move_to(ORIGIN)

        # Illustration for: "Cannot generate second token before first token is created"
        illus_card1 = RoundedRectangle(
            width=2.4,
            height=1.0,
            corner_radius=0.12,
            stroke_color=RED,
            stroke_width=2.5,
            fill_color="#1a0c0c",
            fill_opacity=0.9
        )
        illus_text1 = T("Token 1", size=22, color=RED, weight=BOLD)
        illus_sub1 = T("Missing", size=14, color=MUTED)
        illus_sub1.next_to(illus_text1, DOWN, buff=0.04)
        illus_grp1 = VGroup(illus_card1, VGroup(illus_text1, illus_sub1).move_to(illus_card1))

        # Blocked arrow from token 1 to token 2
        illus_arrow = Arrow(
            LEFT * 0.5, RIGHT * 0.5,
            color=RED,
            stroke_width=4
        )
        cross_line1 = Line(UP * 0.22 + LEFT * 0.22, DOWN * 0.22 + RIGHT * 0.22, color=RED, stroke_width=4.5)
        cross_line2 = Line(DOWN * 0.22 + LEFT * 0.22, UP * 0.22 + RIGHT * 0.22, color=RED, stroke_width=4.5)
        cross_mark = VGroup(cross_line1, cross_line2)
        cross_mark.move_to(illus_arrow.get_center())
        cross_grp = VGroup(illus_arrow, cross_mark)

        illus_card2 = RoundedRectangle(
            width=2.4,
            height=1.0,
            corner_radius=0.12,
            stroke_color=MUTED,
            stroke_width=2.5,
            fill_color="#1e293b",
            fill_opacity=0.5
        )
        illus_text2 = T("Token 2", size=22, color=MUTED, weight=BOLD)
        illus_sub2 = T("Blocked", size=14, color=MUTED)
        illus_sub2.next_to(illus_text2, DOWN, buff=0.04)
        illus_grp2 = VGroup(illus_card2, VGroup(illus_text2, illus_sub2).move_to(illus_card2))

        illus_row = VGroup(illus_grp1, cross_grp, illus_grp2)
        illus_row.arrange(RIGHT, buff=0.4)
        illus_row.move_to(ORIGIN)

        illus_label = T(
            "Cannot generate Token 2 without Token 1",
            size=22,
            color=RED,
            weight=BOLD
        ).next_to(illus_row, DOWN, buff=0.3)

        illus_block = VGroup(illus_row, illus_label)

        dep_label = T(
            "Generated token is appended to the next context",
            size=22,
            color=YELLOW,
            weight=BOLD
        ).next_to(row_groups, DOWN, buff=0.3)

        note_text = T(
            "If the previous step is not finished, the next step cannot start.",
            size=22,
            color=RED,
            weight=BOLD
        )
        note_box = RoundedRectangle(
            width=10.6,
            height=0.8,
            corner_radius=0.14,
            stroke_color=RED,
            stroke_width=2,
            fill_color="#1a0c0c",
            fill_opacity=0.8
        )
        note_box.to_edge(DOWN, buff=0.35)
        note_text.move_to(note_box)
        note = VGroup(note_box, note_text)

        # 6.50s: Show Dependency Blocker Illustration (Mô hình không thể sinh...)
        wait_until(6.50)
        self.play(FadeIn(illus_block, shift=UP * 0.2), run_time=1.0)
        curr_time += 1.0

        # 11.50s: Hide Blocker Illustration and Show Prompt Card in the center
        wait_until(11.50)
        self.play(
            FadeOut(illus_block, shift=DOWN * 0.2),
            FadeIn(prompt_card, shift=UP * 0.2),
            run_time=1.0
        )
        curr_time += 1.0

        # 15.67s: Step 1 box fades in, Prompt Card fades out
        wait_until(15.67)
        self.play(
            FadeOut(prompt_card, shift=DOWN * 0.2),
            FadeIn(row_groups[0], shift=UP * 0.2),
            run_time=1.2
        )
        curr_time += 1.2

        # 19.41s: Arrow 1 grows
        wait_until(19.41)
        self.play(Create(dep_arrow1), run_time=0.8)
        curr_time += 0.8

        # 23.05s: Step 2 box fades in
        wait_until(23.05)
        self.play(FadeIn(row_groups[1], shift=UP * 0.2), run_time=1.2)
        curr_time += 1.2

        # 32.31s: Arrow 2 grows
        wait_until(32.31)
        self.play(Create(dep_arrow2), run_time=0.8)
        curr_time += 0.8

        # 35.75s: Step 3 box fades in
        wait_until(35.75)
        self.play(FadeIn(row_groups[2], shift=UP * 0.2), run_time=1.2)
        curr_time += 1.2

        # 44.48s: Dependency label fades in
        wait_until(44.48)
        self.play(FadeIn(dep_label, shift=UP), run_time=1.0)
        curr_time += 1.0

        # Highlight key dependency sequentially
        h1 = SurroundingRectangle(row_groups[0], color=GREEN, buff=0.08)
        h2 = SurroundingRectangle(row_groups[1], color=GREEN, buff=0.08)
        h3 = SurroundingRectangle(row_groups[2], color=GREEN, buff=0.08)

        wait_until(47.79)
        self.play(Create(h1), run_time=0.6)
        self.play(ReplacementTransform(h1, h2), run_time=0.6)
        self.play(ReplacementTransform(h2, h3), run_time=0.6)
        self.play(FadeOut(h3), run_time=0.5)
        curr_time += 2.3

        # 53.66s: Show Note (tuần tự)
        wait_until(53.66)
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
            FadeOut(row_groups),
            FadeOut(dep_arrow1),
            FadeOut(dep_arrow2),
            FadeOut(dep_label),
            FadeOut(note),
            run_time=1.2
        )
        curr_time += 1.2