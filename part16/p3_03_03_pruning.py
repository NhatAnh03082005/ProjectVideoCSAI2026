# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os

# ============================================================
# PHẦN 3.3 - NETWORK PRUNING
# Visual + voice sync theo từng file audio nhỏ
# Render:
# python -m manim -pql scenes/p3_03_03_pruning.py SceneP30303NetworkPruning
# ============================================================

config.background_color = "#0f172a"

BG = "#0f172a"
WHITE = "#e5e7eb"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"
MUTED = "#94a3b8"
VI_FONT = "Arial"
FONT = None

_MANIM_TEXT = Text


def has_vietnamese(text):
    vietnamese_chars = (
        "ăâđêôơư"
        "áàảãạấầẩẫậắằẳẵặ"
        "éèẻẽẹếềểễệ"
        "íìỉĩị"
        "óòỏõọốồổỗộớờởỡợ"
        "úùủũụứừửữự"
        "ýỳỷỹỵ"
    )
    lowered = str(text).lower()
    return any(ch in lowered for ch in vietnamese_chars)


def Text(text, *args, font=None, **kwargs):
    if font is None:
        if has_vietnamese(text):
            kwargs["font"] = VI_FONT
    else:
        kwargs["font"] = font
    return _MANIM_TEXT(text, *args, **kwargs)


def audio_duration(path, fallback=10.0):
    if not os.path.exists(path):
        print("[WARNING] Không tìm thấy audio:", path)
        return fallback
    try:
        return MP3(path).info.length
    except Exception:
        return fallback


def fit_text(text, width, height=None):
    if text.width > width:
        text.scale_to_fit_width(width)
    if height is not None and text.height > height:
        text.scale_to_fit_height(height)
    return text


def make_box(text, color, width=2.8, height=0.78, font_size=21, fill=0.13):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.3,
        fill_color=color,
        fill_opacity=fill,
    )

    label = Text(
        text,
        font=FONT,
        font_size=font_size,
        color=WHITE,
        line_spacing=0.82,
    )
    fit_text(label, width - 0.28, height - 0.16)
    label.move_to(box.get_center())

    return VGroup(box, label)


def make_title(text):
    title = Text(
        text,
        font=FONT,
        font_size=38,
        color=WHITE,
    )
    fit_text(title, 11.2)
    title.to_edge(UP, buff=0.28)
    return title


def make_subtitle(text, title):
    subtitle = Text(
        text,
        font=FONT,
        font_size=23,
        color=BLUE,
    )
    fit_text(subtitle, 10.8)
    subtitle.next_to(title, DOWN, buff=0.14)
    return subtitle


def make_x_mark(mob, size=0.18, color=RED, stroke_width=4):
    c = mob.get_center()
    return VGroup(
        Line(
            c + LEFT * size + UP * size,
            c + RIGHT * size + DOWN * size,
            color=color,
            stroke_width=stroke_width,
        ),
        Line(
            c + LEFT * size + DOWN * size,
            c + RIGHT * size + UP * size,
            color=color,
            stroke_width=stroke_width,
        ),
    )


class SceneP30303NetworkPruning(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"
        full_audio_path = voice_dir / "p3_03_03_pruning.mp3"
        use_full_audio = full_audio_path.exists()
        active_mobs = []

        def get_audio_path(filename):
            return str(voice_dir / filename)

        def section_title(text, subtitle, color=WHITE, font_size=28):
            t = Text(text, font=FONT, font_size=font_size, color=color)
            fit_text(t, 10.9)
            t.next_to(subtitle, DOWN, buff=0.30)
            return t

        def bottom_note(text, color=YELLOW, font_size=21, y=-2.32):
            note = Text(text, font=FONT, font_size=font_size, color=color)
            fit_text(note, 10.9)
            note.move_to(DOWN * abs(y))
            return note

        def clear_active_before_audio(run_time=0.12):
            nonlocal active_mobs
            mobs = [m for m in active_mobs if m is not None]
            if mobs:
                self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
            active_mobs = []

        def set_active(*mobs):
            nonlocal active_mobs
            active_mobs = [m for m in mobs if m is not None]

        def play_segment(filename, fallback_duration, visual_func, clear_before=True):
            if clear_before:
                clear_active_before_audio(run_time=0.10)

            audio_path = get_audio_path(filename)
            duration = audio_duration(audio_path, fallback=fallback_duration)

            if (not use_full_audio) and os.path.exists(audio_path):
                self.add_sound(audio_path)
            elif not use_full_audio:
                print("[WARNING] Bỏ qua audio vì không tìm thấy:", audio_path)

            local_time = 0.0

            def wait_to(ratio):
                nonlocal local_time
                target = duration * ratio
                delay = max(0, target - local_time)
                if delay > 0:
                    self.wait(delay)
                    local_time += delay

            def play_func(*animations, run_time=0.35, **kwargs):
                nonlocal local_time
                self.play(*animations, run_time=run_time, **kwargs)
                local_time += run_time

            visual_func(wait_to, play_func, duration)

            remain = max(0, duration - local_time)
            if remain > 0:
                self.wait(remain)

        def neural_network(center=ORIGIN, scale=1.0):
            layer_x = [-2.25, -0.45, 1.35]
            layer_ys = [
                [0.80, 0.00, -0.80],
                [1.10, 0.35, -0.35, -1.10],
                [0.80, 0.00, -0.80],
            ]

            layers = []
            nodes = VGroup()
            edges = VGroup()

            for li, ys in enumerate(layer_ys):
                current_layer = []
                for y in ys:
                    node = Circle(
                        radius=0.12 * scale,
                        stroke_color=BLUE if li == 0 else GREEN if li == 2 else PURPLE,
                        stroke_width=2,
                        fill_color=BLUE if li == 0 else GREEN if li == 2 else PURPLE,
                        fill_opacity=0.22,
                    )
                    node.move_to(center + RIGHT * layer_x[li] * scale + UP * y * scale)
                    current_layer.append(node)
                    nodes.add(node)
                layers.append(current_layer)

            for li in range(len(layers) - 1):
                for a in layers[li]:
                    for b in layers[li + 1]:
                        edge = Line(
                            a.get_center(),
                            b.get_center(),
                            color=MUTED,
                            stroke_width=1.2,
                        )
                        edge.set_opacity(0.48)
                        edges.add(edge)

            return VGroup(edges, nodes), layers, edges, nodes

        def matrix_grid(rows=5, cols=6, side=0.22, color=BLUE, removed=None):
            removed = removed or []
            cells = VGroup()
            marks = VGroup()

            for r in range(rows):
                for c in range(cols):
                    idx = r * cols + c
                    is_removed = idx in removed
                    sq = Square(
                        side_length=side,
                        stroke_color=RED if is_removed else color,
                        stroke_width=1.2,
                        fill_color=RED if is_removed else color,
                        fill_opacity=0.20 if is_removed else 0.14,
                    )
                    if is_removed:
                        sq.set_opacity(0.38)
                    cells.add(sq)

            cells.arrange_in_grid(rows=rows, cols=cols, buff=0.05)

            for idx in removed:
                if idx < len(cells):
                    marks.add(
                        make_x_mark(
                            cells[idx],
                            size=0.11,
                            color=RED,
                            stroke_width=2.4,
                        )
                    )

            return VGroup(cells, marks)

        # =====================================================
        # HEADER
        # =====================================================
        title = make_title("Network Pruning")
        subtitle = make_subtitle(
            "Cắt phần ít quan trọng để model nhỏ hơn",
            title,
        )

        if use_full_audio:
            self.add_sound(str(full_audio_path))
        else:
            print("[WARNING] Không tìm thấy audio gộp:", full_audio_path)

        # =====================================================
        # 1) INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            pruning = make_box(
                "Cắt tỉa mô hình",
                YELLOW,
                width=4.15,
                height=0.86,
                font_size=26,
                fill=0.12,
            )
            pruning.move_to(UP * 0.30)

            note = bottom_note(
                "Loại bỏ phần ít quan trọng trong model",
                color=YELLOW,
                font_size=22,
                y=-1.45,
            )

            play(Write(title), run_time=0.55)

            wait_to(0.18)
            play(FadeIn(subtitle, shift=UP), run_time=0.25)

            wait_to(0.42)
            play(FadeIn(pruning, shift=UP), run_time=0.35)

            wait_to(0.72)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(pruning, note)

        play_segment(
            "p3_03_03_01_intro.mp3",
            fallback_duration=5.0,
            visual_func=visual_intro,
            clear_before=False,
        )

        # =====================================================
        # 2) BIG NETWORK
        # =====================================================
        def visual_big_network(wait_to, play, duration):
            st = section_title(
                "Không phải mọi phần đều quan trọng như nhau",
                subtitle,
                color=YELLOW,
                font_size=27,
            )

            net, layers, edges, nodes = neural_network(
                center=LEFT * 2.35 + DOWN * 0.15,
                scale=1.05,
            )

            components = VGroup(
                make_box("Weight", BLUE, width=2.05, height=0.54, font_size=18, fill=0.10),
                make_box("Neuron", GREEN, width=2.05, height=0.54, font_size=18, fill=0.10),
                make_box("Attention head", PURPLE, width=2.75, height=0.54, font_size=18, fill=0.10),
                make_box("Layer", ORANGE, width=2.05, height=0.54, font_size=18, fill=0.10),
                make_box("Block", YELLOW, width=2.05, height=0.54, font_size=18, fill=0.10),
            )
            components.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            components.move_to(RIGHT * 3.35 + DOWN * 0.08)

            note = bottom_note(
                "Một số phần đóng góp ít hơn cho kết quả cuối cùng",
                color=YELLOW,
                font_size=21,
                y=-2.25,
            )

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.16)
            play(FadeIn(net, shift=UP), run_time=0.45)

            wait_to(0.42)
            play(
                LaggedStart(
                    *[FadeIn(c, shift=LEFT) for c in components],
                    lag_ratio=0.12,
                ),
                run_time=0.80,
            )

            wait_to(0.78)
            play(FadeIn(note, shift=UP), run_time=0.30)

            set_active(st, net, components, note)

        play_segment(
            "p3_03_03_02_big_network.mp3",
            fallback_duration=11.0,
            visual_func=visual_big_network,
        )

        # =====================================================
        # 3) REMOVE LESS IMPORTANT PARTS
        # =====================================================
        def visual_remove_parts(wait_to, play, duration):
            clear_title = section_title(
                "Xác định và loại bỏ phần ít quan trọng",
                subtitle,
                color=RED,
                font_size=27,
            )

            net, layers, edges, nodes = neural_network(
                center=LEFT * 1.45 + DOWN * 0.10,
                scale=1.05,
            )

            target_node = layers[1][2]
            target_edge_1 = edges[4]
            target_edge_2 = edges[8]

            node_mark = make_x_mark(
                target_node,
                size=0.20,
                color=RED,
                stroke_width=4,
            )

            weight_mark_1 = make_x_mark(
                target_edge_1,
                size=0.12,
                color=RED,
                stroke_width=3,
            )

            weight_mark_2 = make_x_mark(
                target_edge_2,
                size=0.12,
                color=RED,
                stroke_width=3,
            )

            marks = VGroup(node_mark, weight_mark_1, weight_mark_2)

            weight_label = make_box(
                "Weight ít quan trọng\n-> cắt kết nối",
                RED,
                width=3.05,
                height=0.78,
                font_size=19,
                fill=0.10,
            )
            weight_label.move_to(RIGHT * 3.65 + UP * 0.70)

            neuron_label = make_box(
                "Neuron ít quan trọng\n-> cắt node",
                RED,
                width=3.05,
                height=0.78,
                font_size=19,
                fill=0.10,
            )
            neuron_label.move_to(RIGHT * 3.65 + DOWN * 0.35)

            a_weight = Arrow(
                weight_label.get_left(),
                weight_mark_1.get_center() + RIGHT * 0.12,
                color=RED,
                stroke_width=2.6,
                buff=0.18,
            )

            a_neuron = Arrow(
                neuron_label.get_left(),
                target_node.get_right() + RIGHT * 0.10,
                color=RED,
                stroke_width=2.6,
                buff=0.18,
            )

            note = bottom_note(
                "X trên đường nối là cắt weight, X trên vòng tròn là cắt neuron",
                color=RED,
                font_size=20,
                y=-2.25,
            )

            wait_to(0.02)
            play(FadeIn(clear_title, shift=UP), run_time=0.24)

            wait_to(0.16)
            play(FadeIn(net, shift=UP), run_time=0.42)

            wait_to(0.38)
            play(
                FadeIn(weight_label, shift=LEFT),
                Create(a_weight),
                run_time=0.35,
            )

            wait_to(0.52)
            play(
                target_edge_1.animate.set_opacity(0.15),
                target_edge_2.animate.set_opacity(0.15),
                FadeIn(weight_mark_1),
                FadeIn(weight_mark_2),
                run_time=0.38,
            )

            wait_to(0.66)
            play(
                FadeIn(neuron_label, shift=LEFT),
                Create(a_neuron),
                run_time=0.32,
            )

            wait_to(0.76)
            play(
                target_node.animate.set_opacity(0.18),
                FadeIn(node_mark),
                FadeIn(note, shift=UP),
                run_time=0.40,
            )

            set_active(
                clear_title,
                net,
                weight_label,
                neuron_label,
                a_weight,
                a_neuron,
                marks,
                note,
            )

        play_segment(
            "p3_03_03_03_remove_parts.mp3",
            fallback_duration=8.0,
            visual_func=visual_remove_parts,
        )

        # =====================================================
        # 4) PRUNING LEVELS
        # =====================================================
        def visual_levels(wait_to, play, duration):
            st = section_title(
                "Pruning ở nhiều mức khác nhau",
                subtitle,
                color=BLUE,
                font_size=28,
            )

            intro = make_box(
                "Các mức cắt trong model",
                YELLOW,
                width=4.35,
                height=0.62,
                font_size=22,
                fill=0.10,
            )
            intro.move_to(UP * 0.95)

            weight = make_box(
                "1. Weight riêng lẻ",
                BLUE,
                width=3.35,
                height=0.82,
                font_size=19,
                fill=0.10,
            )

            neuron = make_box(
                "2. Neuron",
                GREEN,
                width=3.35,
                height=0.82,
                font_size=19,
                fill=0.10,
            )

            head = make_box(
                "3. Attention head",
                PURPLE,
                width=3.35,
                height=0.82,
                font_size=19,
                fill=0.10,
            )

            layer = make_box(
                "4. Layer",
                ORANGE,
                width=3.35,
                height=0.82,
                font_size=19,
                fill=0.10,
            )

            block = make_box(
                "5. Cả Block",
                YELLOW,
                width=3.35,
                height=0.82,
                font_size=19,
                fill=0.10,
            )

            top_row = VGroup(weight, neuron, head)
            top_row.arrange(RIGHT, buff=0.35)
            top_row.move_to(UP * 0.05)

            bottom_row = VGroup(layer, block)
            bottom_row.arrange(RIGHT, buff=0.45)
            bottom_row.move_to(DOWN * 1.05)

            # note = bottom_note(
            #     "Đây là các vị trí có thể prune, không phải luồng dữ liệu",
            #     color=YELLOW,
            #     font_size=20,
            #     y=-2.32,
            # )

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.10)
            play(FadeIn(intro, shift=UP), run_time=0.28)

            items = [weight, neuron, head, layer, block]
            ratios = [0.24, 0.38, 0.52, 0.66, 0.80]

            for item, ratio in zip(items, ratios):
                wait_to(ratio)
                play(FadeIn(item, shift=UP), run_time=0.30)

            wait_to(0.90)
            play(FadeIn(shift=UP), run_time=0.25)

            set_active(st, intro, top_row, bottom_row)

        play_segment(
            "p3_03_03_04_levels.mp3",
            fallback_duration=10.0,
            visual_func=visual_levels,
        )

        # =====================================================
        # 5) GOAL
        # =====================================================
        def visual_goal(wait_to, play, duration):
            st = section_title(
                "Mục tiêu: nhỏ hơn và ít phép tính hơn",
                subtitle,
                color=GREEN,
                font_size=28,
            )

            before = make_box(
                "Before pruning\nModel lớn",
                RED,
                width=3.10,
                height=1.00,
                font_size=22,
                fill=0.11,
            )
            before.move_to(LEFT * 3.25 + UP * 0.35)

            after = make_box(
                "After pruning\nModel nhỏ hơn",
                GREEN,
                width=3.25,
                height=1.00,
                font_size=22,
                fill=0.11,
            )
            after.move_to(RIGHT * 3.25 + UP * 0.35)

            arrow = Arrow(
                before.get_right(),
                after.get_left(),
                color=YELLOW,
                stroke_width=5,
                buff=0.25,
            )

            size = make_box(
                "Model size giảm",
                GREEN,
                width=3.10,
                height=0.62,
                font_size=20,
                fill=0.10,
            )

            compute = make_box(
                "Compute giảm",
                BLUE,
                width=3.10,
                height=0.62,
                font_size=20,
                fill=0.10,
            )

            goals = VGroup(size, compute)
            goals.arrange(RIGHT, buff=0.55)
            goals.move_to(DOWN * 1.20)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.18)
            play(FadeIn(before, shift=RIGHT), run_time=0.35)

            wait_to(0.38)
            play(GrowArrow(arrow), run_time=0.28)

            wait_to(0.52)
            play(FadeIn(after, shift=LEFT), run_time=0.35)

            wait_to(0.74)
            play(FadeIn(goals, shift=UP), run_time=0.40)

            set_active(st, before, after, arrow, goals)

        play_segment(
            "p3_03_03_05_goal.mp3",
            fallback_duration=8.5,
            visual_func=visual_goal,
        )

        # =====================================================
        # 6) WARNING
        # =====================================================
        def visual_warning(wait_to, play, duration):
            st = section_title(
                "Cảnh báo quan trọng",
                subtitle,
                color=RED,
                font_size=29,
            )

            warning = make_box(
                "Pruning không tự động\nlàm model chạy nhanh hơn",
                RED,
                width=6.30,
                height=1.05,
                font_size=25,
                fill=0.12,
            )
            warning.move_to(UP * 0.35)

            gpu = make_box(
                "GPU + kernel\nphải tận dụng được",
                YELLOW,
                width=4.50,
                height=0.88,
                font_size=22,
                fill=0.10,
            )
            gpu.move_to(DOWN * 1.10)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.25)
            play(FadeIn(warning, shift=UP), run_time=0.42)

            wait_to(0.68)
            play(FadeIn(gpu, shift=UP), run_time=0.35)

            wait_to(0.84)
            play(Flash(warning[0], color=RED), run_time=0.55)

            set_active(st, warning, gpu)

        play_segment(
            "p3_03_03_06_warning.mp3",
            fallback_duration=6.0,
            visual_func=visual_warning,
        )

        # =====================================================
        # 7) UNSTRUCTURED PRUNING
        # =====================================================
        def visual_unstructured(wait_to, play, duration):
            st = section_title(
                "Unstructured pruning: cắt weight rời rạc",
                subtitle,
                color=RED,
                font_size=27,
            )

            matrix = matrix_grid(
                rows=5,
                cols=6,
                side=0.25,
                color=BLUE,
                removed=[2, 5, 8, 13, 17, 20, 24, 28],
            )
            matrix.move_to(LEFT * 3.35 + UP * 0.05)

            sparse_label = make_box(
                "Sparse matrix\nnhiều lỗ rời rạc",
                RED,
                width=3.20,
                height=0.84,
                font_size=20,
                fill=0.10,
            )
            sparse_label.next_to(matrix, DOWN, buff=0.35)

            gpu_box = make_box(
                "GPU / kernel\nkhó tận dụng",
                YELLOW,
                width=3.25,
                height=0.86,
                font_size=21,
                fill=0.10,
            )
            gpu_box.move_to(RIGHT * 3.35 + UP * 0.35)

            speed_box = make_box(
                "Tốc độ thực tế\ncó thể tăng ít",
                RED,
                width=3.25,
                height=0.86,
                font_size=21,
                fill=0.10,
            )
            speed_box.move_to(RIGHT * 3.35 + DOWN * 0.95)

            arrow = Arrow(
                matrix.get_right(),
                gpu_box.get_left(),
                color=YELLOW,
                stroke_width=3,
                buff=0.25,
            )

            arrow2 = Arrow(
                gpu_box.get_bottom(),
                speed_box.get_top(),
                color=RED,
                stroke_width=3,
                buff=0.18,
            )

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.14)
            play(FadeIn(matrix, shift=UP), run_time=0.38)

            wait_to(0.34)
            play(FadeIn(sparse_label, shift=UP), run_time=0.30)

            wait_to(0.54)
            play(
                Create(arrow),
                FadeIn(gpu_box, shift=LEFT),
                run_time=0.38,
            )

            wait_to(0.74)
            play(
                Create(arrow2),
                FadeIn(speed_box, shift=UP),
                run_time=0.38,
            )

            set_active(st, matrix, sparse_label, gpu_box, speed_box, arrow, arrow2)

        play_segment(
            "p3_03_03_07_unstructured.mp3",
            fallback_duration=11.0,
            visual_func=visual_unstructured,
        )

        # =====================================================
        # 8) STRUCTURED PRUNING
        # =====================================================
        def visual_structured(wait_to, play, duration):
            st = section_title(
                "Structured pruning: cắt theo cấu trúc rõ ràng",
                subtitle,
                color=GREEN,
                font_size=27,
            )

            definition = make_box(
                "Structured = cắt nguyên cụm mà hệ thống có thể tận dụng",
                GREEN,
                width=8.60,
                height=0.66,
                font_size=21,
                fill=0.10,
            )
            definition.move_to(UP * 1.05)

            head_card = make_box(
                "Cắt cả\nattention head",
                PURPLE,
                width=2.75,
                height=0.86,
                font_size=19,
                fill=0.10,
            )

            neuron_card = make_box(
                "Cắt cả\nneuron",
                GREEN,
                width=2.45,
                height=0.86,
                font_size=19,
                fill=0.10,
            )

            layer_card = make_box(
                "Cắt cả\nlayer",
                ORANGE,
                width=2.45,
                height=0.86,
                font_size=19,
                fill=0.10,
            )

            block_card = make_box(
                "Cắt cả\nblock",
                YELLOW,
                width=2.45,
                height=0.86,
                font_size=19,
                fill=0.10,
            )

            row1 = VGroup(head_card, neuron_card, layer_card, block_card)
            row1.arrange(RIGHT, buff=0.32)
            row1.move_to(UP * 0.02)

            sparsity = make_box(
                "Hoặc dùng dạng sparsity mà phần cứng hỗ trợ\nví dụ pattern 2:4, block-sparse, kernel sparse",
                BLUE,
                width=8.80,
                height=0.86,
                font_size=19,
                fill=0.09,
            )
            sparsity.move_to(DOWN * 1.16)

            note = bottom_note(
                "Cấu trúc nhỏ hơn thật -> inference dễ tận dụng hơn",
                color=GREEN,
                font_size=20,
                y=-2.35,
            )

            head_x = make_x_mark(head_card, size=0.18, color=RED, stroke_width=3)
            neuron_x = make_x_mark(neuron_card, size=0.18, color=RED, stroke_width=3)
            layer_x = make_x_mark(layer_card, size=0.18, color=RED, stroke_width=3)
            block_x = make_x_mark(block_card, size=0.18, color=RED, stroke_width=3)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.14)
            play(FadeIn(definition, shift=UP), run_time=0.32)

            wait_to(0.36)
            play(
                FadeIn(head_card, shift=UP),
                FadeIn(head_x),
                run_time=0.34,
            )

            wait_to(0.50)
            play(
                FadeIn(neuron_card, shift=UP),
                FadeIn(neuron_x),
                run_time=0.30,
            )

            wait_to(0.64)
            play(
                FadeIn(layer_card, shift=UP),
                FadeIn(layer_x),
                FadeIn(block_card, shift=UP),
                FadeIn(block_x),
                run_time=0.42,
            )

            wait_to(0.78)
            play(FadeIn(sparsity, shift=UP), run_time=0.35)

            wait_to(0.88)
            play(FadeIn(note, shift=UP), run_time=0.28)

            set_active(
                st,
                definition,
                row1,
                sparsity,
                note,
                head_x,
                neuron_x,
                layer_x,
                block_x,
            )

        play_segment(
            "p3_03_03_08_structured.mp3",
            fallback_duration=12.0,
            visual_func=visual_structured,
        )

        # =====================================================
        # 9) SUMMARY
        # =====================================================
        def visual_summary(wait_to, play, duration):
            st = section_title(
                "Nói ngắn gọn",
                subtitle,
                color=YELLOW,
                font_size=30,
            )

            wrong = make_box(
                "Không chỉ là\ncắt bớt tham số",
                RED,
                width=3.75,
                height=1.00,
                font_size=23,
                fill=0.10,
            )
            wrong.move_to(LEFT * 3.10 + UP * 0.20)

            right = make_box(
                "Phải cắt theo cách\ninference tận dụng được",
                GREEN,
                width=4.40,
                height=1.00,
                font_size=23,
                fill=0.12,
            )
            right.move_to(RIGHT * 2.95 + UP * 0.20)

            arrow = Arrow(
                wrong.get_right(),
                right.get_left(),
                color=YELLOW,
                stroke_width=5,
                buff=0.20,
            )

            final = make_box(
                "Pruning hiệu quả = thuật toán + phần cứng + kernel phù hợp",
                YELLOW,
                width=8.80,
                height=0.80,
                font_size=21,
                fill=0.10,
            )
            final.move_to(DOWN * 1.35)

            wait_to(0.02)
            play(FadeIn(st, shift=UP), run_time=0.24)

            wait_to(0.18)
            play(FadeIn(wrong, shift=RIGHT), run_time=0.35)

            wait_to(0.42)
            play(GrowArrow(arrow), run_time=0.28)

            wait_to(0.56)
            play(FadeIn(right, shift=LEFT), run_time=0.35)

            wait_to(0.78)
            play(FadeIn(final, shift=UP), run_time=0.35)

            wait_to(0.90)
            play(Flash(right[0], color=GREEN), run_time=0.55)

            set_active(st, wrong, right, arrow, final)

        play_segment(
            "p3_03_03_09_summary.mp3",
            fallback_duration=8.0,
            visual_func=visual_summary,
        )

        # =====================================================
        # END
        # =====================================================
        final_mobs = [m for m in active_mobs if m is not None]
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            *[FadeOut(m) for m in final_mobs],
            run_time=0.50,
        )
