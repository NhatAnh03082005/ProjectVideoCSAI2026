import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class OpeningHook(Scene):
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


        # =========================================================================
        # SECTION 1: Chatbot Landscape and Title (0:00 - 0:25, Total 25s)
        # =========================================================================
        
        # 1. Title appears at center (2.0s)
        title = T(
            "Towards Efficient Generative LLM Serving",
            size=36,
            weight=BOLD
        ).move_to(ORIGIN)

        subtitle = T(
            "From a user prompt to real-world AI infrastructure",
            size=22,
            color=MUTED
        ).next_to(title, DOWN, buff=0.25)

        play_audio("voice_part1/p1_01.mp3")
        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=2.0)
        
        # 2. Wait at center (2.0s)
        self.wait(2.0)

        # 3. Move title to edge, fade out subtitle (1.5s)
        self.play(
            title.animate.to_edge(UP),
            FadeOut(subtitle),
            run_time=1.5
        )
        wait_audio("voice_part1/p1_01.mp3", visual_time=5.5)

        # 4. Chatbot brand cards (ChatGPT, Claude, Gemini, Copilot)
        chatgpt_card = RoundedRectangle(width=2.4, height=1.6, corner_radius=0.15, color="#10a37f", fill_color="#0e1b15", fill_opacity=0.85)
        chatgpt_label = T("ChatGPT\n(OpenAI)", size=18, color=WHITE).move_to(chatgpt_card.get_center())
        chatgpt = VGroup(chatgpt_card, chatgpt_label)

        claude_card = RoundedRectangle(width=2.4, height=1.6, corner_radius=0.15, color="#cc7b5c", fill_color="#1d1410", fill_opacity=0.85)
        claude_label = T("Claude\n(Anthropic)", size=18, color=WHITE).move_to(claude_card.get_center())
        claude = VGroup(claude_card, claude_label)

        gemini_card = RoundedRectangle(width=2.4, height=1.6, corner_radius=0.15, color="#1a73e8", fill_color="#0a1424", fill_opacity=0.85)
        gemini_label = T("Gemini\n(Google)", size=18, color=WHITE).move_to(gemini_card.get_center())
        gemini = VGroup(gemini_card, gemini_label)

        copilot_card = RoundedRectangle(width=2.4, height=1.6, corner_radius=0.15, color="#8b5cf6", fill_color="#151028", fill_opacity=0.85)
        copilot_label = T("Copilot\n(Microsoft)", size=18, color=WHITE).move_to(copilot_card.get_center())
        copilot = VGroup(copilot_card, copilot_label)

        chatbot_row = VGroup(chatgpt, claude, gemini, copilot).arrange(RIGHT, buff=0.4).shift(UP * 0.2)
        stats_text = T("Serving Millions of Users & Billions of Tokens Daily", size=22, color=MUTED).next_to(chatbot_row, DOWN, buff=0.6)

        play_audio("voice_part1/p1_02.mp3")
        # 5. Fade in cards (2.0s)
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP*0.3) for card in chatbot_row], lag_ratio=0.3),
            run_time=2.0
        )
        
        # 6. Fade in stats text (1.0s)
        self.play(FadeIn(stats_text, shift=UP*0.2), run_time=1.0)
        
        # 7. Wait (12.5s)
        wait_audio("voice_part1/p1_02.mp3", visual_time=3.0)

        # 8. Fade out chatbot row and stats (1.5s)
        self.play(
            FadeOut(chatbot_row),
            FadeOut(stats_text),
            run_time=1.5
        )
        
        # 9. Wait (0.5s)
        self.wait(0.5)


        # =========================================================================
        # SECTION 2: Single User Chat UI & Workflow (0:25 - 1:15, Total 50s)
        # =========================================================================

        chat_box = RoundedRectangle(
            width=9.5,
            height=3.2,
            corner_radius=0.25,
            color=BLUE,
            fill_color="#111827",
            fill_opacity=1
        ).shift(DOWN * 0.4)

        chat_title = T("User Prompt", size=24, color=BLUE)
        chat_title.next_to(chat_box, UP, buff=0.2)

        prompt_text = "Write me a job application email"

        # Center Y within chat box, text horizontally centered
        center_y = chat_box.get_center()[1] + 0.55

        cursor = Rectangle(
            width=0.035,
            height=0.42,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )

        play_audio("voice_part1/p1_03.mp3")
        self.play(FadeIn(chat_box), FadeIn(chat_title), run_time=0.6)

        # --- Smooth typing via ValueTracker ---
        n_chars = ValueTracker(0)

        # Build full text CENTERED in chat box — position fixed
        full_prompt = T(prompt_text, size=28, color=WHITE)
        full_prompt.move_to([chat_box.get_center()[0], center_y, 0])

        # left edge of the full centered text (constant anchor for cursor start)
        text_left_x = full_prompt.get_left()[0]

        # Visibility mask: show only first k characters
        def update_chars(mob):
            k = int(n_chars.get_value())
            for i, ch in enumerate(mob):
                ch.set_opacity(1 if i < k else 0)

        full_prompt.add_updater(update_chars)
        self.add(full_prompt)

        # Cursor follows after last visible character
        def update_cursor(mob):
            k = int(n_chars.get_value())
            if k <= 0:
                mob.move_to([text_left_x, center_y, 0])
            else:
                last_char = full_prompt[min(k - 1, len(full_prompt) - 1)]
                mob.move_to(last_char.get_right() + RIGHT * 0.06)

        cursor.move_to([text_left_x, center_y, 0])
        cursor.add_updater(update_cursor)
        self.add(cursor)
        self.wait(0.15)

        # Animate typing: reveal all characters linearly
        total_type_time = len(prompt_text) * 0.07  # ~2.2s for 32 chars
        self.play(
            n_chars.animate.set_value(len(prompt_text)),
            rate_func=linear,
            run_time=total_type_time,
        )

        full_prompt.remove_updater(update_chars)
        cursor.remove_updater(update_cursor)

        # Final blink
        self.play(cursor.animate.set_opacity(0), run_time=0.25)
        self.play(cursor.animate.set_opacity(1), run_time=0.25)
        self.play(cursor.animate.set_opacity(0), run_time=0.25)
        self.play(cursor.animate.set_opacity(1), run_time=0.25)

        wait_audio("voice_part1/p1_03.mp3", visual_time=0.6 + total_type_time + 1.0)

        prompt = full_prompt


        # ---------- Token stream response ----------
        response_tokens = ["Dear", "Hiring", "Manager,", "I", "am", "writing", "to", "apply..."]

        full_text = T(
            " ".join(response_tokens), 
            size=24, 
            color=GREEN
        )

        token_group = VGroup()
        char_idx = 0
        for tok in response_tokens:
            num_chars = len(tok)
            word = VGroup(*full_text[char_idx : char_idx + num_chars])
            token_group.add(word)
            char_idx += num_chars

        # Đưa cả dòng vào trong chat box
        token_group.move_to(chat_box.get_center() + DOWN * 0.65)

        # Không cho tràn khung
        if token_group.width > chat_box.width - 1.0:
            token_group.set_width(chat_box.width - 1.0)

        play_audio("voice_part1/p1_04.mp3")
        self.play(
            LaggedStart(
                *[FadeIn(t, shift=UP * 0.15) for t in token_group],
                lag_ratio=0.15
            ),
            run_time=3
        )
        self.wait(1)

        # ---------- Transition: not just a smart model ----------
        overlay = Rectangle(
            width=14,
            height=8,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=0
        )

        key_text = T(
            "Behind every AI answer...\nthere is a serving system.",
            size=38,
            weight=BOLD,
            line_spacing=0.9
        )

        self.play(FadeIn(overlay), Write(key_text))
        wait_audio("voice_part1/p1_04.mp3", visual_time=3.5 + 1.0)
        self.play(FadeOut(overlay), FadeOut(key_text), FadeOut(chat_box), FadeOut(chat_title), FadeOut(prompt), FadeOut(cursor), FadeOut(token_group))

        # ---------- Pipeline ----------
        user = Circle(radius=0.45, color=BLUE, fill_color=BLUE_E, fill_opacity=0.8)
        user_label = T("User", size=22).next_to(user, DOWN)

        server = RoundedRectangle(width=1.6, height=1.1, corner_radius=0.15, color=YELLOW)
        server_label = T("Server", size=22).next_to(server, DOWN)

        gpu = RoundedRectangle(width=1.8, height=1.1, corner_radius=0.15, color=GREEN)
        gpu_label = T("GPU", size=22).next_to(gpu, DOWN)

        model = RoundedRectangle(width=2.0, height=1.1, corner_radius=0.15, color=PURPLE)
        model_label = T("LLM Model", size=22).next_to(model, DOWN)

        output = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.15, color=BLUE)
        output_label = T("Token Stream", size=22).next_to(output, DOWN)

        nodes = VGroup(user, server, gpu, model, output).arrange(RIGHT, buff=1.0).shift(DOWN * 0.2)
        labels = VGroup(user_label, server_label, gpu_label, model_label, output_label)

        for label, node in zip(labels, nodes):
            label.next_to(node, DOWN)

        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrows.add(Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.15, color=WHITE))

        pipeline_title = T("LLM Serving Pipeline", size=34, weight=BOLD).to_edge(UP)

        play_audio("voice_part1/p1_05.mp3")
        self.play(ReplacementTransform(title, pipeline_title), FadeOut(subtitle))
        self.play(LaggedStart(*[FadeIn(n, shift=UP) for n in nodes], lag_ratio=0.2))
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.2))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25))

        # Highlight Server stages (Receive request & tokenize prompt)
        stage_text = T("", size=28)
        stage_text.to_edge(DOWN)

        # Stage 1: Receive request
        t1 = T("1. Receive request", size=28, color=YELLOW).to_edge(DOWN)
        h1 = SurroundingRectangle(server, color=YELLOW, buff=0.15)
        self.play(FadeIn(h1), Transform(stage_text, t1))
        self.wait(1.5)
        self.play(FadeOut(h1))

        # Stage 2: Tokenize prompt
        t2 = T("2. Tokenize prompt", size=28, color=YELLOW).to_edge(DOWN)
        h2 = SurroundingRectangle(server, color=YELLOW, buff=0.15)
        self.play(FadeIn(h2), Transform(stage_text, t2))
        self.wait(1.5)
        self.play(FadeOut(h2))

        # wait for q05 to finish
        wait_audio("voice_part1/p1_05.mp3", visual_time=15.0)

        # Highlight GPU & Model stages (q06)
        play_audio("voice_part1/p1_06.mp3")
        # Stage 3: Run model on GPU
        t3 = T("3. Run model on GPU", size=28, color=YELLOW).to_edge(DOWN)
        h3 = SurroundingRectangle(gpu, color=YELLOW, buff=0.15)
        self.play(FadeIn(h3), Transform(stage_text, t3))
        self.wait(2.0)
        self.play(FadeOut(h3))

        # Stage 4: Generate tokens
        t4 = T("4. Generate tokens", size=28, color=YELLOW).to_edge(DOWN)
        h4 = SurroundingRectangle(model, color=YELLOW, buff=0.15)
        self.play(FadeIn(h4), Transform(stage_text, t4))
        self.wait(2.0)
        self.play(FadeOut(h4))

        # wait for q06 to finish
        wait_audio("voice_part1/p1_06.mp3", visual_time=8.0)

        # Highlight Output stage (q07)
        play_audio("voice_part1/p1_07.mp3")
        # Stage 5: Stream answer back
        t5 = T("5. Stream answer back", size=28, color=YELLOW).to_edge(DOWN)
        h5 = SurroundingRectangle(output, color=YELLOW, buff=0.15)
        self.play(FadeIn(h5), Transform(stage_text, t5))
        self.wait(2.5)
        self.play(FadeOut(h5))

        # wait for q07 to finish
        wait_audio("voice_part1/p1_07.mp3", visual_time=4.5)

        # Pipeline Summary & Request dot travel (q08)
        play_audio("voice_part1/p1_08.mp3")

        request_dot = Dot(color=RED, radius=0.12).move_to(user.get_right())
        request_label = T("request", size=18, color=RED).next_to(request_dot, UP)

        self.play(FadeIn(request_dot), FadeIn(request_label))

        path_points = [
            user.get_right(),
            server.get_center(),
            gpu.get_center(),
            model.get_center(),
            output.get_center()
        ]

        for point in path_points[1:]:
            self.play(
                request_dot.animate.move_to(point),
                request_label.animate.next_to(point, UP),
                run_time=1.2
            )

        # wait for q08 to finish
        wait_audio("voice_part1/p1_08.mp3", visual_time=5.8)
        self.wait(0.2)

        self.play(
            FadeOut(stage_text),
            FadeOut(request_dot),
            FadeOut(request_label),
            FadeOut(nodes),
            FadeOut(labels),
            FadeOut(arrows),
            FadeOut(pipeline_title),
            run_time=1.0
        )
        self.wait(0.2)

        # =========================================================================
        # SECTION 3: Scaling & System Bottlenecks (1:15 - 2:00, Total 45s)
        # =========================================================================

        # ---------- Transition: Testing vs. Serving ----------
        # Build all objects FIRST, then play_audio right before self.play
        overlay = Rectangle(
            width=14,
            height=8,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_width=0
        )

        dev_title = T("Development / Testing", size=24, color=BLUE, weight=BOLD)
        dev_content = T("• Running a model locally\n• Single user request\n• Simple validation", size=18, color=WHITE, line_spacing=1.2)
        dev_col = VGroup(dev_title, dev_content).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        prod_title = T("Production Serving", size=24, color=YELLOW, weight=BOLD)
        prod_content = T("• Millions of active users\n• Multi-GPU clusters\n• Complex infrastructure", size=18, color=WHITE, line_spacing=1.2)
        prod_col = VGroup(prod_title, prod_content).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        comparison = VGroup(dev_col, prod_col).arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        # play_audio RIGHT before the first self.play — no Python code gap
        play_audio("voice_part1/p1_09.mp3")
        # Fade in overlay + comparison together (1.5s)
        self.play(FadeIn(overlay), run_time=1.0)
        self.play(FadeIn(comparison), run_time=1.5)
        # Wait for q09 narration to finish
        wait_audio("voice_part1/p1_09.mp3", visual_time=2.5)
        # Fade out comparison (1.5s)
        self.play(FadeOut(overlay), FadeOut(comparison), run_time=1.5)

        # ---------- Zoom out to multiple users ----------
        # Build ALL objects before play_audio to avoid Python-gap timing issue
        many_title = T("What if millions of users ask at the same time?", size=34, weight=BOLD).to_edge(UP)

        users = VGroup()
        for row in range(4):
            for col in range(8):
                c = Circle(radius=0.16, color=BLUE, fill_color=BLUE_E, fill_opacity=0.8)
                c.move_to(LEFT * 5.2 + RIGHT * col * 0.45 + UP * (1.2 - row * 0.45))
                users.add(c)

        big_server = RoundedRectangle(
            width=2.0,
            height=1.3,
            corner_radius=0.2,
            color=YELLOW,
            fill_color="#2d2a12",
            fill_opacity=0.7
        ).shift(RIGHT * 1.4)

        gpu_cluster = VGroup()
        for i in range(6):
            chip = RoundedRectangle(width=0.75, height=0.5, corner_radius=0.08, color=GREEN)
            chip.move_to(RIGHT * 4.0 + RIGHT * (i % 3) * 0.85 + DOWN * (i // 3) * 0.65)
            gpu_cluster.add(chip)

        server_text = T("Servers", size=22).next_to(big_server, DOWN)
        gpu_text = T("GPU Cluster", size=22).next_to(gpu_cluster, DOWN)

        lines = VGroup()
        for u in users:
            line = Line(u.get_right(), big_server.get_left(), color=BLUE, stroke_width=1.2)
            lines.add(line)

        # play_audio RIGHT before first self.play — no Python gap
        play_audio("voice_part1/p1_10.mp3")
        # Fade in title (1.0s)
        self.play(FadeIn(many_title), run_time=1.0)
        # Fade in users grid (1.5s)
        self.play(LaggedStart(*[FadeIn(u, scale=0.5) for u in users], lag_ratio=0.03), run_time=1.5)
        # Fade in server & GPU clusters (1.0s)
        self.play(FadeIn(big_server), FadeIn(gpu_cluster), FadeIn(server_text), FadeIn(gpu_text), run_time=1.0)
        # Create requests lines (2.5s)
        self.play(LaggedStart(*[Create(line) for line in lines], lag_ratio=0.015), run_time=2.5)
        # Wait for q10 to finish
        wait_audio("voice_part1/p1_10.mp3", visual_time=6.0)

        # ---------- Bottlenecks Display ----------
        # Build ALL objects before play_audio
        bottleneck_box = RoundedRectangle(
            width=8.5,
            height=3.2,
            corner_radius=0.2,
            color=RED,
            fill_color="#1a0c0c",
            fill_opacity=0.9
        ).shift(DOWN * 1.5)
        bottleneck_title = T("Critical Production Challenges", size=22, color=RED, weight=BOLD).move_to(bottleneck_box.get_top() + DOWN * 0.4)

        challenge1 = T("1. Response Latency (Speed)", size=18, color=WHITE)
        challenge2 = T("2. Request Throughput (Concurrency)", size=18, color=WHITE)
        challenge3 = T("3. GPU Memory Limits (KV Cache)", size=18, color=WHITE)
        challenge4 = T("4. Operational Cost ($$$)", size=18, color=WHITE)

        challenges = VGroup(challenge1, challenge2, challenge3, challenge4).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(bottleneck_title, DOWN, buff=0.3)
        challenges_group = VGroup(bottleneck_box, bottleneck_title, challenges)

        # play_audio RIGHT before first self.play — no Python gap
        play_audio("voice_part1/p1_11.mp3")
        # Fade in bottlenecks panel (1.5s)
        self.play(FadeIn(bottleneck_box), FadeIn(bottleneck_title), run_time=1.5)
        # Fade in challenges items (2.5s)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*0.2) for c in challenges], lag_ratio=0.4), run_time=2.5)
        # Wait for q11 to finish
        wait_audio("voice_part1/p1_11.mp3", visual_time=4.0)

        # Transition text/pause (q12)
        play_audio("voice_part1/p1_12.mp3")
        self.wait(2.5)
        
        self.play(Indicate(challenge1, color=YELLOW, scale_factor=1.1), run_time=2.0)
        self.wait(0.5)
        self.play(Indicate(challenge2, color=YELLOW, scale_factor=1.1), run_time=2.0)
        self.wait(0.5)
        self.play(Indicate(challenge3, color=YELLOW, scale_factor=1.1), run_time=2.0)
        self.wait(0.5)
        self.play(Indicate(challenge4, color=YELLOW, scale_factor=1.1), run_time=2.0)
        
        wait_audio("voice_part1/p1_12.mp3", visual_time=12.0)

        # =========================================================================
        # SECTION 4: Central Question & Conclusion (2:00 - 2:30, Total 30s)
        # =========================================================================

        # 1. Fade out chaotic elements (1.0s)
        self.play(
            FadeOut(many_title),
            FadeOut(users),
            FadeOut(big_server),
            FadeOut(gpu_cluster),
            FadeOut(server_text),
            FadeOut(gpu_text),
            FadeOut(lines),
            FadeOut(challenges_group),
            run_time=1.0
        )
        # 2. Wait (0.2s)
        self.wait(0.2)

        # 3. Present big question (2.5s)
        play_audio("voice_part1/p1_13.mp3")
        final_question = T(
            "How can we serve large language models\nfaster, cheaper, and more reliably?",
            size=38,
            weight=BOLD,
            line_spacing=1.0
        )
        self.play(Write(final_question), run_time=2.5)
        self.wait(4.0)

        # 5. Introduce main topic title (2.0s)
        topic = T(
            "LLM Serving",
            size=54,
            color=BLUE,
            weight=BOLD
        ).next_to(final_question, DOWN, buff=0.6)
        
        self.play(FadeIn(topic, scale=1.2), run_time=2.0)
        
        # 6. Final wait for q13 narration
        wait_audio("voice_part1/p1_13.mp3", visual_time=8.5)
        self.wait(1.5)