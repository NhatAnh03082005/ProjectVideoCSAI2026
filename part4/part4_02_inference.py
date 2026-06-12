import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part402Inference(Scene):
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

        def get_first_character(obj):
            while isinstance(obj, VGroup) and not isinstance(obj, Text) and len(obj) > 0:
                obj = obj[0]
            if isinstance(obj, Text) and len(obj) > 0:
                if hasattr(obj, "text") and obj.text:
                    for idx, char in enumerate(obj.text):
                        if char not in ['"', "'", "“", "”", "‘", "’", "(", "[", "{"]:
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

        audio = "voice_part4/p4_02.mp3"
        play_audio(audio)

        # ==========================================
        # PHASE 1: INTRO & HIGH-LEVEL DIAGRAM (0.0s - 19.02s)
        # ==========================================
        title = make_title("Inference (Suy luận)")
        subtitle = make_subtitle("Dùng model đã huấn luyện để tạo ra kết quả", title)

        self.play(Write(title), run_time=1.1)
        curr_time += 1.1
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Prompt -> Tokens -> Model -> Answer
        prompt_box = RoundedRectangle(
            width=2.5,
            height=1.0,
            corner_radius=0.16,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=FILL_SOFT
        )
        prompt_text = T("Prompt", size=22, color=BLUE, weight=BOLD).move_to(prompt_box)

        tokenizer_box = RoundedRectangle(
            width=2.5,
            height=1.0,
            corner_radius=0.16,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        )
        tokenizer_text = T("Mã hóa", size=22, color=YELLOW, weight=BOLD).move_to(tokenizer_box)

        model_box = RoundedRectangle(
            width=2.6,
            height=1.1,
            corner_radius=0.16,
            stroke_color=PURPLE,
            fill_color=PURPLE,
            fill_opacity=FILL_SOFT
        )
        model_text = T("Mô hình", size=22, color=PURPLE, weight=BOLD).move_to(model_box)

        answer_box = RoundedRectangle(
            width=2.5,
            height=1.0,
            corner_radius=0.16,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        )
        answer_text = T("Kết quả", size=22, color=GREEN, weight=BOLD).move_to(answer_box)

        nodes = VGroup(
            VGroup(prompt_box, prompt_text),
            VGroup(tokenizer_box, tokenizer_text),
            VGroup(model_box, model_text),
            VGroup(answer_box, answer_text)
        ).arrange(RIGHT, buff=0.42).shift(UP * 0.8)

        # Baseline align box texts
        align_texts_to_baseline(prompt_text, tokenizer_text, model_text, answer_text)

        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrows.add(Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.12, color=WHITE))

        wait_until(3.5)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in nodes], lag_ratio=0.2), run_time=2.0)
        curr_time += 2.0
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=1.0)
        curr_time += 1.0

        # Example prompt bubble
        prompt_bubble_box = RoundedRectangle(
            width=5.8,
            height=0.75,
            corner_radius=0.12,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.08
        ).next_to(prompt_box, DOWN, buff=0.35).align_to(prompt_box, LEFT)

        prompt_bubble_text = T('Prompt: "Hãy giải thích Transformer là gì"', size=17, color=BLUE, weight=BOLD).move_to(prompt_bubble_box)

        wait_until(8.50)
        self.play(FadeIn(prompt_bubble_box), FadeIn(prompt_bubble_text), run_time=1.0)
        curr_time += 1.0

        # Flow indications
        wait_until(13.5)
        self.play(Indicate(prompt_box, color=BLUE), run_time=1.0)
        curr_time += 1.0
        self.play(Indicate(tokenizer_box, color=YELLOW), run_time=1.0)
        curr_time += 1.0
        self.play(Indicate(model_box, color=PURPLE), run_time=1.0)
        curr_time += 1.0
        self.play(Indicate(answer_box, color=GREEN), run_time=1.0)
        curr_time += 1.0

        # ==========================================
        # PHASE 2: COMPARISON (19.02s - 25.79s)
        # ==========================================
        # Comparison box
        comparison_box = RoundedRectangle(
            width=9.0,
            height=1.7,
            corner_radius=0.18,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).to_edge(DOWN, buff=0.45)

        comp_title = T("SO SÁNH TRỰC QUAN:", size=18, color=YELLOW, weight=BOLD)
        comp_t1 = T("• Training: Dạy học sinh học tập dữ liệu", size=18, color=WHITE)
        comp_t2 = T("• Inference: Hỏi và nhận câu trả lời từ học sinh", size=18, color=WHITE)
        comp_content = VGroup(comp_title, comp_t1, comp_t2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if comp_content.width > 8.0:
            comp_content.scale_to_fit_width(8.0)
        comp_content.move_to(comparison_box)

        wait_until(20.00)
        self.play(FadeIn(comparison_box), FadeIn(comp_content), run_time=1.5)
        curr_time += 1.5

        wait_until(25.79)

        # ==========================================
        # PHASE 3: TOKEN-BY-TOKEN LOOP (25.79s - 47.56s)
        # ==========================================
        # Fade out diagram and comparison elements
        self.play(
            FadeOut(nodes),
            FadeOut(arrows),
            FadeOut(prompt_bubble_box),
            FadeOut(prompt_bubble_text),
            FadeOut(comparison_box),
            FadeOut(comp_content),
            FadeOut(subtitle),
            run_time=1.5
        )
        curr_time += 1.5

        subtitle2 = make_subtitle("Suy luận LLM: Sinh từng token (Autoregressive)", title)
        self.play(FadeIn(subtitle2, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Token-by-token loop setup
        loop_title = T(
            "Mô hình sinh kết quả theo từng bước (Step-by-step)",
            size=23,
            color=YELLOW,
            weight=BOLD
        ).shift(UP * 1.5)

        sentence_start = T('"Transformer is"', size=24, color=WHITE)
        token1 = T(" a", size=24, color=GREEN, weight=BOLD)
        token2 = T(" neural", size=24, color=GREEN, weight=BOLD)
        token3 = T(" architecture", size=24, color=GREEN, weight=BOLD)

        stream = VGroup(sentence_start, token1, token2, token3).arrange(RIGHT, buff=0.08)
        stream.move_to(ORIGIN)

        # Align text stream items by baseline
        ref_char_st = get_first_character(sentence_start)
        ref_yst = ref_char_st.get_bottom()[1]
        for t_item in [token1, token2, token3]:
            char_to_align_st = get_first_character(t_item)
            dy_st = ref_yst - char_to_align_st.get_bottom()[1]
            t_item.shift(UP * dy_st)

        cursor = Rectangle(width=0.045, height=0.45, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        cursor.next_to(sentence_start, RIGHT, buff=0.08)

        wait_until(31.09)
        self.play(FadeIn(loop_title, shift=UP), run_time=0.8)
        curr_time += 0.8
        self.play(FadeIn(sentence_start), FadeIn(cursor), run_time=0.8)
        curr_time += 0.8

        wait_until(36.30)
        self.play(
            FadeIn(token1, shift=UP * 0.12),
            cursor.animate.next_to(token1, RIGHT, buff=0.08),
            run_time=0.9
        )
        curr_time += 0.9
        self.play(
            FadeIn(token2, shift=UP * 0.12),
            cursor.animate.next_to(token2, RIGHT, buff=0.08),
            run_time=0.9
        )
        curr_time += 0.9

        wait_until(41.48)
        self.play(
            FadeIn(token3, shift=UP * 0.12),
            cursor.animate.next_to(token3, RIGHT, buff=0.08),
            run_time=0.9
        )
        curr_time += 0.9

        # Highlight final stream
        self.play(
            Flash(stream, color=GREEN),
            run_time=1.0
        )
        curr_time += 1.0

        wait_until(47.56)

        # ==========================================
        # PHASE 4: SPEED REQUIREMENT (47.56s - 54.41s)
        # ==========================================
        # User experience warning box
        speed_box = RoundedRectangle(
            width=9.0,
            height=1.5,
            corner_radius=0.18,
            stroke_color=RED,
            fill_color=RED,
            fill_opacity=0.12
        ).to_edge(DOWN, buff=0.45)

        speed_title = T("YÊU  CẦU  TRẢI  NGHIỆM  NGƯỜI  DÙNG:", size=18, color=RED, weight=BOLD)
        speed_desc = T("Phản hồi không chỉ cần đúng, mà phải đủ nhanh (mượt mà)", size=18, color=WHITE)
        speed_content = VGroup(speed_title, speed_desc).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        if speed_content.width > 8.0:
            speed_content.scale_to_fit_width(8.0)
        speed_content.move_to(speed_box)

        self.play(
            FadeIn(speed_box),
            FadeIn(speed_content),
            Flash(speed_box, color=RED),
            run_time=1.5
        )
        curr_time += 1.5

        wait_until(54.41)

        # ==========================================
        # PHASE 5: SYSTEM SERVING TRANSITION (54.41s - 65.75s)
        # ==========================================
        self.play(
            FadeOut(speed_box),
            FadeOut(speed_content),
            FadeOut(loop_title),
            FadeOut(stream),
            FadeOut(cursor),
            run_time=1.5
        )
        curr_time += 1.5

        # Final Serving Card
        final_serving_box = RoundedRectangle(
            width=9.0,
            height=1.8,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        ).move_to(ORIGIN)

        final_serving_title = T("BÀI TOÁN TIẾP THEO: SYSTEM SERVING", size=21, color=GREEN, weight=BOLD)
        final_serving_desc = T("Inference đơn lẻ chưa đủ — cần hệ thống để phục vụ nhiều người cùng lúc.", size=18, color=WHITE)
        final_serving_text = VGroup(final_serving_title, final_serving_desc).arrange(DOWN, buff=0.22)
        if final_serving_text.width > 8.0:
            final_serving_text.scale_to_fit_width(8.0)
        final_serving_text.move_to(final_serving_box)

        wait_until(56.50)
        self.play(
            FadeIn(final_serving_box),
            FadeIn(final_serving_text),
            run_time=1.5
        )
        curr_time += 1.5

        # Wait until audio finishes
        wait_audio(audio, visual_time=curr_time)
        curr_time = audio_duration(audio)

        # Fade out everything at the very end
        self.play(
            FadeOut(title),
            FadeOut(subtitle2),
            FadeOut(final_serving_box),
            FadeOut(final_serving_text),
            run_time=1.2
        )
        curr_time += 1.2