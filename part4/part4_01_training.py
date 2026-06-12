import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
from main_segoe_theme import *
import os


class Part401Training(Scene):
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

        audio = "voice_part4/p4_01.mp3"
        play_audio(audio)

        # ==========================================
        # PHASE 1: INTRO (0.0s - 11.66s)
        # ==========================================
        title = make_title("Training, Inference và Serving")
        subtitle = make_subtitle("Ba khái niệm cốt lõi", title)

        self.play(Write(title), run_time=1.2)
        curr_time += 1.2
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Concept boxes (Training, Inference, Serving)
        concept1_box = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.15, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=FILL_SOFT)
        concept1_text = VGroup(
            T("Training", size=24, color=YELLOW, weight=BOLD),
            T("Huấn luyện", size=18, color=WHITE)
        ).arrange(DOWN, buff=0.12)

        concept2_box = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.15, stroke_color=BLUE, fill_color=BLUE, fill_opacity=FILL_SOFT)
        concept2_text = VGroup(
            T("Inference", size=24, color=BLUE, weight=BOLD),
            T("Suy luận", size=18, color=WHITE)
        ).arrange(DOWN, buff=0.12)

        concept3_box = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.15, stroke_color=GREEN, fill_color=GREEN, fill_opacity=FILL_SOFT)
        concept3_text = VGroup(
            T("Serving", size=24, color=GREEN, weight=BOLD),
            T("Phục vụ", size=18, color=WHITE)
        ).arrange(DOWN, buff=0.12)

        # Baseline alignment for text inside concept boxes
        ref_char = get_first_character(concept1_text[0])
        ref_y = ref_char.get_bottom()[1]
        for text_grp in [concept2_text, concept3_text]:
            char_to_align = get_first_character(text_grp[0])
            dy = ref_y - char_to_align.get_bottom()[1]
            text_grp.shift(UP * dy)

        # Center boxes around aligned texts
        concept1_box.move_to(concept1_text.get_center())
        concept2_box.move_to(concept2_text.get_center())
        concept3_box.move_to(concept3_text.get_center())

        concept1 = VGroup(concept1_box, concept1_text)
        concept2 = VGroup(concept2_box, concept2_text)
        concept3 = VGroup(concept3_box, concept3_text)

        concepts = VGroup(concept1, concept2, concept3).arrange(RIGHT, buff=0.45).shift(DOWN * 0.5)

        wait_until(7.92)
        self.play(
            LaggedStart(
                FadeIn(concept1, shift=UP),
                FadeIn(concept2, shift=UP),
                FadeIn(concept3, shift=UP),
                lag_ratio=0.25
            ),
            run_time=1.5
        )
        curr_time += 1.5

        wait_until(11.66)

        # ==========================================
        # PHASE 2: TRAINING LOOP (11.66s - 49.00s)
        # ==========================================
        # Fade out intro elements
        self.play(
            FadeOut(concepts),
            FadeOut(subtitle),
            run_time=0.8
        )
        curr_time += 0.8

        subtitle2 = make_subtitle("Khái niệm 1: Training (Huấn luyện mô hình)", title)
        self.play(FadeIn(subtitle2, shift=UP), run_time=0.8)
        curr_time += 0.8

        # Define Training components
        data_title = T("Training Data", size=22, color=YELLOW, weight=BOLD)
        data_items = VGroup(
            T("Văn bản (Text)", size=18, color=WHITE),
            T("Mã nguồn (Code)", size=18, color=WHITE),
            T("Tài liệu (Documents)", size=18, color=WHITE),
            T("Hội thoại (Dialogues)", size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        data_box = RoundedRectangle(
            width=3.6,
            height=2.6,
            corner_radius=0.18,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=FILL_SOFT
        ).move_to(LEFT * 4.2 + DOWN * 0.2)

        data_title.next_to(data_box, UP, buff=0.15)
        data_items.move_to(data_box.get_center())

        model_box = RoundedRectangle(
            width=3.2,
            height=1.5,
            corner_radius=0.18,
            stroke_color=PURPLE,
            fill_color=PURPLE,
            fill_opacity=FILL_SOFT
        ).move_to(ORIGIN + DOWN * 0.2)
        model_text = VGroup(
            T("Large Language", size=20, color=PURPLE, weight=BOLD),
            T("Model", size=20, color=PURPLE, weight=BOLD)
        ).arrange(DOWN, buff=0.1).move_to(model_box)

        # Align model text parts baseline
        ref_char_m = get_first_character(model_text[0])
        ref_ym = ref_char_m.get_bottom()[1]
        char_to_align_m = get_first_character(model_text[1])
        model_text[1].shift(UP * (ref_ym - char_to_align_m.get_bottom()[1] - 0.45)) # manual vertical offset since it's stacked

        loss_box = RoundedRectangle(
            width=3.0,
            height=1.1,
            corner_radius=0.18,
            stroke_color=RED,
            fill_color=RED,
            fill_opacity=FILL_SOFT
        ).move_to(RIGHT * 4.2 + UP * 0.8)
        loss_text = T("Prediction Error", size=18, color=RED, weight=BOLD).move_to(loss_box)

        weights_box = RoundedRectangle(
            width=3.0,
            height=1.1,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        ).move_to(RIGHT * 4.2 + DOWN * 1.2)
        weights_text = T("Updated Weights", size=18, color=GREEN, weight=BOLD).move_to(weights_box)

        # Arrows
        arrow1 = Arrow(data_box.get_right(), model_box.get_left(), buff=0.15, color=YELLOW)
        arrow2 = Arrow(model_box.get_right() + UP * 0.2, loss_box.get_left(), buff=0.15, color=RED)
        arrow3 = Arrow(loss_box.get_bottom(), weights_box.get_top(), buff=0.15, color=GREEN)
        arrow4 = CurvedArrow(weights_box.get_left(), model_box.get_bottom() + RIGHT * 0.2, angle=-TAU / 4, color=GREEN)
        loop_label = T("repeat many times", size=18, color=MUTED).next_to(arrow4, DOWN, buff=0.1)

        # Small interactive badge for predicting next token
        predict_badge = T("Dự đoán token tiếp theo", size=16, color=YELLOW, weight=BOLD).next_to(model_box, UP, buff=0.15)

        wait_until(13.94)
        self.play(
            FadeIn(data_box),
            FadeIn(data_title),
            FadeIn(model_box),
            FadeIn(model_text),
            Create(arrow1),
            run_time=1.5
        )
        curr_time += 1.5

        wait_until(17.75)
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT) for item in data_items], lag_ratio=0.25),
            run_time=1.8
        )
        curr_time += 1.8

        wait_until(27.43)
        self.play(
            FadeIn(weights_box),
            FadeIn(weights_text),
            Create(arrow4),
            run_time=1.2
        )
        curr_time += 1.2

        wait_until(32.01)
        self.play(
            FadeIn(predict_badge, shift=DOWN),
            run_time=1.0
        )
        curr_time += 1.0

        wait_until(37.73)
        self.play(
            FadeIn(loss_box),
            FadeIn(loss_text),
            Create(arrow2),
            Create(arrow3),
            run_time=1.5
        )
        curr_time += 1.5

        wait_until(44.60)
        self.play(
            FadeIn(loop_label),
            Flash(weights_box, color=GREEN),
            run_time=1.2
        )
        curr_time += 1.2

        wait_until(49.00)

        # ==========================================
        # PHASE 3: RESOURCE WARNING (49.00s - 55.34s)
        # ==========================================
        warning_box = RoundedRectangle(
            width=11.2,
            height=1.3,
            corner_radius=0.18,
            stroke_color=RED,
            fill_color=RED,
            fill_opacity=0.15
        ).to_edge(DOWN, buff=0.45)

        w_label = T("TÀI NGUYÊN KHỔNG LỒ:", size=18, color=RED, weight=BOLD)
        w1 = T("Nhiều GPU", size=18, color=WHITE)
        w2 = T("Thời gian dài", size=18, color=WHITE)
        w3 = T("Chi phí lớn", size=18, color=WHITE)

        warning_content = VGroup(w_label, w1, w2, w3).arrange(RIGHT, buff=0.35)
        
        # Align baseline of warning content items
        ref_char_w = get_first_character(w_label)
        ref_yw = ref_char_w.get_bottom()[1]
        for item in [w1, w2, w3]:
            char_to_align_w = get_first_character(item)
            dy_w = ref_yw - char_to_align_w.get_bottom()[1]
            item.shift(UP * dy_w)

        warning_content.move_to(warning_box)

        self.play(
            FadeIn(warning_box),
            FadeIn(warning_content),
            Flash(warning_box, color=RED),
            run_time=1.5
        )
        curr_time += 1.5

        wait_until(55.34)

        # ==========================================
        # PHASE 4: TRANSITION TO SERVING (55.34s - 72.8s)
        # ==========================================
        # Dim/Fade out training loop components, except Model Box & Model Text
        self.play(
            FadeOut(data_box),
            FadeOut(data_title),
            FadeOut(data_items),
            FadeOut(loss_box),
            FadeOut(loss_text),
            FadeOut(weights_box),
            FadeOut(weights_text),
            FadeOut(warning_box),
            FadeOut(warning_content),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(arrow3),
            FadeOut(arrow4),
            FadeOut(loop_label),
            FadeOut(predict_badge),
            run_time=1.5
        )
        curr_time += 1.5

        # Move Model Box to center
        self.play(
            model_box.animate.move_to(ORIGIN),
            model_text.animate.move_to(ORIGIN),
            run_time=1.2
        )
        curr_time += 1.2

        # Create Model Done badge
        done_badge = T("Huấn luyện hoàn tất", size=18, color=GREEN, weight=BOLD).next_to(model_box, UP, buff=0.25)

        wait_until(60.08)
        self.play(
            FadeIn(done_badge, shift=UP),
            run_time=1.0
        )
        curr_time += 1.0

        # Create Serving Card
        serving_card = RoundedRectangle(
            width=10.6,
            height=1.8,
            corner_radius=0.18,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        ).to_edge(DOWN, buff=0.55)

        serving_title = T("BÀI TOÁN THỰC TẾ: LLM SERVING", size=21, color=GREEN, weight=BOLD)
        serving_desc = T("Làm thế nào để sử dụng và phục vụ mô hình hiệu quả trong thực tế?", size=18, color=WHITE)
        serving_text = VGroup(serving_title, serving_desc).arrange(DOWN, buff=0.18).move_to(serving_card)

        # Baseline align serving card texts
        ref_char_s = get_first_character(serving_title)
        ref_ys = ref_char_s.get_bottom()[1]
        char_to_align_s = get_first_character(serving_desc)
        serving_desc.shift(UP * (ref_ys - char_to_align_s.get_bottom()[1] - 0.45)) # manual vertical offset since stacked

        wait_until(66.17)
        self.play(
            FadeIn(serving_card),
            FadeIn(serving_text),
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
            FadeOut(model_box),
            FadeOut(model_text),
            FadeOut(done_badge),
            FadeOut(serving_card),
            FadeOut(serving_text),
            run_time=1.2
        )
        curr_time += 1.2
