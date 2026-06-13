from manim import *
from mutagen.mp3 import MP3
import os
import numpy as np

# ============================================================
# SLIDE 9 — MEMORY FOOTPRINT, MODEL SIZE & KV CACHE (7 cảnh)
# Style: 3Blue1Brown (số chạy, ma trận, thanh/cốc bộ nhớ lớn dần) + theme Slide 7/8.
# Icon: SVG Lucide (assets/), recolor theo palette.
# Render (đứng TRONG slide9_themed/ để voice/ & assets/ đúng path):
#   manim -qh slide9_scenes.py Slide9aHook
#   ... Slide9bWeights Slide9cKVCache Slide9dGrows
#   ... Slide9eCenterpiece Slide9fOOM Slide9gOutro
# ============================================================

# ---------- THEME (đồng bộ slide7/8) ----------
FONT_VI = "Arial"
BG = "#0f172a"
WHITE = "#e5e7eb"
MUTED = "#94a3b8"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"
TEAL = "#2dd4bf"
MAROON = "#e11d48"
SLATE = "#64748b"

FILL_SOFT = 0.12
FILL_MEDIUM = 0.18

# Quy ước màu Slide 9
C_WEIGHT = BLUE      # trọng số mô hình (cố định)
C_KV = YELLOW        # KV cache
C_KV_HI = RED        # KV khi dâng cao / vượt ngưỡng
C_BUF = SLATE        # temporary buffers
C_OOM = RED          # tràn bộ nhớ
C_MEM = YELLOW       # tag thách thức Memory

config.background_color = BG

TEXT_SS = 4
ASSETS = "assets"


def T(text, size=24, color=WHITE, weight=NORMAL, line_spacing=-1, vi=False):
    # Render cỡ lớn rồi scale xuống -> tránh "hở chữ" của ManimPango ở cỡ nhỏ.
    kwargs = dict(font_size=size * TEXT_SS, color=color, weight=weight, line_spacing=line_spacing)
    if vi or any(ord(ch) > 127 or ch.isdigit() for ch in text):
        kwargs["font"] = FONT_VI
    return Text(text, **kwargs).scale(1 / TEXT_SS)


def svg_icon(name, color, height=1.0, sw=3.0):
    m = SVGMobject(os.path.join(ASSETS, name + ".svg"))
    m.set_height(height)
    m.set_stroke(color=color, width=sw)
    m.set_fill(opacity=0)
    return m


def audio_duration(path):
    if not os.path.exists(path):
        print(f"[WARNING] Khong tim thay audio: {path}")
        return 0
    return MP3(path).info.length


class VoiceScene(Scene):
    def say(self, path):
        self.add_sound(path)
        return self.renderer.time, audio_duration(path)

    def fill(self, start, dur, pad=0.18):
        rem = dur + pad - (self.renderer.time - start)
        if rem > 0.05:
            self.wait(rem)

    def make_tag(self, name, color, vi=True):
        chip = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.08,
                                stroke_color=color, fill_color=color, fill_opacity=1)
        label = T(name, size=22, color=color, weight=BOLD, vi=vi).next_to(chip, RIGHT, buff=0.18)
        return VGroup(chip, label).to_corner(UL, buff=0.45)


# ============================================================
# CẢNH 1 — HOOK: con số gây sốc (175B -> >=10 A100)
# ============================================================
class Slide9aHook(VoiceScene):
    """Hook được bố trí theo nguyên tắc 3Blue1Brown:
    - Mỗi khung hình chỉ có một ý chính.
    - Số liệu được gắn với vật thể bằng brace/pill, không đặt đè lên icon.
    - Dùng biến đổi hình học giữa các trạng thái thay vì chồng nhiều lớp chữ.
    """

    @staticmethod
    def chip_symbol(color=TEAL, size=1.0):
        core = RoundedRectangle(
            width=1.05 * size,
            height=1.05 * size,
            corner_radius=0.16 * size,
            stroke_color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.08,
        )
        inner = RoundedRectangle(
            width=0.50 * size,
            height=0.50 * size,
            corner_radius=0.08 * size,
            stroke_color=color,
            stroke_width=2.5,
            fill_opacity=0,
        )
        pins = VGroup()
        pin = 0.18 * size
        for a in (-0.34, 0, 0.34):
            pins.add(
                Line([a * size, 0.525 * size, 0], [a * size, 0.525 * size + pin, 0],
                     color=color, stroke_width=2.5),
                Line([a * size, -0.525 * size, 0], [a * size, -0.525 * size - pin, 0],
                     color=color, stroke_width=2.5),
                Line([0.525 * size, a * size, 0], [0.525 * size + pin, a * size, 0],
                     color=color, stroke_width=2.5),
                Line([-0.525 * size, a * size, 0], [-0.525 * size - pin, a * size, 0],
                     color=color, stroke_width=2.5),
            )
        return VGroup(core, inner, pins)

    @classmethod
    def gpu_tile(cls, color=TEAL, scale=1.0):
        body = RoundedRectangle(
            width=1.12 * scale,
            height=0.80 * scale,
            corner_radius=0.12 * scale,
            stroke_color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.05,
        )
        chip = cls.chip_symbol(color, size=0.42 * scale).move_to(body.get_center() + UP * 0.07 * scale)
        memory = Rectangle(
            width=0.64 * scale,
            height=0.08 * scale,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.8,
        ).move_to(body.get_center() + DOWN * 0.27 * scale)
        return VGroup(body, chip, memory)

    @staticmethod
    def pc_icon(color=BLUE, scale=1.0):
        screen = RoundedRectangle(
            width=0.88 * scale,
            height=0.55 * scale,
            corner_radius=0.08 * scale,
            stroke_color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.03,
        )
        stem = Line(
            screen.get_bottom() + DOWN * 0.02 * scale,
            screen.get_bottom() + DOWN * 0.18 * scale,
            color=color,
            stroke_width=2.5,
        )
        foot = Line(
            stem.get_end() + LEFT * 0.17 * scale,
            stem.get_end() + RIGHT * 0.17 * scale,
            color=color,
            stroke_width=2.5,
        )
        return VGroup(screen, stem, foot)

    @staticmethod
    def memory_cells(count, color, rows=1, cell=0.38, buff=0.10):
        cells = VGroup(*[
            RoundedRectangle(
                width=cell,
                height=cell,
                corner_radius=0.06,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.35,
            ) for _ in range(count)
        ])
        cols = int(np.ceil(count / rows))
        cells.arrange_in_grid(rows=rows, cols=cols, buff=buff)
        return cells

    @staticmethod
    def broken_link(color=RED):
        left = RoundedRectangle(width=0.72, height=0.34, corner_radius=0.17,
                                stroke_color=color, stroke_width=4).rotate(25 * DEGREES)
        right = left.copy().rotate(-50 * DEGREES).shift(RIGHT * 0.78)
        left.shift(LEFT * 0.40)
        slash = Line(LEFT * 0.18 + UP * 0.30, RIGHT * 0.18 + DOWN * 0.30,
                     color=color, stroke_width=5)
        return VGroup(left, right, slash)

    def construct(self):
        names = ["Latency", "Memory", "Throughput", "Hardware", "Trade-off"]
        cols = [RED, YELLOW, GREEN, TEAL, MAROON]
        chips = VGroup()
        for nm, c in zip(names, cols):
            box = RoundedRectangle(width=2.25, height=0.95, corner_radius=0.15,
                                   stroke_color=c, fill_color=c, fill_opacity=FILL_MEDIUM)
            chips.add(VGroup(box, T(nm, size=21, color=WHITE, weight=BOLD).move_to(box)))
        chips.arrange(RIGHT, buff=0.26).move_to(UP * 2.7)

        # CÂU 01: 5 thách thức
        s, d = self.say("voice/s9a_01.mp3")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in chips], lag_ratio=0.12),
                  run_time=1.3)
        self.fill(s, d)

        # CÂU 02: so sánh 350 GB trọng số với 40 GB của một A100.
        # Hai card có cùng kích thước; toàn bộ nội dung được neo theo trục dọc riêng.
        # Không dùng mũi tên xuyên qua card, chỉ giữ một huy hiệu tỉ lệ ở khoảng trống giữa.
        s, d = self.say("voice/s9a_02.mp3")
        mem = chips[1]
        num2 = T("2", size=30, color=YELLOW, weight=BOLD).next_to(mem, UP, buff=0.12)
        self.play(mem[0].animate.set_fill(YELLOW, opacity=0.5),
                  Indicate(mem, color=YELLOW, scale_factor=1.12),
                  FadeIn(num2, scale=0.6), run_time=0.8)
        others = VGroup(*[chips[i] for i in (0, 2, 3, 4)])
        tag = self.make_tag("Memory", YELLOW)
        self.play(others.animate.set_opacity(0.1), run_time=0.35)
        self.play(FadeOut(others), FadeOut(num2), FadeOut(mem), FadeIn(tag), run_time=0.5)

        title = T("GPT-3 · 175B · FP16", size=28, color=WHITE, weight=BOLD, vi=True
                  ).to_edge(UP, buff=0.82)

        card_w, card_h = 4.85, 4.20
        left_card = RoundedRectangle(
            width=card_w, height=card_h, corner_radius=0.22,
            stroke_color=BLUE, stroke_width=3,
            fill_color=BLUE, fill_opacity=0.05,
        ).move_to(LEFT * 3.15 + DOWN * 0.08)

        right_card = RoundedRectangle(
            width=card_w, height=card_h, corner_radius=0.22,
            stroke_color=TEAL, stroke_width=3,
            fill_color=TEAL, fill_opacity=0.045,
        ).move_to(RIGHT * 3.15 + DOWN * 0.08)

        # ----- Card trái: icon → tên → ma trận bộ nhớ → brace → số liệu -----
        model_chip = self.chip_symbol(BLUE, size=0.94)
        model_chip.move_to(left_card.get_center() + UP * 1.20)

        model_name = T("GPT-3", size=24, color=BLUE, weight=BOLD)
        model_name.next_to(model_chip, DOWN, buff=0.13)

        weights_cells = self.memory_cells(
            9, BLUE, rows=3, cell=0.31, buff=0.10
        )
        weights_cells.next_to(model_name, DOWN, buff=0.27)

        left_brace = Brace(weights_cells, DOWN, color=BLUE, buff=0.13)
        weights_value = T("350 GB", size=26, color=BLUE, weight=BOLD, vi=True)
        weights_value.next_to(left_brace, DOWN, buff=0.11)

        left_group = VGroup(
            left_card, model_chip, model_name,
            weights_cells, left_brace, weights_value
        )

        # ----- Card phải: cùng nhịp dọc với card trái -----
        one_gpu = self.gpu_tile(TEAL, scale=1.22)
        one_gpu.move_to(right_card.get_center() + UP * 1.20)

        gpu_name = T("A100", size=24, color=TEAL, weight=BOLD)
        gpu_name.next_to(one_gpu, DOWN, buff=0.16)

        gpu_cell = self.memory_cells(
            1, TEAL, rows=1, cell=0.52
        )
        gpu_cell.next_to(gpu_name, DOWN, buff=0.35)

        right_brace = Brace(gpu_cell, DOWN, color=TEAL, buff=0.13)
        gpu_value = T("40 GB", size=26, color=TEAL, weight=BOLD, vi=True)
        gpu_value.next_to(right_brace, DOWN, buff=0.11)

        right_group = VGroup(
            right_card, one_gpu, gpu_name,
            gpu_cell, right_brace, gpu_value
        )

        # Huy hiệu ở vùng âm giữa hai card: không chạm bất kỳ vật thể nào.
        ratio_ring = Circle(
            radius=0.53, stroke_color=RED, stroke_width=4,
            fill_color=RED, fill_opacity=0.08,
        )
        ratio_text = T("8.75×", size=20, color=RED, weight=BOLD).move_to(ratio_ring)
        ratio_badge = VGroup(ratio_ring, ratio_text).move_to(DOWN * 0.05)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(left_card), FadeIn(right_card), run_time=0.5)
        self.play(
            FadeIn(model_chip, scale=0.82),
            FadeIn(model_name),
            LaggedStart(*[GrowFromCenter(c) for c in weights_cells], lag_ratio=0.06),
            GrowFromCenter(left_brace),
            FadeIn(weights_value, shift=UP * 0.08),
            run_time=1.25,
        )
        self.play(
            FadeIn(one_gpu, scale=0.82),
            FadeIn(gpu_name),
            GrowFromCenter(gpu_cell),
            GrowFromCenter(right_brace),
            FadeIn(gpu_value, shift=UP * 0.08),
            run_time=0.85,
        )
        self.play(FadeIn(ratio_badge, scale=0.72), run_time=0.55)
        self.fill(s, d)

        # CÂU 03: tách token counter thành một dải riêng dưới hai card.
        # Card được giảm độ nổi để mắt tập trung vào trạng thái "0 token".
        s, d = self.say("voice/s9a_03.mp3")
        token_band = RoundedRectangle(
            width=5.05, height=0.70, corner_radius=0.16,
            stroke_color=MUTED, stroke_width=2,
            fill_color=MUTED, fill_opacity=0.035,
        ).move_to(DOWN * 3.00)

        empty_tokens = VGroup(*[
            RoundedRectangle(
                width=0.44, height=0.36, corner_radius=0.07,
                stroke_color=MUTED, stroke_width=2,
                fill_color=MUTED, fill_opacity=0.02,
            )
            for _ in range(6)
        ]).arrange(RIGHT, buff=0.11)
        empty_tokens.move_to(token_band.get_center() + LEFT * 0.48)

        token_zero = T("0 token", size=21, color=RED, weight=BOLD, vi=True)
        token_zero.next_to(empty_tokens, RIGHT, buff=0.28)

        no_token = Line(
            empty_tokens.get_left() + UP * 0.28,
            empty_tokens.get_right() + DOWN * 0.28,
            color=RED, stroke_width=5,
        )

        self.play(
            VGroup(left_group, right_group, ratio_badge).animate.set_opacity(0.62),
            FadeIn(token_band, shift=UP * 0.08),
            FadeIn(empty_tokens),
            FadeIn(token_zero),
            Create(no_token),
            run_time=0.9,
        )
        self.play(
            Circumscribe(weights_value, color=BLUE, run_time=1.0),
            Indicate(token_zero, color=RED, scale_factor=1.12),
            run_time=1.0,
        )
        self.fill(s, d)

        # CÂU 04: biến đổi thành cụm 10 A100. Nhãn 350 GB nằm dưới brace,
        # tách hẳn khỏi hai hàng GPU nên không còn dính icon.
        s, d = self.say("voice/s9a_04.mp3")
        self.play(FadeOut(VGroup(title, left_group, right_group, ratio_badge,
                                 token_band, empty_tokens, token_zero, no_token)),
                  run_time=0.5)

        grid_title = T("≥ 10 × A100-40GB", size=28, color=WHITE,
                       weight=BOLD, vi=True).to_edge(UP, buff=0.95)
        gpu_grid = VGroup(*[self.gpu_tile(TEAL, scale=1.0) for _ in range(10)])
        gpu_grid.arrange_in_grid(rows=2, cols=5, buff=(0.26, 0.34)).move_to(UP * 0.28)
        capacity_brace = Brace(gpu_grid, DOWN, color=BLUE, buff=0.28)
        capacity_pill = RoundedRectangle(width=3.65, height=0.74, corner_radius=0.16,
                                         stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.12)
        capacity_text = T("350 GB + phần đệm", size=23, color=BLUE,
                          weight=BOLD, vi=True).move_to(capacity_pill)
        capacity_group = VGroup(capacity_pill, capacity_text).next_to(
            capacity_brace, DOWN, buff=0.18)

        self.play(FadeIn(grid_title, shift=DOWN * 0.15), run_time=0.45)
        self.play(LaggedStart(*[GrowFromCenter(g) for g in gpu_grid], lag_ratio=0.07),
                  run_time=1.6)
        self.play(GrowFromCenter(capacity_brace), FadeIn(capacity_group, shift=UP * 0.12),
                  run_time=0.8)
        self.fill(s, d)

        # CÂU 05: so sánh trực quan 10 A100 nối chung với 15 PC rời rạc.
        # Dùng đường nối và biểu tượng broken-link thay cho một câu chú thích dài.
        s, d = self.say("voice/s9a_05.mp3")
        self.play(FadeOut(VGroup(grid_title, gpu_grid, capacity_brace, capacity_group)),
                  run_time=0.45)

        memory_pill = RoundedRectangle(width=4.2, height=0.80, corner_radius=0.18,
                                       stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.12)
        memory_pill.to_edge(UP, buff=0.72)
        memory_pill_text = T("350 GB trọng số", size=25, color=BLUE,
                             weight=BOLD, vi=True).move_to(memory_pill)

        dc_card = RoundedRectangle(width=5.55, height=4.70, corner_radius=0.24,
                                   stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.035)
        dc_card.move_to(LEFT * 3.45 + DOWN * 0.40)
        dc_title = T("10 × A100", size=24, color=TEAL, weight=BOLD).next_to(
            dc_card.get_top(), DOWN, buff=0.24)
        dc_grid = VGroup(*[self.gpu_tile(TEAL, scale=0.62) for _ in range(10)])
        dc_grid.arrange_in_grid(rows=2, cols=5, buff=(0.16, 0.22)).move_to(
            dc_card.get_center() + UP * 0.18)

        connections = VGroup()
        for r in range(2):
            for c in range(4):
                i = r * 5 + c
                connections.add(Line(dc_grid[i].get_right(), dc_grid[i + 1].get_left(),
                                     color=TEAL, stroke_width=2.5))
        for c in range(5):
            connections.add(Line(dc_grid[c].get_bottom(), dc_grid[5 + c].get_top(),
                                 color=TEAL, stroke_width=2.0))
        shared_bar = RoundedRectangle(width=3.95, height=0.38, corner_radius=0.10,
                                      stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.35)
        shared_bar.next_to(dc_grid, DOWN, buff=0.42)
        shared_lbl = T("bộ nhớ nối chung", size=18, color=BLUE, weight=BOLD, vi=True).move_to(shared_bar)
        dc_group = VGroup(dc_card, dc_title, connections, dc_grid, shared_bar, shared_lbl)

        pc_card = RoundedRectangle(width=5.55, height=4.70, corner_radius=0.24,
                                   stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.025)
        pc_card.move_to(RIGHT * 3.45 + DOWN * 0.40)
        pc_title = T("≈ 15 × RTX 4090", size=23, color=BLUE, weight=BOLD, vi=True).next_to(
            pc_card.get_top(), DOWN, buff=0.24)
        pc_grid = VGroup(*[self.pc_icon(BLUE, scale=0.66) for _ in range(15)])
        pc_grid.arrange_in_grid(rows=3, cols=5, buff=(0.18, 0.25)).move_to(
            pc_card.get_center() + UP * 0.24)
        link_break = self.broken_link(RED).scale(0.72).next_to(pc_grid, DOWN, buff=0.27)
        isolated_lbl = T("VRAM rời rạc", size=18, color=RED, weight=BOLD, vi=True).next_to(
            link_break, DOWN, buff=0.12)
        pc_group = VGroup(pc_card, pc_title, pc_grid, link_break, isolated_lbl)

        approx = T("≈", size=48, color=WHITE, weight=BOLD).move_to(DOWN * 0.15)

        self.play(FadeIn(memory_pill), FadeIn(memory_pill_text), run_time=0.5)
        self.play(FadeIn(dc_card), FadeIn(pc_card), FadeIn(dc_title), FadeIn(pc_title),
                  run_time=0.6)
        self.play(FadeIn(connections),
                  LaggedStart(*[GrowFromCenter(g) for g in dc_grid], lag_ratio=0.04),
                  LaggedStart(*[GrowFromCenter(p) for p in pc_grid], lag_ratio=0.025),
                  FadeIn(approx, scale=0.7), run_time=1.5)
        self.play(FadeIn(shared_bar, shift=UP * 0.08), FadeIn(shared_lbl),
                  FadeIn(link_break, scale=0.8), FadeIn(isolated_lbl), run_time=0.8)
        self.play(Indicate(VGroup(shared_bar, shared_lbl), color=TEAL, scale_factor=1.05),
                  Indicate(VGroup(link_break, isolated_lbl), color=RED, scale_factor=1.08),
                  run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)

class Slide9bWeights(VoiceScene):
    """
    Slide 9B dùng PNG nền trong suốt để tạo khối bộ nhớ có chiều sâu và ánh sáng.
    Đặt toàn bộ các file s9b_*.png cùng thư mục với file Python này.
    """

    @staticmethod
    def png(name):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Thiếu asset: {name}. Hãy đặt file này cùng thư mục với slide9_scenes.py"
            )
        return path

    @staticmethod
    def outlined_text(text, size, color=WHITE, stroke=BG, width=7, vi=True):
        mob = T(text, size=size, color=color, weight=BOLD, vi=vi)
        mob.set_stroke(stroke, width=width, background=True)
        return mob

    def make_title(self):
        title = T("Weights", size=34, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.56)
        underline = Line(LEFT * 1.10, RIGHT * 1.10, color=BLUE, stroke_width=3)
        underline.next_to(title, DOWN, buff=0.10)
        glow = underline.copy().set_stroke(width=11, opacity=0.16)
        return VGroup(title, glow, underline)

    def construct(self):
        self.add(self.make_tag("Memory", YELLOW))

        title_group = self.make_title()
        self.play(FadeIn(title_group[0], shift=DOWN * 0.15),
                  FadeIn(title_group[1:]), run_time=0.55)

        # ----------------------------------------------------
        # CÂU 01 — 1 tham số FP16 = 2 byte
        # ----------------------------------------------------
        s, d = self.say("voice/s9b_01.mp3")

        params_img = ImageMobject(self.png("s9b_parameter_matrix.png"))
        params_img.set_height(4.65).move_to(LEFT * 4.25 + DOWN * 0.35)
        params_lbl = self.outlined_text("175B", 31, BLUE).next_to(
            params_img, DOWN, buff=-0.08
        )

        fp16_img = ImageMobject(self.png("s9b_fp16_chip.png"))
        fp16_img.set_height(3.45).move_to(DOWN * 0.35)
        fp16_top = self.outlined_text("FP16", 25, WHITE).move_to(
            fp16_img.get_center() + UP * 1.08
        )
        fp16_byte = self.outlined_text("2 byte", 24, TEAL).move_to(
            fp16_img.get_center() + DOWN * 1.18
        )

        result_img = ImageMobject(self.png("s9b_memory_slab.png"))
        result_img.set_width(4.60).move_to(RIGHT * 4.20 + DOWN * 0.30)

        multiply = self.outlined_text("×", 46, WHITE, width=8, vi=False)
        multiply.move_to(LEFT * 1.95 + DOWN * 0.25)
        equal = self.outlined_text("=", 43, WHITE, width=8, vi=False)
        equal.move_to(RIGHT * 1.95 + DOWN * 0.25)

        self.play(FadeIn(params_img, scale=0.92),
                  FadeIn(params_lbl, shift=UP * 0.12),
                  run_time=0.75)
        self.play(FadeIn(multiply, scale=0.75),
                  FadeIn(fp16_img, scale=0.90),
                  FadeIn(fp16_top),
                  FadeIn(fp16_byte, shift=UP * 0.10),
                  run_time=0.85)
        self.play(FadeIn(equal, scale=0.75),
                  FadeIn(result_img, shift=LEFT * 0.20),
                  run_time=0.75)
        self.fill(s, d)

        # ----------------------------------------------------
        # CÂU 02 — 175B × 2 byte = 350 GB
        # ----------------------------------------------------
        s, d = self.say("voice/s9b_02.mp3")

        self.play(
            FadeOut(Group(params_img, params_lbl, multiply,
                          fp16_img, fp16_top, fp16_byte, equal)),
            result_img.animate.set_width(9.6).move_to(DOWN * 0.20),
            run_time=1.0,
        )

        # Chữ trắng + nền tối trong suốt, không còn chìm vào ma trận màu xanh.
        value_plate = RoundedRectangle(
            width=3.35, height=0.88, corner_radius=0.20,
            stroke_color=WHITE, stroke_width=1.6,
            fill_color=BG, fill_opacity=0.68,
        ).move_to(result_img.get_center())
        value = self.outlined_text("350 GB", 39, WHITE, width=9)
        value.move_to(value_plate)

        self.play(FadeIn(value_plate, scale=0.86),
                  FadeIn(value, scale=0.86),
                  Flash(value_plate, color=BLUE, flash_radius=1.4),
                  run_time=0.9)
        self.fill(s, d)

        # ----------------------------------------------------
        # CÂU 03 — 8 GPU đầy + GPU thứ 9 dùng 30 GB + GPU thứ 10 làm đệm
        # ----------------------------------------------------
        s, d = self.say("voice/s9b_03.mp3")

        self.play(FadeOut(Group(result_img, value_plate, value)), run_time=0.45)

        slots = VGroup()
        slot_labels = VGroup()
        gpu_icons = Group()

        slot_w, slot_h = 1.12, 0.74
        for i in range(10):
            if i < 8:
                color = BLUE
                fill_color = BLUE
                fill_opacity = 0.18
                label = "40 GB"
                icon_name = "s9b_gpu_module.png"
            elif i == 8:
                color = BLUE
                fill_color = BLUE
                fill_opacity = 0.12
                label = "30 GB"
                icon_name = "s9b_gpu_module.png"
            else:
                color = YELLOW
                fill_color = YELLOW
                fill_opacity = 0.09
                label = "+ đệm"
                icon_name = "s9b_gpu_buffer_module.png"

            slot = RoundedRectangle(
                width=slot_w, height=slot_h, corner_radius=0.10,
                stroke_color=color, stroke_width=2.8,
                fill_color=fill_color, fill_opacity=fill_opacity,
            )
            slots.add(slot)

            txt = T(label, size=17 if i < 9 else 16, color=WHITE if i < 9 else YELLOW,
                    weight=BOLD, vi=True)
            txt.set_stroke(BG, width=5, background=True)
            slot_labels.add(txt)

            icon = ImageMobject(self.png(icon_name))
            icon.set_height(1.10)
            gpu_icons.add(icon)

        slots.arrange(RIGHT, buff=0.10).move_to(UP * 0.65)
        for i in range(10):
            slot_labels[i].move_to(slots[i])
            gpu_icons[i].next_to(slots[i], DOWN, buff=0.18)

        # 75% fill trong GPU thứ 9.
        used_30 = Rectangle(
            width=slot_w * 0.75, height=slot_h - 0.08,
            stroke_width=0, fill_color=BLUE, fill_opacity=0.38,
        )
        used_30.align_to(slots[8], LEFT).move_to(
            slots[8].get_left() + RIGHT * used_30.width / 2
        )

        divider = self.outlined_text("350 ÷ 40 = 8.75", 25, WHITE, width=7)
        divider.next_to(slots, UP, buff=0.42)

        brace = Brace(gpu_icons, DOWN, color=TEAL, buff=0.24)
        need = T("≥ 10 GPU", size=27, color=TEAL, weight=BOLD, vi=True)
        need.set_stroke(BG, width=6, background=True)
        need.next_to(brace, DOWN, buff=0.12)

        self.play(FadeIn(divider, shift=DOWN * 0.10), run_time=0.5)
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    FadeIn(slots[i], shift=UP * 0.10),
                    FadeIn(slot_labels[i]),
                    FadeIn(gpu_icons[i], shift=UP * 0.10),
                )
                for i in range(10)
            ], lag_ratio=0.055),
            run_time=1.75,
        )
        self.add(used_30)
        self.play(GrowFromCenter(brace), FadeIn(need, shift=UP * 0.10),
                  run_time=0.75)
        self.fill(s, d)

        # ----------------------------------------------------
        # CÂU 04 — Weights cố định, nạp một lần
        # ----------------------------------------------------
        s, d = self.say("voice/s9b_04.mp3")

        self.play(FadeOut(Group(
            divider, slots, slot_labels, gpu_icons, used_30, brace, need
        )), run_time=0.45)

        locked_img = ImageMobject(self.png("s9b_memory_slab_locked.png"))
        locked_img.set_width(8.50).move_to(RIGHT * 0.15 + DOWN * 0.25)

        load_once = T("LOAD ONCE", size=22, color=WHITE, weight=BOLD)
        load_once.set_stroke(BG, width=7, background=True)
        load_once.move_to(LEFT * 5.25 + DOWN * 0.05)
        load_arrow = Arrow(
            load_once.get_right() + RIGHT * 0.16,
            locked_img.get_left() + RIGHT * 0.28,
            color=WHITE, stroke_width=4, buff=0.10,
        )

        locked_plate = RoundedRectangle(
            width=3.25, height=0.84, corner_radius=0.20,
            stroke_color=WHITE, stroke_width=1.5,
            fill_color=BG, fill_opacity=0.72,
        ).move_to(locked_img.get_center() + LEFT * 0.45)
        locked_value = self.outlined_text("350 GB", 36, WHITE, width=9)
        locked_value.move_to(locked_plate)

        fixed_badge = RoundedRectangle(
            width=1.70, height=0.52, corner_radius=0.14,
            stroke_color=BLUE, stroke_width=2,
            fill_color=BLUE, fill_opacity=0.10,
        )
        fixed_text = T("CỐ ĐỊNH", size=17, color=BLUE, weight=BOLD, vi=True)
        fixed_text.move_to(fixed_badge)
        fixed_group = VGroup(fixed_badge, fixed_text).next_to(
            locked_img, DOWN, buff=-0.03
        ).shift(LEFT * 0.55)

        self.play(FadeIn(locked_img, scale=0.92), run_time=0.75)
        self.play(GrowArrow(load_arrow), FadeIn(load_once, shift=RIGHT * 0.10),
                  run_time=0.65)
        self.play(FadeIn(locked_plate, scale=0.86),
                  FadeIn(locked_value, scale=0.86),
                  FadeIn(fixed_group, shift=UP * 0.08),
                  run_time=0.75)
        self.play(Indicate(fixed_group, color=BLUE, scale_factor=1.08),
                  run_time=0.65)
        self.fill(s, d)

        # ----------------------------------------------------
        # CÂU 05 — Bên cạnh weights cố định còn KV cache biến động
        # ----------------------------------------------------
        s, d = self.say("voice/s9b_05.mp3")

        self.play(
            FadeOut(Group(load_once, load_arrow, fixed_group)),
            locked_img.animate.set_width(6.10).move_to(LEFT * 3.55 + DOWN * 0.25),
            locked_plate.animate.scale(0.76).move_to(LEFT * 3.75 + DOWN * 0.25),
            locked_value.animate.scale(0.76).move_to(LEFT * 3.75 + DOWN * 0.25),
            run_time=0.9,
        )

        plus = self.outlined_text("+", 50, WHITE, width=9, vi=False)
        plus.move_to(DOWN * 0.20)

        kv_img = ImageMobject(self.png("s9b_kv_cache_stack.png"))
        kv_img.set_height(4.35).move_to(RIGHT * 3.55 + DOWN * 0.10)
        kv_label = T("KV cache", size=27, color=YELLOW, weight=BOLD)
        kv_label.set_stroke(BG, width=7, background=True)
        kv_label.next_to(kv_img, DOWN, buff=-0.16)

        self.play(FadeIn(plus, scale=0.72),
                  FadeIn(kv_img, shift=UP * 0.15),
                  FadeIn(kv_label, shift=UP * 0.08),
                  run_time=0.95)
        self.play(Indicate(kv_img, color=YELLOW, scale_factor=1.03),
                  run_time=0.75)
        self.fill(s, d)
        self.wait(0.3)

# ============================================================
# CẢNH 3 — KV CACHE: vì sao cần (attention with/without cache)
# ============================================================
class Slide9cKVCache(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Memory", YELLOW))

        def token_box(label, color=WHITE, active=False):
            box = RoundedRectangle(width=0.72, height=0.58, corner_radius=0.11,
                                   stroke_color=color, stroke_width=3,
                                   fill_color=color, fill_opacity=0.12 if active else 0.045)
            txt = T(label, size=19, color=color, weight=BOLD if active else NORMAL)
            return VGroup(box, txt.move_to(box))

        def kv_pair(color=BLUE, active=False):
            k = RoundedRectangle(width=0.46, height=0.42, corner_radius=0.05,
                                 stroke_color=color, stroke_width=2.5,
                                 fill_color=color, fill_opacity=0.22 if active else 0.10)
            v = k.copy()
            k.add(T("K", size=15, color=color, weight=BOLD).move_to(k))
            v.add(T("V", size=15, color=color, weight=BOLD).move_to(v))
            return VGroup(k, v).arrange(DOWN, buff=0.10)

        def pulse_rect(mob, color, buff=0.12):
            return SurroundingRectangle(mob, color=color, stroke_width=3, buff=buff)

        s, d = self.say("voice/s9c_01.mp3")
        title = T("KV Cache — vì sao cần?", size=32, color=YELLOW, weight=BOLD, vi=True
                  ).to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.fill(s, d)

        n = 5
        toks = VGroup(*[
            token_box(f"t{i+1}", YELLOW if i == n - 1 else WHITE, active=(i == n - 1))
            for i in range(n)
        ]).arrange(RIGHT, buff=0.48).move_to(UP * 1.55 + LEFT * 0.70)

        kvs = VGroup(*[
            kv_pair(YELLOW if i == n - 1 else BLUE, active=(i == n - 1))
            for i in range(n)
        ])
        for i in range(n):
            kvs[i].next_to(toks[i], DOWN, buff=0.34)

        bot = svg_icon("bot", WHITE, height=1.0).to_corner(DL, buff=0.85)
        bot_bubble = RoundedRectangle(width=1.05, height=0.44, corner_radius=0.12,
                                      stroke_color=MUTED, stroke_width=2,
                                      fill_color=MUTED, fill_opacity=0.04)
        bot_bubble.next_to(bot, RIGHT, buff=0.22).shift(UP * 0.18)
        qdots = VGroup(*[Dot(radius=0.035, color=MUTED) for _ in range(3)]).arrange(RIGHT, buff=0.08).move_to(bot_bubble)
        bot_group = VGroup(bot, bot_bubble, qdots)

        s, d = self.say("voice/s9c_02.mp3")
        self.play(FadeIn(bot_group), LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in toks],
                  lag_ratio=0.12), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(kvs[i], shift=UP * 0.08) for i in range(n)],
                              lag_ratio=0.09), run_time=0.9)

        new_tok = toks[-1]
        fan_lines = VGroup(*[
            ArcBetweenPoints(new_tok.get_bottom() + DOWN * 0.04,
                             toks[i].get_bottom() + DOWN * 0.04,
                             angle=0.35 + 0.06 * i,
                             color=YELLOW, stroke_width=3)
            for i in range(n - 1)
        ])
        attn_dot = Dot(new_tok.get_bottom() + DOWN * 0.18, radius=0.06, color=YELLOW)
        self.play(FadeIn(attn_dot, scale=0.6),
                  LaggedStart(*[Create(l) for l in fan_lines], lag_ratio=0.12),
                  run_time=1.0)
        self.fill(s, d)

        s, d = self.say("voice/s9c_03.mp3")
        old_kvs = VGroup(*[kvs[i] for i in range(n - 1)])
        recompute_panel = RoundedRectangle(width=4.65, height=0.82, corner_radius=0.16,
                                           stroke_color=RED, stroke_width=2.5,
                                           fill_color=RED, fill_opacity=0.06)
        recompute_panel.move_to(DOWN * 2.28 + LEFT * 0.25)
        recompute_cells = VGroup(*[
            RoundedRectangle(width=0.45, height=0.34, corner_radius=0.05,
                             stroke_color=RED, stroke_width=2,
                             fill_color=RED, fill_opacity=0.18).add(
                T("K,V", size=10, color=RED, weight=BOLD).move_to(ORIGIN))
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.22).move_to(recompute_panel)
        recompute_cells_label = T("tính lại", size=16, color=RED, weight=BOLD, vi=True)
        recompute_cells_label.next_to(recompute_panel, LEFT, buff=0.18)
        red_x = VGroup(Line(LEFT * 0.12 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.12, color=RED, stroke_width=5),
                       Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12, color=RED, stroke_width=5))
        red_x.next_to(recompute_panel, RIGHT, buff=0.20)
        old_box = pulse_rect(old_kvs, RED, buff=0.14)
        self.play(Create(old_box), FadeIn(recompute_panel, shift=UP * 0.08),
                  FadeIn(recompute_cells_label),
                  LaggedStart(*[TransformFromCopy(old_kvs[i], recompute_cells[i])
                                for i in range(n - 1)], lag_ratio=0.10),
                  run_time=1.2)
        self.play(FadeIn(red_x, scale=0.6), old_box.animate.set_stroke(width=5),
                  rate_func=there_and_back, run_time=0.8)
        self.fill(s, d)

        s, d = self.say("voice/s9c_04.mp3")
        self.play(FadeOut(VGroup(recompute_panel, recompute_cells, recompute_cells_label, red_x, old_box)),
                  run_time=0.35)
        cache = RoundedRectangle(width=2.75, height=2.70, corner_radius=0.18,
                                 stroke_color=YELLOW, stroke_width=3,
                                 fill_color=YELLOW, fill_opacity=0.06)
        cache.to_edge(RIGHT, buff=0.62).shift(DOWN * 0.55)
        cache_lbl = T("KV Cache", size=21, color=YELLOW, weight=BOLD, vi=True).next_to(cache, UP, buff=0.12)
        cache_slots = VGroup()
        for i in range(n - 1):
            slot = VGroup(
                RoundedRectangle(width=0.34, height=0.28, corner_radius=0.04,
                                 stroke_color=BLUE, stroke_width=2,
                                 fill_color=BLUE, fill_opacity=0.22).add(T("K", size=10, color=BLUE, weight=BOLD).move_to(ORIGIN)),
                RoundedRectangle(width=0.34, height=0.28, corner_radius=0.04,
                                 stroke_color=BLUE, stroke_width=2,
                                 fill_color=BLUE, fill_opacity=0.22).add(T("V", size=10, color=BLUE, weight=BOLD).move_to(ORIGIN)),
            ).arrange(RIGHT, buff=0.08)
            cache_slots.add(slot)
        cache_slots.arrange(DOWN, buff=0.12).move_to(cache.get_center() + DOWN * 0.05)

        save_y = kvs.get_bottom()[1] - 0.28
        save_arrow = Arrow([old_kvs.get_right()[0] + 0.18, save_y, 0],
                           [cache.get_left()[0] - 0.18, save_y, 0],
                           color=BLUE, stroke_width=4, buff=0,
                           max_tip_length_to_length_ratio=0.08)
        self.play(FadeIn(cache), FadeIn(cache_lbl, shift=UP * 0.08), run_time=0.55)
        self.play(Create(save_arrow), run_time=0.45)
        self.play(ShowPassingFlash(save_arrow.copy().set_stroke(width=8), time_width=0.35),
                  run_time=0.65)
        self.play(LaggedStart(*[TransformFromCopy(kvs[i], cache_slots[i]) for i in range(n - 1)],
                              lag_ratio=0.08),
                  old_kvs.animate.set_opacity(0.45),
                  run_time=1.0)
        self.fill(s, d)

        s, d = self.say("voice/s9c_05.mp3")
        current_kv = kvs[-1]
        current_box = pulse_rect(current_kv, YELLOW, buff=0.10)
        read_arrow = Arrow(cache.get_left() + LEFT * 0.16 + DOWN * 0.34,
                           current_kv.get_right() + RIGHT * 0.14 + DOWN * 0.12,
                           color=YELLOW, stroke_width=4.5, buff=0,
                           max_tip_length_to_length_ratio=0.08)
        self.play(Create(current_box), current_kv.animate.set_opacity(1),
                  save_arrow.animate.set_opacity(0.22),
                  run_time=0.45)
        self.play(Create(read_arrow), run_time=0.55)
        self.play(ShowPassingFlash(read_arrow.copy().set_stroke(width=8), time_width=0.35),
                  Indicate(cache_slots, color=YELLOW, scale_factor=1.04),
                  run_time=1.2)
        self.fill(s, d)

        s, d = self.say("voice/s9c_06.mp3")
        speed_badge = RoundedRectangle(width=2.35, height=0.48, corner_radius=0.14,
                                       stroke_color=GREEN, stroke_width=2.5,
                                       fill_color=GREEN, fill_opacity=0.10)
        speed_txt = T("decode nhanh hơn", size=17, color=GREEN, weight=BOLD, vi=True).move_to(speed_badge)
        speed_group = VGroup(speed_badge, speed_txt).to_edge(DOWN, buff=0.48).shift(LEFT * 1.45)
        mem_badge = RoundedRectangle(width=2.10, height=0.48, corner_radius=0.14,
                                     stroke_color=YELLOW, stroke_width=2.5,
                                     fill_color=YELLOW, fill_opacity=0.10)
        mem_txt = T("+ bộ nhớ", size=17, color=YELLOW, weight=BOLD, vi=True).move_to(mem_badge)
        mem_group = VGroup(mem_badge, mem_txt).next_to(speed_group, RIGHT, buff=0.35)
        self.play(FadeIn(speed_group, shift=UP * 0.12),
                  FadeIn(mem_group, shift=UP * 0.12),
                  Flash(cache, color=YELLOW, flash_radius=1.6),
                  run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 4 — KV CACHE TĂNG TUYẾN TÍNH
# ============================================================
class Slide9dGrows(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Memory", YELLOW))
        title = T("KV Cache tăng TUYẾN TÍNH", size=32, color=YELLOW, weight=BOLD, vi=True
                  ).to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        # CÂU 01: 1 token -> (K,V) × lớp × head
        s, d = self.say("voice/s9d_01.mp3")
        pair = VGroup(
            Square(0.5, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.25).add(
                T("K", size=18, color=YELLOW)),
            Square(0.5, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.25).add(
                T("V", size=18, color=YELLOW)),
        ).arrange(RIGHT, buff=0.12).move_to(LEFT * 4.2 + UP * 0.4)
        plbl = T("1 token → 1 cặp (K,V)", size=22, color=WHITE, vi=True).next_to(pair, DOWN, buff=0.3)
        self.play(FadeIn(pair, scale=0.7), FadeIn(plbl), run_time=0.7)
        grid = VGroup(*[Square(0.16, stroke_color=YELLOW, stroke_width=1.5,
                       fill_color=YELLOW, fill_opacity=0.22) for _ in range(4 * 6)])
        grid.arrange_in_grid(rows=4, cols=6, buff=0.06).move_to(LEFT * 0.2 + UP * 0.4)
        glbl = T("× số lớp × số đầu chú ý", size=22, color=WHITE, vi=True).next_to(grid, DOWN, buff=0.3)
        self.play(TransformFromCopy(pair, grid), FadeIn(glbl), run_time=1.0)
        self.fill(s, d)

        # CÂU 02: thêm token/user -> kho lớn thêm
        s, d = self.say("voice/s9d_02.mp3")
        store = Rectangle(width=1.0, height=0.4, stroke_color=YELLOW, fill_color=YELLOW,
                          fill_opacity=0.3).to_edge(RIGHT, buff=1.2).shift(UP * 0.4)
        slbl = T("kho KV", size=20, color=YELLOW, vi=True).next_to(store, UP, buff=0.15)
        self.play(FadeIn(store), FadeIn(slbl), run_time=0.4)
        for h in (0.8, 1.3, 1.9):
            self.play(store.animate.stretch_to_fit_height(h).align_to(
                store, DOWN).move_to(store.get_bottom() + UP * h / 2), run_time=0.35)
        self.fill(s, d)

        # CÂU 03+04: đồ thị tuyến tính vs cấp số nhân (gạch bỏ)
        s, d = self.say("voice/s9d_03.mp3")
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=5.2, y_length=3.2,
                  axis_config={"include_tip": False, "stroke_color": MUTED}).to_edge(DOWN, buff=0.7).shift(LEFT * 0.5)
        xl = T("số token / request", size=18, color=MUTED, vi=True).next_to(ax, DOWN, buff=0.15)
        yl = T("bộ nhớ KV", size=18, color=MUTED, vi=True).next_to(ax, LEFT, buff=0.1).rotate(PI / 2)
        self.play(FadeOut(VGroup(pair, plbl, grid, glbl, store, slbl)), Create(ax),
                  FadeIn(xl), FadeIn(yl), run_time=0.8)
        lin = ax.plot(lambda x: 0.9 * x, x_range=[0, 5.6], color=YELLOW, stroke_width=6)
        lin_lbl = T("TUYẾN TÍNH", size=22, color=YELLOW, weight=BOLD, vi=True).next_to(
            ax.c2p(5.6, 5.0), RIGHT, buff=0.05)
        self.play(Create(lin), FadeIn(lin_lbl), run_time=1.0)
        self.fill(s, d)

        s, d = self.say("voice/s9d_04.mp3")
        exp_y_max = 5.55
        exp_x_max = np.log(exp_y_max / 0.15) / np.log(2.4)
        
        exp = ax.plot(
            lambda x: 0.15 * (2.4 ** x),
            x_range=[0, exp_x_max],
            color=SLATE,
            stroke_width=4,
        )
        exp.set_fill(opacity=0)
        cross_center = ax.c2p(4.0, 5.0)
        cross = VGroup(
            Line(LEFT * 0.45 + UP * 0.45, RIGHT * 0.45 + DOWN * 0.45,
                 color=RED, stroke_width=6),
            Line(LEFT * 0.45 + DOWN * 0.45, RIGHT * 0.45 + UP * 0.45,
                 color=RED, stroke_width=6),
        ).move_to(cross_center)
        target_time = d * 0.45
        elapsed = self.renderer.time - s

        if target_time - elapsed > 0.05:
            self.wait(target_time - elapsed)

        self.play(
            Create(exp),
            run_time=0.48,
        )
        self.play(
            Create(cross),
            exp.animate.set_stroke(opacity=0.55).set_fill(opacity=0),
            run_time=0.38,
        )
        self.fill(s, d)

        # CÂU 05: nhiều lớp/đầu/người -> tổng phình nhanh
        s, d = self.say("voice/s9d_05.mp3")
        note = T("nhiều lớp × nhiều đầu × nhiều người  →  tổng vẫn phình rất nhanh", size=23,
                 color=WHITE, weight=BOLD, vi=True).to_edge(UP, buff=2.0)
        self.play(FadeIn(note, shift=DOWN * 0.15),
                  lin.animate.set_stroke(width=9), run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 5 — CENTERPIECE: KV cache VƯỢT model size (OPT-30B)
# ============================================================
class Slide9eCenterpiece(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Memory", YELLOW))

        # CÂU 01: tiêu đề OPT-30B
        s, d = self.say("voice/s9e_01.mp3")
        title = T("OPT-30B — KV cache có thể VƯỢT cả model", size=30, color=WHITE,
                  weight=BOLD, vi=True).to_edge(UP, buff=0.7)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)

        ax = Axes(x_range=[0, 6, 1], y_range=[0, 250, 50], x_length=8.5, y_length=4.6,
                  axis_config={"include_tip": False, "stroke_color": MUTED},
                  y_axis_config={"include_numbers": True, "font_size": 22}).shift(DOWN * 0.5 + LEFT * 0.3)
        ylab = T("Size (GB)", size=20, color=MUTED, vi=True).next_to(ax.y_axis, UP, buff=0.15)
        xlab = T("Sequence length (batch 16)", size=20, color=MUTED, vi=True).next_to(
            ax, DOWN, buff=0.85)
        self.play(Create(ax), FadeIn(ylab), FadeIn(xlab), run_time=1.0)
        self.fill(s, d)

        # CÂU 02: đường model size 60 GB nét đứt
        s, d = self.say("voice/s9e_02.mp3")
        y60 = ax.c2p(0, 60)[1]
        msize = DashedLine(np.array([ax.c2p(0, 60)[0], y60, 0]),
                           np.array([ax.c2p(6, 60)[0], y60, 0]), color=BLUE, stroke_width=5)
        mlbl = T("Model weights\n≈ 60 GB", size=18, color=BLUE, weight=BOLD, vi=True)
        mlbl.set_stroke(BG, width=6, background=True)
        mlbl.next_to(msize.get_end(), RIGHT, buff=0.25).shift(UP * 0.12)
        self.play(Create(msize), FadeIn(mlbl, shift=LEFT * 0.08), run_time=1.0)
        self.fill(s, d)

        # CÂU 03: cột mọc dần theo seq length
        s, d = self.say("voice/s9e_03.mp3")
        seqs = ["256", "512", "2048", "4096", "8192"]
        vals = [8, 28, 57, 115, 230]
        bars = VGroup()
        blbls = VGroup()
        for i, (sq, vv) in enumerate(zip(seqs, vals)):
            xc = i + 1
            bot = ax.c2p(xc, 0)
            top = ax.c2p(xc, vv)
            bw = 0.62
            col = C_KV
            bar = Rectangle(width=bw, height=top[1] - bot[1], stroke_color=col,
                            fill_color=col, fill_opacity=0.55)
            bar.move_to([bot[0], (bot[1] + top[1]) / 2, 0])
            bars.add(bar)
            blbls.add(T(sq, size=18, color=MUTED).next_to(bot, DOWN, buff=0.12))
        for i in range(len(bars)):
            self.play(GrowFromEdge(bars[i], DOWN), FadeIn(blbls[i]), run_time=0.5)
        self.fill(s, d)

        # CÂU 04: cột cuối ~230 vượt vạch -> đỏ
        s, d = self.say("voice/s9e_04.mp3")
        last = bars[-1]
        v230 = T("≈ 230 GB", size=22, color=RED, weight=BOLD, vi=True).next_to(last, UP, buff=0.1)
        self.play(last.animate.set_color(RED).set_fill(RED, 0.7), FadeIn(v230),
                  Flash(last.get_top(), color=RED, line_length=0.3), run_time=1.0)
        self.fill(s, d)

        # CÂU 05: phần phát sinh ngốn hơn cả model
        s, d = self.say("voice/s9e_05.mp3")
        verdict = T("KV cache  >  Model weights !", size=30, color=RED, weight=BOLD, vi=True
                    ).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(verdict, scale=0.85),
                  Wiggle(VGroup(last, v230)), run_time=1.0)
        self.fill(s, d)

        # CÂU 06: không hiếm gặp
        s, d = self.say("voice/s9e_06.mp3")
        self.play(Indicate(verdict, color=RED, scale_factor=1.1), run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 6 — OOM: cốc GPU tràn -> từ chối request
# ============================================================
class Slide9fOOM(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Memory", YELLOW))

        cup_w, cup_h = 3.0, 4.6
        cx = -3.2
        bottom_y = -2.4
        top_y = bottom_y + cup_h
        # CÂU 01: cốc + vạch đỏ giới hạn
        s, d = self.say("voice/s9f_01.mp3")
        left = Line([cx - cup_w / 2, top_y, 0], [cx - cup_w / 2, bottom_y, 0], color=WHITE, stroke_width=5)
        right = Line([cx + cup_w / 2, top_y, 0], [cx + cup_w / 2, bottom_y, 0], color=WHITE, stroke_width=5)
        base = Line([cx - cup_w / 2, bottom_y, 0], [cx + cup_w / 2, bottom_y, 0], color=WHITE, stroke_width=5)
        limit = DashedLine([cx - cup_w / 2 - 0.2, top_y, 0], [cx + cup_w / 2 + 0.2, top_y, 0],
                           color=RED, stroke_width=5)
        limit_lbl = T("giới hạn GPU", size=20, color=RED, weight=BOLD, vi=True).next_to(
            limit, UP, buff=0.1)
        cup = VGroup(left, right, base)
        self.play(Create(cup), Create(limit), FadeIn(limit_lbl), run_time=1.0)
        self.fill(s, d)

        def layer(h0, h1, color, op):
            r = Rectangle(width=cup_w - 0.12, height=(h1 - h0), stroke_width=0,
                          fill_color=color, fill_opacity=op)
            r.move_to([cx, bottom_y + (h0 + h1) / 2, 0])
            return r

        # CÂU 02: trọng số (xanh) đáy
        s, d = self.say("voice/s9f_02.mp3")
        w_top = 0.30 * cup_h
        weights = layer(0, w_top, BLUE, 0.45)
        w_lbl = T("Model Weights", size=20, color=BLUE, weight=BOLD, vi=True).next_to(
            weights, LEFT, buff=0.3)
        self.play(FadeIn(weights, shift=UP * 0.1), FadeIn(w_lbl), run_time=0.8)
        self.fill(s, d)

        # CÂU 03: buffers (xám)
        s, d = self.say("voice/s9f_03.mp3")
        b_top = w_top + 0.09 * cup_h
        buffers = layer(w_top, b_top, SLATE, 0.6)
        b_lbl = T("Temporary Buffers", size=18, color=SLATE, weight=BOLD, vi=True).next_to(
            buffers, LEFT, buff=0.3)
        self.play(FadeIn(buffers, shift=UP * 0.05), FadeIn(b_lbl), run_time=0.7)
        self.fill(s, d)

        # CÂU 04: phần còn lại cho KV
        s, d = self.say("voice/s9f_04.mp3")
        kv_lbl = T("KV Cache", size=22, color=YELLOW, weight=BOLD, vi=True).next_to(
            limit, RIGHT, buff=0.6).shift(DOWN * 0.0)
        free = layer(b_top, cup_h, YELLOW, 0.06)
        self.play(FadeIn(free), FadeIn(kv_lbl), run_time=0.7)
        self.fill(s, d)

        # CÂU 05: chatbot đọc tài liệu + nhiều user
        s, d = self.say("voice/s9f_05.mp3")
        doc = svg_icon("file-text", MUTED, height=1.3).move_to(RIGHT * 2.6 + UP * 1.6)
        doc_lbl = T("prompt dài hàng chục nghìn token", size=20, color=MUTED, vi=True).next_to(
            doc, DOWN, buff=0.2)
        users = VGroup(*[svg_icon("user", WHITE, height=0.7) for _ in range(4)])
        users.arrange(RIGHT, buff=0.4).move_to(RIGHT * 2.6 + DOWN * 0.4)
        u_lbl = T("nhiều người dùng cùng lúc", size=20, color=WHITE, vi=True).next_to(
            users, DOWN, buff=0.25)
        self.play(FadeIn(doc), FadeIn(doc_lbl), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(u, shift=UP * 0.15) for u in users], lag_ratio=0.15),
                  FadeIn(u_lbl), run_time=1.0)
        self.fill(s, d)

        # CÂU 06: mỗi user 1 vùng KV dâng song song
        s, d = self.say("voice/s9f_06.mp3")
        level = ValueTracker(b_top)

        def kv_fill():
            h = level.get_value() - b_top
            if h <= 0.001:
                h = 0.001
            frac = (level.get_value() - b_top) / (cup_h - b_top)
            frac = min(max(frac, 0), 1)

            fill_col = RED if frac >= 0.985 else YELLOW
            r = Rectangle(width=cup_w - 0.12, height=h, stroke_width=0, fill_color=fill_col,
                          fill_opacity=0.8)
            r.move_to([cx, b_top + bottom_y + h / 2, 0])
            return r

        kv = always_redraw(kv_fill)
        self.add(kv)
        self.play(level.animate.set_value(0.65 * cup_h), run_time=0.8)
        self.play(level.animate.set_value(0.82 * cup_h), run_time=0.8)
        self.fill(s, d)

        # CÂU 07: chạm vạch -> OOM -> từ chối request
        s, d = self.say("voice/s9f_07.mp3")
        self.play(level.animate.set_value(cup_h), run_time=1.0)
        alert = svg_icon("triangle-alert", RED, height=1.0).move_to([cx, top_y - 0.7, 0])
        oom = T("OOM — tràn bộ nhớ", size=26, color=RED, weight=BOLD, vi=True).next_to(
            limit_lbl, RIGHT, buff=0.5)
        ban = svg_icon("ban", RED, height=0.9).move_to(users[-1])
        reject = T("từ chối request", size=20, color=RED, weight=BOLD, vi=True).next_to(
            users, DOWN, buff=0.25)
        self.play(FadeIn(alert), FadeIn(oom), run_time=0.5)
        self.play(FadeIn(ban), Transform(u_lbl, reject),
                  Flash(limit.get_center(), color=RED, line_length=0.4), run_time=0.8)
        for _ in range(2):
            self.play(oom.animate.set_opacity(0.3), run_time=0.25)
            self.play(oom.animate.set_opacity(1.0), run_time=0.25)
        self.fill(s, d)

        # CÂU 08: GPU còn thừa sức tính, bị chặn vì hết nhớ
        s, d = self.say("voice/s9f_08.mp3")
        comp = svg_icon("cpu", GREEN, height=1.0).move_to(RIGHT * 2.6 + DOWN * 2.3)
        comp_lbl = T("GPU vẫn còn dư sức tính — bị chặn vì HẾT BỘ NHỚ", size=22, color=GREEN,
                     weight=BOLD, vi=True).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(comp), FadeIn(comp_lbl, shift=UP * 0.15),
                  Indicate(comp, color=GREEN), run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 7 — TỔNG KẾT & CHUYỂN TIẾP -> Throughput
# ============================================================
class Slide9gOutro(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Memory", YELLOW))

        # CÂU 01: 3 nguồn bộ nhớ -> THANH bộ nhớ 3 lớp (hình, ít chữ)
        s, d = self.say("voice/s9g_01.mp3")
        head = T("GPU Memory", size=24, color=WHITE, weight=BOLD, vi=True).to_edge(UP, buff=0.9)
        bar_x, base_y, bw = -2.4, -2.2, 1.3

        def seg(y0, h, color, op):
            r = Rectangle(width=bw, height=h, stroke_width=2, stroke_color=color,
                          fill_color=color, fill_opacity=op)
            r.move_to([bar_x, base_y + y0 + h / 2, 0])
            return r

        h_w, h_b, h_kv = 1.5, 0.45, 1.0
        weights = seg(0, h_w, BLUE, 0.5)
        buffers = seg(h_w, h_b, SLATE, 0.55)
        kv = seg(h_w + h_b, h_kv, YELLOW, 0.55)
        w_l = T("Weights", size=18, color=BLUE, weight=BOLD, vi=True).next_to(weights, RIGHT, buff=0.3)
        b_l = T("Buffers", size=16, color=SLATE, vi=True).next_to(buffers, RIGHT, buff=0.3)
        kv_l = T("KV cache", size=18, color=YELLOW, weight=BOLD, vi=True).next_to(kv, RIGHT, buff=0.3)
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.4)
        self.play(LaggedStart(FadeIn(weights, shift=UP * 0.1), FadeIn(w_l),
                  FadeIn(buffers, shift=UP * 0.1), FadeIn(b_l),
                  FadeIn(kv, shift=UP * 0.1), FadeIn(kv_l), lag_ratio=0.2), run_time=1.4)
        self.fill(s, d)

        # CÂU 02: KV tuyến tính nhưng VƯỢT model size -> dâng đỏ qua vạch
        s, d = self.say("voice/s9g_02.mp3")
        ms_y = base_y + h_w
        model_line = DashedLine([bar_x - bw / 2 - 0.5, ms_y, 0], [bar_x + bw / 2 + 0.5, ms_y, 0],
                                color=BLUE, stroke_width=4)
        ms_lbl = T("Model size", size=16, color=BLUE, vi=True).next_to(model_line, LEFT, buff=0.2)
        kv_big = seg(h_w + h_b, 2.7, RED, 0.6)
        kv_l2 = T("KV > Model size", size=18, color=RED, weight=BOLD, vi=True).next_to(
            kv_big, RIGHT, buff=0.3)
        self.play(Create(model_line), FadeIn(ms_lbl), run_time=0.6)
        self.play(Transform(kv, kv_big), Transform(kv_l, kv_l2), run_time=1.1)
        self.fill(s, d)

        # CÂU 03: không chỉ "model nhanh?" mà "đủ bộ nhớ?" -> icon ✗ / ✓ (hình)
        s, d = self.say("voice/s9g_03.mp3")
        speed = svg_icon("cpu", MUTED, height=1.0).move_to(RIGHT * 2.7 + UP * 1.4)
        sx = Cross(speed, stroke_color=RED, stroke_width=6).scale(0.75)
        s_cap = T("tốc độ tính", size=18, color=MUTED, vi=True).next_to(speed, DOWN, buff=0.2)
        chk = VMobject(stroke_color=GREEN, stroke_width=10)
        chk.set_points_as_corners([np.array([-0.25, 0.0, 0]), np.array([-0.05, -0.22, 0]),
                                   np.array([0.35, 0.32, 0])]).move_to(RIGHT * 2.7 + DOWN * 0.7)
        m_cap = T("đủ bộ nhớ?", size=18, color=GREEN, weight=BOLD, vi=True).next_to(chk, DOWN, buff=0.25)
        self.play(FadeIn(speed), FadeIn(s_cap), run_time=0.5)
        self.play(Create(sx), run_time=0.5)
        self.play(Create(chk), FadeIn(m_cap),
                  Indicate(VGroup(weights, buffers, kv), color=GREEN, scale_factor=1.05), run_time=1.0)
        self.fill(s, d)

        # CÂU 04: câu chốt + chuyển Throughput
        s, d = self.say("voice/s9g_04.mp3")
        self.play(FadeOut(VGroup(head, weights, buffers, kv, w_l, b_l, kv_l, model_line,
                  ms_lbl, speed, sx, s_cap, chk, m_cap)), run_time=0.5)
        punch = T("Bộ nhớ — không phải tốc độ tính —\nmới là trần thật sự của LLM Serving.",
                  size=30, color=WHITE, weight=BOLD, vi=True, line_spacing=0.9).move_to(UP * 0.4)
        self.play(Write(punch), run_time=1.5)
        self.play(punch.animate.set_color(YELLOW), run_time=0.6)
        self.fill(s, d)

        # CÂU 05: dẫn sang Throughput #3
        s, d = self.say("voice/s9g_05.mp3")
        nxt = RoundedRectangle(width=3.0, height=0.95, corner_radius=0.15, stroke_color=GREEN,
                               fill_color=GREEN, fill_opacity=0.18)
        nxt.add(T("Throughput", size=24, color=WHITE, weight=BOLD).move_to(nxt))
        num3 = T("3", size=26, color=GREEN, weight=BOLD).next_to(nxt, UP, buff=0.12).shift(LEFT * 1.25)
        grp = VGroup(nxt, num3).to_edge(DOWN, buff=0.7)
        arr = Arrow(punch.get_bottom(), nxt.get_top(), color=GREEN, buff=0.25, stroke_width=5)
        self.play(GrowArrow(arr), FadeIn(grp, shift=UP * 0.2), run_time=1.0)
        self.play(Indicate(nxt, color=GREEN, scale_factor=1.1), run_time=0.8)
        self.fill(s, d)
        self.wait(0.4)
