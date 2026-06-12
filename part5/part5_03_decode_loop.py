import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part503DecodeLoop(Scene):
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

        audio = "voice_part5/p5_03.mp3"
        play_audio(audio)

        # Title and Subtitle
        title = T(
            "Autoregressive Decode Loop",
            size=40,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "Prompt → Model → Next Token → Append → Repeat",
            size=23,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Loop nodes (placed in upper half Y = 0.5)
        context_box = RoundedRectangle(
            width=3.0,
            height=1.15,
            corner_radius=0.16,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_color=BLUE,
            fill_opacity=FILL_SOFT
        ).shift(LEFT * 3.8 + UP * 0.9)

        context_text = T("Current\ncontext", size=22, color=BLUE, weight=BOLD).move_to(context_box)

        model_box = RoundedRectangle(
            width=2.8,
            height=1.15,
            corner_radius=0.16,
            stroke_color=PURPLE,
            stroke_width=2.5,
            fill_color=PURPLE,
            fill_opacity=FILL_SOFT
        ).shift(UP * 0.9)

        model_text = T("LLM\ndecode()", size=22, color=PURPLE, weight=BOLD).move_to(model_box)

        next_box = RoundedRectangle(
            width=2.8,
            height=1.15,
            corner_radius=0.16,
            stroke_color=GREEN,
            stroke_width=2.5,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        ).shift(RIGHT * 3.8 + UP * 0.9)

        next_text = T("Next\ntoken", size=22, color=GREEN, weight=BOLD).move_to(next_box)

        append_box = RoundedRectangle(
            width=4.4,
            height=1.05,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).shift(DOWN * 0.9)

        append_text = T("Append token to context", size=22, color=YELLOW, weight=BOLD).move_to(append_box)

        nodes = VGroup(
            VGroup(context_box, context_text),
            VGroup(model_box, model_text),
            VGroup(next_box, next_text),
            VGroup(append_box, append_text)
        )

        arrow1 = Arrow(context_box.get_right(), model_box.get_left(), buff=0.12, color=WHITE)
        arrow2 = Arrow(model_box.get_right(), next_box.get_left(), buff=0.12, color=WHITE)
        arrow3 = Arrow(next_box.get_bottom(), append_box.get_right(), buff=0.15, color=WHITE)
        arrow4 = CurvedArrow(append_box.get_left(), context_box.get_bottom(), angle=-TAU / 6, color=YELLOW)

        # Faded background outline showing the loop structure immediately
        self.play(
            FadeIn(nodes),
            FadeIn(arrow1),
            FadeIn(arrow2),
            FadeIn(arrow3),
            FadeIn(arrow4),
            run_time=1.5
        )
        curr_time += 1.5

        # Save state and fade them out slightly
        for obj in [context_box, model_box, next_box, append_box, arrow1, arrow2, arrow3, arrow4]:
            obj.save_state()
            obj.set_stroke(opacity=0.25)
            obj.set_fill(opacity=0.01)
        for txt in [context_text, model_text, next_text, append_text]:
            txt.save_state()
            txt.set_opacity(0.25)

        repeat_label = T(
            "Repeat until max tokens or <end>",
            size=23,
            color=YELLOW,
            weight=BOLD
        ).next_to(append_box, DOWN, buff=0.35)

        # Dot representation
        dot = Dot(radius=0.11, color=RED).move_to(context_box.get_center())

        def run_dot_loop(run_time_per_segment=0.4):
            self.play(dot.animate.move_to(model_box.get_center()), run_time=run_time_per_segment)
            self.play(dot.animate.move_to(next_box.get_center()), run_time=run_time_per_segment)
            self.play(dot.animate.move_to(append_box.get_center()), run_time=run_time_per_segment)
            self.play(dot.animate.move_to(context_box.get_center()), run_time=run_time_per_segment)

        # 5.50s: Highlight Context block
        wait_until(5.50)
        self.play(
            context_box.animate.restore(),
            context_text.animate.restore(),
            run_time=0.8
        )
        curr_time += 0.8

        # 8.50s: Highlight Model block and send Prompt to model
        wait_until(8.50)
        self.play(
            model_box.animate.restore(),
            model_text.animate.restore(),
            arrow1.animate.restore(),
            run_time=0.8
        )
        curr_time += 0.8
        self.add(dot)
        self.play(dot.animate.move_to(model_box.get_center()), run_time=0.8)
        curr_time += 0.8

        # 13.00s: Highlight Next Token block and generate token
        wait_until(13.00)
        self.play(
            next_box.animate.restore(),
            next_text.animate.restore(),
            arrow2.animate.restore(),
            run_time=0.8
        )
        curr_time += 0.8
        self.play(dot.animate.move_to(next_box.get_center()), run_time=0.8)
        curr_time += 0.8

        # 16.50s: Highlight Append block and move token there
        wait_until(16.50)
        self.play(
            append_box.animate.restore(),
            append_text.animate.restore(),
            arrow3.animate.restore(),
            run_time=0.8
        )
        curr_time += 0.8
        self.play(dot.animate.move_to(append_box.get_center()), run_time=0.8)
        curr_time += 0.8

        # 20.00s: Highlight loop back curved arrow and return to Context
        wait_until(20.00)
        self.play(
            arrow4.animate.restore(),
            run_time=0.8
        )
        curr_time += 0.8
        self.play(dot.animate.move_to(context_box.get_center()), run_time=0.9)
        curr_time += 0.9

        # 24.50s: Show repeat label & run 2 loops automatically
        wait_until(24.50)
        self.play(FadeIn(repeat_label, shift=UP * 0.15), run_time=0.8)
        curr_time += 0.8
        run_dot_loop(run_time_per_segment=0.4)
        curr_time += 1.6
        run_dot_loop(run_time_per_segment=0.4)
        curr_time += 1.6

        # Pseudocode box in the lower half
        code_box = RoundedRectangle(
            width=10.8,
            height=1.9,
            corner_radius=0.16,
            stroke_color=MUTED,
            fill_color="#111827",
            fill_opacity=0.95
        ).to_edge(DOWN, buff=0.35)

        code_lines = VGroup(
            T("for step in range(max_new_tokens):", size=20, color=WHITE),
            T("    next_token = model.decode(context)", size=20, color=GREEN),
            T("    context.append(next_token)", size=20, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        code_lines.move_to(code_box.get_center() + LEFT * 0.65)

        # 31.00s: Shrink & shift loop UP, show Pseudocode at the bottom
        wait_until(31.00)
        self.play(
            VGroup(nodes, arrow1, arrow2, arrow3, arrow4, repeat_label, dot).animate.shift(UP * 0.4),
            FadeIn(code_box),
            LaggedStart(*[Write(line) for line in code_lines], lag_ratio=0.2),
            run_time=1.5
        )
        curr_time += 1.5

        # 36.50s: Highlight line 2 (model.decode) & run dot to Next Box
        wait_until(36.50)
        self.play(
            code_lines[0].animate.set_opacity(0.35),
            code_lines[1].animate.set_opacity(1.0).set_color(GREEN),
            code_lines[2].animate.set_opacity(0.35),
            run_time=0.6
        )
        curr_time += 0.6
        self.play(dot.animate.move_to(model_box.get_center()), run_time=0.5)
        self.play(dot.animate.move_to(next_box.get_center()), run_time=0.5)
        curr_time += 1.0

        # 40.50s: Highlight line 3 (context.append) & run dot back to Context Box
        wait_until(40.50)
        self.play(
            code_lines[1].animate.set_opacity(0.35),
            code_lines[2].animate.set_opacity(1.0).set_color(YELLOW),
            run_time=0.6
        )
        curr_time += 0.6
        self.play(dot.animate.move_to(append_box.get_center()), run_time=0.5)
        self.play(dot.animate.move_to(context_box.get_center()), run_time=0.5)
        curr_time += 1.0

        # 45.00s: Show append visual math (Context + Token = New Context)
        append_visual_box = RoundedRectangle(
            width=12.2,
            height=1.2,
            corner_radius=0.14,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#1e293b",
            fill_opacity=0.95
        ).move_to(UP * 0.8)

        vis_txt1 = T('Context: "Thủ đô của Việt Nam là"', size=15, color=WHITE)
        vis_txt2 = T(' + ', size=15, color=YELLOW)
        vis_txt3 = T('" Hà"', size=15, color=GREEN, weight=BOLD)
        vis_txt4 = T(' ──> ', size=15, color=YELLOW)
        vis_txt5 = T('Context: "Thủ đô của Việt Nam là Hà"', size=15, color=GREEN, weight=BOLD)

        append_visual_content = VGroup(vis_txt1, vis_txt2, vis_txt3, vis_txt4, vis_txt5)
        append_visual_content.arrange(RIGHT, buff=0.08)
        append_visual_content.move_to(append_visual_box)
        append_visual = VGroup(append_visual_box, append_visual_content)

        wait_until(45.00)
        self.play(
            code_lines.animate.set_opacity(1.0),
            FadeOut(nodes),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(arrow3),
            FadeOut(arrow4),
            FadeOut(repeat_label),
            FadeOut(dot),
            FadeIn(append_visual),
            run_time=1.2
        )
        curr_time += 1.2

        # Sequential vs Parallel Comparison
        seq_box = RoundedRectangle(
            width=5.2,
            height=2.5,
            corner_radius=0.16,
            stroke_color=RED,
            stroke_width=2.5,
            fill_color="#1a0c0c",
            fill_opacity=0.9
        ).shift(LEFT * 2.8 + UP * 0.2)
        seq_title = T("Sequential Decoding (AR)", size=22, color=RED, weight=BOLD)
        seq_title.next_to(seq_box.get_top(), DOWN, buff=0.25)
        
        seq_step1 = T("Step 1: Hà", size=18, color=WHITE)
        seq_step2 = T("Step 2: Nội", size=18, color=WHITE)
        seq_step3 = T("Step 3: .", size=18, color=WHITE)
        seq_steps = VGroup(seq_step1, seq_step2, seq_step3).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        seq_steps.next_to(seq_title, DOWN, buff=0.25)
        
        seq_group = VGroup(seq_box, seq_title, seq_steps)

        par_box = RoundedRectangle(
            width=5.2,
            height=2.5,
            corner_radius=0.16,
            stroke_color=GREEN,
            stroke_width=2.5,
            fill_color="#061e14",
            fill_opacity=0.9
        ).shift(RIGHT * 2.8 + UP * 0.2)
        par_title = T("Standard Parallel Model", size=22, color=GREEN, weight=BOLD)
        par_title.next_to(par_box.get_top(), DOWN, buff=0.25)
        
        par_lbl1 = T("Input ──> [Model] ──> Full Output", size=18, color=WHITE)
        par_lbl2 = T("(One-shot generation)", size=16, color=MUTED)
        par_lines = VGroup(par_lbl1, par_lbl2).arrange(DOWN, buff=0.15)
        par_lines.next_to(par_title, DOWN, buff=0.3)
        
        par_group = VGroup(par_box, par_title, par_lines)

        compare_group = VGroup(seq_group, par_group)

        warning_text = T(
            "Bottleneck: Sequential dependency cannot be parallelized.",
            size=22,
            color=RED,
            weight=BOLD
        )
        warning_box = RoundedRectangle(
            width=10.8,
            height=0.8,
            corner_radius=0.14,
            stroke_color=RED,
            stroke_width=2,
            fill_color="#1a0c0c",
            fill_opacity=0.8
        )
        warning_box.to_edge(DOWN, buff=0.35)
        warning_text.move_to(warning_box)
        warning_note = VGroup(warning_box, warning_text)

        # 51.50s: Fade out Pseudocode and visual, Show Comparison
        wait_until(51.50)
        self.play(
            FadeOut(code_box),
            FadeOut(code_lines),
            FadeOut(append_visual),
            FadeIn(compare_group),
            run_time=1.2
        )
        curr_time += 1.2

        # 57.00s: Highlight Sequential block, flash step elements
        wait_until(57.00)
        self.play(
            seq_box.animate.set_stroke(width=4.5),
            run_time=0.5
        )
        curr_time += 0.5
        self.play(Flash(seq_step1, color=RED), run_time=0.5)
        self.play(Flash(seq_step2, color=RED), run_time=0.5)
        self.play(Flash(seq_step3, color=RED), run_time=0.5)
        curr_time += 1.5

        # 61.00s: Show resource bottleneck warning note at the bottom
        wait_until(61.00)
        self.play(FadeIn(warning_note, shift=UP * 0.15), run_time=1.0)
        curr_time += 1.0
        self.play(Flash(warning_box, color=RED), run_time=0.8)
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
            FadeOut(subtitle),
            FadeOut(compare_group),
            FadeOut(warning_note),
            run_time=1.2
        )
        curr_time += 1.2