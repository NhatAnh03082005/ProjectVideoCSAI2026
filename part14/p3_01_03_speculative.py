# -*- coding: utf-8 -*-

from manim import *
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.visual_utils import *


class SceneP3SpeculativeDecoding(Scene):
    def construct(self):
        self.camera.background_color = BG

        audio = "voice/p3_01_03_speculative.mp3"
        play_audio(self, audio)
        visual_time = 0

        # =====================================================
        # HELPER
        # =====================================================
        def add_time(duration):
            nonlocal visual_time
            visual_time += duration

        def pause_to(target_time):
            nonlocal visual_time
            delay = max(0, target_time - visual_time)
            if delay > 0:
                self.wait(delay)
                visual_time += delay

        def clear(*mobjects, run_time=0.30):
            nonlocal visual_time
            self.play(
                *[FadeOut(mob) for mob in mobjects],
                run_time=run_time
            )
            visual_time += run_time

        def make_token(text, color=GREEN, width=0.82, font_size=22):
            return token_box(
                text,
                color=color,
                width=width,
                height=0.58,
                font_size=font_size
            )

        def bottom_note(text, font_size=21, color=YELLOW, max_width=10.5):
            note = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=max_width
            )
            note.move_to(DOWN * 2.35)
            return note

        # =====================================================
        # TITLE - INTRO
        # 0s -> 10.8s
        # =====================================================
        title = safe_text(
            "Speculative Decoding",
            font_size=39,
            color=WHITE,
            max_width=11
        )
        title.to_edge(UP, buff=0.42)

        subtitle = safe_text(
            "Model nhỏ đoán nhanh - model lớn kiểm tra",
            font_size=26,
            color=PURPLE,
            max_width=11
        )
        subtitle.next_to(title, DOWN, buff=0.22)

        intro_box = model_box(
            "Giải mã suy đoán",
            PURPLE,
            width=4.35,
            height=0.9,
            font_size=25
        )
        intro_box.move_to(UP * 0.45)

        intro_note = bottom_note(
            "Tăng tốc sinh token nhưng vẫn kiểm soát chất lượng",
            font_size=21,
            color=YELLOW,
            max_width=10.2
        )

        self.play(Write(title), run_time=0.60)
        add_time(0.60)

        pause_to(1.2)

        self.play(FadeIn(subtitle, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(2.8)

        self.play(FadeIn(intro_box, scale=0.96), run_time=0.45)
        add_time(0.45)

        pause_to(5.4)

        self.play(FadeIn(intro_note, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(10.8)

        clear(intro_box, intro_note, run_time=0.25)

        # =====================================================
        # CẢNH 1 - HAI MÔ HÌNH
        # 10.8s -> 30s
        # =====================================================
        two_models_title = safe_text(
            "Ta tưởng tượng có hai mô hình",
            font_size=30,
            color=WHITE,
            max_width=10.5
        )
        two_models_title.next_to(subtitle, DOWN, buff=0.42)

        target = model_box(
            "Target Model\nlớn, chính xác",
            PURPLE,
            width=3.35,
            height=1.18,
            font_size=23
        )
        draft = model_box(
            "Draft Model\nnhỏ, nhanh",
            GREEN,
            width=3.35,
            height=1.18,
            font_size=23
        )

        target.move_to(LEFT * 3.0 + UP * 0.05)
        draft.move_to(RIGHT * 3.0 + UP * 0.05)

        target_note = VGroup(
            safe_text("mô hình chính", font_size=20, color=PURPLE, max_width=3.5),
            safe_text("chất lượng cao", font_size=20, color=WHITE, max_width=3.5),
            safe_text("chậm hơn / tốn tài nguyên", font_size=19, color=MUTED, max_width=3.8),
        )
        target_note.arrange(DOWN, buff=0.09)
        target_note.next_to(target, DOWN, buff=0.28)

        draft_note = VGroup(
            safe_text("mô hình nhỏ hơn", font_size=20, color=GREEN, max_width=3.5),
            safe_text("yếu hơn", font_size=20, color=WHITE, max_width=3.5),
            safe_text("nhanh hơn nhiều", font_size=19, color=GREEN, max_width=3.8),
        )
        draft_note.arrange(DOWN, buff=0.09)
        draft_note.next_to(draft, DOWN, buff=0.28)

        pause_to(11.0)

        self.play(Write(two_models_title), run_time=0.40)
        add_time(0.40)

        # Hiện cả hai model sớm, không để voice nói trước hình.
        pause_to(11.8)

        self.play(
            FadeIn(target, shift=UP),
            FadeIn(draft, shift=UP),
            run_time=0.55
        )
        add_time(0.55)

        # Khi voice nói target model, note target đã xuất hiện.
        pause_to(13.6)

        self.play(
            target[0].animate.set_stroke(PURPLE, width=4),
            FadeIn(target_note, shift=UP),
            run_time=0.45
        )
        add_time(0.45)

        # Khi voice chuyển sang draft model, draft đã có sẵn và được highlight.
        pause_to(20.0)

        self.play(
            draft[0].animate.set_stroke(GREEN, width=4),
            FadeIn(draft_note, shift=UP),
            run_time=0.45
        )
        add_time(0.45)

        pause_to(29.7)

        clear(two_models_title, target, draft, target_note, draft_note, run_time=0.30)

        # =====================================================
        # CẢNH 2 - DRAFT ĐOÁN TRƯỚC
        # 30s -> 51s
        # =====================================================
        pipeline_title = safe_text(
            "Draft model đoán trước vài token",
            font_size=29,
            color=WHITE,
            max_width=11
        )
        pipeline_title.next_to(subtitle, DOWN, buff=0.42)

        draft_small = model_box(
            "Draft Model\nđoán nhanh",
            GREEN,
            width=2.75,
            height=1.05,
            font_size=22
        )
        target_large = model_box(
            "Target Model\nkiểm tra",
            PURPLE,
            width=2.75,
            height=1.05,
            font_size=22
        )

        draft_small.move_to(LEFT * 4.05 + UP * 0.3)
        target_large.move_to(RIGHT * 4.05 + UP * 0.3)

        draft_tokens = VGroup(
            make_token("Hà", GREEN),
            make_token("Nội", GREEN),
            make_token("là", GREEN),
            make_token("thủ", GREEN, width=0.88),
            make_token("đô", GREEN),
        )
        draft_tokens.arrange(RIGHT, buff=0.16)
        draft_tokens.move_to(DOWN * 0.15)

        draft_arrow = Arrow(
            draft_small.get_right(),
            draft_tokens.get_left(),
            color=GREEN,
            stroke_width=3,
            buff=0.15
        )

        verify_arrow = Arrow(
            draft_tokens.get_right(),
            target_large.get_left(),
            color=PURPLE,
            stroke_width=3,
            buff=0.15
        )

        draft_label = bottom_note(
            "Draft model viết nháp thật nhanh",
            font_size=21,
            color=GREEN
        )

        verify_label = safe_text(
            "Target model kiểm tra bản nháp",
            font_size=22,
            color=PURPLE,
            max_width=7
        )
        verify_label.next_to(draft_tokens, UP, buff=0.55)

        pause_to(30.0)

        self.play(Write(pipeline_title), run_time=0.40)
        add_time(0.40)

        pause_to(31.2)

        self.play(FadeIn(draft_small), FadeIn(target_large), run_time=0.45)
        add_time(0.45)

        pause_to(33.4)

        self.play(Create(draft_arrow), FadeIn(draft_label, shift=UP), run_time=0.40)
        add_time(0.40)

        # Token hiện sớm hơn lời đọc một chút.
        token_times = [38.5, 39.3, 40.1, 40.9, 41.7]

        for tok, target_time in zip(draft_tokens, token_times):
            pause_to(target_time)
            self.play(FadeIn(tok, scale=0.85), run_time=0.20)
            add_time(0.20)

        pause_to(45.8)

        self.play(FadeOut(draft_label), run_time=0.18)
        add_time(0.18)

        self.play(Create(verify_arrow), FadeIn(verify_label, shift=UP), run_time=0.45)
        add_time(0.45)

        pause_to(51.0)

        # =====================================================
        # CẢNH 3 - BẢN NHÁP ĐÚNG: ACCEPT
        # 51s -> 70s
        # =====================================================
        ok_marks = VGroup()
        for tok in draft_tokens:
            mark = Text("OK", font=FONT, font_size=25, color=GREEN)
            mark.next_to(tok, UP, buff=0.12)
            ok_marks.add(mark)

        accept_brace = Brace(draft_tokens, DOWN, color=GREEN)
        accept_text = safe_text(
            "Bản nháp đúng -> accept nhiều token cùng lúc",
            font_size=20,
            color=GREEN,
            max_width=7.8
        )
        accept_text.next_to(accept_brace, DOWN, buff=0.12)

        sequential_note = bottom_note(
            "Không cần sinh Hà, rồi Nội, rồi là, rồi thủ, rồi đô một cách tuần tự",
            font_size=20,
            color=YELLOW,
            max_width=10.2
        )

        # OK xuất hiện ngay khi voice nói target model kiểm tra và chấp nhận.
        pause_to(46.2)

        self.play(
            LaggedStart(
                *[FadeIn(m, scale=1.1) for m in ok_marks],
                lag_ratio=0.04
            ),
            run_time=0.48
        )
        add_time(0.48)

        pause_to(48.8)

        self.play(Create(accept_brace), FadeIn(accept_text, shift=UP), run_time=0.45)
        add_time(0.45)

        pause_to(51.0)

        self.play(FadeIn(sequential_note, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(52.2)

        clear(
            pipeline_title,
            ok_marks,
            accept_brace,
            accept_text,
            sequential_note,
            verify_label,
            draft_tokens,
            run_time=0.25
        )

        # =====================================================
        # CẢNH 4 - BẢN NHÁP SAI: FALLBACK
        # 53s -> 60s
        # =====================================================
        wrong_title = safe_text(
            "Nếu bản nháp sai ở một token...",
            font_size=27,
            color=RED,
            max_width=10
        )
        wrong_title.next_to(subtitle, DOWN, buff=0.42)

        bad_tokens = VGroup(
            make_token("Hà", GREEN),
            make_token("Nội", GREEN),
            make_token("là", GREEN),
            make_token("thủ", GREEN, width=0.88),
            make_token("thức", RED, width=0.95),
        )
        bad_tokens.arrange(RIGHT, buff=0.16)
        bad_tokens.move_to(DOWN * 0.12)

        bad_marks = VGroup()
        for i, tok in enumerate(bad_tokens):
            if i < 4:
                mark = Text("OK", font=FONT, font_size=24, color=GREEN)
            else:
                mark = Text("X", font=FONT, font_size=27, color=RED)
            mark.next_to(tok, UP, buff=0.12)
            bad_marks.add(mark)

        bad_cross = Cross(bad_tokens[-1], stroke_color=RED, stroke_width=5)

        fallback_box = model_box(
            "Dừng tại token sai\n-> target model sinh tiếp",
            RED,
            width=4.9,
            height=1.0,
            font_size=21
        )
        fallback_box.move_to(DOWN * 1.45)

        pause_to(52.6)

        self.play(Write(wrong_title), run_time=0.40)
        add_time(0.40)

        pause_to(53.4)

        self.play(
            LaggedStart(
                *[FadeIn(tok, scale=0.85) for tok in bad_tokens],
                lag_ratio=0.04
            ),
            run_time=0.55
        )
        add_time(0.55)

        pause_to(59.8)

        self.play(
            LaggedStart(
                *[FadeIn(m, scale=1.1) for m in bad_marks],
                lag_ratio=0.035
            ),
            run_time=0.45
        )
        add_time(0.45)

        pause_to(62.7)

        self.play(Create(bad_cross), run_time=0.28)
        add_time(0.28)

        pause_to(65.0)

        self.play(FadeIn(fallback_box, shift=UP), run_time=0.45)
        add_time(0.45)

        pause_to(71.0)

        clear(
            draft_small,
            target_large,
            draft_arrow,
            verify_arrow,
            wrong_title,
            bad_tokens,
            bad_marks,
            bad_cross,
            fallback_box,
            run_time=0.30
        )

        # =====================================================
        # CẢNH 5 - ẨN DỤ + VAI TRÒ HAI MODEL
        # 71s -> 97s
        # =====================================================
        role_title = safe_text(
            "Trợ lý viết nháp - chuyên gia kiểm tra",
            font_size=29,
            color=WHITE,
            max_width=11
        )
        role_title.next_to(subtitle, DOWN, buff=0.42)

        assistant_box = model_box(
            "Draft model\nviết nháp nhanh",
            GREEN,
            width=3.45,
            height=1.1,
            font_size=23
        )

        expert_box = model_box(
            "Target model\nkiểm tra & quyết định",
            PURPLE,
            width=3.95,
            height=1.1,
            font_size=23
        )

        assistant_box.move_to(LEFT * 3.0 + UP * 0.1)
        expert_box.move_to(RIGHT * 3.0 + UP * 0.1)

        role_arrow = Arrow(
            assistant_box.get_right(),
            expert_box.get_left(),
            color=YELLOW,
            stroke_width=3,
            buff=0.22
        )

        role_notes = VGroup(
            model_box("đúng -> accept", GREEN, width=2.65, height=0.68, font_size=20),
            model_box("sai -> sửa", RED, width=2.35, height=0.68, font_size=20),
            model_box("quyết định cuối", YELLOW, width=3.1, height=0.68, font_size=20),
        )
        role_notes.arrange(RIGHT, buff=0.25)
        role_notes.move_to(DOWN * 1.35)

        role_bottom = bottom_note(
            "Model nhỏ không trả lời thay model lớn.",
            font_size=21,
            color=YELLOW
        )

        pause_to(71.4)

        self.play(Write(role_title), run_time=0.40)
        add_time(0.40)

        pause_to(73.2)

        self.play(FadeIn(assistant_box, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(76.0)

        self.play(Create(role_arrow), FadeIn(expert_box, shift=UP), run_time=0.50)
        add_time(0.50)

        pause_to(80.0)

        self.play(FadeIn(role_notes[0], shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(83.7)

        self.play(FadeIn(role_notes[1], shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(87.1)

        self.play(FadeIn(role_bottom, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(93.0)

        self.play(FadeIn(role_notes[2], shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(96.8)

        clear(role_title, assistant_box, expert_box, role_arrow, role_notes, role_bottom, run_time=0.30)

        # =====================================================
        # CẢNH 6 - GIỮ QUYẾT ĐỊNH CỦA MODEL LỚN
        # 97s -> 108s
        # =====================================================
        quality_title = safe_text(
            "Đầu ra vẫn theo model lớn",
            font_size=29,
            color=WHITE,
            max_width=11
        )
        quality_title.next_to(subtitle, DOWN, buff=0.42)

        verify_box = model_box(
            "Kiểm tra đúng\n-> giữ chất lượng",
            PURPLE,
            width=3.85,
            height=1.05,
            font_size=22
        )

        near_box = model_box(
            "Sai\n-> quay lại để sửa",
            RED,
            width=3.85,
            height=1.05,
            font_size=21
        )

        quality_steps = VGroup(verify_box, near_box)
        quality_steps.arrange(RIGHT, buff=0.45)
        quality_steps.move_to(UP * 0.05)

        quality_note = bottom_note(
            "Chỉ thay đổi cách sinh nhanh hơn, không đổi model quyết định cuối cùng.",
            font_size=21,
            color=YELLOW,
            max_width=10.4
        )

        pause_to(97.5)

        self.play(Write(quality_title), run_time=0.40)
        add_time(0.40)

        pause_to(99.0)

        self.play(FadeIn(verify_box, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(102.8)

        self.play(FadeIn(near_box, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(104.0)

        self.play(FadeIn(quality_note, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(108.0)

        clear(quality_title, quality_steps, quality_note, run_time=0.30)

        # =====================================================
        # CẢNH 7 - VÌ SAO NHANH HƠN
        # 108s -> 140s
        # =====================================================
        speed_title = safe_text(
            "Vì sao có thể nhanh hơn?",
            font_size=30,
            color=WHITE,
            max_width=11
        )
        speed_title.next_to(subtitle, DOWN, buff=0.42)

        old_way = model_box(
            "Cách thường\nmodel lớn sinh từng token",
            BLUE,
            width=4.0,
            height=1.15,
            font_size=22
        )

        new_way = model_box(
            "Speculative\nverify cả nhóm token",
            GREEN,
            width=4.0,
            height=1.15,
            font_size=22
        )

        old_way.move_to(LEFT * 2.75 + UP * 0.1)
        new_way.move_to(RIGHT * 2.75 + UP * 0.1)

        speed_arrow = DoubleArrow(
            old_way.get_right(),
            new_way.get_left(),
            color=YELLOW,
            stroke_width=3,
            buff=0.25
        )

        group_tokens = VGroup(
            make_token("Hà", GREEN),
            make_token("Nội", GREEN),
            make_token("là", GREEN),
            make_token("...", GREEN),
        )
        group_tokens.arrange(RIGHT, buff=0.13)
        group_tokens.move_to(DOWN * 1.25)

        group_box = SurroundingRectangle(
            group_tokens,
            color=YELLOW,
            buff=0.14,
            corner_radius=0.12
        )

        speed_note = bottom_note(
            "Nếu draft đoán tốt, số lần gọi model lớn giảm xuống.",
            font_size=21,
            color=YELLOW
        )

        pause_to(108.4)

        self.play(Write(speed_title), run_time=0.40)
        add_time(0.40)

        pause_to(116.6)

        self.play(FadeIn(old_way, shift=LEFT), run_time=0.40)
        add_time(0.40)

        pause_to(123.0)

        self.play(Create(speed_arrow), FadeIn(new_way, shift=RIGHT), run_time=0.50)
        add_time(0.50)

        pause_to(130.8)

        self.play(
            FadeIn(group_tokens, scale=0.9),
            Create(group_box),
            run_time=0.50
        )
        add_time(0.50)

        pause_to(138.0)

        self.play(FadeIn(speed_note, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(140.0)

        clear(speed_title, old_way, new_way, speed_arrow, group_tokens, group_box, speed_note, run_time=0.30)

        # =====================================================
        # CẢNH 8 - KHI NÀO HIỆU QUẢ
        # 140s -> 156s
        # =====================================================
        limit_title = safe_text(
            "Khi nào tăng tốc hiệu quả?",
            font_size=30,
            color=WHITE,
            max_width=11
        )
        limit_title.next_to(subtitle, DOWN, buff=0.42)

        good_case = model_box(
            "Draft nhanh\nvà đoán gần target",
            GREEN,
            width=4.1,
            height=1.15,
            font_size=22
        )

        bad_case = model_box(
            "Draft sai nhiều\n-> sửa liên tục",
            RED,
            width=4.1,
            height=1.15,
            font_size=22
        )

        good_case.move_to(LEFT * 2.75 + UP * 0.15)
        bad_case.move_to(RIGHT * 2.75 + UP * 0.15)

        limit_note = bottom_note(
            "Draft model càng đoán gần target model, lợi ích tăng tốc càng rõ.",
            font_size=21,
            color=YELLOW
        )

        pause_to(140.8)

        self.play(Write(limit_title), run_time=0.40)
        add_time(0.40)

        pause_to(145.6)

        self.play(FadeIn(good_case, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(150.8)

        self.play(FadeIn(bad_case, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(153.8)

        self.play(FadeIn(limit_note, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(156.0)

        clear(limit_title, good_case, bad_case, limit_note, run_time=0.30)

        # =====================================================
        # CẢNH 9 - TÓM TẮT
        # 156s -> hết
        # =====================================================
        summary_title = safe_text(
            "Tóm tắt Speculative Decoding",
            font_size=30,
            color=YELLOW,
            max_width=11
        )
        summary_title.next_to(subtitle, DOWN, buff=0.42)

        step1 = model_box(
            "1. Model nhỏ\nđoán nhanh",
            GREEN,
            width=3.1,
            height=1.05,
            font_size=22
        )

        step2 = model_box(
            "2. Model lớn\nkiểm tra",
            PURPLE,
            width=3.1,
            height=1.05,
            font_size=22
        )

        step3 = model_box(
            "3. Sinh nhiều token\nmỗi bước suy luận",
            YELLOW,
            width=3.65,
            height=1.05,
            font_size=21
        )

        summary_steps = VGroup(step1, step2, step3)
        summary_steps.arrange(RIGHT, buff=0.35)
        summary_steps.move_to(UP * 0.0)

        s_arrow1 = Arrow(
            step1.get_right(),
            step2.get_left(),
            color=MUTED,
            stroke_width=2.5,
            buff=0.12
        )

        s_arrow2 = Arrow(
            step2.get_right(),
            step3.get_left(),
            color=MUTED,
            stroke_width=2.5,
            buff=0.12
        )

        # innovation_note = bottom_note(
        #     "Algorithmic Innovation: thay đổi cách quá trình sinh token diễn ra.",
        #     font_size=21,
        #     color=BLUE,
        #     max_width=10.5
        # )

        pause_to(156.7)

        self.play(Write(summary_title), run_time=0.40)
        add_time(0.40)

        pause_to(158.7)

        self.play(FadeIn(step1, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(160.6)

        self.play(Create(s_arrow1), FadeIn(step2, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(162.2)

        self.play(Create(s_arrow2), FadeIn(step3, shift=UP), run_time=0.40)
        add_time(0.40)

        pause_to(163.6)

        # self.play(FadeIn(innovation_note, shift=UP), run_time=0.35)
        # add_time(0.35)

        wait_audio(self, audio, visual_time)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(summary_title),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(s_arrow1),
            FadeOut(s_arrow2),
            # FadeOut(innovation_note),
            run_time=0.8
        )
