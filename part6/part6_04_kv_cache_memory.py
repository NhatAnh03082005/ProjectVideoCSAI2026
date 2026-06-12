import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part604KVCacheMemory(Scene):
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

        audio = "voice_part6/p6_04.mp3"
        play_audio(audio)

        title = T(
            "KV Cache: faster decode, higher memory usage",
            size=30,
            color=WHITE,
            weight=BOLD
        ).to_edge(UP, buff=0.35)

        subtitle = T(
            "KV Cache giúp tránh tính lại, nhưng chiếm nhiều GPU memory",
            size=22,
            color=BLUE
        ).next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # GPU memory container
        gpu_box = RoundedRectangle(
            width=3.3,
            height=4.3,
            corner_radius=0.2,
            stroke_color=GREEN,
            fill_color="#102018",
            fill_opacity=0.85
        ).shift(LEFT * 3.8 + DOWN * 0.15)

        gpu_title = T(
            "GPU VRAM",
            size=25,
            color=GREEN,
            weight=BOLD
        ).next_to(gpu_box, UP, buff=0.2)

        model_mem = Rectangle(
            width=2.7,
            height=1.2,
            stroke_color=PURPLE,
            fill_color=PURPLE,
            fill_opacity=0.45
        ).move_to(gpu_box.get_center() + DOWN * 1.35)

        model_text = T(
            "Model\nweights",
            size=19,
            color=WHITE,
            weight=BOLD
        ).move_to(model_mem)

        # Initial State (moderate KV Cache)
        kv_mem = Rectangle(
            width=2.7,
            height=0.7,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.55
        ).next_to(model_mem, UP, buff=0.08)

        kv_text = T(
            "KV Cache",
            size=20,
            color=WHITE,
            weight=BOLD
        ).move_to(kv_mem)

        free_mem = Rectangle(
            width=2.7,
            height=1.9,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.25
        ).next_to(kv_mem, UP, buff=0.08)

        free_text = T(
            "Free VRAM",
            size=18,
            color=WHITE,
            weight=BOLD
        ).move_to(free_mem)

        # Factors that grow KV cache
        factor_title = T(
            "KV Cache grows when:",
            size=27,
            color=YELLOW,
            weight=BOLD
        ).shift(RIGHT * 2.4 + UP * 1.55)

        factors = VGroup(
            T("1. Long prompt", size=23, color=WHITE),
            T("2. Long output", size=23, color=WHITE),
            T("3. Large batch size", size=23, color=WHITE),
            T("4. Many concurrent requests", size=23, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        factors.next_to(factor_title, DOWN, buff=0.4)

        # Save states for faded look
        gpu_box.save_state()
        gpu_box.set_stroke(opacity=0.25)
        gpu_box.set_fill(opacity=0.01)

        gpu_title.save_state()
        gpu_title.set_opacity(0.25)

        model_mem.save_state()
        model_mem.set_stroke(opacity=0.25)
        model_mem.set_fill(opacity=0.01)

        kv_mem.save_state()
        kv_mem.set_stroke(opacity=0.25)
        kv_mem.set_fill(opacity=0.01)

        free_mem.save_state()
        free_mem.set_stroke(opacity=0.25)
        free_mem.set_fill(opacity=0.01)

        factor_title.save_state()
        factor_title.set_opacity(0.25)

        for f in factors:
            f.save_state()
            f.set_opacity(0.25)

        # 0.00s: Show faded outlines to avoid empty screens
        self.play(
            FadeIn(gpu_box),
            FadeIn(gpu_title),
            FadeIn(model_mem),
            FadeIn(kv_mem),
            FadeIn(free_mem),
            FadeIn(factor_title),
            FadeIn(factors),
            run_time=1.5
        )
        curr_time += 1.5

        # 7.40s: "Đó là bộ nhớ."
        wait_until(7.40)
        self.play(
            gpu_box.animate.restore(),
            gpu_title.animate.restore(),
            model_mem.animate.restore(),
            kv_mem.animate.restore(),
            free_mem.animate.restore(),
            FadeIn(model_text),
            FadeIn(kv_text),
            FadeIn(free_text),
            run_time=1.2
        )
        curr_time += 1.2

        # 9.52s: "K V két phải lưu ki và va liu..."
        wait_until(9.52)
        self.play(
            Flash(kv_mem, color=YELLOW, flash_radius=1.2),
            Indicate(kv_mem, color=YELLOW, scale_factor=1.05),
            run_time=1.2
        )
        curr_time += 1.2

        # 14.52s: "Khi pờ rom càng dài, két càng lớn." -> State 2
        kv_mem_2 = Rectangle(
            width=2.7,
            height=1.1,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.55
        ).next_to(model_mem, UP, buff=0.08)

        free_mem_2 = Rectangle(
            width=2.7,
            height=1.5,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.25
        ).next_to(kv_mem_2, UP, buff=0.08)

        wait_until(14.52)
        self.play(
            factors[0].animate.restore().set_color(YELLOW),
            Transform(kv_mem, kv_mem_2),
            Transform(free_mem, free_mem_2),
            kv_text.animate.move_to(kv_mem_2),
            free_text.animate.move_to(free_mem_2),
            run_time=1.2
        )
        curr_time += 1.2

        # 17.98s: "Khi câu trả lời càng dài, két cũng tiếp tục tăng." -> State 3
        kv_mem_3 = Rectangle(
            width=2.7,
            height=1.5,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.55
        ).next_to(model_mem, UP, buff=0.08)

        free_mem_3 = Rectangle(
            width=2.7,
            height=1.1,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.25
        ).next_to(kv_mem_3, UP, buff=0.08)

        wait_until(17.98)
        self.play(
            factors[1].animate.restore().set_color(YELLOW),
            Transform(kv_mem, kv_mem_3),
            Transform(free_mem, free_mem_3),
            kv_text.animate.move_to(kv_mem_3),
            free_text.animate.move_to(free_mem_3),
            run_time=1.2
        )
        curr_time += 1.2

        # 21.88s: "Khi bát sai lớn, tức là hệ thống xử lý nhiều rì quét cùng lúc..." -> State 4
        kv_mem_4 = Rectangle(
            width=2.7,
            height=1.9,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.55
        ).next_to(model_mem, UP, buff=0.08)

        free_mem_4 = Rectangle(
            width=2.7,
            height=0.7,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.25
        ).next_to(kv_mem_4, UP, buff=0.08)

        wait_until(21.88)
        self.play(
            factors[2].animate.restore().set_color(YELLOW),
            Transform(kv_mem, kv_mem_4),
            Transform(free_mem, free_mem_4),
            kv_text.animate.move_to(kv_mem_4),
            free_text.animate.move_to(free_mem_4),
            run_time=1.2
        )
        curr_time += 1.2

        # 25.00s: "Và khi có nhiều người dùng đồng thời..." -> State 5
        kv_mem_5 = Rectangle(
            width=2.7,
            height=2.3,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.65
        ).next_to(model_mem, UP, buff=0.08)

        free_mem_5 = Rectangle(
            width=2.7,
            height=0.3,
            stroke_color=RED,
            fill_color=RED,
            fill_opacity=0.35
        ).next_to(kv_mem_5, UP, buff=0.08)

        free_text_small = T("low VRAM", size=11, color=RED, weight=BOLD).move_to(free_mem_5)

        wait_until(25.00)
        self.play(
            factors[3].animate.restore().set_color(YELLOW),
            Transform(kv_mem, kv_mem_5),
            Transform(free_mem, free_mem_5),
            kv_text.animate.move_to(kv_mem_5),
            Transform(free_text, free_text_small),
            run_time=1.2
        )
        curr_time += 1.2

        # 28.73s: "Và khi có nhiều người dùng đồng thời, bộ nhớ G P U có thể nhanh chóng trở thành nút thắt."
        wait_until(28.73)
        self.play(
            Flash(gpu_box, color=RED, flash_radius=2.0),
            Indicate(gpu_box, color=RED, scale_factor=1.03),
            run_time=1.5
        )
        curr_time += 1.5

        # 34.48s: "Đây là lý do đì cốt thường dễ bị mem mo ri bao."
        warning_box = RoundedRectangle(
            width=11.2,
            height=1.0,
            corner_radius=0.18,
            stroke_color=RED,
            fill_color="#1a0c0c",
            fill_opacity=0.9
        ).to_edge(DOWN, buff=0.3)

        warning_text = T(
            "Decode often becomes memory-bound: Speed is limited by reading and writing KV Cache",
            size=16,
            color=WHITE,
            weight=BOLD
        ).move_to(warning_box)
        warning_text.scale_to_fit_width(10.2)

        wait_until(34.48)
        self.play(
            FadeIn(warning_box),
            Write(warning_text),
            run_time=1.2
        )
        curr_time += 1.2

        # 38.26s: "Nghĩa là tốc độ không chỉ bị giới hạn bởi số phép tính, mà còn bị giới hạn bởi việc đọc ghi dữ liệu trong bộ nhớ."
        wait_until(38.26)
        self.play(
            Flash(warning_box, color=RED, flash_radius=1.8),
            Indicate(warning_box, color=RED, scale_factor=1.03),
            run_time=1.5
        )
        curr_time += 1.5

        # 45.25s: "Trong thực tế, một hệ thống sơ ving tốt..."
        solution_box = RoundedRectangle(
            width=11.2,
            height=1.0,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color="#0c1a10",
            fill_opacity=0.9
        ).to_edge(DOWN, buff=0.3)

        solution_text = T(
            "Efficient LLM serving must reuse KV Cache while optimizing memory footprint",
            size=16,
            color=WHITE,
            weight=BOLD
        ).move_to(solution_box)
        solution_text.scale_to_fit_width(10.2)

        wait_until(45.25)
        self.play(
            FadeOut(warning_box),
            FadeOut(warning_text),
            run_time=0.4
        )
        self.play(
            FadeIn(solution_box),
            Write(solution_text),
            run_time=0.8
        )
        curr_time += 1.2

        # 54.26s: "Những vấn đề như pờ rom dài, ao pút dài..."
        wait_until(54.26)
        self.play(
            FadeOut(solution_box),
            FadeOut(solution_text),
            run_time=0.5
        )
        curr_time += 0.5

        # Sequentially highlight factors
        # Factor 1 (55.00s)
        wait_until(55.00)
        self.play(Indicate(factors[0], color=YELLOW, scale_factor=1.12), run_time=0.6)
        curr_time += 0.6

        # Factor 2 (56.50s)
        wait_until(56.50)
        self.play(Indicate(factors[1], color=YELLOW, scale_factor=1.12), run_time=0.6)
        curr_time += 0.6

        # Factor 3 (58.00s)
        wait_until(58.00)
        self.play(Indicate(factors[2], color=YELLOW, scale_factor=1.12), run_time=0.6)
        curr_time += 0.6

        # Factor 4 (59.50s)
        wait_until(59.50)
        self.play(Indicate(factors[3], color=YELLOW, scale_factor=1.12), run_time=0.6)
        curr_time += 0.6

        # 62.72s: "Vì vậy, hiểu pờ rì phiu, đì cốt và K V két..."
        bridge_box = RoundedRectangle(
            width=11.2,
            height=1.2,
            corner_radius=0.18,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=FILL_SOFT
        ).to_edge(ORIGIN)

        bridge_text = T(
            "Next: Latency, Throughput & GPU Memory Bottlenecks",
            size=22,
            color=BLUE,
            weight=BOLD
        ).move_to(bridge_box)
        bridge_text.scale_to_fit_width(10.2)

        wait_until(62.72)
        self.play(
            FadeOut(gpu_box),
            FadeOut(gpu_title),
            FadeOut(model_mem),
            FadeOut(model_text),
            FadeOut(kv_mem),
            FadeOut(kv_text),
            FadeOut(free_mem),
            FadeOut(free_text),
            FadeOut(factor_title),
            FadeOut(factors),
            run_time=0.8
        )
        self.play(
            FadeIn(bridge_box),
            Write(bridge_text),
            run_time=0.8
        )
        curr_time += 1.6

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
            FadeOut(bridge_box),
            FadeOut(bridge_text),
            run_time=1.2
        )
        curr_time += 1.2