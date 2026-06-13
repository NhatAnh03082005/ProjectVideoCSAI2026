# -*- coding: utf-8 -*-

from manim import *
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.visual_utils import *


class SceneP3EarlyExit(Scene):
    def construct(self):
        self.camera.background_color = BG

        audio = "voice/p3_01_04_early_exit.mp3"
        play_audio(self, audio)
        visual_time = 0

        # =====================================================
        # HELPERS
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

        def clear(*mobjects, run_time=0.32):
            nonlocal visual_time
            self.play(*[FadeOut(mob) for mob in mobjects], run_time=run_time)
            visual_time += run_time

        def bottom_note(text, font_size=20, color=YELLOW, max_width=9.8):
            note = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=max_width
            )
            note.move_to(DOWN * 2.35)
            return note

        def section_title(text, color=WHITE, font_size=27):
            t = safe_text(
                text,
                font_size=font_size,
                color=color,
                max_width=10.5
            )
            t.next_to(subtitle, DOWN, buff=0.34)
            return t

        def make_floor(label, color=MUTED, width=3.15, height=0.38):
            rect = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.07,
                stroke_color=color,
                stroke_width=1.6,
                fill_color=color,
                fill_opacity=0.09,
            )
            text = safe_text(
                label,
                font_size=17,
                color=WHITE,
                max_width=width - 0.25
            )
            text.move_to(rect.get_center())
            return VGroup(rect, text)

        def make_tower(x=0.0, y=-0.10, width=3.15):
            floors = VGroup()
            floor_map = {}

            for number in [80, 70, 60, 50, 40, 30, 20, 10]:
                color = BLUE if number in [80, 30, 20] else MUTED
                floor = make_floor(f"Layer {number}", color=color, width=width)
                floors.add(floor)
                floor_map[number] = floor

            floors.arrange(DOWN, buff=0.05)
            floors.move_to(RIGHT * x + UP * y)
            return floors, floor_map

        def make_building(x=0.0, y=-0.20, width=3.15):
            floors = VGroup()
            floor_map = {}

            for number in [80, 70, 60, 50, 40, 30, 20, 10]:
                color = BLUE if number in [80, 30, 20] else MUTED
                floor = make_floor(f"Tầng {number}", color=color, width=width)
                floors.add(floor)
                floor_map[number] = floor

            floors.arrange(DOWN, buff=0.055)
            floors.move_to(RIGHT * x + UP * y)
            return floors, floor_map

        def token(name, color=GREEN):
            dot = Circle(
                radius=0.17,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.50,
            )
            label = safe_text(
                name,
                font_size=15,
                color=WHITE,
                max_width=0.60
            )
            label.move_to(dot.get_center())
            return VGroup(dot, label)

        def exit_head(label="Exit head", color=YELLOW):
            return model_box(
                label,
                color,
                width=1.65,
                height=0.34,
                font_size=14
            )

        # =====================================================
        # HEADER
        # =====================================================
        title = safe_text(
            "Early Exiting",
            font_size=39,
            color=WHITE,
            max_width=11
        )
        title.to_edge(UP, buff=0.40)

        subtitle = safe_text(
            "Thoát sớm khi mô hình đã đủ tự tin",
            font_size=26,
            color=BLUE,
            max_width=11,
        )
        subtitle.next_to(title, DOWN, buff=0.20)

        self.play(Write(title), run_time=0.60)
        add_time(0.60)

        pause_to(1.10)

        self.play(FadeIn(subtitle, shift=UP), run_time=0.42)
        add_time(0.42)

        # =====================================================
        # CẢNH 1 - NHIỀU LAYER
        # Voice: Early exiting, LLM lớn có rất nhiều layer.
        # =====================================================
        intro_title = section_title("LLM lớn có nhiều layer")
        tower, floor_map = make_tower(x=-0.30, y=-0.10, width=3.05)

        layer_count = model_box(
            "Ví dụ:\n80 layer",
            PURPLE,
            width=2.65,
            height=0.78,
            font_size=21,
        )
        layer_count.next_to(tower, RIGHT, buff=0.55)

        # intro_note = bottom_note(
        #     "Early Exiting = cho phép thoát sớm ở layer giữa",
        #     color=YELLOW,
        # )

        pause_to(2.45)

        self.play(Write(intro_title), run_time=0.42)
        add_time(0.42)

        pause_to(3.20)

        self.play(FadeIn(tower, shift=UP), run_time=0.55)
        add_time(0.55)

        pause_to(4.60)

        self.play(FadeIn(layer_count, shift=LEFT), run_time=0.35)
        add_time(0.35)

        pause_to(5.50)

        # self.play(FadeIn(intro_note, shift=UP), run_time=0.35)
        # add_time(0.35)

        pause_to(6.30)

        clear(tower, intro_title, layer_count, run_time=0.28)

        # =====================================================
        # CẢNH 2 - BÌNH THƯỜNG ĐI HẾT TOÀN BỘ LAYER
        # Voice: Bình thường token đi qua toàn bộ layer.
        # =====================================================
        full_title = section_title("Bình thường: đi qua toàn bộ mạng")
        full_tower, full_map = make_tower(x=0.0, y=-0.20, width=3.10)

        full_token = token("t", GREEN)
        full_token.move_to(full_map[10].get_left() + LEFT * 0.52)

        start_arrow = Arrow(
            full_token.get_right(),
            full_map[10].get_left(),
            color=GREEN,
            stroke_width=3,
            buff=0.10,
        )

        top_badge = model_box(
            "Layer 80\nđầu ra cuối",
            PURPLE,
            width=2.35,
            height=0.72,
            font_size=18
        )
        top_badge.next_to(full_map[80], RIGHT, buff=0.45)

        full_note = bottom_note(
            "Mỗi token phải đi từ layer đầu đến layer cuối.",
            color=YELLOW,
        )

        pause_to(6.55)

        self.play(
            Write(full_title),
            FadeIn(full_tower, shift=UP),
            run_time=0.45
        )
        add_time(0.45)

        pause_to(7.25)

        self.play(FadeIn(full_token), Create(start_arrow), run_time=0.40)
        add_time(0.40)

        pause_to(8.20)

        self.play(
            full_token.animate.move_to(full_map[80].get_left() + LEFT * 0.52),
            run_time=1.35,
            rate_func=linear,
        )
        add_time(1.35)

        pause_to(11.25)

        self.play(FadeIn(top_badge, shift=LEFT), run_time=0.35)
        add_time(0.35)

        pause_to(13.25)

        self.play(FadeIn(full_note, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(15.70)

        clear(
            full_tower,
            full_title,
            full_token,
            start_arrow,
            top_badge,
            full_note,
            run_time=0.28
        )

        # =====================================================
        # CẢNH 3 - KHÔNG PHẢI TOKEN NÀO CŨNG KHÓ
        # Voice: Có bước model đã tự tin ngay từ layer giữa.
        # =====================================================
        difficulty_title = section_title("Không phải bước nào cũng khó")

        easy_box = model_box(
            "Token dễ\nngữ cảnh rõ",
            GREEN,
            width=3.15,
            height=0.92,
            font_size=21
        )
        hard_box = model_box(
            "Token khó\ncần thêm thông tin",
            RED,
            width=3.25,
            height=0.92,
            font_size=20
        )

        easy_box.move_to(LEFT * 2.25 + UP * 0.65)
        hard_box.move_to(RIGHT * 2.25 + UP * 0.65)

        easy_path = VGroup(
            make_floor("Layer 10", MUTED, width=2.35, height=0.34),
            make_floor("Layer 20", GREEN, width=2.35, height=0.34),
            make_floor("Dừng sớm", GREEN, width=2.35, height=0.34),
        )
        easy_path.arrange(DOWN, buff=0.08)
        easy_path.next_to(easy_box, DOWN, buff=0.34)

        hard_path = VGroup(
            make_floor("Layer 10", MUTED, width=2.35, height=0.34),
            make_floor("Layer 40", MUTED, width=2.35, height=0.34),
            make_floor("Layer 80", RED, width=2.35, height=0.34),
        )
        hard_path.arrange(DOWN, buff=0.08)
        hard_path.next_to(hard_box, DOWN, buff=0.34)

        easy_arrow = Arrow(
            easy_box.get_bottom(),
            easy_path.get_top(),
            color=GREEN,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.18,
        )
        hard_arrow = Arrow(
            hard_box.get_bottom(),
            hard_path.get_top(),
            color=RED,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.18,
        )

        confident_note = bottom_note(
            "Khi xác suất nghiêng mạnh về một token, model có thể tự tin sớm.",
            color=YELLOW,
            max_width=10.2,
        )

        pause_to(16.05)

        self.play(
            Write(difficulty_title),
            FadeIn(easy_box, shift=UP),
            FadeIn(hard_box, shift=UP),
            run_time=0.52,
        )
        add_time(0.52)

        pause_to(21.20)

        self.play(
            Create(easy_arrow),
            FadeIn(easy_path, shift=UP),
            Create(hard_arrow),
            FadeIn(hard_path, shift=UP),
            run_time=0.55,
        )
        add_time(0.55)

        pause_to(25.10)

        self.play(FadeIn(confident_note, shift=UP), run_time=0.38)
        add_time(0.38)

        pause_to(30.85)

        clear(
            difficulty_title,
            easy_box,
            hard_box,
            easy_arrow,
            hard_arrow,
            easy_path,
            hard_path,
            confident_note,
            run_time=0.28
        )

        # =====================================================
        # CẢNH 4 - CÂU HỎI EARLY EXITING + EXIT HEAD
        # Voice: Nếu layer giữa đủ tự tin, có cần chạy tiếp không?
        # =====================================================
        question_title = section_title("Có cần chạy tiếp đến layer cuối?")
        mid_tower, mid_map = make_tower(x=-0.65, y=-0.05, width=3.10)

        mid_highlight = SurroundingRectangle(
            mid_map[20],
            color=YELLOW,
            buff=0.055,
            corner_radius=0.08
        )

        layer20_note = model_box(
            "Layer giữa\nđã đủ tự tin?",
            YELLOW,
            width=2.70,
            height=0.82,
            font_size=19
        )
        layer20_note.next_to(mid_map[20], RIGHT, buff=0.55)

        exit20 = exit_head("Exit head", YELLOW)
        exit30 = exit_head("Exit head", YELLOW)
        exit20.next_to(mid_map[20], RIGHT, buff=0.45)
        exit30.next_to(mid_map[30], RIGHT, buff=0.45)

        exit_note = bottom_note(
            "Gắn thêm exit head hoặc bộ dự đoán trung gian ở một số layer.",
            color=YELLOW,
            max_width=10.2,
        )

        pause_to(31.15)

        self.play(
            Write(question_title),
            FadeIn(mid_tower, shift=UP),
            run_time=0.52
        )
        add_time(0.52)

        pause_to(32.85)

        self.play(
            Create(mid_highlight),
            FadeIn(layer20_note, shift=LEFT),
            run_time=0.48
        )
        add_time(0.48)

        pause_to(37.20)

        self.play(
            FadeOut(layer20_note),
            FadeIn(exit20, shift=LEFT),
            FadeIn(exit30, shift=LEFT),
            run_time=0.48
        )
        add_time(0.48)

        pause_to(40.70)

        self.play(FadeIn(exit_note, shift=UP), run_time=0.36)
        add_time(0.36)

        pause_to(44.00)

        clear(
            question_title,
            mid_tower,
            mid_highlight,
            exit20,
            exit30,
            exit_note,
            run_time=0.28
        )

        # =====================================================
        # CẢNH 5 - TOKEN DỄ THOÁT SỚM, TOKEN KHÓ ĐI TIẾP
        # Bố cục đã chỉnh cân: tower ở giữa, box hai bên gần tower.
        # =====================================================
        path_title = section_title("Token dễ thoát sớm, token khó đi tiếp")
        path_tower, path_map = make_tower(x=0.0, y=-0.05, width=3.10)

        easy_token = token("dễ", GREEN)
        hard_token = token("khó", RED)

        easy_token.move_to(path_map[10].get_left() + LEFT * 0.55)
        hard_token.move_to(path_map[10].get_right() + RIGHT * 0.55)

        easy_out = model_box(
            "xuất token\nở layer 20",
            GREEN,
            width=2.55,
            height=0.76,
            font_size=18
        )
        easy_out.next_to(path_map[20], LEFT, buff=0.45)

        hard_out = model_box(
            "đi tiếp\nđến layer 80",
            RED,
            width=2.55,
            height=0.76,
            font_size=18
        )
        hard_out.next_to(path_map[80], RIGHT, buff=0.45)

        save_note = bottom_note(
            "Token dễ dùng ít tính toán hơn, token khó vẫn đi qua toàn bộ mô hình.",
            color=YELLOW,
            max_width=10.6,
        )

        pause_to(44.25)

        self.play(
            Write(path_title),
            FadeIn(path_tower, shift=UP),
            run_time=0.52
        )
        add_time(0.52)

        pause_to(45.15)

        self.play(FadeIn(easy_token), run_time=0.22)
        add_time(0.22)

        self.play(
            easy_token.animate.move_to(path_map[20].get_left() + LEFT * 0.55),
            run_time=0.55,
            rate_func=linear,
        )
        add_time(0.55)

        self.play(
            FadeIn(easy_out, shift=RIGHT),
            run_time=0.32
        )
        add_time(0.32)

        pause_to(48.00)

        self.play(FadeIn(hard_token), run_time=0.22)
        add_time(0.22)

        self.play(
            hard_token.animate.move_to(path_map[80].get_right() + RIGHT * 0.55),
            run_time=0.90,
            rate_func=linear,
        )
        add_time(0.90)

        self.play(
            FadeIn(hard_out, shift=LEFT),
            run_time=0.32
        )
        add_time(0.32)

        pause_to(50.80)

        self.play(FadeIn(save_note, shift=UP), run_time=0.36)
        add_time(0.36)

        pause_to(54.45)

        clear(
            path_title,
            path_tower,
            easy_token,
            hard_token,
            easy_out,
            hard_out,
            save_note,
            run_time=0.28
        )

        # =====================================================
        # CẢNH 6 - TÒA NHÀ 80 TẦNG
        # Bố cục cân lại: building ở giữa lệch nhẹ trái, label gần hơn.
        # =====================================================
        building_title = section_title("Mô hình như tòa nhà 80 tầng")

        building, floor_positions = make_building(x=-0.35, y=-0.35, width=3.05)

        elevator_line = Line(
            building.get_right() + RIGHT * 0.40 + DOWN * 1.75,
            building.get_right() + RIGHT * 0.40 + UP * 1.75,
            color=MUTED,
            stroke_width=4,
        )

        easy_elevator = token("dễ", GREEN)
        hard_elevator = token("khó", RED)

        easy_elevator.move_to(floor_positions[10].get_right() + RIGHT * 0.40)
        hard_elevator.move_to(floor_positions[10].get_right() + RIGHT * 0.40)

        easy_stop = model_box(
            "xuống ở tầng 20/30",
            GREEN,
            width=3.00,
            height=0.68,
            font_size=18
        )
        easy_stop.next_to(floor_positions[20], RIGHT, buff=0.85)

        hard_stop = model_box(
            "đi tiếp đến tầng 80",
            RED,
            width=3.00,
            height=0.68,
            font_size=18
        )
        hard_stop.next_to(floor_positions[80], RIGHT, buff=0.85)

        pause_to(54.70)

        self.play(
            Write(building_title),
            FadeIn(building, shift=UP),
            Create(elevator_line),
            run_time=0.58
        )
        add_time(0.58)

        pause_to(56.55)

        self.play(FadeIn(hard_elevator), run_time=0.22)
        add_time(0.22)

        self.play(
            hard_elevator.animate.move_to(floor_positions[80].get_right() + RIGHT * 0.40),
            run_time=1.00,
            rate_func=linear,
        )
        add_time(1.00)

        self.play(FadeIn(hard_stop, shift=LEFT), run_time=0.32)
        add_time(0.32)

        pause_to(61.35)

        self.play(FadeIn(easy_elevator), run_time=0.22)
        add_time(0.22)

        self.play(
            easy_elevator.animate.move_to(floor_positions[20].get_right() + RIGHT * 0.40),
            run_time=0.62,
            rate_func=linear,
        )
        add_time(0.62)

        self.play(FadeIn(easy_stop, shift=LEFT), run_time=0.32)
        add_time(0.32)

        pause_to(65.00)

        clear(
            building_title,
            building,
            elevator_line,
            easy_elevator,
            hard_elevator,
            easy_stop,
            hard_stop,
            run_time=0.28
        )

        # =====================================================
        # CẢNH 7 - KHÓ KHĂN: KHI NÀO ĐỦ TỰ TIN?
        # =====================================================
        confidence_title = section_title(
            "Khi nào thì đủ tự tin?",
            color=YELLOW
        )

        confidence_box = model_box(
            "Confidence\ncao?",
            YELLOW,
            width=3.10,
            height=1.00,
            font_size=23
        )
        confidence_box.move_to(LEFT * 2.45 + UP * 0.20)

        risk_box = model_box(
            "Dừng quá sớm\n-> sinh sai",
            RED,
            width=3.40,
            height=1.00,
            font_size=22
        )
        risk_box.move_to(RIGHT * 2.45 + UP * 0.20)

        risk_arrow = Arrow(
            confidence_box.get_right(),
            risk_box.get_left(),
            color=RED,
            stroke_width=3,
            buff=0.18
        )

        risk_note = bottom_note(
            "Biểu diễn trung gian có thể chưa đủ thông tin.",
            color=RED,
            max_width=10.2,
        )

        pause_to(65.20)

        self.play(Write(confidence_title), run_time=0.42)
        add_time(0.42)

        pause_to(66.85)

        self.play(FadeIn(confidence_box, shift=UP), run_time=0.38)
        add_time(0.38)

        pause_to(69.70)

        self.play(
            Create(risk_arrow),
            FadeIn(risk_box, shift=UP),
            run_time=0.48
        )
        add_time(0.48)

        pause_to(72.00)

        self.play(FadeIn(risk_note, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(75.95)

        clear(
            confidence_title,
            confidence_box,
            risk_box,
            risk_arrow,
            risk_note,
            run_time=0.28
        )

        # =====================================================
        # CẢNH 8 - CẦN TIÊU CHÍ CONFIDENCE
        # =====================================================
        criterion_title = section_title("Cần tiêu chí kiểm tra đủ tốt")

        threshold = model_box(
            "Tiêu chí Confidence",
            PURPLE,
            width=3.85,
            height=0.78,
            font_size=21
        )
        check = model_box(
            "Cơ chế kiểm tra",
            BLUE,
            width=3.25,
            height=0.78,
            font_size=21
        )

        threshold.move_to(LEFT * 2.30 + UP * 0.20)
        check.move_to(RIGHT * 2.30 + UP * 0.20)

        criterion_arrow = DoubleArrow(
            threshold.get_right(),
            check.get_left(),
            color=YELLOW,
            stroke_width=3,
            buff=0.08
        )

        # criterion_note = bottom_note(
        #     "Chỉ thoát sớm khi mô hình thật sự đủ tự tin.",
        #     color=YELLOW,
        # )

        pause_to(76.15)

        self.play(Write(criterion_title), run_time=0.40)
        add_time(0.40)

        pause_to(77.35)

        self.play(
            FadeIn(threshold, shift=UP),
            Create(criterion_arrow),
            FadeIn(check, shift=UP),
            run_time=0.52
        )
        add_time(0.52)

        pause_to(79.35)

        # self.play(FadeIn(criterion_note, shift=UP), run_time=0.35)
        # add_time(0.35)

        pause_to(81.30)

        clear(
            criterion_title,
            threshold,
            criterion_arrow,
            check,
          #  criterion_note,
            run_time=0.28
        )

        # =====================================================
        # CẢNH 9 - TÓM TẮT
        # =====================================================
        summary_title = section_title(
            "Tóm tắt Early Exiting",
            color=YELLOW
        )

        step1 = model_box(
            "Không bắt mọi token\nđi hết toàn bộ mạng",
            BLUE,
            width=3.45,
            height=1.05,
            font_size=20
        )
        step2 = model_box(
            "Token dễ\nthoát sớm",
            GREEN,
            width=2.75,
            height=1.05,
            font_size=21
        )
        step3 = model_box(
            "Tiết kiệm\ntính toán",
            YELLOW,
            width=2.85,
            height=1.05,
            font_size=21
        )

        steps = VGroup(step1, step2, step3)
        steps.arrange(RIGHT, buff=0.50)
        steps.move_to(UP * 0.10)

        arrow1 = Arrow(
            step1.get_right(),
            step2.get_left(),
            color=MUTED,
            stroke_width=2.5,
            buff=0.04
        )
        arrow2 = Arrow(
            step2.get_right(),
            step3.get_left(),
            color=MUTED,
            stroke_width=2.5,
            buff=0.04
        )

        final_note = bottom_note(
            "Bước dễ thoát sớm, bước khó vẫn đi qua toàn bộ mô hình.",
            color=GREEN,
            max_width=10.5,
        )

        pause_to(81.55)

        self.play(Write(summary_title), run_time=0.40)
        add_time(0.40)

        pause_to(82.85)

        self.play(FadeIn(step1, shift=UP), run_time=0.35)
        add_time(0.35)

        pause_to(84.35)

        self.play(
            Create(arrow1),
            FadeIn(step2, shift=UP),
            run_time=0.42
        )
        add_time(0.42)

        pause_to(85.75)

        self.play(
            Create(arrow2),
            FadeIn(step3, shift=UP),
            run_time=0.42
        )
        add_time(0.42)

        pause_to(86.75)

        self.play(FadeIn(final_note, shift=UP), run_time=0.35)
        add_time(0.35)

        wait_audio(self, audio, visual_time)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(summary_title),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(final_note),
            run_time=0.8,
        )