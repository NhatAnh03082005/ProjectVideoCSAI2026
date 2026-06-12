import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os

class Part301TransformerDecoder(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Helpers for audio playback
        def play_audio(path):
            resolved = resolve_audio_path(path)
            if os.path.exists(resolved):
                self.add_sound(resolved)
            else:
                print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path} (đã phân giải thành {resolved})")

        audio = "voice_part3/p3_01.mp3"
        play_audio(audio)

        # Precise speech timestamps from -5% rate audio file
        t_speech = [
            0.29,  # S1: Intro
            8.75,  # S2: Model names
            18.73, # S3: Decoder block intro
            27.61, # S4: Chatbot prompt & answer
            36.77, # S5: Warning box
            41.53, # S6: Loop concept
            45.65, # S7: Autoregressive token sliding
            51.73, # S8: Serving comparison title
            58.35, # S9: Continuous iteration loop
            67.11, # S10: Metric tiles
            75.63, # S11: Summary base & foundation stack
            82.45  # End of speech / Transition out
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
        title = T("LLM Background", size=42, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.35)

        subtitle = T("Most modern LLMs are based on Transformer Decoder", size=22, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.2)

        # ----------------------------------------------------
        # SEGMENT 2: MODEL CARDS
        # ----------------------------------------------------
        model_names = ["GPT", "LLaMA", "Mistral", "Gemini", "DeepSeek"]
        model_colors = [GREEN, BLUE, YELLOW, PURPLE, ORANGE]
        model_cards = VGroup()

        for name, color in zip(model_names, model_colors):
            card_box = RoundedRectangle(
                width=1.9, height=0.9, corner_radius=0.12,
                stroke_color=color, fill_color=color, fill_opacity=FILL_SOFT
            )
            card_label = T(name, size=21, color=color, weight=BOLD).move_to(card_box)
            model_cards.add(VGroup(card_box, card_label))

        model_cards.arrange(RIGHT, buff=0.3).shift(UP * 0.9)
        model_intro_label = T("Different model architectures, one common foundation...", size=22, color=MUTED)
        model_intro_label.next_to(model_cards, DOWN, buff=0.3)

        # ----------------------------------------------------
        # PERSISTENT DECODER ARCHITECTURE (BOTTOM ZONE)
        # ----------------------------------------------------
        # Persistent container box (Y range: ~ -2.4 to -0.4)
        dec_bg = RoundedRectangle(
            width=10.0, height=2.1, corner_radius=0.18,
            stroke_color=BLUE, stroke_width=2, fill_color="#0f172a", fill_opacity=0.95
        ).shift(DOWN * 1.4)

        dec_title = T("Transformer Decoder Block", size=18, color=BLUE, weight=BOLD)
        dec_title.move_to(dec_bg.get_top() + DOWN * 0.22 + LEFT * 2.8)

        # Internal queues & blocks inside Decoder
        input_container = RoundedRectangle(
            width=3.8, height=0.9, corner_radius=0.12,
            stroke_color=MUTED, stroke_width=1.5, fill_color=BG, fill_opacity=0.8
        ).move_to(dec_bg.get_center() + LEFT * 2.6 + DOWN * 0.1)

        input_container_lbl = T("Input Tokens", size=13, color=MUTED).next_to(input_container, UP, buff=0.06)

        # Stacked layers
        layers_container = RoundedRectangle(
            width=2.4, height=1.3, corner_radius=0.12,
            stroke_color=YELLOW, stroke_width=1.5, fill_color=BG, fill_opacity=0.8
        ).move_to(dec_bg.get_center() + RIGHT * 1.1 + DOWN * 0.1)

        layers_lbl = T("Decoder Layers", size=13, color=YELLOW).next_to(layers_container, UP, buff=0.06)

        # Draw stacked internal layers
        layer_colors = [BLUE, PURPLE, ORANGE]
        layers_stack = VGroup()
        for idx, col in enumerate(layer_colors):
            l_box = Rectangle(
                width=2.1, height=0.25, stroke_color=col, stroke_width=1,
                fill_color=col, fill_opacity=FILL_SOFT
            )
            l_lbl = T(f"Layer {idx+1}", size=12, color=col, weight=BOLD).move_to(l_box)
            layers_stack.add(VGroup(l_box, l_lbl))
        layers_stack.arrange(UP, buff=0.08).move_to(layers_container.get_center())

        # Output Container
        output_container = RoundedRectangle(
            width=1.5, height=0.9, corner_radius=0.12,
            stroke_color=GREEN, stroke_width=1.5, fill_color=BG, fill_opacity=0.8
        ).move_to(dec_bg.get_center() + RIGHT * 3.7 + DOWN * 0.1)

        output_container_lbl = T("Next Token", size=13, color=GREEN).next_to(output_container, UP, buff=0.06)

        # Arrows connecting modules
        arrow_in_to_layers = Arrow(input_container.get_right(), layers_container.get_left(), color=YELLOW, buff=0.12)
        arrow_layers_to_out = Arrow(layers_container.get_right(), output_container.get_left(), color=YELLOW, buff=0.12)

        decoder_architecture = VGroup(
            dec_bg, dec_title,
            input_container, input_container_lbl,
            layers_container, layers_lbl, layers_stack,
            output_container, output_container_lbl,
            arrow_in_to_layers, arrow_layers_to_out
        )

        # Helper to construct token box
        def make_token_box(text, color=BLUE):
            box = RoundedRectangle(
                width=0.52, height=0.52, corner_radius=0.08,
                stroke_color=color, fill_color=color, fill_opacity=FILL_MEDIUM
            )
            lbl = T(text, size=15, color=color, weight=BOLD).move_to(box)
            return VGroup(box, lbl)

        # ----------------------------------------------------
        # ANIMATIONS EXECUTION
        # ----------------------------------------------------

        # --- SEGMENT 1: INTRO (0.29s to 8.75s) ---
        wait_until(t_speech[0])
        play_anim(Write(title), run_time=1.0)
        play_anim(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        wait_until(t_speech[1])

        # --- SEGMENT 2: MODEL CARDS (8.75s to 18.73s) ---
        play_anim(
            LaggedStart(*[FadeIn(card, shift=UP * 0.3) for card in model_cards], lag_ratio=0.15),
            run_time=1.8
        )
        play_anim(FadeIn(model_intro_label, shift=UP * 0.2), run_time=0.8)
        wait_until(t_speech[2])

        # --- SEGMENT 3: DECODER INTRO (18.73s to 27.61s) ---
        # Smooth transition of model cards into the decoder container
        play_anim(
            FadeOut(model_cards),
            FadeOut(model_intro_label),
            run_time=0.8
        )
        play_anim(
            FadeIn(decoder_architecture),
            run_time=1.2
        )
        wait_until(t_speech[3])

        # --- SEGMENT 4: CHATBOT PROMPT & RESPONSE (27.61s to 36.77s) ---
        # Chatbot Window at top Y=0.9
        chat_box = RoundedRectangle(
            width=10.0, height=1.6, corner_radius=0.18,
            stroke_color=GREEN, fill_color="#0f172a", fill_opacity=0.95
        ).shift(UP * 0.9)

        prompt_lbl = T("User: Thủ đô của Việt Nam là", size=20, color=WHITE)
        prompt_lbl.move_to(chat_box.get_left() + RIGHT * 0.7 + UP * 0.3, aligned_edge=LEFT)

        # Single text object for the response to keep all characters on the exact same baseline
        response_text = T("Assistant: Hà Nội", size=20, color=GREEN)
        response_text.move_to(chat_box.get_left() + RIGHT * 0.7 + DOWN * 0.3, aligned_edge=LEFT)

        play_anim(FadeIn(chat_box), Write(prompt_lbl), run_time=1.5)

        # Tokens sliding into the decoder input container below
        tokens_text = ["Thủ", "đô", "của", "Việt", "Nam", "là"]
        input_tokens = VGroup(*[make_token_box(t, color=BLUE) for t in tokens_text])
        input_tokens.arrange(RIGHT, buff=0.1).move_to(input_container.get_center())

        play_anim(
            LaggedStart(*[FadeIn(tok, shift=DOWN * 0.2) for tok in input_tokens], lag_ratio=0.1),
            run_time=1.2
        )

        # Forward pass pulse animation through the layers
        pulse = Rectangle(
            width=2.2, height=0.3, stroke_color=YELLOW, stroke_width=2,
            fill_color=YELLOW, fill_opacity=0.4
        ).move_to(layers_stack[0].get_center())

        play_anim(FadeIn(pulse), run_time=0.3)
        play_anim(pulse.animate.move_to(layers_stack[1].get_center()), run_time=0.4)
        play_anim(pulse.animate.move_to(layers_stack[2].get_center()), run_time=0.4)
        play_anim(FadeOut(pulse), run_time=0.3)

        # Prediction: Output token "Hà"
        ha_token = make_token_box("Hà", color=GREEN).move_to(output_container.get_center())
        play_anim(FadeIn(ha_token, scale=0.5), run_time=0.5)

        # Display response part 1 ("Assistant:  Hà")
        play_anim(Write(response_text[0:12]), run_time=0.8)
        wait_until(t_speech[4])

        # --- SEGMENT 5: WARNING BOX (36.77s to 41.53s) ---
        # Warning sits at the bottom of the screen to avoid overlapping other parts
        warning_box = RoundedRectangle(
            width=7.5, height=0.6, corner_radius=0.1,
            stroke_color=RED, fill_color=RED, fill_opacity=0.15
        ).shift(DOWN * 3.1)

        warning_lbl = T("Không sinh toàn bộ câu trả lời trong một lần!", size=19, color=RED, weight=BOLD)
        warning_lbl.move_to(warning_box)

        play_anim(FadeIn(warning_box), Write(warning_lbl), run_time=0.8)
        play_anim(Flash(warning_box, color=RED, flash_radius=1.2), run_time=0.6)
        wait_until(t_speech[5])

        # --- SEGMENT 6: LOOP concept (41.53s to 45.65s) ---
        # Draw feedback loop path, arched higher to allow the label to sit under it
        loop_arrow = CurvedArrow(
            output_container.get_top() + UP * 0.1,
            input_container.get_top() + UP * 0.1,
            angle=-TAU / 3.0,
            color=YELLOW,
            stroke_width=3
        )
        # Position label directly under the loop arrow peak, above the decoder container top
        loop_lbl = T("Vòng lặp sinh Token (Autoregressive)", size=16, color=YELLOW, weight=BOLD)
        loop_lbl.move_to(DOWN * 0.08)

        play_anim(Create(loop_arrow), Write(loop_lbl), run_time=1.2)
        wait_until(t_speech[6])

        # --- SEGMENT 7: FEEDBACK ANIMATION & NEXT PASS (45.65s to 51.73s) ---
        # Clean warning block out of the way
        play_anim(FadeOut(warning_box), FadeOut(warning_lbl), run_time=0.6)

        # Slide token 'Hà' back into input queue
        ha_input_tok = make_token_box("Hà", color=GREEN)
        
        # Prepare the target layout of all 7 tokens grouped together and centered inside the input_container
        all_tokens_group = VGroup(*[tok.copy() for tok in input_tokens], ha_input_tok)
        all_tokens_group.arrange(RIGHT, buff=0.08)
        all_tokens_group.scale(0.8)
        all_tokens_group.move_to(input_container.get_center())

        # Animate the first 6 tokens shifting and scaling to their target positions in the 7-token layout
        play_anim(
            Transform(input_tokens, VGroup(*all_tokens_group[0:6])),
            ha_token.animate.move_to(loop_arrow.get_start() + UP * 0.2),
            run_time=0.8
        )
        
        # Slide along curved path
        path_points = [
            loop_arrow.get_start(),
            loop_arrow.point_from_proportion(0.5) + UP * 0.3,
            loop_arrow.get_end()
        ]
        
        play_anim(
            ha_token.animate.move_to(path_points[1]),
            run_time=0.6
        )
        
        # Slide to the final target position in the group (the 7th token) and scale it down to match
        play_anim(
            ha_token.animate.move_to(all_tokens_group[6].get_center()).scale(0.8),
            run_time=0.6
        )
        
        # Flash input queue and replace animation token with normal colored block
        self.remove(ha_token)
        self.add(ha_input_tok)
        play_anim(Flash(ha_input_tok, color=GREEN), run_time=0.4)

        # Run second forward pass
        pulse2 = Rectangle(
            width=2.2, height=0.3, stroke_color=YELLOW, stroke_width=2,
            fill_color=YELLOW, fill_opacity=0.4
        ).move_to(layers_stack[0].get_center())

        play_anim(FadeIn(pulse2), run_time=0.3)
        play_anim(pulse2.animate.move_to(layers_stack[1].get_center()), run_time=0.3)
        play_anim(pulse2.animate.move_to(layers_stack[2].get_center()), run_time=0.3)
        play_anim(FadeOut(pulse2), run_time=0.3)

        # Predict token "Nội"
        noi_token = make_token_box("Nội", color=GREEN).move_to(output_container.get_center())
        play_anim(FadeIn(noi_token, scale=0.5), run_time=0.5)

        # Show final response (" Nội")
        play_anim(Write(response_text[12:]), run_time=0.6)
        wait_until(t_speech[7])

        # --- SEGMENT 8: SERVING COMPARISON TITLE (51.73s to 58.35s) ---
        # Fade out top chatbot windows and labels
        play_anim(
            FadeOut(chat_box),
            FadeOut(prompt_lbl),
            FadeOut(response_text),
            FadeOut(loop_arrow),
            FadeOut(loop_lbl),
            FadeOut(noi_token),
            FadeOut(ha_input_tok),
            FadeOut(input_tokens),
            run_time=0.8
        )

        compare_title = T("LLM Serving is Iterative", size=28, color=YELLOW, weight=BOLD).shift(UP * 1.3)
        compare_subtitle = T("NOT a single forward pass • A continuous loop of tokens", size=20, color=WHITE)
        compare_subtitle.next_to(compare_title, DOWN, buff=0.22)

        play_anim(FadeIn(compare_title, shift=UP * 0.2), Write(compare_subtitle), run_time=1.2)
        wait_until(t_speech[8])

        # --- SEGMENT 9: CONTINUOUS ITERATION LOOP (58.35s to 67.11s) ---
        # Run a rapid loop animation (simulate generating 3 more tokens fast)
        sim_tokens = ["là", "thành", "phố"]
        for t_text in sim_tokens:
            p_line = Rectangle(
                width=2.2, height=0.3, stroke_color=YELLOW, stroke_width=2,
                fill_color=YELLOW, fill_opacity=0.4
            ).move_to(layers_stack[0].get_center())
            
            # Fast pulse up
            play_anim(FadeIn(p_line), run_time=0.18)
            play_anim(p_line.animate.move_to(layers_stack[2].get_center()), run_time=0.25)
            
            # Predict
            tok_out = make_token_box(t_text, color=GREEN).move_to(output_container.get_center())
            play_anim(FadeIn(tok_out), FadeOut(p_line), run_time=0.22)
            
            # Loop back fast
            play_anim(tok_out.animate.move_to(input_container.get_center() + RIGHT * 1.1).scale(0.85), run_time=0.3)
            play_anim(Flash(input_container, color=GREEN, flash_radius=0.8), run_time=0.2)
            self.remove(tok_out)

        wait_until(t_speech[9])

        # --- SEGMENT 10: METRIC TILES (67.11s to 75.63s) ---
        play_anim(FadeOut(compare_title), FadeOut(compare_subtitle), run_time=0.8)

        # 4 beautiful metric tiles representing LLM serving profile
        metric_names = ["Latency", "Throughput", "Memory", "Cost"]
        metric_vals = ["Time per Token", "Tokens / Sec", "KV Cache Size", "GPU Compute"]
        metric_desc = ["Lower is better", "Higher is better", "Grows per token", "Hardware cost"]
        m_colors = [RED, YELLOW, BLUE, ORANGE]
        
        metric_tiles = VGroup()
        for m_name, m_val, m_d, col in zip(metric_names, metric_vals, metric_desc, m_colors):
            tile_box = RoundedRectangle(
                width=2.3, height=1.3, corner_radius=0.12,
                stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=FILL_SOFT
            )
            name_lbl = T(m_name, size=18, color=col, weight=BOLD).move_to(tile_box.get_top() + DOWN * 0.25)
            val_lbl = T(m_val, size=14, color=WHITE).next_to(name_lbl, DOWN, buff=0.08)
            desc_lbl = T(m_d, size=11, color=MUTED).next_to(val_lbl, DOWN, buff=0.05)
            
            tile_group = VGroup(tile_box, name_lbl, val_lbl, desc_lbl)
            metric_tiles.add(tile_group)

        metric_tiles.arrange(RIGHT, buff=0.24).shift(UP * 0.9)

        play_anim(
            LaggedStart(*[FadeIn(tile, shift=UP * 0.3) for tile in metric_tiles], lag_ratio=0.15),
            run_time=1.8
        )
        wait_until(t_speech[10])

        # --- SEGMENT 11: SUMMARY BASE & STACK (75.63s to 82.45s) ---
        final_label = T(
            "Transformer Decoder is the foundation of serving optimizations.",
            size=23, color=YELLOW, weight=BOLD
        ).to_edge(DOWN, buff=0.25)

        # Group all other on-screen objects and dim them by 90% (set opacity to 0.1)
        other_elements = VGroup(title, subtitle, decoder_architecture, metric_tiles)
        play_anim(other_elements.animate.set_opacity(0.1), run_time=1.0)

        # We will build/stack serving optimizations on top of the decoder block
        opt_names = ["KV Cache", "Continuous Batching", "Quantization", "Model Parallelism"]
        opt_colors = [GREEN, BLUE, ORANGE, PURPLE]
        
        opt_stack = VGroup()
        # The decoder container is centered at DOWN*1.4, its top edge is at DOWN * 0.35.
        # We start stacking optimization slabs right above it (Y coordinate starts from -0.35 and goes up).
        for idx, (opt_name, col) in enumerate(zip(opt_names, opt_colors)):
            slab = RoundedRectangle(
                width=6.0, height=0.38, corner_radius=0.08,
                stroke_color=col, stroke_width=1, fill_color=col, fill_opacity=0.25
            )
            s_lbl = T(opt_name, size=16, color=col, weight=BOLD).move_to(slab)
            opt_stack.add(VGroup(slab, s_lbl))
            
        opt_stack.arrange(UP, buff=0.08).next_to(dec_bg, UP, buff=0.15)

        play_anim(FadeIn(final_label, shift=UP * 0.2), run_time=1.0)
        
        # Show optimizations stacking on top
        play_anim(
            LaggedStart(*[FadeIn(slab, shift=DOWN * 0.15) for slab in opt_stack], lag_ratio=0.2),
            run_time=2.2
        )
        wait_until(t_speech[11])

        # --- TRANSITION OUT (82.45s to 83.3s) ---
        play_anim(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(decoder_architecture),
            FadeOut(metric_tiles),
            FadeOut(final_label),
            FadeOut(opt_stack),
            run_time=0.8
        )
        self.wait(0.05)