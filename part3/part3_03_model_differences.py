import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part303ModelDifferences(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Helpers for audio playback
        def play_audio(path):
            resolved = resolve_audio_path(path)
            if os.path.exists(resolved):
                self.add_sound(resolved)
            else:
                print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path} (đã phân giải thành {resolved})")

        audio = "voice_part3/p3_03.mp3"
        play_audio(audio)

        # Precise speech timestamps from -5% rate audio file
        t_speech = [
            0.10,   # S1: Intro (0.10s)
            7.89,   # S2: First difference: Layers (7.89s)
            23.10,  # S5: Second difference: Hidden dimension (23.10s)
            38.41,  # S8: Attention heads (38.41s)
            47.58,  # S10: Positional embedding / Traditional MHA (47.58s)
            51.85,  # S11: MQA / GQA (51.85s)
            65.46,  # S13: MoE (65.46s)
            85.37,  # S16: Conclusion (85.37s)
            99.08   # End of speech (99.08s)
        ]

        self.current_time = 0.0

        def wait_until(target_time):
            diff = target_time - self.current_time
            if diff > 0.01:
                self.wait(diff)
                self.current_time = target_time
            elif diff < -0.05:
                print(f"[WARNING] Animation runtime exceeded target time {target_time}s by {-diff:.3f}s")

        def play_anim(*anims, run_time=1.0, **kwargs):
            self.play(*anims, run_time=run_time, **kwargs)
            self.current_time += run_time

        # ----------------------------------------------------
        # VISUAL HEADER DEFINITIONS
        # ----------------------------------------------------
        title = T(
            "Modern LLMs differ in design choices",
            size=38,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "But most still follow the Transformer-decoder family",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        # ----------------------------------------------------
        # TABLE CONTAINER & COMPONENTS
        # ----------------------------------------------------
        table_box = RoundedRectangle(
            width=11.2,
            height=4.6,
            corner_radius=0.22,
            stroke_color=BLUE,
            fill_color="#111827",
            fill_opacity=0.95
        ).shift(DOWN * 0.15)

        h1 = T("Design choice", size=22, color=YELLOW, weight=BOLD)
        h2 = T("Why it matters for serving", size=22, color=YELLOW, weight=BOLD)
        
        headers = VGroup(h1, h2).arrange(RIGHT, buff=2.2)
        
        # Align headers' baselines vertically
        h_dy = headers[0][0].get_bottom()[1] - headers[1][0].get_bottom()[1]
        headers[1].shift(UP * h_dy)
        
        headers.move_to(table_box.get_top() + DOWN * 0.45)

        rows_data = [
            ("Number of layers", "more sequential computation"),
            ("Hidden dimension", "larger activation / memory use"),
            ("Attention heads", "attention cost and parallelism"),
            ("Positional embedding", "long-context behavior"),
            ("MQA / GQA", "smaller KV cache during decode"),
            ("MoE", "conditional compute with experts"),
        ]

        rows = VGroup()
        start_y = 1.15
        row_height = 0.50
        for i, (left, right) in enumerate(rows_data):
            l = T(left, size=19, color=WHITE)
            r = T(right, size=19, color=MUTED)
            
            # Position horizontally
            l.align_to(headers[0], LEFT)
            r.align_to(headers[1], LEFT)
            
            # Position baseline at fixed Y coordinate
            target_y = start_y - i * row_height
            l_dy = target_y - l[0].get_bottom()[1]
            l.shift(UP * l_dy)
            
            # Align right column baseline to left column
            r_dy = target_y - r[0].get_bottom()[1]
            r.shift(UP * r_dy)
            
            row = VGroup(l, r)
            rows.add(row)

        # Highlights and Notes
        highlight_mqa = SurroundingRectangle(rows[4], color=GREEN, buff=0.08)
        highlight_moe = SurroundingRectangle(rows[5], color=PURPLE, buff=0.08)

        mqa_note = T(
            "MQA/GQA can reduce KV-cache memory.",
            size=22,
            color=GREEN,
            weight=BOLD
        ).to_edge(DOWN, buff=0.55)

        moe_note = T(
            "MoE activates only selected experts per token.",
            size=22,
            color=PURPLE,
            weight=BOLD
        ).to_edge(DOWN, buff=0.55)

        # ----------------------------------------------------
        # ANIMATIONS EXECUTION
        # ----------------------------------------------------
        wait_until(t_speech[0])  # 0.10s
        play_anim(Write(title), run_time=1.2)
        play_anim(FadeIn(subtitle, shift=UP), run_time=0.8)
        play_anim(FadeIn(table_box), FadeIn(headers), run_time=1.0)
        
        # Wait and show rows matching the voice segments
        wait_until(t_speech[1])  # 7.89s
        play_anim(FadeIn(rows[0], shift=RIGHT * 0.15), run_time=0.8)
        
        wait_until(t_speech[2])  # 23.10s
        play_anim(FadeIn(rows[1], shift=RIGHT * 0.15), run_time=0.8)
        
        wait_until(t_speech[3])  # 38.41s
        play_anim(FadeIn(rows[2], shift=RIGHT * 0.15), run_time=0.8)
        
        wait_until(t_speech[4])  # 47.58s
        play_anim(FadeIn(rows[3], shift=RIGHT * 0.15), run_time=0.8)
        
        wait_until(t_speech[5])  # 51.85s
        play_anim(
            FadeIn(rows[4], shift=RIGHT * 0.15),
            Create(highlight_mqa),
            FadeIn(mqa_note, shift=UP),
            run_time=1.2
        )
        
        wait_until(t_speech[6])  # 65.46s
        play_anim(
            FadeIn(rows[5], shift=RIGHT * 0.15),
            ReplacementTransform(highlight_mqa, highlight_moe),
            FadeOut(mqa_note),
            FadeIn(moe_note, shift=UP),
            run_time=1.2
        )
        
        wait_until(t_speech[7])  # 85.37s
        play_anim(
            FadeOut(highlight_moe),
            FadeOut(moe_note),
            run_time=1.0
        )
        
        wait_until(t_speech[8])  # 99.08s
        
        # Clean up everything at the end
        visual_group = VGroup(table_box, headers, rows)
        play_anim(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(visual_group),
            run_time=1.0
        )
        self.wait(0.05)