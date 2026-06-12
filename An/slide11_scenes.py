from manim import *
from mutagen.mp3 import MP3
import os

# ============================================================
# SLIDE 11 — HARDWARE COMPATIBILITY & ACCELERATION (5 cảnh)
# Style: 3Blue1Brown (bản đồ phần cứng, ghép cặp, tỏa nhánh G/Y/R) + theme Phần 2.
# Icon: SVG Lucide (assets/), recolor. KHÔNG LaTeX (chỉ Text). KHÔNG logo thương hiệu thật.
# Render (đứng TRONG slide11_themed/):
#   PYTHONUTF8=1 manim -qh --disable_caching slide11_scenes.py Slide11aBridge
#   ... Slide11bDevices Slide11cRuntime Slide11dCenterpiece Slide11eOutro
# ============================================================

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

# Quy ước màu Slide 11
C_HW = TEAL          # tag Hardware
C_OPT = BLUE         # khối Optimization
C_WORKS = GREEN      # works well
C_NEEDS = YELLOW     # needs adaptation
C_NOT = RED          # not supported
C_CLOUD = TEAL
C_PERSONAL = PURPLE
C_EDGE = ORANGE
C_TRADEOFF = MAROON

config.background_color = BG
TEXT_SS = 4
ASSETS = "assets"


def T(text, size=24, color=WHITE, weight=NORMAL, line_spacing=-1, vi=False):
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


def chip(text, color, fs=18):
    label = T(text, size=fs, color=color, weight=BOLD, vi=True)
    box = RoundedRectangle(width=label.width + 0.45, height=0.55, corner_radius=0.1,
                           stroke_color=color, fill_color=color, fill_opacity=0.15)
    label.move_to(box)
    return VGroup(box, label)


def check(color):
    c = VMobject(stroke_color=color, stroke_width=9)
    c.set_points_as_corners([np.array([-0.18, 0.0, 0]), np.array([-0.03, -0.16, 0]),
                             np.array([0.24, 0.24, 0])])
    return c


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
        c = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.08,
                             stroke_color=color, fill_color=color, fill_opacity=1)
        label = T(name, size=22, color=color, weight=BOLD, vi=vi).next_to(c, RIGHT, buff=0.18)
        return VGroup(c, label).to_corner(UL, buff=0.45)


# ============================================================
# CẢNH 1 — BRIDGE: nghiên cứu (1 GPU) vs thực tế (nhiều thiết bị)
# ============================================================
# Thay toàn bộ class Slide11aBridge hiện tại bằng đoạn dưới đây.
class Slide11aBridge(VoiceScene):
    def construct(self):
        def device_node(icon_name, label, color, pos):
            halo = Circle(
                radius=0.56,
                stroke_color=color,
                stroke_width=2.5,
                fill_color=color,
                fill_opacity=0.055,
            )
            icon = svg_icon(icon_name, color, height=0.60, sw=2.6).move_to(halo)
            name = T(label, size=14, color=color, weight=BOLD, vi=True)
            name.next_to(halo, RIGHT, buff=0.24)
            return VGroup(halo, icon, name).move_to(pos)

        def curved_link(start, end, bend):
            mid_x = (start[0] + end[0]) / 2
            return CubicBezier(
                start,
                np.array([mid_x - 0.25, start[1] + bend, 0]),
                np.array([mid_x + 0.25, end[1] + bend * 0.2, 0]),
                end,
            ).set_stroke(MUTED, width=2.2, opacity=0.45)

        def travelling_pulse(path, color, delay=0):
            dot = Dot(radius=0.065, color=color).move_to(path.get_start())
            ring = Circle(radius=0.15, color=color, stroke_width=2).move_to(dot)
            return Succession(
                Wait(delay),
                AnimationGroup(FadeIn(dot, scale=0.4), FadeIn(ring), run_time=0.12),
                AnimationGroup(
                    MoveAlongPath(dot, path, rate_func=linear),
                    MoveAlongPath(ring, path, rate_func=linear),
                    run_time=0.90,
                ),
                AnimationGroup(FadeOut(dot, scale=0.4), FadeOut(ring), run_time=0.14),
            )

        # ====================================================
        # CÂU 01 — Throughput #3 -> Hardware #4
        # ====================================================
        s, d = self.say("voice/s11a_01.mp3")

        tag_t = self.make_tag("Throughput", GREEN)
        tag_h = self.make_tag("Hardware", TEAL)
        self.add(tag_t)

        divider = Line(UP * 0.24, DOWN * 0.24, color=TEAL, stroke_width=2)
        divider.next_to(tag_h, RIGHT, buff=0.28)
        challenge = T(
            "TƯƠNG THÍCH PHẦN CỨNG",
            size=14, color=MUTED, weight=BOLD, vi=True,
        ).next_to(divider, RIGHT, buff=0.24)
        number = T("04", size=58, color=TEAL, weight=BOLD).set_opacity(0.12)
        number.to_corner(UR, buff=0.40)

        self.play(
            ReplacementTransform(tag_t, tag_h),
            Create(divider),
            FadeIn(challenge, shift=LEFT * 0.12),
            FadeIn(number, shift=LEFT * 0.15),
            run_time=0.75,
        )
        self.play(
            ShowPassingFlash(tag_h[0].copy().set_stroke(TEAL, width=7), time_width=0.35),
            run_time=0.50,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 02 — “ống kính nghiên cứu”: một GPU rất mạnh
        # ====================================================
        s, d = self.say("voice/s11a_02.mp3")

        lab_title = T(
            "MỘT GIẢ ĐỊNH RẤT TIỆN TRONG NGHIÊN CỨU",
            size=25, color=WHITE, weight=BOLD, vi=True,
        ).to_edge(UP, buff=0.88)

        lab_box = RoundedRectangle(
            width=7.25, height=4.35, corner_radius=0.20,
            stroke_color=SLATE, stroke_width=2,
            fill_color="#111c31", fill_opacity=0.96,
        ).move_to(DOWN * 0.22)

        lab_header = VGroup(
            Dot(radius=0.055, color=TEAL),
            T("RESEARCH LAB", size=14, color=TEAL, weight=BOLD),
        ).arrange(RIGHT, buff=0.12)
        lab_header.move_to(lab_box.get_corner(UL) + RIGHT * 0.95 + DOWN * 0.34)

        rack = RoundedRectangle(
            width=2.25, height=2.45, corner_radius=0.10,
            stroke_color=MUTED, stroke_width=2.5,
            fill_color=BG, fill_opacity=0.85,
        ).move_to(DOWN * 0.18)

        rack_slots = VGroup(*[
            RoundedRectangle(
                width=1.75, height=0.38, corner_radius=0.04,
                stroke_color=SLATE, stroke_width=1.8,
                fill_color=SLATE, fill_opacity=0.08,
            ) for _ in range(4)
        ]).arrange(DOWN, buff=0.12).move_to(rack)

        leds = VGroup(*[Dot(radius=0.035, color=GREEN) for _ in range(4)])
        for led, slot in zip(leds, rack_slots):
            led.move_to(slot.get_right() + LEFT * 0.18)

        gpu_glow = Circle(
            radius=0.58, stroke_color=TEAL, stroke_width=0,
            fill_color=TEAL, fill_opacity=0,
        ).move_to(rack)
        gpu_core = Circle(
            radius=0.50,
            stroke_color=TEAL, stroke_width=3,
            fill_color=BG, fill_opacity=0.92,
        ).move_to(rack)
        gpu_text = T("GPU", size=22, color=TEAL, weight=BOLD).move_to(gpu_core)
        gpu = VGroup(gpu_glow, gpu_core, gpu_text)

        prompt = VGroup(
            T("PROMPT", size=14, color=MUTED, weight=BOLD),
            VGroup(*[Dot(radius=0.035, color=BLUE) for _ in range(6)]).arrange(RIGHT, buff=0.10),
        ).arrange(DOWN, buff=0.16).move_to([-2.55, -0.18, 0])

        output = VGroup(
            T("OUTPUT", size=14, color=MUTED, weight=BOLD),
            VGroup(*[
                Line(LEFT * 0.18, RIGHT * 0.18, color=GREEN, stroke_width=3)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.12),
        ).arrange(DOWN, buff=0.16).move_to([2.55, -0.18, 0])

        in_path = Line(prompt.get_right() + RIGHT * 0.14, gpu_core.get_left() + LEFT * 0.05)
        out_path = Line(gpu_core.get_right() + RIGHT * 0.05, output.get_left() + LEFT * 0.14)
        in_path.set_stroke(BLUE, width=2.4, opacity=0.55)
        out_path.set_stroke(GREEN, width=2.4, opacity=0.55)

        assumption = VGroup(
            T("1 GPU NVIDIA rất mạnh", size=22, color=TEAL, weight=BOLD, vi=True),
            T(
                "data-center · nhiều bộ nhớ · điện năng dồi dào",
                size=15, color=MUTED, vi=True,
            ),
        ).arrange(DOWN, buff=0.12).next_to(lab_box, DOWN, buff=0.18)

        lab_group = VGroup(
            lab_box, lab_header, rack, rack_slots, leds, gpu,
            prompt, output, in_path, out_path, assumption,
        )

        self.play(FadeIn(lab_title, shift=DOWN * 0.12), run_time=0.45)
        self.play(FadeIn(lab_box, scale=0.97), FadeIn(lab_header), run_time=0.55)
        self.play(
            FadeIn(rack),
            LaggedStart(*[FadeIn(slot, shift=UP * 0.05) for slot in rack_slots], lag_ratio=0.10),
            FadeIn(leds),
            run_time=0.70,
        )
        self.play(
            FadeIn(gpu, scale=0.55),
            FadeIn(prompt, shift=RIGHT * 0.10),
            FadeIn(output, shift=LEFT * 0.10),
            Create(in_path), Create(out_path),
            FadeIn(assumption, shift=UP * 0.08),
            run_time=0.75,
        )
        self.play(
            travelling_pulse(in_path, BLUE),
            travelling_pulse(out_path, GREEN, delay=0.48),
            gpu_glow.animate(rate_func=there_and_back).scale(1.16).set_stroke(opacity=0.25),
            run_time=1.55,
        )
        self.play(
            ShowPassingFlash(gpu_core.copy().set_stroke(TEAL, width=8), time_width=0.30),
            run_time=0.55,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 03 — thu nhỏ “lab” và bung ra nhiều thiết bị
        # ====================================================
        s, d = self.say("voice/s11a_03.mp3")

        q1 = T("CÙNG MỘT CÁCH TỐI ƯU", size=27, color=BLUE, weight=BOLD, vi=True)
        q2a = T("có chạy tốt trên", size=24, color=WHITE, weight=BOLD, vi=True)
        q2b = T("MỌI THIẾT BỊ?", size=27, color=WHITE, weight=BOLD, vi=True)
        q2 = VGroup(q2a, q2b).arrange(RIGHT, buff=0.18)
        question = VGroup(q1, q2).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.72)
        underline = Line(q2b.get_left(), q2b.get_right(), color=TEAL, stroke_width=5)
        underline.next_to(q2b, DOWN, buff=0.08)

        lab_card = VGroup(lab_group, lab_title)
        self.play(
            lab_card.animate.scale(0.52).move_to(LEFT * 4.45 + DOWN * 0.32),
            FadeOut(challenge, shift=UP * 0.08),
            FadeOut(divider),
            FadeOut(number),
            FadeIn(question, shift=DOWN * 0.12),
            run_time=0.95,
        )

        case_label = chip("1 trường hợp", TEAL, fs=14)
        case_label.next_to(lab_card, DOWN, buff=0.14)
        self.play(FadeIn(case_label, shift=UP * 0.08), Create(underline), run_time=0.45)

        hub_halo = Circle(
            radius=0.86, stroke_color=BLUE, stroke_width=2.5,
            fill_color=BLUE, fill_opacity=0.06,
        ).move_to([-0.55, -0.32, 0])
        hub = RoundedRectangle(
            width=1.28, height=0.82, corner_radius=0.14,
            stroke_color=BLUE, stroke_width=3,
            fill_color=BLUE, fill_opacity=0.16,
        ).move_to(hub_halo)
        hub_text = T("OPT", size=23, color=BLUE, weight=BOLD).move_to(hub)
        hub_group = VGroup(hub_halo, hub, hub_text)

        nodes = VGroup(
            device_node("server", "cloud", TEAL, [3.25, 1.62, 0]),
            device_node("laptop", "máy cá nhân", PURPLE, [3.55, 0.48, 0]),
            device_node("smartphone", "điện thoại", ORANGE, [3.55, -0.78, 0]),
            device_node("cpu", "edge", YELLOW, [3.20, -2.00, 0]),
        )
        colors = [TEAL, PURPLE, ORANGE, YELLOW]
        bends = [0.95, 0.45, -0.35, -0.85]

        links = VGroup(*[
            curved_link(hub_group.get_right(), node[0].get_left(), bend)
            for node, bend in zip(nodes, bends)
        ])

        marks = VGroup(*[
            T("?", size=29, color=color, weight=BOLD).next_to(node, RIGHT, buff=0.22)
            for node, color in zip(nodes, colors)
        ])

        self.play(FadeIn(hub_group, scale=0.65), run_time=0.45)
        self.play(
            LaggedStart(*[Create(link) for link in links], lag_ratio=0.10),
            LaggedStart(*[FadeIn(node, shift=LEFT * 0.18) for node in nodes], lag_ratio=0.12),
            run_time=1.10,
        )
        self.play(
            *[
                travelling_pulse(path, color, delay=i * 0.13)
                for i, (path, color) in enumerate(zip(links, colors))
            ],
            LaggedStart(*[GrowFromCenter(mark) for mark in marks], lag_ratio=0.14),
            hub_halo.animate(rate_func=there_and_back).scale(1.10).set_stroke(opacity=0.20),
            run_time=1.85,
        )
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    Indicate(node[0], color=color, scale_factor=1.07),
                    Indicate(mark, color=color, scale_factor=1.14),
                )
                for node, mark, color in zip(nodes, marks, colors)
            ], lag_ratio=0.12),
            Indicate(q2b, color=TEAL, scale_factor=1.04),
            run_time=1.25,
        )
        self.fill(s, d)
        self.wait(0.30)

# ============================================================
# CẢNH 2 — BẢN ĐỒ PHẦN CỨNG (3 tầng, không đồng nhất)
# ============================================================
class Slide11bDevices(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Hardware", TEAL))
        # CÂU 01: tiêu đề
        s, d = self.say("voice/s11b_01.mp3")
        title = T("LLM triển khai ở RẤT nhiều nơi", size=30, color=WHITE, weight=BOLD, vi=True
                  ).to_edge(UP, buff=0.7)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
        self.fill(s, d)

        def tier(y, color, tname, icon_names, chips_texts):
            tlabel = T(tname, size=20, color=color, weight=BOLD, vi=True).move_to([-5.4, y, 0])
            icons = VGroup(*[svg_icon(n, color, 0.8) for n in icon_names]).arrange(RIGHT, buff=0.35)
            icons.move_to([-2.9, y, 0])
            chips = VGroup(*[chip(c, color) for c in chips_texts]).arrange(RIGHT, buff=0.3)
            chips.next_to(icons, RIGHT, buff=0.7)
            return tlabel, icons, chips

        t1 = tier(1.5, C_CLOUD, "Cloud /\ndata-center", ["cloud", "server"],
                  ["NVIDIA GPU", "AMD GPU", "TPU"])
        t2 = tier(-0.1, C_PERSONAL, "Máy\ncá nhân", ["laptop", "monitor"],
                  ["CPU", "consumer GPU"])
        t3 = tier(-1.7, C_EDGE, "Mobile /\nedge", ["smartphone", "cpu"],
                  ["bộ nhớ ↓", "năng lượng ↓", "tính toán ↓"])

        # CÂU 02..04: từng tầng
        for sid, (tl, ic, ch) in zip(["s11b_02", "s11b_03", "s11b_04"], [t1, t2, t3]):
            s, d = self.say(f"voice/{sid}.mp3")
            self.play(FadeIn(tl, shift=RIGHT * 0.1),
                      LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in ic], lag_ratio=0.15),
                      run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in ch], lag_ratio=0.2),
                      run_time=0.9)
            self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 3 — MỖI PHẦN CỨNG MỘT HỆ SINH THÁI / RUNTIME
# ============================================================
class Slide11cRuntime(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Hardware", TEAL))
        # CÂU 01: tiêu đề
        s, d = self.say("voice/s11c_01.mp3")
        title = T("Mỗi phần cứng — một hệ sinh thái riêng", size=30, color=WHITE, weight=BOLD,
                  vi=True).to_edge(UP, buff=0.7)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
        self.fill(s, d)

        def pair(y, hw, rt):
            hwc = chip(hw, TEAL).move_to([-3.4, y, 0])
            rtc = chip(rt, YELLOW).move_to([1.8, y, 0])
            ln = Line(hwc.get_right(), rtc.get_left(), color=MUTED, stroke_width=3)
            return hwc, rtc, ln

        # CÂU 02: NVIDIA-CUDA, AMD-ROCm
        s, d = self.say("voice/s11c_02.mp3")
        h1, r1, l1 = pair(1.6, "NVIDIA", "CUDA")
        h2, r2, l2 = pair(0.5, "AMD", "ROCm")
        self.play(FadeIn(h1), Create(l1), FadeIn(r1), run_time=0.8)
        self.play(FadeIn(h2), Create(l2), FadeIn(r2), run_time=0.8)
        self.fill(s, d)

        # CÂU 03: rừng runtime khác
        s, d = self.say("voice/s11c_03.mp3")
        others = VGroup(*[chip(x, YELLOW) for x in ["Vulkan", "OpenCL", "DirectX", "SYCL"]]
                        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to([1.8, -1.3, 0])
        oh = chip("khác", TEAL).move_to([-3.4, -1.3, 0])
        ol = Line(oh.get_right(), others.get_left(), color=MUTED, stroke_width=3)
        self.play(FadeIn(oh), Create(ol),
                  LaggedStart(*[FadeIn(c, scale=0.8) for c in others], lag_ratio=0.15), run_time=1.3)
        self.fill(s, d)

        # CÂU 04: accelerator -> runtime riêng
        s, d = self.say("voice/s11c_04.mp3")
        acc = chip("Accelerator", TEAL).move_to([-3.4, -2.5, 0])
        accr = chip("runtime + compiler riêng", ORANGE).move_to([1.8, -2.5, 0])
        accl = Line(acc.get_right(), accr.get_left(), color=MUTED, stroke_width=3)
        self.play(FadeIn(acc), Create(accl), FadeIn(accr), run_time=0.9)
        self.fill(s, d)

        # CÂU 05: không có mẫu số chung
        s, d = self.say("voice/s11c_05.mp3")
        allrt = VGroup(r1, r2, others, accr)
        note = T("→ không có mẫu số chung", size=24, color=RED, weight=BOLD, vi=True
                 ).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        self.play(LaggedStart(*[Indicate(c, color=YELLOW, scale_factor=1.1) for c in allrt],
                  lag_ratio=0.1), FadeIn(note, shift=LEFT * 0.2), run_time=1.4)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 4 — CENTERPIECE: 1 tối ưu tỏa nhánh G/Y/R
# ============================================================
class Slide11dCenterpiece(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Hardware", TEAL))
        title = T("Một tối ưu — KHÔNG chạy tốt khắp nơi", size=30, color=WHITE, weight=BOLD,
                  vi=True).to_edge(UP, buff=0.7)
        # CÂU 01: khối Optimization + backends
        s, d = self.say("voice/s11d_01.mp3")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
        opt = RoundedRectangle(width=2.4, height=1.3, corner_radius=0.15, stroke_color=C_OPT,
                               fill_color=C_OPT, fill_opacity=0.2).move_to(LEFT * 3.8 + DOWN * 0.3)
        opt.add(T("Optimization", size=20, color=C_OPT, weight=BOLD, vi=True).move_to(opt))
        ys = [2.0, 0.7, -0.6, -1.9]
        names = ["NVIDIA", "AMD", "Mobile", "Edge"]
        backs = VGroup(*[chip(n, WHITE).move_to([3.3, y, 0]) for n, y in zip(names, ys)])
        self.play(FadeIn(opt, scale=0.8), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in backs],
                  lag_ratio=0.12), run_time=1.2)
        self.fill(s, d)

        def beam(back, color, verdict):
            ar = Arrow(opt.get_right(), back.get_left(), color=color, buff=0.15, stroke_width=4)
            vl = T(verdict, size=17, color=color, weight=BOLD, vi=True).next_to(back, RIGHT, buff=0.25)
            return ar, vl

        # CÂU 02: NVIDIA works (G), AMD needs (Y)
        s, d = self.say("voice/s11d_02.mp3")
        a1, v1 = beam(backs[0], C_WORKS, "works well")
        a2, v2 = beam(backs[1], C_NEEDS, "needs adaptation")
        self.play(GrowArrow(a1), backs[0].animate.set_color(C_WORKS), FadeIn(v1), run_time=0.7)
        self.play(GrowArrow(a2), backs[1].animate.set_color(C_NEEDS), FadeIn(v2), run_time=0.7)
        self.fill(s, d)

        # CÂU 03: Mobile not supported (R)
        s, d = self.say("voice/s11d_03.mp3")
        a3, v3 = beam(backs[2], C_NOT, "not supported")
        self.play(GrowArrow(a3), backs[2].animate.set_color(C_NOT), FadeIn(v3), run_time=0.8)
        self.fill(s, d)

        # CÂU 04: Edge thiếu bộ nhớ (R)
        s, d = self.say("voice/s11d_04.mp3")
        a4, v4 = beam(backs[3], C_NOT, "thiếu bộ nhớ")
        self.play(GrowArrow(a4), backs[3].animate.set_color(C_NOT), FadeIn(v4), run_time=0.8)
        self.fill(s, d)

        # CÂU 05: nơi mượt / chỉnh / chịu thua
        s, d = self.say("voice/s11d_05.mp3")
        cap = T("cùng 1 ý tưởng:  nơi mượt · nơi cần chỉnh · nơi chịu thua", size=22, color=WHITE,
                weight=BOLD, vi=True).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap, shift=UP * 0.15),
                  LaggedStart(Indicate(v1, color=C_WORKS), Indicate(v2, color=C_NEEDS),
                  Indicate(v3, color=C_NOT), Indicate(v4, color=C_NOT), lag_ratio=0.2), run_time=1.4)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 5 — OUTRO (hình-trước, ít chữ) -> Trade-off #5
# ============================================================
# ============================================================
# THAY TOÀN BỘ class Slide11eOutro hiện tại bằng đoạn dưới đây
# Ý tưởng mới: 4 câu thoại = 4 lớp hình ảnh rõ ràng
#   1) System problem: request được route tới đúng hardware + backend
#   2) Heterogeneity: phổ thiết bị từ server mạnh -> edge hạn chế
#   3) Đã check 4 bottleneck -> còn câu hỏi chất lượng
#   4) Chuyển sang Trade-off #5 bằng cán cân nhanh/rẻ vs chất lượng
# ============================================================
class Slide11eOutro(VoiceScene):
    def construct(self):
        tag = self.make_tag("Hardware", TEAL)
        self.add(tag)

        # ---------------------- local helpers ----------------------
        def small_check(color=GREEN):
            m = VMobject(stroke_color=color, stroke_width=7)
            m.set_points_as_corners([
                np.array([-0.15, 0.00, 0]),
                np.array([-0.03, -0.13, 0]),
                np.array([0.22, 0.18, 0]),
            ])
            return m

        def device_icon(kind, color):
            """Icon bằng shape đơn giản để tránh lệ thuộc assets SVG."""
            if kind == "server":
                body = VGroup(*[
                    RoundedRectangle(
                        width=0.78, height=0.20, corner_radius=0.035,
                        stroke_color=color, stroke_width=2.2,
                        fill_color=color, fill_opacity=0.055,
                    ) for _ in range(3)
                ]).arrange(DOWN, buff=0.07)
                lights = VGroup(*[Dot(radius=0.025, color=color) for _ in range(3)])
                for dot, slot in zip(lights, body):
                    dot.move_to(slot.get_right() + LEFT * 0.11)
                return VGroup(body, lights)

            if kind == "laptop":
                screen = RoundedRectangle(
                    width=0.72, height=0.43, corner_radius=0.04,
                    stroke_color=color, stroke_width=2.2,
                    fill_color=color, fill_opacity=0.055,
                )
                base = Line(LEFT * 0.46, RIGHT * 0.46, color=color, stroke_width=4)
                base.next_to(screen, DOWN, buff=0.05)
                return VGroup(screen, base)

            if kind == "phone":
                phone = RoundedRectangle(
                    width=0.38, height=0.76, corner_radius=0.08,
                    stroke_color=color, stroke_width=2.3,
                    fill_color=color, fill_opacity=0.055,
                )
                speaker = Line(LEFT * 0.08, RIGHT * 0.08, color=color, stroke_width=2)
                speaker.move_to(phone.get_top() + DOWN * 0.08)
                return VGroup(phone, speaker)

            # edge / chip
            chip_body = RoundedRectangle(
                width=0.58, height=0.58, corner_radius=0.05,
                stroke_color=color, stroke_width=2.3,
                fill_color=color, fill_opacity=0.055,
            )
            pins = VGroup()
            for x in [-0.23, 0, 0.23]:
                pins.add(Line([x, 0.34, 0], [x, 0.46, 0], color=color, stroke_width=2))
                pins.add(Line([x, -0.34, 0], [x, -0.46, 0], color=color, stroke_width=2))
            for y in [-0.23, 0, 0.23]:
                pins.add(Line([-0.34, y, 0], [-0.46, y, 0], color=color, stroke_width=2))
                pins.add(Line([0.34, y, 0], [0.46, y, 0], color=color, stroke_width=2))
            return VGroup(chip_body, pins)

        def backend_chip(text, color, fs=13):
            label = T(text, size=fs, color=color, weight=BOLD, vi=True)
            box = RoundedRectangle(
                width=label.width + 0.34, height=0.36, corner_radius=0.09,
                stroke_color=color, stroke_width=1.8,
                fill_color=color, fill_opacity=0.12,
            )
            label.move_to(box)
            return VGroup(box, label)

        def resource_meter(value, color, label=""):
            """value: 0..1, vẽ thanh tài nguyên nhỏ gọn."""
            bg = RoundedRectangle(
                width=0.92, height=0.10, corner_radius=0.035,
                stroke_color=SLATE, stroke_width=1.1,
                fill_color=SLATE, fill_opacity=0.15,
            )
            fg = RoundedRectangle(
                width=max(0.07, 0.92 * value), height=0.10, corner_radius=0.035,
                stroke_color=color, stroke_width=0,
                fill_color=color, fill_opacity=0.88,
            )
            fg.move_to(bg)
            fg.align_to(bg, LEFT)
            bar = VGroup(bg, fg)
            txt = T(label, size=8.5, color=MUTED, weight=BOLD, vi=True)
            return VGroup(txt, bar).arrange(RIGHT, buff=0.07)

        def environment_card(kind, title, backend, color, power, pos):
            card = RoundedRectangle(
                width=2.02, height=1.42, corner_radius=0.14,
                stroke_color=color, stroke_width=2.25,
                fill_color=color, fill_opacity=0.065,
            )
            icon = device_icon(kind, color).scale(0.64)
            name = T(title, size=13, color=WHITE, weight=BOLD, vi=True)
            be = backend_chip(backend, color, fs=10.5)
            meter = resource_meter(power, color, "tài nguyên").scale(0.96)
            inner = VGroup(icon, name, be, meter).arrange(DOWN, buff=0.085).move_to(card)
            return VGroup(card, inner).move_to(pos)

        def pulse_along(path, color, delay=0):
            dot = Dot(radius=0.055, color=color).move_to(path.get_start())
            halo = Circle(radius=0.16, stroke_color=color, stroke_width=2).move_to(dot)
            return Succession(
                Wait(delay),
                AnimationGroup(FadeIn(dot, scale=0.45), FadeIn(halo), run_time=0.10),
                AnimationGroup(
                    MoveAlongPath(dot, path, rate_func=linear),
                    MoveAlongPath(halo, path, rate_func=linear),
                    run_time=0.80,
                ),
                AnimationGroup(FadeOut(dot, scale=0.45), FadeOut(halo), run_time=0.12),
            )

        def status_mark(kind, color):
            disk = Circle(
                radius=0.23, stroke_color=color, stroke_width=2.4,
                fill_color=BG, fill_opacity=0.94,
            )
            if kind == "ok":
                mark = small_check(color).scale(0.92).move_to(disk)
            elif kind == "adjust":
                mark = VGroup(
                    Line(UP * 0.12, DOWN * 0.03, color=color, stroke_width=5.5),
                    Dot(DOWN * 0.14, radius=0.034, color=color),
                ).move_to(disk)
            else:
                mark = T("?", size=23, color=color, weight=BOLD).move_to(disk)
            return VGroup(disk, mark)

        # ====================================================
        # CÂU 01 — serving là bài toán hệ thống: đúng hardware + backend
        # ====================================================
        s, d = self.say("voice/s11e_01.mp3")

        title1 = T(
            "LLM serving = chọn đúng hệ thống cho từng môi trường",
            size=25, color=WHITE, weight=BOLD, vi=True,
        ).to_edge(UP, buff=0.86)
        subtitle1 = T(
            "không chỉ tối ưu thuật toán",
            size=15, color=MUTED, weight=BOLD, vi=True,
        ).next_to(title1, DOWN, buff=0.10)

        request = VGroup(
            RoundedRectangle(
                width=1.30, height=0.76, corner_radius=0.14,
                stroke_color=BLUE, stroke_width=2.8,
                fill_color=BLUE, fill_opacity=0.14,
            ),
            T("LLM\nrequest", size=15, color=BLUE, weight=BOLD, vi=True),
        )
        request[1].move_to(request[0])
        request.move_to(LEFT * 4.95 + UP * 0.12)

        cards = VGroup(
            environment_card("server", "Data-center", "CUDA / ROCm / TPU", TEAL, 0.95, [1.05, 1.28, 0]),
            environment_card("laptop", "Máy cá nhân", "Vulkan / DirectX", PURPLE, 0.62, [1.30, -0.25, 0]),
            environment_card("phone", "Mobile / edge", "runtime riêng", ORANGE, 0.32, [1.05, -1.78, 0]),
        )

        router = Circle(
            radius=0.47, stroke_color=BLUE, stroke_width=2.8,
            fill_color=BLUE, fill_opacity=0.10,
        ).move_to(LEFT * 2.45 + UP * 0.10)
        router_lbl = T("route", size=15, color=BLUE, weight=BOLD).move_to(router)
        router_group = VGroup(router, router_lbl)

        entry = Line(request.get_right(), router.get_left(), color=BLUE, stroke_width=2.8)
        routes = VGroup(*[
            CubicBezier(
                router.get_right(),
                router.get_right() + RIGHT * 0.75 + UP * bend,
                card.get_left() + LEFT * 0.62,
                card.get_left(),
            ).set_stroke(color, width=2.5, opacity=0.62)
            for card, bend, color in zip(cards, [0.58, 0.0, -0.58], [TEAL, PURPLE, ORANGE])
        ])
        marks = VGroup(*[
            status_mark("ok", GREEN).next_to(card, RIGHT, buff=0.16)
            for card in cards
        ])

        self.play(FadeIn(title1, shift=DOWN * 0.12), FadeIn(subtitle1), run_time=0.45)
        self.play(FadeIn(request, scale=0.75), FadeIn(router_group, scale=0.75), Create(entry), run_time=0.55)
        self.play(
            LaggedStart(*[FadeIn(card, shift=LEFT * 0.18) for card in cards], lag_ratio=0.11),
            LaggedStart(*[Create(route) for route in routes], lag_ratio=0.10),
            run_time=1.05,
        )
        self.play(
            pulse_along(entry, BLUE),
            *[pulse_along(path, color, delay=0.20 + i * 0.16)
              for i, (path, color) in enumerate(zip(routes, [TEAL, PURPLE, ORANGE]))],
            LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.13),
            run_time=1.55,
        )
        self.play(
            LaggedStart(*[
                Indicate(card[0], color=color, scale_factor=1.045)
                for card, color in zip(cards, [TEAL, PURPLE, ORANGE])
            ], lag_ratio=0.10),
            run_time=0.80,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 02 — không đồng nhất: phổ thiết bị từ mạnh đến hạn chế
        # ====================================================
        s, d = self.say("voice/s11e_02.mp3")

        hetero_title = T("KHÔNG ĐỒNG NHẤT", size=32, color=TEAL, weight=BOLD, vi=True)
        hetero_title.to_edge(UP, buff=0.92)
        spectrum_line = Line(LEFT * 3.75, RIGHT * 3.75, color=SLATE, stroke_width=3).move_to(DOWN * 1.72)
        left_note = T("máy chủ mạnh", size=15, color=TEAL, weight=BOLD, vi=True).next_to(spectrum_line, LEFT, buff=0.22)
        right_note = T("thiết bị cuối", size=15, color=ORANGE, weight=BOLD, vi=True).next_to(spectrum_line, RIGHT, buff=0.22)
        arrow_tip = Arrow(
            spectrum_line.get_start(), spectrum_line.get_end(),
            color=SLATE, stroke_width=0, buff=0, max_tip_length_to_length_ratio=0.055,
        )

        spectrum_cards = VGroup(
            environment_card("server", "Server", "nhiều tài nguyên", TEAL, 0.95, [-2.80, -0.10, 0]),
            environment_card("laptop", "PC", "trung bình", PURPLE, 0.62, [0.00, -0.10, 0]),
            environment_card("phone", "Phone", "hạn chế", ORANGE, 0.36, [2.80, -0.10, 0]),
        ).scale(0.90)
        spectrum_marks = VGroup(
            status_mark("ok", GREEN).next_to(spectrum_cards[0], UP, buff=0.12),
            status_mark("adjust", YELLOW).next_to(spectrum_cards[1], UP, buff=0.12),
            status_mark("adjust", YELLOW).next_to(spectrum_cards[2], UP, buff=0.12),
        )
        scan_box = DashedVMobject(
            SurroundingRectangle(VGroup(spectrum_cards, spectrum_marks), color=TEAL, corner_radius=0.18, buff=0.28),
            num_dashes=42,
        ).set_stroke(TEAL, width=2.1, opacity=0.68)

        self.play(
            FadeOut(VGroup(title1, subtitle1, request, router_group, entry, routes, cards, marks), shift=UP * 0.08),
            FadeIn(hetero_title, shift=DOWN * 0.12),
            run_time=0.65,
        )
        self.play(
            FadeIn(spectrum_cards, shift=UP * 0.10),
            LaggedStart(*[GrowFromCenter(m) for m in spectrum_marks], lag_ratio=0.12),
            Create(spectrum_line), FadeIn(arrow_tip), FadeIn(left_note), FadeIn(right_note),
            run_time=1.05,
        )
        self.play(
            Create(scan_box),
            LaggedStart(*[
                Indicate(card[0], color=color, scale_factor=1.045)
                for card, color in zip(spectrum_cards, [TEAL, PURPLE, ORANGE])
            ], lag_ratio=0.14),
            run_time=1.30,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 03 — 4 bottleneck đã check, còn chất lượng
        # ====================================================
        s, d = self.say("voice/s11e_03.mp3")

        checks_title = T(
            "Giả sử 4 nút thắt đã được xử lý...",
            size=25, color=WHITE, weight=BOLD, vi=True,
        ).to_edge(UP, buff=0.92)
        solved = VGroup(
            backend_chip("Latency", RED, fs=15),
            backend_chip("Memory", YELLOW, fs=15),
            backend_chip("Throughput", GREEN, fs=15),
            backend_chip("Hardware", TEAL, fs=15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(LEFT * 3.30 + DOWN * 0.12)
        solved_ticks = VGroup(*[
            small_check(GREEN).scale(0.66).next_to(item, RIGHT, buff=0.22)
            for item in solved
        ])

        quality_orb = Circle(
            radius=0.82, stroke_color=MAROON, stroke_width=3.2,
            fill_color=MAROON, fill_opacity=0.10,
        ).move_to(RIGHT * 2.50 + DOWN * 0.02)
        quality_q = T("?", size=62, color=MAROON, weight=BOLD).move_to(quality_orb)
        quality_lbl = T("chất lượng", size=21, color=MAROON, weight=BOLD, vi=True)
        quality_lbl.next_to(quality_orb, DOWN, buff=0.18)
        bridge = Arrow(
            solved.get_right() + RIGHT * 0.45,
            quality_orb.get_left() + LEFT * 0.10,
            color=MUTED, stroke_width=3.0, buff=0,
            max_tip_length_to_length_ratio=0.075,
        )
        final_question = T(
            "câu hỏi cuối",
            size=15, color=MUTED, weight=BOLD, vi=True,
        ).next_to(bridge, UP, buff=0.16)

        self.play(
            FadeOut(VGroup(hetero_title, spectrum_cards, spectrum_marks, spectrum_line, arrow_tip,
                           left_note, right_note, scan_box), shift=DOWN * 0.10),
            FadeIn(checks_title, shift=DOWN * 0.12),
            run_time=0.65,
        )
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT * 0.12) for item in solved], lag_ratio=0.10),
            run_time=0.65,
        )
        self.play(
            LaggedStart(*[Create(t) for t in solved_ticks], lag_ratio=0.10),
            Create(bridge), FadeIn(final_question),
            FadeIn(quality_orb, scale=0.72), FadeIn(quality_q, scale=0.55), FadeIn(quality_lbl),
            run_time=1.15,
        )
        self.play(
            Flash(quality_orb, color=MAROON, flash_radius=1.15, line_length=0.15, num_lines=14),
            Indicate(VGroup(quality_q, quality_lbl), color=MAROON, scale_factor=1.08),
            run_time=0.85,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 04 — Trade-off #5: cán cân đòn thật, vật nằm TRÊN đĩa cân
        # ====================================================
        s, d = self.say("voice/s11e_04.mp3")

        trade_tag = self.make_tag("Trade-off", MAROON)
        trade_title = T("Trade-off #5", size=35, color=MAROON, weight=BOLD).to_edge(UP, buff=0.90)
        trade_subtitle = T(
            "nhanh hơn / rẻ hơn  ↔  chất lượng còn giữ được không?",
            size=17, color=WHITE, weight=BOLD, vi=True,
        ).next_to(trade_title, DOWN, buff=0.10)

        # ----------------------------------------------------
        # 1) Thân cân đứng yên — chỉ phần đòn cân chuyển động
        # ----------------------------------------------------
        pivot_point = np.array([0.0, 0.42, 0.0])

        post = RoundedRectangle(
            width=0.34, height=2.45, corner_radius=0.08,
            stroke_color=MAROON, stroke_width=3.0,
            fill_color=MAROON, fill_opacity=0.055,
        ).move_to(pivot_point + DOWN * 1.45)

        left_pedestal = CubicBezier(
            np.array([-0.23, -1.66, 0]),
            np.array([-0.28, -2.05, 0]),
            np.array([-0.58, -2.22, 0]),
            np.array([-0.93, -2.28, 0]),
        ).set_stroke(MAROON, width=3.0)
        right_pedestal = left_pedestal.copy().flip(RIGHT)

        base_top = ArcBetweenPoints(
            np.array([-0.93, -2.28, 0]),
            np.array([0.93, -2.28, 0]),
            angle=-PI / 3,
            color=MAROON, stroke_width=3.0,
        )
        base = RoundedRectangle(
            width=2.18, height=0.19, corner_radius=0.04,
            stroke_color=MAROON, stroke_width=3.0,
            fill_color=MAROON, fill_opacity=0.055,
        ).move_to([0, -2.47, 0])

        pivot_outer = Circle(
            radius=0.33, stroke_color=MAROON, stroke_width=3.2,
            fill_color=BG, fill_opacity=1,
        ).move_to(pivot_point)
        pivot_inner = Circle(
            radius=0.18, stroke_color=MAROON, stroke_width=2.7,
            fill_color=MAROON, fill_opacity=0.08,
        ).move_to(pivot_point)

        finial_stem = Line(
            pivot_point + UP * 0.32,
            pivot_point + UP * 0.60,
            color=MAROON, stroke_width=3.0,
        )
        finial = Circle(
            radius=0.13, stroke_color=MAROON, stroke_width=2.7,
            fill_color=BG, fill_opacity=1,
        ).move_to(pivot_point + UP * 0.72)

        stand = VGroup(
            post, left_pedestal, right_pedestal, base_top, base,
            pivot_outer, pivot_inner, finial_stem, finial,
        )

        # ----------------------------------------------------
        # 2) Đòn cân động: hai đĩa luôn nằm ngang như cân thật
        # ----------------------------------------------------
        angle = ValueTracker(0.0)
        HALF_BEAM = 4.18
        PAN_DROP = 1.16
        PAN_HALF_WIDTH = 0.88

        def rotated(v, theta):
            c, sn = np.cos(theta), np.sin(theta)
            return np.array([
                c * v[0] - sn * v[1],
                sn * v[0] + c * v[1],
                0.0,
            ])

        def beam_end(side):
            # side = -1: trái, side = +1: phải
            return pivot_point + rotated(np.array([side * HALF_BEAM, 0, 0]), angle.get_value())

        def pan_rim_center(side):
            end = beam_end(side)
            return np.array([end[0], end[1] - PAN_DROP, 0])

        def build_moving_scale():
            theta = angle.get_value()
            left_end = beam_end(-1)
            right_end = beam_end(+1)

            # Hai đường song song tạo cảm giác đòn cân có độ dày.
            normal = rotated(np.array([0, 0.055, 0]), theta)
            beam_top = Line(
                left_end + normal, right_end + normal,
                color=MAROON, stroke_width=3.4,
            )
            beam_bottom = Line(
                left_end - normal, right_end - normal,
                color=MAROON, stroke_width=3.4,
            )

            pieces = VGroup(beam_top, beam_bottom)

            for side, end in [(-1, left_end), (+1, right_end)]:
                rim_center = pan_rim_center(side)
                rim_left = rim_center + LEFT * PAN_HALF_WIDTH
                rim_right = rim_center + RIGHT * PAN_HALF_WIDTH

                end_joint = Circle(
                    radius=0.115, stroke_color=MAROON, stroke_width=2.7,
                    fill_color=BG, fill_opacity=1,
                ).move_to(end)
                end_pin = Dot(end, radius=0.038, color=MAROON)

                # Hai dây treo nối từ một khớp đòn xuống hai mép đĩa.
                rope_left = Line(end, rim_left, color=MAROON, stroke_width=2.4)
                rope_right = Line(end, rim_right, color=MAROON, stroke_width=2.4)
                rim = Line(rim_left, rim_right, color=MAROON, stroke_width=3.0)
                bowl = ArcBetweenPoints(
                    rim_left, rim_right,
                    angle=-PI / 2.15,
                    color=MAROON, stroke_width=3.0,
                )
                pieces.add(end_joint, end_pin, rope_left, rope_right, rim, bowl)

            return pieces

        moving_scale = always_redraw(build_moving_scale)

        # ----------------------------------------------------
        # 3) Vật nặng được đặt trực tiếp lên đĩa, không bay lơ lửng
        # ----------------------------------------------------
        speed_chip_row = VGroup(
            backend_chip("nhanh", BLUE, fs=14),
            backend_chip("rẻ", GREEN, fs=14),
        ).arrange(RIGHT, buff=0.12).scale(0.96)
        speed_plate = RoundedRectangle(
            width=speed_chip_row.width + 0.34,
            height=speed_chip_row.height + 0.20,
            corner_radius=0.12,
            stroke_color=MUTED,
            stroke_width=1.8,
            fill_color=BG,
            fill_opacity=0.96,
        )
        speed_plate.move_to(speed_chip_row)
        speed_tokens = VGroup(speed_plate, speed_chip_row)

        quality_token = VGroup(
            Circle(
                radius=0.38, stroke_color=MAROON, stroke_width=3.2,
                fill_color=BG, fill_opacity=0.98,
            ),
            Circle(
                radius=0.30, stroke_color=MAROON, stroke_width=1.4,
                fill_color=MAROON, fill_opacity=0.12,
            ),
            T("?", size=34, color=MAROON, weight=BOLD),
        )
        quality_token[1].move_to(quality_token[0])
        quality_token[2].move_to(quality_token[0])

        left_drop = ValueTracker(1.20)
        right_drop = ValueTracker(1.20)

        def put_left_weight_on_pan(mob):
            mob.move_to(pan_rim_center(-1) + UP * (0.42 + left_drop.get_value()))

        def put_right_weight_on_pan(mob):
            mob.move_to(pan_rim_center(+1) + UP * (0.48 + right_drop.get_value()))

        speed_tokens.add_updater(put_left_weight_on_pan)
        quality_token.add_updater(put_right_weight_on_pan)

        left_label = T("nhanh / rẻ", size=22, color=WHITE, weight=BOLD, vi=True)
        right_label = T("chất lượng ?", size=22, color=WHITE, weight=BOLD, vi=True)
        left_label.add_updater(
            lambda m: m.move_to(pan_rim_center(-1) + DOWN * 0.78)
        )
        right_label.add_updater(
            lambda m: m.move_to(pan_rim_center(+1) + DOWN * 0.78)
        )

        # ----------------------------------------------------
        # 4) Chuyển cảnh và chuyển động vật lý
        # ----------------------------------------------------
        self.play(
            ReplacementTransform(tag, trade_tag),
            FadeOut(VGroup(
                checks_title, solved, solved_ticks, bridge, final_question,
                quality_orb, quality_q, quality_lbl,
            ), shift=DOWN * 0.10),
            FadeIn(trade_title, shift=DOWN * 0.10),
            FadeIn(trade_subtitle),
            run_time=0.70,
        )

        self.play(
            LaggedStart(
                Create(base),
                Create(base_top),
                AnimationGroup(Create(left_pedestal), Create(right_pedestal)),
                Create(post),
                GrowFromCenter(pivot_outer),
                GrowFromCenter(pivot_inner),
                Create(finial_stem),
                GrowFromCenter(finial),
                lag_ratio=0.10,
            ),
            run_time=1.05,
        )
        self.play(Create(moving_scale), run_time=0.85)

        # "nhanh" và "rẻ" rơi xuống, chạm đĩa trái -> đòn cân nghiêng trái.
        self.add(speed_tokens)
        self.play(
            FadeIn(speed_tokens, shift=UP * 0.18),
            left_drop.animate.set_value(0.0),
            angle.animate.set_value(4.0 * DEGREES),
            run_time=0.85,
            rate_func=smooth,
        )

        # Dấu hỏi chất lượng rơi vào đĩa phải, cân dao động rồi ổn định.
        self.add(quality_token)
        self.play(
            FadeIn(quality_token, shift=UP * 0.18),
            right_drop.animate.set_value(0.0),
            angle.animate.set_value(-2.0 * DEGREES),
            run_time=0.82,
            rate_func=smooth,
        )
        self.play(
            angle.animate.set_value(2.0 * DEGREES),
            run_time=0.52,
            rate_func=smooth,
        )

        self.play(
            FadeIn(left_label, shift=UP * 0.08),
            FadeIn(right_label, shift=UP * 0.08),
            run_time=0.42,
        )
        self.play(
            Flash(
                quality_token,
                color=MAROON,
                flash_radius=0.68,
                line_length=0.11,
                num_lines=10,
            ),
            Indicate(quality_token, color=MAROON, scale_factor=1.08),
            run_time=0.72,
        )

        self.fill(s, d)
        self.wait(0.35)

        # Tránh updater còn chạy nếu ghép scene theo cách khác.
        speed_tokens.clear_updaters()
        quality_token.clear_updaters()
        left_label.clear_updaters()
        right_label.clear_updaters()
