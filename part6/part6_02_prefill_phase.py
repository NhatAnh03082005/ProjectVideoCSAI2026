import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part602PrefillPhase(Scene):
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

        # Timestamps tracking
        curr_time = 0

        def wait_until(target_time):
            nonlocal curr_time
            wait_duration = target_time - curr_time
            if wait_duration > 0.05:
                self.wait(wait_duration)
                curr_time = target_time

        audio = "voice_part6/p6_02.mp3"
        play_audio(audio)

        # Title & Subtitle (0.00s)
        title = T(
            "Prefill / Context Phase",
            size=42,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "Xử lý toàn bộ prompt ban đầu và tạo KV Cache",
            size=23,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # 3.40s: "Trong pờ rì phiu, hệ thống nhận pờ rom ban đầu từ người dùng."
        prompt_box = RoundedRectangle(
            width=10.6,
            height=1.1,
            corner_radius=0.18,
            stroke_color=BLUE,
            fill_color="#0a1424",
            fill_opacity=0.92
        ).shift(UP * 1.55)

        prompt_label = T(
            'Prompt: "Hãy tóm tắt tài liệu sau..."',
            size=24,
            color=WHITE,
            weight=BOLD
        ).move_to(prompt_box)

        wait_until(3.40)
        self.play(FadeIn(prompt_box), Write(prompt_label), run_time=1.2)
        curr_time += 1.2

        # 7.95s: "pờ rom này được tóc cần nai dờ chuyển thành một chuỗi tóc cần."
        token_title = T(
            "Tokenizer converts prompt into tokens",
            size=24,
            color=YELLOW,
            weight=BOLD
        ).next_to(prompt_box, DOWN, buff=0.35)

        token_texts = ["Hãy", "tóm", "tắt", "tài", "liệu", "sau", "..."]
        token_group = VGroup()

        for tok in token_texts:
            box = RoundedRectangle(
                width=1.05,
                height=0.65,
                corner_radius=0.12,
                stroke_color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=FILL_SOFT
            )
            label = T(tok, size=19, color=YELLOW, weight=BOLD).move_to(box)
            token_group.add(VGroup(box, label))

        token_group.arrange(RIGHT, buff=0.18).next_to(token_title, DOWN, buff=0.32)

        wait_until(7.95)
        self.play(FadeIn(token_title, shift=UP), run_time=0.8)
        curr_time += 0.8
        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in token_group], lag_ratio=0.1),
            run_time=1.2
        )
        curr_time += 1.2

        # 12.15s: "Sau đó, toàn bộ chuỗi tóc cần của pờ rom được đưa qua mô hình."
        model_box = RoundedRectangle(
            width=4.5,
            height=1.2,
            corner_radius=0.18,
            stroke_color=PURPLE,
            fill_color="#171127",
            fill_opacity=0.95
        ).shift(DOWN * 1.75 + LEFT * 2.4)

        model_text = T(
            "LLM Prefill\nprocess all prompt tokens",
            size=22,
            color=PURPLE,
            weight=BOLD
        ).move_to(model_box)

        arrow1 = Arrow(token_group.get_bottom(), model_box.get_top(), buff=0.15, color=WHITE)

        wait_until(12.15)
        self.play(FadeIn(model_box), FadeIn(model_text), Create(arrow1), run_time=1.2)
        curr_time += 1.2

        # 16.90s: "Điểm quan trọng là các tóc cần trong pờ rom đã có sẵn ngay từ đầu."
        parallel_note = T(
            "Prompt tokens are already available at the start",
            size=22,
            color=YELLOW,
            weight=BOLD
        ).to_edge(DOWN, buff=0.65)

        wait_until(16.90)
        self.play(FadeIn(parallel_note, shift=UP), run_time=1.0)
        curr_time += 1.0

        # 21.45s: "Vì vậy, trong nhiều trường hợp, mô hình có thể xử lý nhiều tóc cần của pờ rom song song..."
        parallel_note_2 = T(
            "Enables parallel processing of all prompt tokens",
            size=22,
            color=GREEN,
            weight=BOLD
        ).to_edge(DOWN, buff=0.65)

        wait_until(21.45)
        self.play(
            FadeOut(parallel_note),
            FadeIn(parallel_note_2, shift=UP),
            *[Indicate(tok, color=YELLOW, scale_factor=1.12) for tok in token_group],
            run_time=1.2
        )
        curr_time += 1.2

        # 28.55s: "Đây là lý do pờ rì phiu thường có đặc điểm com piu in ten sịp."
        line1 = T(
            "Prefill Bottleneck: Compute-bound (highly parallel)",
            size=22,
            color=RED,
            weight=BOLD
        ).to_edge(DOWN, buff=0.65)

        wait_until(28.55)
        self.play(FadeOut(parallel_note_2), FadeIn(line1, shift=UP), run_time=1.0)
        curr_time += 1.0

        # 33.05s: "Nghĩa là nó cần nhiều phép tính, đặc biệt khi pờ rom dài."
        line2 = T(
            "Requires heavy matrix multiplication, especially for long prompts",
            size=19,
            color=WHITE
        )

        wait_until(33.05)
        self.play(
            line1.animate.shift(UP * 0.25),
            FadeIn(line2.next_to(line1, DOWN, buff=0.12).shift(UP * 0.25), shift=UP),
            run_time=1.0
        )
        curr_time += 1.0

        # 37.30s: "Ví dụ, nếu người dùng đưa vào một tài liệu dài..."
        long_prompt_label = T(
            'Prompt: "[Long Document / Code ... 2000+ tokens]"',
            size=24,
            color=YELLOW,
            weight=BOLD
        ).move_to(prompt_box)

        long_doc_note = T(
            "Must process the entire context before generating the first token",
            size=19,
            color=YELLOW
        ).to_edge(DOWN, buff=0.15)

        wait_until(37.30)
        self.play(
            Transform(prompt_label, long_prompt_label),
            prompt_box.animate.set_stroke(color=YELLOW),
            FadeIn(long_doc_note, shift=UP),
            run_time=1.2
        )
        curr_time += 1.2

        # 45.80s: "Pha pờ rì phiu cũng là lúc hệ thống tạo ra K V két ban đầu."
        cache_box = RoundedRectangle(
            width=4.5,
            height=1.2,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color="#102018",
            fill_opacity=0.95
        ).shift(DOWN * 1.75 + RIGHT * 2.8)

        cache_text = T(
            "Initial KV Cache\nfor prompt tokens",
            size=22,
            color=GREEN,
            weight=BOLD
        ).move_to(cache_box)

        arrow2 = Arrow(model_box.get_right(), cache_box.get_left(), buff=0.15, color=GREEN)

        wait_until(45.80)
        self.play(
            FadeOut(line1),
            FadeOut(line2),
            FadeOut(long_doc_note),
            FadeIn(cache_box),
            FadeIn(cache_text),
            Create(arrow2),
            run_time=1.5
        )
        curr_time += 1.5

        # 50.15s: "K V két lưu lại thông tin ki và va liu của các tóc cần..."
        kv_note = T(
            "KV Cache stores Key and Value tensors of prompt tokens",
            size=22,
            color=GREEN,
            weight=BOLD
        ).to_edge(DOWN, buff=0.65)

        wait_until(50.15)
        self.play(FadeIn(kv_note, shift=UP), run_time=1.0)
        curr_time += 1.0

        # 55.05s: "Những thông tin này sẽ được tái sử dụng ở các bước đì cốt sau."
        reuse_note = T(
            "Reused in subsequent Decode steps to avoid recomputing",
            size=19,
            color=WHITE
        )

        wait_until(55.05)
        self.play(
            kv_note.animate.shift(UP * 0.25),
            FadeIn(reuse_note.next_to(kv_note, DOWN, buff=0.12).shift(UP * 0.25), shift=UP),
            run_time=1.0
        )
        curr_time += 1.0

        # 59.30s: "Nhờ vậy, khi sinh tóc cần mới, mô hình không cần tính lại toàn bộ pờ rom từ đầu."
        wait_until(59.30)
        self.play(
            Flash(cache_box, color=GREEN, flash_radius=1.5),
            Indicate(cache_box, color=GREEN, scale_factor=1.05),
            run_time=1.2
        )
        curr_time += 1.2

        # 65.30s: "Đây là nền tảng quan trọng giúp in phờ rần của eo, eo, em khả thi hơn trong thực tế."
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
            "KV Cache is the foundation for efficient LLM serving",
            size=22,
            color=YELLOW,
            weight=BOLD
        ).move_to(conclusion_box)

        wait_until(65.30)
        self.play(
            FadeOut(kv_note),
            FadeOut(reuse_note),
            FadeIn(conclusion_box),
            Write(conclusion_text),
            Flash(cache_box, color=YELLOW, flash_radius=1.5),
            run_time=1.5
        )
        curr_time += 1.5

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
            FadeOut(prompt_box),
            FadeOut(prompt_label),
            FadeOut(token_title),
            FadeOut(token_group),
            FadeOut(model_box),
            FadeOut(model_text),
            FadeOut(cache_box),
            FadeOut(cache_text),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(conclusion_box),
            FadeOut(conclusion_text),
            run_time=1.2
        )
        curr_time += 1.2
