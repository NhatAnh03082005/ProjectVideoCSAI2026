import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part304CommonCore(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Helpers for audio playback
        def play_audio(path):
            resolved = resolve_audio_path(path)
            if os.path.exists(resolved):
                self.add_sound(resolved)
            else:
                print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path} (đã phân giải thành {resolved})")

        audio = "voice_part3/p3_04.mp3"
        play_audio(audio)

        # Precise speech timestamps from -5% rate audio file
        t_speech = [
            0.10,   # S1: Intro: Tuy có nhiều khác biệt... (0.10s)
            7.18,   # S2: Phần lớn đều bắt đầu... (7.18s)
            15.90,  # S4: Sau đó, dữ liệu đi qua... (15.90s)
            20.50,  # S5: Trong mỗi bờ lóc... (20.50s)
            28.33,  # S6: Cuối cùng, mô hình... (28.33s)
            39.18,  # S8: Chính cấu trúc lõi... (39.18s)
            47.71,  # S9: Ví dụ, vì nhiều mô hình... (47.71s)
            54.85,  # S10: Vì quá trình đì cốt... (54.85s)
            62.98,  # S11: Vì nhiều rì quét... (62.98s)
            70.85,  # S12: Vì mô đồ guây... (70.85s)
            76.68,  # S13: Và nếu một mô hình... (76.68s)
            84.76,  # S14: Vì vậy, hiểu kiến trúc... (84.76s)
            91.33,  # S15: Nó còn giúp ta hiểu... (91.33s)
            102.21, # S16: Đây là nền tảng... (102.21s)
            108.34  # End of speech (108.34s)
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
            "Different details, similar core",
            size=40,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "This common structure is why serving optimizations can generalize",
            size=21,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        # ----------------------------------------------------
        # CORE PIPELINE OF AN LLM
        # ----------------------------------------------------
        embed_box = RoundedRectangle(
            width=2.2,
            height=1.0,
            corner_radius=0.16,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=FILL_SOFT
        )
        embed_text = T("Token\nEmbedding", size=20, color=BLUE, weight=BOLD).move_to(embed_box)
        embed_node = VGroup(embed_box, embed_text)

        blocks_box = RoundedRectangle(
            width=3.4,
            height=1.4,
            corner_radius=0.16,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        )
        blocks_text = T("N × Transformer\nBlocks", size=22, color=YELLOW, weight=BOLD).move_to(blocks_box)
        blocks_node = VGroup(blocks_box, blocks_text)

        output_box = RoundedRectangle(
            width=2.5,
            height=1.0,
            corner_radius=0.16,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        )
        output_text = T("Next-token\nprobability", size=20, color=GREEN, weight=BOLD).move_to(output_box)
        output_node = VGroup(output_box, output_text)

        core_nodes = VGroup(embed_node, blocks_node, output_node).arrange(RIGHT, buff=0.65).shift(UP * 0.85)

        core_arrows = VGroup(
            Arrow(core_nodes[0].get_right(), core_nodes[1].get_left(), buff=0.15, color=WHITE),
            Arrow(core_nodes[1].get_right(), core_nodes[2].get_left(), buff=0.15, color=WHITE)
        )

        # Inside blocks mini components
        mini_title = T(
            "Inside each block:",
            size=24,
            color=MUTED,
            weight=BOLD
        ).shift(DOWN * 0.25)

        components = VGroup(
            T("Self-Attention", size=21, color=YELLOW, weight=BOLD),
            T("FFN", size=21, color=GREEN, weight=BOLD),
            T("Norm", size=21, color=BLUE, weight=BOLD),
            T("Residual", size=21, color=PURPLE, weight=BOLD),
        ).arrange(RIGHT, buff=0.45)
        
        # Align components' baselines
        c_ref_y = components[0][0].get_bottom()[1]
        for c_obj in components:
            dy = c_ref_y - c_obj[0].get_bottom()[1]
            c_obj.shift(UP * dy)

        components.next_to(mini_title, DOWN, buff=0.35)

        # Serving optimization bullets
        serving_box = RoundedRectangle(
            width=11.2,
            height=2.0,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color="#102018",
            fill_opacity=0.9
        ).to_edge(DOWN, buff=0.45)

        opt_header = T("Shared core enables key serving optimizations:", size=21, color=YELLOW, weight=BOLD)
        
        opt1 = T("Attention kernels", size=18, color=WHITE)
        bullet1 = T("•", size=18, color=YELLOW)
        opt2 = T("KV cache", size=18, color=WHITE)
        bullet2 = T("•", size=18, color=YELLOW)
        opt3 = T("Batching & Scheduling", size=18, color=WHITE)
        
        opt4 = T("Quantization", size=18, color=WHITE)
        bullet4 = T("•", size=18, color=YELLOW)
        opt5 = T("Multi-GPU parallelism", size=18, color=WHITE)
        
        opt_line1 = VGroup(opt1, bullet1, opt2, bullet2, opt3).arrange(RIGHT, buff=0.22)
        opt_line2 = VGroup(opt4, bullet4, opt5).arrange(RIGHT, buff=0.22)
        
        # Align texts by baseline, and center bullets vertically relative to texts
        ref_y1 = opt1[0].get_bottom()[1]
        opt2.shift(UP * (ref_y1 - opt2[0].get_bottom()[1]))
        opt3.shift(UP * (ref_y1 - opt3[0].get_bottom()[1]))
        
        ref_center_y1 = opt1.get_center()[1]
        bullet1.move_to([bullet1.get_center()[0], ref_center_y1, 0])
        bullet2.move_to([bullet2.get_center()[0], ref_center_y1, 0])
        
        # Align line 2: use opt5[0] ("M") as reference, and align opt4[1] ("u") to it
        ref_y2 = opt5[0].get_bottom()[1]
        opt4.shift(UP * (ref_y2 - opt4[1].get_bottom()[1]))
        
        ref_center_y2 = opt5.get_center()[1]
        bullet4.move_to([bullet4.get_center()[0], ref_center_y2, 0])
        
        opt_rows = VGroup(opt_line1, opt_line2).arrange(DOWN, buff=0.24)
        
        serving_content = VGroup(opt_header, opt_rows).arrange(DOWN, buff=0.28)
        serving_content.move_to(serving_box)

        bridge = T(
            "Next: Training vs Inference vs Serving",
            size=27,
            color=BLUE,
            weight=BOLD
        ).next_to(serving_box, UP, buff=0.45)

        # ----------------------------------------------------
        # ANIMATIONS EXECUTION
        # ----------------------------------------------------
        wait_until(t_speech[0])  # 0.10s
        play_anim(Write(title), run_time=1.2)
        play_anim(FadeIn(subtitle, shift=UP), run_time=0.8)
        
        # S02 (7.18s): Token Embedding
        wait_until(t_speech[1])
        play_anim(FadeIn(embed_node, shift=UP * 0.2), run_time=0.8)
        
        # S04 (15.90s): Blocks & Arrow 1
        wait_until(t_speech[2])
        play_anim(
            GrowArrow(core_arrows[0]),
            FadeIn(blocks_node, shift=UP * 0.2),
            run_time=1.0
        )
        
        # S05 (20.50s): Inside Block components
        wait_until(t_speech[3])
        play_anim(FadeIn(mini_title, shift=UP), run_time=0.6)
        play_anim(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.15) for c in components],
                lag_ratio=0.18
            ),
            run_time=1.2
        )
        
        # S06 (28.33s): Next-token & Arrow 2
        wait_until(t_speech[4])
        play_anim(
            GrowArrow(core_arrows[1]),
            FadeIn(output_node, shift=UP * 0.2),
            run_time=1.0
        )
        
        # S08 (39.18s): Clear components, show serving box & header
        wait_until(t_speech[5])
        play_anim(
            FadeOut(mini_title),
            FadeOut(components),
            run_time=0.8
        )
        play_anim(
            FadeIn(serving_box),
            FadeIn(opt_header, shift=UP * 0.1),
            run_time=1.0
        )
        
        # S09 (47.71s): Attention kernels
        wait_until(t_speech[6])
        play_anim(FadeIn(opt1, shift=UP * 0.15), run_time=0.6)
        
        # S10 (54.85s): KV cache
        wait_until(t_speech[7])
        play_anim(
            FadeIn(bullet1),
            FadeIn(opt2, shift=UP * 0.15),
            run_time=0.6
        )
        
        # S11 (62.98s): Batching
        wait_until(t_speech[8])
        play_anim(
            FadeIn(bullet2),
            FadeIn(opt3, shift=UP * 0.15),
            run_time=0.6
        )
        
        # S12 (70.85s): Quantization
        wait_until(t_speech[9])
        play_anim(
            FadeIn(opt4, shift=UP * 0.15),
            run_time=0.6
        )
        
        # S13 (76.68s): Multi-GPU
        wait_until(t_speech[10])
        play_anim(
            FadeIn(bullet4),
            FadeIn(opt5, shift=UP * 0.15),
            run_time=0.6
        )
        
        # S14 (84.76s): Bridge appears
        wait_until(t_speech[11])
        play_anim(FadeIn(bridge, shift=UP * 0.25), run_time=0.8)
        
        # S15 (91.33s): Keep stable
        wait_until(t_speech[12])
        
        # S16 (102.21s): Highlight the bridge
        wait_until(t_speech[13])
        play_anim(Indicate(bridge, color=BLUE, scale_factor=1.1), run_time=1.2)
        
        # End of speech (108.34s)
        wait_until(t_speech[14])
        
        visual_group = VGroup(
            core_nodes, core_arrows, serving_box, opt_header, opt_rows, bridge
        )
        play_anim(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(visual_group),
            run_time=1.0
        )
        self.wait(0.05)
