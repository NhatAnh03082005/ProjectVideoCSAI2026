# -*- coding: utf-8 -*-

from manim import *
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.visual_utils import *


class SceneP3NonAutoregressive(Scene):
    def construct(self):
        self.camera.background_color = BG

        audio = "voice/p3_01_02_non_ar.mp3"
        play_audio(self, audio)
        visual_time = 0

        # =====================================================
        # HELPER
        # =====================================================
        def make_token(text, color=BLUE, width=0.82, font_size=22):
            return token_box(
                text,
                color=color,
                width=width,
                height=0.58,
                font_size=font_size
            )

        def pause_to(target_time):
            nonlocal visual_time
            delay = max(0, target_time - visual_time)
            if delay > 0:
                self.wait(delay)
                visual_time += delay

        def add_time(duration):
            nonlocal visual_time
            visual_time += duration

        def clear(*mobjects, run_time=0.45):
            nonlocal visual_time
            self.play(
                *[FadeOut(mob) for mob in mobjects],
                run_time=run_time
            )
            visual_time += run_time

        def bottom_note(text, font_size=22, color=YELLOW, max_width=10.2):
            """
            Caption để cao hơn đáy màn hình, tránh bị thanh video che
            và tránh dính vào các object phía dưới.
            """
            t = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=max_width
            )
            t.move_to(DOWN * 2.35)
            return t

        # =====================================================
        # TITLE
        # Voice:
        # Hướng đầu tiên là non-autoregressive decoding...
        # =====================================================
        title = safe_text(
            "Non-autoregressive Decoding",
            font_size=40,
            color=WHITE,
            max_width=11
        )
        title.to_edge(UP, buff=0.45)

        subtitle = safe_text(
            "Sinh nhiều token song song",
            font_size=28,
            color=GREEN,
            max_width=10
        )
        subtitle.next_to(title, DOWN, buff=0.22)

        self.play(Write(title), run_time=0.75)
        add_time(0.75)

        self.play(FadeIn(subtitle, shift=UP), run_time=0.55)
        add_time(0.55)

        intro_note = safe_text(
            "Giải mã không tự hồi quy",
            font_size=28,
            color=YELLOW,
            max_width=8
        )
        intro_note.move_to(UP * 0.35)

        self.play(FadeIn(intro_note, shift=UP), run_time=0.55)
        add_time(0.55)

        pause_to(5.0)

        clear(intro_note, run_time=0.3)

        # =====================================================
        # CẢNH 1 - Ý TƯỞNG SINH SONG SONG
        # Voice:
        # Ý tưởng: thay vì sinh từng token một,
        # sinh nhiều token song song trong cùng một lần.
        # =====================================================
        idea_box = model_box(
            "Ý tưởng:\nsinh nhiều token cùng lúc",
            GREEN,
            width=5.2,
            height=1.2,
            font_size=25
        )
        idea_box.move_to(UP * 0.72)

        parallel_tokens = VGroup(
            make_token("token 1", GREEN, width=1.15),
            make_token("token 2", GREEN, width=1.15),
            make_token("token 3", GREEN, width=1.15),
            make_token("token 4", GREEN, width=1.15),
        )
        parallel_tokens.arrange(RIGHT, buff=0.25)
        parallel_tokens.move_to(DOWN * 0.25)

        source_dot = Dot(color=GREEN, radius=0.07)
        source_dot.next_to(parallel_tokens, DOWN, buff=0.42)

        parallel_arrows = VGroup()
        for tok in parallel_tokens:
            parallel_arrows.add(
                Arrow(
                    source_dot.get_center(),
                    tok.get_bottom(),
                    color=GREEN,
                    stroke_width=2.5,
                    buff=0.08
                )
            )

        idea_caption = bottom_note(
            "Nhiều token được tạo gần như cùng lúc",
            font_size=22,
            color=GREEN
        )

        pause_to(7.1)

        self.play(FadeIn(idea_box, scale=0.96), run_time=0.5)
        add_time(0.5)

        # Khi voice chuyển sang "thay vì sinh từng token một", visual chuẩn bị nguồn sinh.
        pause_to(9.2)

        self.play(FadeIn(source_dot), run_time=0.18)
        add_time(0.18)

        # Khi voice nói "sinh nhiều token song song", mũi tên và token mới xuất hiện.
        pause_to(11.8)

        self.play(
            LaggedStart(
                *[Create(arr) for arr in parallel_arrows],
                lag_ratio=0.03
            ),
            run_time=0.4
        )
        add_time(0.4)

        self.play(
            LaggedStart(
                *[FadeIn(tok, scale=0.85) for tok in parallel_tokens],
                lag_ratio=0.03
            ),
            run_time=0.5
        )
        add_time(0.5)

        self.play(FadeIn(idea_caption, shift=UP), run_time=0.4)
        add_time(0.4)

        pause_to(15.0)

        clear(
            idea_box,
            parallel_tokens,
            parallel_arrows,
            source_dot,
            idea_caption,
            run_time=0.35
        )

        # =====================================================
        # CẢNH 2 - SO SÁNH TRÁI / PHẢI
        # Voice:
        # Trên hình, bên trái là autoregressive...
        # Bên phải là non-autoregressive...
        # =====================================================
        compare_title = safe_text(
            "So sánh hai cách sinh",
            font_size=30,
            color=WHITE,
            max_width=10
        )
        compare_title.next_to(subtitle, DOWN, buff=0.38)

        left_title = safe_text(
            "Autoregressive",
            font_size=27,
            color=BLUE,
            max_width=4.5
        )

        right_title = safe_text(
            "Non-autoregressive",
            font_size=27,
            color=GREEN,
            max_width=5.2
        )

        left_tokens = VGroup(
            make_token("1", BLUE),
            make_token("2", BLUE),
            make_token("3", BLUE),
            make_token("4", BLUE),
        )
        left_tokens.arrange(RIGHT, buff=0.23)

        right_tokens = VGroup(
            make_token("1", GREEN),
            make_token("2", GREEN),
            make_token("3", GREEN),
            make_token("4", GREEN),
        )
        right_tokens.arrange(RIGHT, buff=0.23)

        left_group = VGroup(left_title, left_tokens).arrange(DOWN, buff=0.43)
        right_group = VGroup(right_title, right_tokens).arrange(DOWN, buff=0.43)

        left_group.move_to(LEFT * 3.25 + UP * 0.10)
        right_group.move_to(RIGHT * 3.25 + UP * 0.10)

        divider = DashedLine(
            UP * 1.45,
            DOWN * 1.85,
            color=MUTED,
            stroke_width=2
        )

        left_arrows = VGroup()
        for i in range(len(left_tokens) - 1):
            left_arrows.add(
                Arrow(
                    left_tokens[i].get_right(),
                    left_tokens[i + 1].get_left(),
                    buff=0.08,
                    color=MUTED,
                    stroke_width=2.2
                )
            )

        right_source = Dot(color=GREEN, radius=0.06)
        right_source.next_to(right_tokens, DOWN, buff=0.42)

        right_arrows = VGroup()
        for tok in right_tokens:
            right_arrows.add(
                Arrow(
                    right_source.get_center(),
                    tok.get_bottom(),
                    color=GREEN,
                    stroke_width=2.3,
                    buff=0.08
                )
            )

        left_note = safe_text(
            "1 -> 2 -> 3 -> 4",
            font_size=22,
            color=BLUE,
            max_width=4.2
        )
        left_note.next_to(left_group, DOWN, buff=0.38)

        right_note = safe_text(
            "1, 2, 3, 4 cùng lúc",
            font_size=22,
            color=GREEN,
            max_width=4.8
        )
        right_note.next_to(right_group, DOWN, buff=0.78)

        # compare_caption = bottom_note(
        #     # # "Trái: viết từng chữ. Phải: điền nhiều chữ cùng lúc.",
        #     # font_size=21,
        #     # color=YELLOW
        # )

        pause_to(15.4)

        self.play(Write(compare_title), run_time=0.5)
        add_time(0.5)

        self.play(
            Create(divider),
            FadeIn(left_title),
            FadeIn(right_title),
            run_time=0.6
        )
        add_time(0.6)

        # Bên trái chỉ hiện khi voice nói "Ở bên trái..."
        pause_to(18.6)

        for i, tok in enumerate(left_tokens):
            self.play(FadeIn(tok, scale=0.85), run_time=0.22)
            add_time(0.22)

            if i < len(left_arrows):
                self.play(Create(left_arrows[i]), run_time=0.11)
                add_time(0.11)

        self.play(FadeIn(left_note, shift=UP), run_time=0.32)
        add_time(0.32)

        # Bên phải chỉ hiện khi voice nói "Ở bên phải..."
        pause_to(29.6)

        self.play(FadeIn(right_source), run_time=0.15)
        add_time(0.15)

        self.play(
            LaggedStart(
                *[Create(arr) for arr in right_arrows],
                lag_ratio=0.02
            ),
            run_time=0.32
        )
        add_time(0.32)

        self.play(
            LaggedStart(
                *[FadeIn(tok, scale=0.85) for tok in right_tokens],
                lag_ratio=0.015
            ),
            run_time=0.42
        )
        add_time(0.42)

        self.play(FadeIn(right_note, shift=UP), run_time=0.32)
        add_time(0.32)

        # Caption tổng kết sau khi cả hai bên đã được đọc xong.
        pause_to(36.0)

        # self.play(FadeIn(compare_caption, shift=UP), run_time=0.38)
        # add_time(0.38)

        pause_to(37.0)

        # Xóa caption trước khi hiện box ưu điểm để không bị dính chữ
        # clear(compare_caption, run_time=0.25)

        # =====================================================
        # CẢNH 3 - ƯU ĐIỂM NHANH HƠN
        # Voice:
        # Ưu điểm: tốc độ có thể nhanh hơn...
        # =====================================================
        speed_box = RoundedRectangle(
            width=9.8,
            height=0.82,
            corner_radius=0.16,
            stroke_color=GREEN,
            stroke_width=2,
            fill_color=GREEN,
            fill_opacity=0.10
        )
        speed_box.move_to(DOWN * 2.20)

        speed_text = safe_text(
            "Ưu điểm: nhanh hơn nhờ tận dụng song song",
            font_size=22,
            color=GREEN,
            max_width=9.2
        )
        speed_text.move_to(speed_box.get_center())

        pause_to(38.0)

        self.play(Create(speed_box), FadeIn(speed_text), run_time=0.5)
        add_time(0.5)

        self.play(Flash(right_group, color=GREEN), run_time=0.42)
        add_time(0.42)

        pause_to(45.1)

        clear(speed_box, speed_text, run_time=0.25)

        # =====================================================
        # CẢNH 4 - NHƯỢC ĐIỂM
        # Voice:
        # Nhưng nhược điểm là chất lượng thường khó bằng cách sinh tuần tự.
        # =====================================================
        quality_warning = bottom_note(
            "Nhược điểm: chất lượng thường khó bằng cách sinh tuần tự",
            font_size=22,
            color=RED,
            max_width=10
        )

        pause_to(45.7)

        self.play(FadeIn(quality_warning, shift=UP), run_time=0.45)
        add_time(0.45)

        self.play(
            Flash(left_group, color=BLUE),
            Flash(right_group, color=RED),
            run_time=0.45
        )
        add_time(0.45)

        pause_to(48.5)

        clear(
            compare_title,
            divider,
            left_group,
            right_group,
            left_arrows,
            right_arrows,
            right_source,
            left_note,
            right_note,
            quality_warning,
            run_time=0.4
        )

        # =====================================================
        # CẢNH 5 - PHỤ THUỘC NGÔN NGỮ
        # Voice:
        # Lý do là ngôn ngữ tự nhiên có tính phụ thuộc rất mạnh...
        # =====================================================
        dep_title = safe_text(
            "Ngôn ngữ tự nhiên có tính phụ thuộc mạnh",
            font_size=31,
            color=WHITE,
            max_width=10
        )
        dep_title.next_to(subtitle, DOWN, buff=0.40)

        sentence_tokens = VGroup(
            make_token("trước", BLUE, width=1.05),
            make_token("ảnh", YELLOW, width=0.8),
            make_token("hưởng", YELLOW, width=1.1),
            make_token("sau", GREEN, width=0.8),
        )
        sentence_tokens.arrange(RIGHT, buff=0.18)
        sentence_tokens.move_to(UP * 0.05)

        dep_arrow = CurvedArrow(
            sentence_tokens[0].get_bottom(),
            sentence_tokens[-1].get_bottom(),
            color=YELLOW,
            stroke_width=3,
            angle=-TAU / 5
        )

        dep_note = bottom_note(
            "Token sau phụ thuộc vào token trước",
            font_size=22,
            color=YELLOW,
            max_width=9.5
        )

        # Hiện title ngay khi voice bắt đầu nói "Lý do là..."
        pause_to(49.0)

        self.play(Write(dep_title), run_time=0.5)
        add_time(0.5)

        # Hiện token ngay khi voice nói "token phía sau..."
        pause_to(53.4)

        self.play(
            LaggedStart(
                *[FadeIn(tok, shift=UP) for tok in sentence_tokens],
                lag_ratio=0.07
            ),
            run_time=0.65
        )
        add_time(0.65)

        self.play(Create(dep_arrow), run_time=0.48)
        add_time(0.48)

        self.play(FadeIn(dep_note, shift=UP), run_time=0.38)
        add_time(0.38)

        pause_to(56.8)

        # =====================================================
        # CẢNH 6 - VÍ DỤ ĂN / UỐNG
        # Voice:
        # Ví dụ: nếu đổi từ ăn thành uống...
        # =====================================================
        example_title = safe_text(
            "Một từ đổi -> phần sau đổi theo",
            font_size=28,
            color=YELLOW,
            max_width=10
        )
        example_title.next_to(dep_title, DOWN, buff=0.28)

        old_sentence = VGroup(
            make_token("Tôi", MUTED, width=0.75),
            make_token("ăn", GREEN, width=0.7),
            make_token("cơm", GREEN, width=0.8),
        )
        old_sentence.arrange(RIGHT, buff=0.14)
        old_sentence.move_to(LEFT * 2.55 + DOWN * 0.95)

        new_sentence = VGroup(
            make_token("Tôi", MUTED, width=0.75),
            make_token("uống", RED, width=0.95),
            make_token("nước", RED, width=0.95),
        )
        new_sentence.arrange(RIGHT, buff=0.14)
        new_sentence.move_to(RIGHT * 2.55 + DOWN * 0.95)

        change_arrow = Arrow(
            old_sentence.get_right(),
            new_sentence.get_left(),
            buff=0.25,
            color=YELLOW,
            stroke_width=3
        )

        pause_to(57.1)

        self.play(FadeIn(example_title, shift=UP), run_time=0.45)
        add_time(0.45)

        # Hiện "Tôi ăn cơm" trước khi voice nói "ăn cơm".
        self.play(FadeIn(old_sentence), run_time=0.42)
        add_time(0.42)

        pause_to(64.9)

        # Hiện "Tôi uống nước" khi voice nói "uống nước".
        self.play(Create(change_arrow), FadeIn(new_sentence), run_time=0.58)
        add_time(0.58)

        self.play(
            Flash(new_sentence[1], color=RED),
            Flash(new_sentence[2], color=RED),
            run_time=0.4
        )
        add_time(0.4)

        pause_to(66.8)

        clear(
            dep_title,
            sentence_tokens,
            dep_arrow,
            dep_note,
            example_title,
            old_sentence,
            new_sentence,
            change_arrow,
            run_time=0.4
        )

        # =====================================================
        # CẢNH 7 - LỖI KHI SINH SONG SONG
        # Voice:
        # Nếu sinh nhiều token cùng lúc khi chưa chắc token trước là gì...
        # =====================================================
        error_title = safe_text(
            "Sinh song song khi chưa chắc ngữ cảnh",
            font_size=31,
            color=WHITE,
            max_width=10.5
        )
        error_title.next_to(subtitle, DOWN, buff=0.40)

        bad_tokens = VGroup(
            make_token("Hà", GREEN),
            make_token("Nội", GREEN),
            make_token("là", GREEN),
            make_token("thủ", RED, width=0.85),
            make_token("thức", RED, width=0.9),
        )
        bad_tokens.arrange(RIGHT, buff=0.18)
        bad_tokens.move_to(UP * 0.0)

        crosses = VGroup(
            Cross(bad_tokens[3], stroke_color=RED, stroke_width=5),
            Cross(bad_tokens[4], stroke_color=RED, stroke_width=5),
        )

        error_notes = VGroup(
            safe_text("mất mạch", font_size=22, color=RED, max_width=3),
            safe_text("lặp ý", font_size=22, color=RED, max_width=3),
            safe_text("sai ngữ cảnh", font_size=22, color=RED, max_width=4),
        )
        error_notes.arrange(RIGHT, buff=0.55)
        error_notes.move_to(DOWN * 2.35)

        pause_to(67.3)

        self.play(Write(error_title), run_time=0.45)
        add_time(0.45)

        pause_to(68.7)

        self.play(
            LaggedStart(
                *[FadeIn(tok, scale=0.85) for tok in bad_tokens],
                lag_ratio=0.05
            ),
            run_time=0.62
        )
        add_time(0.62)

        pause_to(73.7)

        self.play(Create(crosses), run_time=0.4)
        add_time(0.4)

        for note, target_time in zip(error_notes, [74.0, 75.8, 77.3]):
            pause_to(target_time)
            self.play(FadeIn(note, shift=UP), run_time=0.28)
            add_time(0.28)

        pause_to(80.8)

        clear(
            error_title,
            bad_tokens,
            crosses,
            error_notes,
            run_time=0.4
        )

        # =====================================================
        # CẢNH 8 - TRADE-OFF
        # Voice:
        # Tóm lại, tăng tốc bằng song song nhưng đánh đổi...
        # =====================================================
        tradeoff_title = safe_text(
            "Trade-off của Non-autoregressive Decoding",
            font_size=30,
            color=YELLOW,
            max_width=11
        )
        tradeoff_title.next_to(subtitle, DOWN, buff=0.42)

        speed_side = model_box(
            "Tốc độ có thể nhanh hơn",
            GREEN,
            width=3.65,
            height=1.2,
            font_size=23
        )

        quality_side = model_box(
            "Khó giữ\nmạch lạc hơn",
            RED,
            width=3.65,
            height=1.2,
            font_size=23
        )

        speed_side.move_to(LEFT * 2.6 + DOWN * 0.05)
        quality_side.move_to(RIGHT * 2.6 + DOWN * 0.05)

        trade_arrow = DoubleArrow(
            speed_side.get_right(),
            quality_side.get_left(),
            color=YELLOW,
            stroke_width=3,
            buff=0.25
        )

        final_note = safe_text(
            "Nhanh hơn, nhưng phải đánh đổi với độ tin cậy và tính mạch lạc.",
            font_size=21,
            color=YELLOW,
            max_width=10.5
        )
        final_note.move_to(DOWN * 2.35)

        pause_to(82.1)

        self.play(Write(tradeoff_title), run_time=0.5)
        add_time(0.5)

        self.play(FadeIn(speed_side, shift=LEFT), run_time=0.48)
        add_time(0.48)

        self.play(
            Create(trade_arrow),
            FadeIn(quality_side, shift=RIGHT),
            run_time=0.58
        )
        add_time(0.58)

        pause_to(88.0)

        self.play(FadeIn(final_note, shift=UP), run_time=0.48)
        add_time(0.48)

        self.play(Flash(trade_arrow, color=YELLOW), run_time=0.35)
        add_time(0.35)

        wait_audio(self, audio, visual_time)
