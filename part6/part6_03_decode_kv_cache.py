import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part603DecodeKVCache(Scene):
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

        # Baseline alignment helpers
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

        audio = "voice_part6/p6_03.mp3"
        play_audio(audio)

        # Title & Subtitle (0.00s)
        title = T(
            "Decode Phase + KV Cache",
            size=42,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "KV Cache giúp tái sử dụng ngữ cảnh thay vì tính lại từ đầu",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # 0.00s: Faded outlines of core components to avoid empty screens
        context_box = RoundedRectangle(
            width=5.2,
            height=1.1,
            corner_radius=0.16,
            stroke_color=BLUE,
            fill_color="#0a1424",
            fill_opacity=0.92
        ).shift(LEFT * 3.3 + UP * 1.55)

        context_text = T(
            "Current context\nprompt + generated tokens",
            size=18,
            color=BLUE,
            weight=BOLD
        ).move_to(context_box)

        cache_box = RoundedRectangle(
            width=4.6,
            height=1.1,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color="#102018",
            fill_opacity=0.95
        ).shift(RIGHT * 3.1 + UP * 1.55)

        cache_text = T(
            "KV Cache\nstored Keys / Values",
            size=20,
            color=GREEN,
            weight=BOLD
        ).move_to(cache_box)

        model_box = RoundedRectangle(
            width=3.6,
            height=1.25,
            corner_radius=0.18,
            stroke_color=PURPLE,
            fill_color="#171127",
            fill_opacity=0.95
        ).shift(UP * 0.1)

        model_text = T(
            "LLM decode step",
            size=24,
            color=PURPLE,
            weight=BOLD
        ).move_to(model_box)

        next_box = RoundedRectangle(
            width=3.2,
            height=1.0,
            corner_radius=0.16,
            stroke_color=YELLOW,
            fill_color="#1f1608",
            fill_opacity=0.95
        ).shift(DOWN * 1.3)

        next_text = T(
            "Next token",
            size=24,
            color=YELLOW,
            weight=BOLD
        ).move_to(next_box)

        arrow_context = Arrow(context_box.get_bottom(), model_box.get_left(), buff=0.18, color=BLUE)
        arrow_cache = Arrow(cache_box.get_bottom(), model_box.get_right(), buff=0.18, color=GREEN)
        arrow_next = Arrow(model_box.get_bottom(), next_box.get_top(), buff=0.18, color=YELLOW)

        # Save states for faded look
        context_box.save_state()
        context_box.set_stroke(opacity=0.25)
        context_box.set_fill(opacity=0.01)

        cache_box.save_state()
        cache_box.set_stroke(opacity=0.25)
        cache_box.set_fill(opacity=0.01)

        model_box.save_state()
        model_box.set_stroke(opacity=0.25)
        model_box.set_fill(opacity=0.01)

        next_box.save_state()
        next_box.set_stroke(opacity=0.25)
        next_box.set_fill(opacity=0.01)

        self.play(
            FadeIn(context_box),
            FadeIn(cache_box),
            FadeIn(model_box),
            FadeIn(next_box),
            run_time=1.5
        )
        curr_time += 1.5

        # 6.30s: "Đây là pha mô hình bắt đầu sinh câu trả lời từng tóc cần một."
        wait_until(6.30)
        self.play(
            model_box.animate.restore(),
            next_box.animate.restore(),
            FadeIn(model_text),
            FadeIn(next_text),
            Create(arrow_next),
            run_time=1.2
        )
        curr_time += 1.2

        # 10.50s: "Ở mỗi bước đì cốt, mô hình cần nhìn lại pờ rom ban đầu và toàn bộ các tóc cần đã sinh trước đó."
        wait_until(10.50)
        self.play(
            context_box.animate.restore(),
            FadeIn(context_text),
            Create(arrow_context),
            run_time=1.2
        )
        curr_time += 1.2

        # 16.90s: "Nếu không có K V két, mô hình sẽ phải tính lại ki và va liu cho toàn bộ ngữ cảnh ở mỗi bước."
        problem_note = T(
            "Without KV Cache: LLM must recompute all previous tokens at each step",
            size=22,
            color=RED,
            weight=BOLD
        ).to_edge(DOWN, buff=0.65)

        wait_until(16.90)
        self.play(FadeIn(problem_note, shift=UP), run_time=1.2)
        curr_time += 1.2

        # 23.33s: "Điều này cực kỳ tốn kém, đặc biệt khi pờ rom dài hoặc ao pút dài."
        cost_note = T(
            "Computation grows quadratically with context length (O(N²))",
            size=19,
            color=WHITE
        )

        wait_until(23.33)
        self.play(
            problem_note.animate.shift(UP * 0.25),
            FadeIn(cost_note.next_to(problem_note, DOWN, buff=0.12).shift(UP * 0.25), shift=UP),
            run_time=1.2
        )
        curr_time += 1.2

        # 28.31s: "K V két giải quyết vấn đề này bằng cách lưu lại ki và va liu của các tóc cần trước đó trong ét ten sần."
        solution_note = T(
            "KV Cache stores past Keys and Values to avoid recomputation",
            size=22,
            color=GREEN,
            weight=BOLD
        ).to_edge(DOWN, buff=0.65)

        wait_until(28.31)
        self.play(
            FadeOut(problem_note),
            FadeOut(cost_note),
            run_time=0.4
        )
        self.play(
            cache_box.animate.restore(),
            FadeIn(cache_text),
            Create(arrow_cache),
            FadeIn(solution_note, shift=UP),
            run_time=0.8
        )
        curr_time += 1.2

        # 34.75s: "Khi tóc cần mới được sinh ra, mô hình chỉ cần tính ki và va liu cho tóc cần mới."
        solution_note_2 = T(
            "Only compute Key/Value for the single newly generated token",
            size=19,
            color=WHITE
        )

        wait_until(34.75)
        self.play(
            solution_note.animate.shift(UP * 0.25),
            FadeIn(solution_note_2.next_to(solution_note, DOWN, buff=0.12).shift(UP * 0.25), shift=UP),
            run_time=1.2
        )
        curr_time += 1.2

        # 40.50s: "Các ki và va liu cũ được lấy lại từ két."
        wait_until(40.50)
        self.play(
            Flash(cache_box, color=GREEN, flash_radius=1.5),
            Indicate(cache_box, color=GREEN, scale_factor=1.05),
            run_time=1.2
        )
        curr_time += 1.2

        # 43.86s: "Có thể hiểu trực quan K V két giống như một cuốn sổ ghi nhớ."
        analogy_box = RoundedRectangle(
            width=11.2,
            height=1.1,
            corner_radius=0.18,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).to_edge(DOWN, buff=0.55)

        analogy_text = T(
            "Analogy: KV Cache = Note-taking\nRead notes instead of re-reading the entire book",
            size=20,
            color=WHITE,
            weight=BOLD
        ).move_to(analogy_box)

        wait_until(43.86)
        self.play(
            FadeOut(solution_note),
            FadeOut(solution_note_2),
            run_time=0.4
        )
        self.play(
            FadeIn(analogy_box),
            Write(analogy_text),
            run_time=0.8
        )
        curr_time += 1.2

        # 48.23s: "Khi đọc một tài liệu dài, nếu mỗi lần viết thêm một từ mà phải đọc lại toàn bộ tài liệu từ đầu thì rất chậm."
        wait_until(48.23)
        self.play(
            Indicate(analogy_box, color=RED, scale_factor=1.03),
            run_time=1.2
        )
        curr_time += 1.2

        # 54.77s: "Nhưng nếu ta đã ghi chú những thông tin quan trọng, ta có thể tra lại ghi chú đó thay vì xử lý lại mọi thứ."
        wait_until(54.77)
        self.play(
            Flash(analogy_box, color=GREEN, flash_radius=1.8),
            Indicate(analogy_box, color=GREEN, scale_factor=1.05),
            run_time=1.5
        )
        curr_time += 1.5

        # 61.62s: "Nhờ K V két, đì cốt nhanh hơn rất nhiều so với việc tính lại toàn bộ ngữ cảnh ở mỗi tóc cần."
        conclusion_box = RoundedRectangle(
            width=11.2,
            height=0.9,
            corner_radius=0.15,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).to_edge(DOWN, buff=0.55)

        conclusion_text = T(
            "KV Cache makes autoregressive decoding highly efficient",
            size=22,
            color=YELLOW,
            weight=BOLD
        ).move_to(conclusion_box)

        tokens = ["Hà", "Nội", "."]
        token_objs = VGroup()

        for tok in tokens:
            token = T(tok, size=26, color=YELLOW, weight=BOLD)
            token_objs.add(token)

        token_objs.arrange(RIGHT, buff=0.18).next_to(next_box, RIGHT, buff=0.55)
        align_texts_to_baseline(next_text, token_objs[0], token_objs[1], token_objs[2])

        wait_until(61.62)
        self.play(
            FadeOut(analogy_box),
            FadeOut(analogy_text),
            run_time=0.4
        )
        self.play(
            FadeIn(conclusion_box),
            Write(conclusion_text),
            run_time=0.8
        )
        curr_time += 1.2

        # Token 1: "Hà"
        wait_until(63.00)
        self.play(
            FadeIn(token_objs[0], shift=UP * 0.12),
            Flash(next_box, color=YELLOW, flash_radius=0.6),
            Indicate(cache_box, color=GREEN, scale_factor=1.03),
            run_time=0.5
        )
        curr_time += 0.5

        # Token 2: "Nội"
        wait_until(64.20)
        self.play(
            FadeIn(token_objs[1], shift=UP * 0.12),
            Flash(next_box, color=YELLOW, flash_radius=0.6),
            Indicate(cache_box, color=GREEN, scale_factor=1.03),
            run_time=0.5
        )
        curr_time += 0.5

        # Token 3: "."
        wait_until(65.40)
        self.play(
            FadeIn(token_objs[2], shift=UP * 0.12),
            Flash(next_box, color=YELLOW, flash_radius=0.6),
            Indicate(cache_box, color=GREEN, scale_factor=1.03),
            run_time=0.5
        )
        curr_time += 0.5

        # Wait until audio finishes
        wait_audio(audio, visual_time=curr_time)
        curr_time = audio_duration(audio)

        # 2.5s visual pause at the end
        self.wait(2.5)
        curr_time += 2.5

        # Fade out everything
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(context_box),
            FadeOut(context_text),
            FadeOut(cache_box),
            FadeOut(cache_text),
            FadeOut(model_box),
            FadeOut(model_text),
            FadeOut(next_box),
            FadeOut(next_text),
            FadeOut(arrow_context),
            FadeOut(arrow_cache),
            FadeOut(arrow_next),
            FadeOut(conclusion_box),
            FadeOut(conclusion_text),
            FadeOut(token_objs),
            run_time=1.2
        )
        curr_time += 1.2
