from manim import *
from mutagen.mp3 import MP3
import os

# ============================================================
# SLIDE 8 — LATENCY AND RESPONSE TIME (chi tiết, 7 cảnh)
# Style: ByteByteGo × 3Blue1Brown. Theme đồng bộ Slide 7.
# Render (đứng TRONG slide8_themed/ để voice/ đúng path):
#   manim -qh slide8_scenes.py Slide8aHook
#   ... Slide8bTTFT / Slide8cTPOT / Slide8dFormula
#   ... Slide8eTDS / Slide8fHumanAxis / Slide8gOutro
# ============================================================

# ---------- THEME (đồng bộ slide7_themed) ----------
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

FILL_SOFT = 0.12
FILL_MEDIUM = 0.18

# Quy ước màu Slide 8
C_LATENCY = RED
C_MEMORY = YELLOW
C_THROUGHPUT = GREEN
C_HARDWARE = TEAL
C_ACCURACY = MAROON
C_TTFT = YELLOW
C_TPOT = TEAL
C_TOTAL = MAROON
C_TDS = GREEN
C_READ = ORANGE
C_SPEAK = PURPLE

config.background_color = BG

TEXT_SS = 4


def T(text, size=24, color=WHITE, weight=NORMAL, line_spacing=-1, vi=False):
    # Render cỡ lớn rồi scale xuống -> tránh "hở chữ" của ManimPango ở cỡ nhỏ.
    kwargs = dict(font_size=size * TEXT_SS, color=color, weight=weight, line_spacing=line_spacing)
    if vi or any(ord(ch) > 127 or ch.isdigit() for ch in text):
        kwargs["font"] = FONT_VI
    return Text(text, **kwargs).scale(1 / TEXT_SS)


def audio_duration(path):
    if not os.path.exists(path):
        print(f"[WARNING] Không tìm thấy audio: {path}")
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

    def make_node_label(self, name, color, vi=False):
        chip = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.08,
                                stroke_color=color, fill_color=color, fill_opacity=1)
        label = T(name, size=22, color=color, weight=BOLD, vi=vi).next_to(chip, RIGHT, buff=0.18)
        return VGroup(chip, label).to_corner(UL, buff=0.45)


# ============================================================
# CẢNH 1 — HOOK: bản đồ 5 thách thức -> zoom Latency -> chat chờ
# ============================================================
class Slide8aHook(VoiceScene):
    def construct(self):
        names = ["Latency", "Memory", "Throughput", "Hardware", "Trade-off"]
        cols = [C_LATENCY, C_MEMORY, C_THROUGHPUT, C_HARDWARE, C_ACCURACY]
        chips = VGroup()
        for nm, c in zip(names, cols):
            box = RoundedRectangle(width=2.25, height=0.95, corner_radius=0.15,
                                   stroke_color=c, fill_color=c, fill_opacity=FILL_MEDIUM)
            chips.add(VGroup(box, T(nm, size=21, color=WHITE, weight=BOLD).move_to(box)))
        chips.arrange(RIGHT, buff=0.28).move_to(ORIGIN)

        # ----- CÂU 01: hiện 5 thách thức -----
        s, d = self.say("voice/s8a_01.mp3")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in chips], lag_ratio=0.13),
                  run_time=1.3)
        self.fill(s, d)

        # ----- CÂU 02: nhấn Latency #1, mờ 4 chip kia, zoom -----
        s, d = self.say("voice/s8a_02.mp3")
        lat = chips[0]
        num1 = T("1", size=28, color=WHITE, weight=BOLD).next_to(lat, UP, buff=0.15)
        self.play(lat[0].animate.set_fill(C_LATENCY, opacity=0.45),
                  Indicate(lat, color=C_LATENCY, scale_factor=1.12),
                  FadeIn(num1, scale=0.6), run_time=0.9)
        self.play(VGroup(*[chips[i] for i in range(1, 5)]).animate.set_opacity(0.12),
                  run_time=0.5)
        self.play(FadeOut(VGroup(*[chips[i] for i in range(1, 5)])),
                  FadeOut(num1),
                  lat.animate.scale(0.42).to_corner(UL, buff=0.45), run_time=0.9)
        tag = self.make_node_label("Latency", C_LATENCY, vi=True)
        self.play(FadeIn(tag), FadeOut(lat), run_time=0.4)
        self.fill(s, d)

        # ----- Khung chat + đồng hồ + thanh kiên nhẫn -----
        clk = ValueTracker(0.0)
        sw_c = RIGHT * 3.6 + UP * 0.6
        ring = Circle(radius=1.0, color=MUTED, stroke_width=8).move_to(sw_c)
        stopwatch_btn = RoundedRectangle(
            width=0.44, height=0.24, corner_radius=0.06,
            stroke_color=MUTED, stroke_width=3,
            fill_color=MUTED, fill_opacity=0.25
        ).move_to(sw_c + UP * 1.18)

        def cc(frac):
            return interpolate_color(ManimColor(MUTED), ManimColor(RED), min(frac, 1))

        def hand_dir():
            a = clk.get_value() / 8 * TAU
            return np.array([np.sin(a), np.cos(a), 0])

        hand = always_redraw(lambda: Line(sw_c + 0.55 * hand_dir(), sw_c + 0.92 * hand_dir(),
                                          color=cc(clk.get_value() / 8), stroke_width=7))
        # Sửa DOWN * 0.42 thành move_to(sw_c) để vào giữa tâm
        num = always_redraw(lambda: T(f"{clk.get_value():.1f}s", size=30,
                                      color=cc(clk.get_value() / 8), weight=BOLD
                                      ).move_to(sw_c))

        phone = RoundedRectangle(width=4.4, height=4.4, corner_radius=0.3,
                                 stroke_color=MUTED, stroke_width=4).move_to(LEFT * 3.4 + DOWN * 0.2)
        user_b = RoundedRectangle(width=3.4, height=0.8, corner_radius=0.2, stroke_width=0,
                                  fill_color=BLUE, fill_opacity=0.85
                                  ).move_to(phone.get_top() + DOWN * 0.75 + RIGHT * 0.2)
        user_t = T("Explain LLM serving latency", size=17, color="#0b1220").move_to(user_b)
        ans = RoundedRectangle(width=3.4, height=1.7, corner_radius=0.2, stroke_color=GREEN,
                               fill_color=GREEN, fill_opacity=0.07
                               ).move_to(phone.get_center() + DOWN * 0.5 + LEFT * 0.15)
        dots = VGroup(*[Dot(radius=0.1, color=MUTED) for _ in range(3)]
                      ).arrange(RIGHT, buff=0.2).move_to(ans)

        # thanh kiên nhẫn (cạn dần)
        pw = 4.2
        pat_bg = RoundedRectangle(width=pw, height=0.34, corner_radius=0.1,
                                  stroke_color=MUTED, stroke_width=2, fill_opacity=0
                                  ).to_edge(DOWN, buff=0.7)
        pat_lbl = T("Kiên nhẫn của người dùng", size=16, color=MUTED).next_to(pat_bg, UP, buff=0.12)
        pat_fill = always_redraw(lambda: RoundedRectangle(
            width=max(pw * (1 - clk.get_value() / 8), 0.02), height=0.34, corner_radius=0.1,
            fill_color=cc(clk.get_value() / 8), fill_opacity=0.85, stroke_width=0
        ).align_to(pat_bg, LEFT).set_y(pat_bg.get_y()))

        # ----- CÂU 03: gửi prompt, màn hình im lặng, đồng hồ chạy -----
        s, d = self.say("voice/s8a_03.mp3")
        self.play(Create(phone), run_time=0.7)
        self.play(FadeIn(user_b, shift=UP * 0.2), Write(user_t), run_time=0.9)
        self.play(FadeIn(ans), FadeIn(dots), Create(ring), FadeIn(stopwatch_btn), run_time=0.6)
        self.add(hand, num, pat_fill)
        self.play(Create(pat_bg), FadeIn(pat_lbl), run_time=0.4)
        self.play(clk.animate.set_value(4.5), dots.animate.set_opacity(0.4),
                  run_time=max(d - 2.6, 1.2), rate_func=linear)
        self.fill(s, d)

        # ----- CÂU 04: Chỉnh sửa để hiện chữ đúng 6.0s và XUẤT HIỆN NHANH -----
        s, d = self.say("voice/s8a_04.mp3")

        total_time = max(d - 0.4, 1.2)
        t_to_6 = (1.5 / 3.5) * total_time
        t_to_6_5 = (0.5 / 3.5) * total_time
        t_to_8 = (1.5 / 3.5) * total_time

        self.play(
            clk.animate.set_value(6.0),
            run_time=t_to_6,
            rate_func=linear
        )

        warn = T("Request bị lỗi?", size=22, color=RED, weight=BOLD).move_to(ans.get_center())

        self.play(
            clk.animate.set_value(6.5),
            FadeOut(dots),
            FadeIn(warn, scale=0.8),
            run_time=t_to_6_5,
            rate_func=linear
        )

        self.play(
            clk.animate.set_value(8.0),
            run_time=t_to_8,
            rate_func=linear
        )

        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 2 — TTFT (vàng)
# ============================================================
class Slide8bTTFT(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Latency", C_LATENCY, vi=True)
        self.add(tag)

        base_y = UP * 0.2
        x0 = LEFT * 5.6
        track = Line(x0 + base_y, RIGHT * 5.6 + base_y, stroke_color=MUTED, stroke_width=3)
        send_lbl = T("Gửi prompt", size=18, color=MUTED).next_to(x0 + base_y, UP, buff=0.4).shift(RIGHT * 0.4)
        send_dot = Dot(x0 + base_y, color=WHITE)

        ttft_w = 5.2
        ttft_seg = Rectangle(width=ttft_w, height=0.5, fill_color=C_TTFT, fill_opacity=0.9,
                             stroke_width=0).move_to(x0 + base_y + RIGHT * ttft_w / 2)
        first_dot = Dot(x0 + base_y + RIGHT * ttft_w, color=C_TTFT)
        first_lbl = T("Token đầu tiên", size=18, color=C_TTFT).next_to(first_dot, UP, buff=0.4)
        ttft_name = T("TTFT — Time To First Token", size=24, color=C_TTFT, weight=BOLD).next_to(ttft_seg, UP, buff=1.0)

        # ----- CÂU 01: định nghĩa TTFT -----
        s, d = self.say("voice/s8b_01.mp3")
        self.play(Create(track), FadeIn(send_dot), FadeIn(send_lbl, shift=UP * 0.1), run_time=0.8)
        self.play(GrowFromEdge(ttft_seg, LEFT), run_time=1.0)
        self.play(FadeIn(first_dot), FadeIn(first_lbl, shift=UP * 0.1),
                  Write(ttft_name), run_time=0.9)
        self.fill(s, d)

        # ----- CÂU 02: TTFT cao -> im lặng dài -----
        s, d = self.say("voice/s8b_02.mp3")
        brace = Brace(ttft_seg, direction=DOWN, color=MUTED)
        ttft_val = T("8.0s", size=26, color=C_TTFT, weight=BOLD).next_to(brace, DOWN, buff=0.15)
        self.play(
            GrowFromCenter(brace),
            FadeIn(ttft_val, shift=UP * 0.15),
            Indicate(ttft_seg, color=WHITE),
            run_time=1.0
        )

        silence_box = RoundedRectangle(width=2.5, height=0.6, corner_radius=0.1,
                                       stroke_color=RED, fill_color=RED, fill_opacity=0.15)
        silence_txt = T("Khoảng im lặng", size=20, color=RED, weight=BOLD).move_to(silence_box)
        silence_group = VGroup(silence_box, silence_txt).next_to(ttft_val, DOWN, buff=0.25)
        self.play(
            FadeIn(silence_group, shift=UP * 0.1),
            ttft_seg.animate.set_fill(C_TTFT, opacity=0.55),
            run_time=0.6
        )
        self.play(
            Indicate(silence_group, color=RED, scale_factor=1.15),
            Flash(silence_group, color=RED, line_length=0.2, flash_radius=1.6, num_lines=12),
            run_time=0.7
        )
        self.fill(s, d)

        # ----- CÂU 03: nhạy cảm -> chưa có dấu hiệu hoạt động -----
        s, d = self.say("voice/s8b_03.mp3")
        self.play(Indicate(ttft_name, color=WHITE, scale_factor=1.06), run_time=0.8)
        self.fill(s, d)
        self.wait(0.2)


# ============================================================
# CẢNH 3 — TPOT (teal) + so sánh 2 nhịp
# ============================================================
class Slide8cTPOT(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Latency", C_LATENCY, vi=True)
        self.add(tag)

        base_y = UP * 1.6
        x0 = LEFT * 5.6
        track = Line(x0 + base_y, RIGHT * 5.6 + base_y, stroke_color=MUTED, stroke_width=3)
        ttft_w = 3.0
        ttft_seg = Rectangle(width=ttft_w, height=0.5, fill_color=C_TTFT, fill_opacity=0.85,
                             stroke_width=0).move_to(x0 + base_y + RIGHT * ttft_w / 2)
        ttft_lbl = T("TTFT", size=20, color=C_TTFT, weight=BOLD, vi=True).next_to(ttft_seg, UP, buff=0.3)
        self.add(track, ttft_seg, ttft_lbl)

        # ----- CÂU 01: token kế tiếp -----
        s, d = self.say("voice/s8c_01.mp3")
        pips = VGroup()
        px = ttft_w + 0.15
        for i in range(9):
            pip = Rectangle(width=0.16, height=0.5, fill_color=C_TPOT, fill_opacity=0.9,
                            stroke_width=0).move_to(x0 + base_y + RIGHT * (px + i * 0.32))
            pips.add(pip)
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in pips], lag_ratio=0.18), run_time=1.6)
        self.fill(s, d)

        # ----- CÂU 02: định nghĩa TPOT -----
        s, d = self.say("voice/s8c_02.mp3")
        tpot_lbl = T("TPOT — Time Per Output Token", size=20, color=C_TPOT, weight=BOLD).next_to(pips, UP, buff=0.3)
        tpot_lbl.align_to(ttft_lbl, DOWN)
        gap = DoubleArrow(pips[0].get_bottom() + DOWN * 0.1, pips[1].get_bottom() + DOWN * 0.1,
                          color=C_TPOT, stroke_width=3, buff=0, tip_length=0.12)
        gap_lbl = T("1 token", size=15, color=C_TPOT).next_to(gap, DOWN, buff=0.08)

        self.play(Write(tpot_lbl), run_time=0.8)
        self.play(GrowFromCenter(gap), FadeIn(gap_lbl), run_time=0.6)
        self.fill(s, d)

        # ----- CÂU 03: so sánh TPOT thấp (mượt) vs cao (khựng) -----
        s, d = self.say("voice/s8c_03.mp3")
        self.play(FadeOut(gap), FadeOut(gap_lbl), run_time=0.2)
        # làn mượt (xanh): pip sát nhau
        lane1_y = DOWN * 0.4
        smooth = VGroup(*[Rectangle(width=0.16, height=0.45, fill_color=GREEN, fill_opacity=0.9,
                                    stroke_width=0).move_to(LEFT * 1.8 + lane1_y + RIGHT * i * 0.3)
                          for i in range(12)])
        smooth_lbl = T("TPOT thấp → mượt", size=18, color=GREEN, weight=BOLD).next_to(smooth, LEFT, buff=0.3)
        # làn khựng (đỏ): pip thưa
        lane2_y = DOWN * 1.7
        choppy = VGroup(*[Rectangle(width=0.16, height=0.45, fill_color=RED, fill_opacity=0.9,
                                    stroke_width=0).move_to(LEFT * 1.8 + lane2_y + RIGHT * i * 0.72)
                          for i in range(6)])
        choppy_lbl = T("TPOT cao → khựng", size=18, color=RED, weight=BOLD).next_to(choppy, LEFT, buff=0.3)
        self.play(FadeIn(smooth_lbl), LaggedStart(*[FadeIn(p) for p in smooth], lag_ratio=0.05), run_time=1.1)
        self.play(FadeIn(choppy_lbl), LaggedStart(*[FadeIn(p) for p in choppy], lag_ratio=0.18), run_time=1.1)
        self.fill(s, d)

        # ----- CÂU 04: trải nghiệm không mượt (Phong cách 3Blue1Brown) -----
        s, d = self.say("voice/s8c_04.mp3")

        choppy_target = DOWN * 0.15 + RIGHT * 1.45
        self.play(
            FadeOut(smooth),
            FadeOut(smooth_lbl),
            choppy.animate.move_to(choppy_target),
            choppy_lbl.animate.next_to(choppy_target + LEFT * (choppy.width / 2), LEFT, buff=0.4),
            run_time=0.8
        )

        bob_img = ImageMobject("bob_transparent.png").scale(0.72)
        bob_img.to_corner(DL, buff=0.12).shift(RIGHT * 0.35)

        ux_line1 = T("Máy vẫn chạy,", size=22, color=WHITE, weight=BOLD)
        ux_line2 = T("nhưng trải nghiệm khựng!", size=22, color=RED, weight=BOLD)
        ux_text = VGroup(ux_line1, ux_line2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        ux_bubble = RoundedRectangle(
            width=ux_text.width + 0.55,
            height=ux_text.height + 0.45,
            corner_radius=0.16,
            stroke_color=RED,
            stroke_width=2,
            fill_color="#111827",
            fill_opacity=0.92
        )
        ux_bubble.move_to(ux_text)
        ux_group = VGroup(ux_bubble, ux_text).next_to(bob_img, RIGHT, buff=0.32).shift(UP * 0.25)
        tail = Triangle(fill_color="#111827", fill_opacity=0.92, stroke_color=RED, stroke_width=2)
        tail.scale(0.16).rotate(30 * DEGREES)
        tail.next_to(ux_bubble, LEFT, buff=-0.04).shift(DOWN * 0.18)

        self.play(FadeIn(bob_img, shift=UP * 0.8), run_time=0.6)
        self.play(
            FadeIn(VGroup(ux_bubble, tail), shift=UP * 0.18),
            FadeIn(ux_text, shift=UP * 0.18),
            Indicate(choppy, color=WHITE, scale_factor=1.15),
            run_time=0.8
        )
        self.play(
            bob_img.animate.scale(1.05).rotate(4 * DEGREES),
            rate_func=there_and_back,
            run_time=0.35
        )
        self.play(
            bob_img.animate.scale(1.05).rotate(-4 * DEGREES),
            rate_func=there_and_back,
            run_time=0.35
        )

        self.fill(s, d)
        self.wait(0.2)


# ============================================================
# CẢNH 4 — CÔNG THỨC (maroon): gom block
# ============================================================
class Slide8dFormula(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Latency", C_LATENCY, vi=True)
        self.add(tag)

        ttft_block = RoundedRectangle(width=1.8, height=0.7, corner_radius=0.1, stroke_width=0,
                                      fill_color=C_TTFT, fill_opacity=0.9).move_to(LEFT * 4 + UP * 2)
        ttft_tx = T("TTFT", size=22, color="#0b1220", weight=BOLD, vi=True).move_to(ttft_block)
        tpots = VGroup(*[RoundedRectangle(width=0.5, height=0.55, corner_radius=0.06, stroke_width=0,
                                          fill_color=C_TPOT, fill_opacity=0.9)
                         for _ in range(8)]).arrange(RIGHT, buff=0.12).move_to(RIGHT * 3 + UP * 2)

        # ----- CÂU 01: ghép 2 phần -----
        s, d = self.say("voice/s8d_01.mp3")
        self.play(FadeIn(VGroup(ttft_block, ttft_tx), shift=DOWN * 0.2),
                  LaggedStart(*[FadeIn(t, scale=0.6) for t in tpots], lag_ratio=0.1), run_time=1.3)
        self.fill(s, d)

        # ----- CÂU 02: công thức -----
        s, d = self.say("voice/s8d_02.mp3")
        lead = T("Latency", size=34, color=WHITE, weight=BOLD).move_to(LEFT * 4 + DOWN * 0.3)
        eq = T("=", size=34, color=WHITE, weight=BOLD).next_to(lead, RIGHT, buff=0.3)
        ttft_t = T("TTFT", size=34, color=C_TTFT, weight=BOLD, vi=True).next_to(eq, RIGHT, buff=0.3)
        plus = T("+", size=34, color=WHITE, weight=BOLD).next_to(ttft_t, RIGHT, buff=0.3)
        tpot_t = T("TPOT × N", size=34, color=C_TPOT, weight=BOLD).next_to(plus, RIGHT, buff=0.3)
        self.play(Write(lead), Write(eq), run_time=0.7)
        self.play(ReplacementTransform(VGroup(ttft_block, ttft_tx).copy(), ttft_t),
                  FadeIn(plus), run_time=0.8)
        self.play(ReplacementTransform(tpots.copy(), tpot_t), run_time=0.9)
        self.fill(s, d)

        # ----- CÂU 03: nhấn mạnh phụ thuộc số token -----
        s, d = self.say("voice/s8d_03.mp3")
        box = SurroundingRectangle(VGroup(lead, eq, ttft_t, plus, tpot_t), color=C_TOTAL, buff=0.3,
                                   corner_radius=0.15)
        approx = T("≈ TTFT + TPOT × số token đầu ra", size=22, color=C_TOTAL, weight=BOLD).next_to(box, DOWN, buff=0.4)
        self.play(Create(box), FadeIn(approx, shift=UP * 0.1), run_time=0.9)
        self.play(Indicate(tpot_t, color=WHITE, scale_factor=1.1), run_time=0.9)
        self.fill(s, d)
        self.wait(0.2)


# ============================================================
# CẢNH 5 — CẦU NỐI + TDS
# ============================================================
class Slide8eTDS(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Latency", C_LATENCY, vi=True)
        self.add(tag)
        formula = T("Latency ≈ TTFT + TPOT × N", size=18, color=MUTED, weight=BOLD).to_corner(UR, buff=0.5)
        self.add(formula)

        # ----- CÂU 01: streaming chưa đủ -----
        s, d = self.say("voice/s8e_01.mp3")
        line_words = ["LLM", "serving", "is", "challenging", "because", "…"]
        words = VGroup(*[T(w, size=24, color=WHITE) for w in line_words]
                       ).arrange(RIGHT, buff=0.25).move_to(UP * 1.5)
        for w in words:
            w.set_opacity(0)
        self.play(FadeIn(words[0]), run_time=0.3)
        words[0].set_opacity(1)
        self.fill(s, d)

        # ----- CÂU 02: người đọc đuổi kịp -> chờ -----
        s, d = self.say("voice/s8e_02.mp3")
        reader = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=0.9).scale(0.18).rotate(-PI / 2)
        reader.next_to(words[0], DOWN, buff=0.3)
        self.play(FadeIn(reader), run_time=0.3)
        for i in range(1, len(words)):
            words[i].set_opacity(1)
            self.play(FadeIn(words[i]), reader.animate.next_to(words[i], DOWN, buff=0.3),
                      run_time=0.32)
        waitg = T("chờ…", size=20, color=RED, weight=BOLD).next_to(reader, DOWN, buff=0.2)
        self.play(FadeIn(waitg), Flash(reader, color=RED, flash_radius=0.5), run_time=0.6)
        self.fill(s, d)

        # ----- CÂU 03: câu hỏi đủ nhanh? -----
        s, d = self.say("voice/s8e_03.mp3")
        q = T("Token có ra đủ nhanh cho người đọc?", size=24, color=WHITE, weight=BOLD).move_to(UP * 0.3)
        self.play(FadeOut(waitg), FadeOut(reader), Write(q), run_time=0.9)
        self.fill(s, d)

        # ----- CÂU 04: TDS = băng chuyền -----
        s, d = self.say("voice/s8e_04.mp3")
        self.play(FadeOut(words), q.animate.scale(0.7).to_edge(UP, buff=1.2).set_color(MUTED), run_time=0.6)
        belt = Line(LEFT * 5 + DOWN * 0.8, RIGHT * 5 + DOWN * 0.8, stroke_color=MUTED, stroke_width=3)
        toks = VGroup(*[RoundedRectangle(width=0.55, height=0.5, corner_radius=0.08, stroke_width=0,
                                         fill_color=C_TDS, fill_opacity=0.85)
                        for _ in range(7)]).arrange(RIGHT, buff=0.35)
        toks.move_to(belt.get_center() + UP * 0.0)
        tds_name = T("Tốc độ giao token — TDS", size=22, color=C_TDS, weight=BOLD).next_to(belt, UP, buff=0.7)
        tds_sub = T("TDS ≈ số token mỗi giây", size=18, color=C_TDS).next_to(belt, DOWN, buff=0.4)
        self.play(Create(belt), Write(tds_name), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in toks], lag_ratio=0.1),
                  FadeIn(tds_sub), run_time=1.2)
        self.fill(s, d)

        # ----- CÂU 05+06: chậm -> phải chờ -----
        s, d = self.say("voice/s8e_05.mp3")
        self.play(toks.animate.shift(RIGHT * 0.0), Indicate(tds_sub, color=WHITE), run_time=0.6)
        slow = T("token ra chậm → người dùng chờ", size=20, color=RED, weight=BOLD).next_to(tds_sub, DOWN, buff=0.4)
        self.play(FadeIn(slow), run_time=0.5)
        self.fill(s, d)
        s, d = self.say("voice/s8e_06.mp3")
        self.play(Indicate(slow, color=WHITE, scale_factor=1.05), run_time=0.9)
        self.fill(s, d)
        self.wait(0.2)


# ============================================================
# CẢNH 6 — CENTERPIECE: TRỤC TỐC ĐỘ CON NGƯỜI vs LLM
# ============================================================
class Slide8fHumanAxis(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Latency", C_LATENCY, vi=True)
        self.add(tag)

        # Trục WPM dùng chung
        axis = NumberLine(x_range=[0, 250, 50], length=11, include_numbers=True,
                          color=MUTED, font_size=20).to_edge(DOWN, buff=1.3)
        axis_lbl = T("Tốc độ (từ mỗi phút — WPM)", size=18, color=MUTED).next_to(axis, DOWN, buff=0.18)

        def x_at(v):
            return axis.number_to_point(v)[0]

        x_left = axis.number_to_point(0)[0]

        def bar(value, y, color):
            w = x_at(value) - x_left
            r = Rectangle(width=w, height=0.3, fill_color=color, fill_opacity=0.85, stroke_width=0)
            r.move_to([x_left + w / 2, y, 0])
            return r

        # ----- CÂU 01: đặt lên cùng một thước -----
        s, d = self.say("voice/s8f_01.mp3")
        self.play(Create(axis), FadeIn(axis_lbl), run_time=1.0)
        self.fill(s, d)

        # ----- CÂU 02: dải đọc (cam) -----
        s, d = self.say("voice/s8f_02.mp3")
        read_data = [("18–24", 236), ("25–44", 200), ("45–54", 192), ("55–64", 185), ("65+", 175)]
        read_bars = VGroup()
        ry = 2.0
        for name, v in read_data:
            b = bar(v, ry, C_READ)
            lb = T(name, size=13, color=C_READ).next_to(b, LEFT, buff=0.15)
            vt = T(str(v), size=13, color=WHITE).next_to(b, RIGHT, buff=0.1)
            read_bars.add(VGroup(b, lb, vt))
            ry -= 0.38
        read_title = T("Tốc độ Đọc", size=20, color=C_READ, weight=BOLD)
        read_title.next_to(read_bars[0][0], UP, buff=0.25).align_to(read_bars[0][0], LEFT)
        self.play(FadeIn(read_title, shift=UP * 0.2), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(g[0], LEFT) for g in read_bars], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(g[1]) for g in read_bars], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(g[2]) for g in read_bars], lag_ratio=0.15), run_time=1.8)
        self.fill(s, d)

        # ----- CÂU 03: dải nói (tím) -----
        s, d = self.say("voice/s8f_03.mp3")
        self.play(read_bars.animate.set_opacity(0.5), run_time=0.4)
        speak_data = [("English", 150), ("Chinese", 158), ("Korean", 150), ("French", 195), ("Spanish", 218)]
        speak_bars = VGroup()
        sy = -0.6
        for name, v in speak_data:
            b = bar(v, sy, C_SPEAK)
            lb = T(name, size=13, color=C_SPEAK).next_to(b, LEFT, buff=0.15)
            vt = T(str(v), size=13, color=WHITE).next_to(b, RIGHT, buff=0.1)
            speak_bars.add(VGroup(b, lb, vt))
            sy -= 0.38
        speak_title = T("Tốc độ Nói", size=20, color=C_SPEAK, weight=BOLD)
        speak_title.next_to(speak_bars[0][0], UP, buff=0.25).align_to(speak_bars[0][0], LEFT)
        self.play(FadeIn(speak_title, shift=UP * 0.2), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(g[0], LEFT) for g in speak_bars], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(g[1]) for g in speak_bars], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(g[2]) for g in speak_bars], lag_ratio=0.15), run_time=1.8)
        self.fill(s, d)

        # ----- CÂU 04+05: token≠từ, dải tự nhiên -----
        s, d = self.say("voice/s8f_04.mp3")
        self.play(speak_bars.animate.set_opacity(0.75), read_bars.animate.set_opacity(0.75), run_time=0.5)
        self.fill(s, d)
        s, d = self.say("voice/s8f_05.mp3")
        bx = (x_at(150) + x_at(236)) / 2

        top_y = read_bars[0][0].get_top()[1]
        bottom_y = speak_bars[-1][0].get_bottom()[1]
        band_top = top_y + 0.15
        band_bottom = bottom_y - 0.4
        band_h = band_top - band_bottom
        band_y = (band_top + band_bottom) / 2

        band = Rectangle(width=x_at(236) - x_at(150), height=band_h, fill_color=WHITE, fill_opacity=0.07,
                         stroke_color=WHITE, stroke_width=1).move_to([bx, band_y, 0])
        band_lbl = T("dải con người", size=14, color=WHITE).move_to([bx, band_bottom + 0.15, 0])
        self.play(FadeIn(band), FadeIn(band_lbl), run_time=0.8)
        self.fill(s, d)

        # ----- CÂU 06: kim LLM vào -----
        s, d = self.say("voice/s8f_06.mp3")
        llm = ValueTracker(95)
        axis_line_y = axis.number_to_point(0)[1]
        needle = always_redraw(lambda: DashedLine(
            [x_at(llm.get_value()), axis_line_y, 0], [x_at(llm.get_value()), 2.4, 0],
            color=(GREEN if llm.get_value() >= 236 else RED), stroke_width=4))

        def get_lbl_pos():
            val = llm.get_value()
            safe_x = min(x_at(val), x_at(230))
            return [safe_x, 2.65, 0]

        needle_lbl = always_redraw(lambda: T(f"LLM: {int(llm.get_value())} WPM", size=16,
                                             color=(GREEN if llm.get_value() >= 236 else RED), weight=BOLD
                                             ).move_to(get_lbl_pos()))
        self.add(needle, needle_lbl)
        self.play(FadeIn(needle, shift=UP * 0.2), run_time=0.5)
        self.fill(s, d)

        # ----- CÂU 07: dưới dải -> phải chờ (đỏ) -----
        s, d = self.say("voice/s8f_07.mp3")
        verdict = T("Dưới dải người → phải chờ", size=22, color=RED, weight=BOLD).to_edge(UP, buff=0.25)
        self.play(llm.animate.set_value(95), FadeIn(verdict), run_time=0.6)
        self.play(Indicate(verdict, color=WHITE), run_time=0.8)
        self.fill(s, d)

        # ----- CÂU 08: TTS ngắt quãng -----
        s, d = self.say("voice/s8f_08.mp3")
        tts = T("This… is… a… response…", size=19, color=RED, weight=BOLD).next_to(verdict, DOWN, buff=0.15)
        self.play(FadeIn(tts), run_time=0.6)
        self.fill(s, d)

        # ----- CÂU 09: vượt dải -> mượt (xanh) -----
        s, d = self.say("voice/s8f_09.mp3")
        new_verdict = T("Vượt dải người → mượt", size=22, color=GREEN, weight=BOLD).to_edge(UP, buff=0.25)
        new_tts = T("This is a response, generated smoothly.", size=19, color=GREEN, weight=BOLD).next_to(new_verdict, DOWN, buff=0.15)
        self.play(llm.animate.set_value(245), run_time=1.0)
        self.play(Transform(verdict, new_verdict), Transform(tts, new_tts), run_time=0.6)
        self.fill(s, d)

        # ----- CÂU 10: ý nghĩa TDS -----
        s, d = self.say("voice/s8f_10.mp3")
        self.play(Flash(needle_lbl, color=GREEN, flash_radius=0.6), run_time=0.8)
        self.fill(s, d)
        self.wait(0.2)


# ============================================================
# CẢNH 7 — TỔNG HỢP + CHUYỂN TIẾP
# ============================================================
class Slide8gOutro(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Latency", C_LATENCY, vi=True)
        self.add(tag)

        def eye_icon(color=C_TDS, scale=1.0):
            eye = VGroup(
                Ellipse(
                    width=0.92,
                    height=0.50,
                    stroke_color=color,
                    stroke_width=4
                ),
                Dot(radius=0.11, color=color),
            )
            return eye.scale(scale)

        def clock_icon(color=C_TTFT, scale=1.0):
            ring = Circle(radius=0.34, color=color, stroke_width=4)

            hand_1 = Line(
                ORIGIN,
                UP * 0.20,
                color=color,
                stroke_width=4
            )

            hand_2 = Line(
                ORIGIN,
                RIGHT * 0.15,
                color=color,
                stroke_width=4
            )

            knob = RoundedRectangle(
                width=0.18,
                height=0.09,
                corner_radius=0.02,
                stroke_width=0,
                fill_color=color,
                fill_opacity=1
            ).next_to(ring, UP, buff=0.02)

            return VGroup(
                ring,
                hand_1,
                hand_2,
                knob
            ).scale(scale)

        def metric_caption(main, sub, color, size=20):
            main_text = T(
                main,
                size=size,
                color=color,
                weight=BOLD,
                vi=True
            )

            sub_text = T(
                sub,
                size=14,
                color=MUTED,
                weight=BOLD,
                vi=True
            )

            return VGroup(
                main_text,
                sub_text
            ).arrange(DOWN, buff=0.08)

        # ====================================================
        # CÂU 01–04: TIMELINE
        # ====================================================

        timeline_y = 0.42

        send_x = -5.15
        first_token_x = -2.55
        last_token_x = 4.35

        token_count = 8

        token_positions = [
            first_token_x
            + i * (last_token_x - first_token_x) / (token_count - 1)
            for i in range(token_count)
        ]

        axis = Line(
            [send_x, timeline_y, 0],
            [last_token_x, timeline_y, 0],
            color=MUTED,
            stroke_width=3
        )

        send_dot = Dot(
            [send_x, timeline_y, 0],
            radius=0.09,
            color=WHITE
        )

        send_label = T(
            "Gửi prompt",
            size=16,
            color=MUTED,
            weight=BOLD,
            vi=True
        )

        send_label.next_to(
            send_dot,
            LEFT,
            buff=0.18
        ).shift(DOWN * 0.12)

        tokens = VGroup(*[
            Dot(
                [x, timeline_y, 0],
                radius=0.10,
                color=C_TPOT
            )
            for x in token_positions
        ])

        tokens[0].set_color(C_TTFT)

        title = T(
            "Một dòng thời gian phản hồi",
            size=25,
            color=WHITE,
            weight=BOLD,
            vi=True
        ).move_to([0, 2.55, 0])

        # ----- CÂU 01 -----

        start, duration = self.say("voice/s8g_01.mp3")

        self.play(
            FadeIn(title, shift=DOWN * 0.12),
            Create(axis),
            FadeIn(send_dot, scale=0.6),
            FadeIn(send_label, shift=RIGHT * 0.10),
            run_time=1.0
        )

        self.fill(start, duration)

        # ----- CÂU 02: TTFT và TPOT -----

        start, duration = self.say("voice/s8g_02.mp3")

        self.play(
            FadeIn(tokens[0], scale=0.5),
            run_time=0.35
        )

        ttft_reference = Line(
            [send_x, timeline_y, 0],
            [first_token_x, timeline_y, 0]
        )

        ttft_brace = Brace(
            ttft_reference,
            DOWN,
            color=C_TTFT,
            buff=0.08
        )

        ttft_label = T(
            "TTFT",
            size=20,
            color=C_TTFT,
            weight=BOLD,
            vi=True
        ).next_to(
            ttft_brace,
            DOWN,
            buff=0.08
        )

        self.play(
            GrowFromCenter(ttft_brace),
            FadeIn(ttft_label, shift=UP * 0.08),
            run_time=0.65
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(token, scale=0.5)
                    for token in tokens[1:]
                ],
                lag_ratio=0.11
            ),
            run_time=1.1
        )

        tpot_y = timeline_y - 0.52

        tpot_gap = DoubleArrow(
            [token_positions[2], tpot_y, 0],
            [token_positions[3], tpot_y, 0],
            color=C_TPOT,
            stroke_width=3,
            buff=0.08,
            tip_length=0.11
        )

        tpot_label = T(
            "TPOT",
            size=19,
            color=C_TPOT,
            weight=BOLD,
            vi=True
        ).next_to(
            tpot_gap,
            DOWN,
            buff=0.08
        )

        self.play(
            GrowFromCenter(tpot_gap),
            FadeIn(tpot_label, shift=UP * 0.08),
            run_time=0.55
        )

        self.fill(start, duration)

        # ----- CÂU 03: TOTAL LATENCY -----
        # Biến đổi tiêu đề thành nhãn Total latency.
        # Vì vậy không còn hai dòng chữ nằm cùng một khu vực.

        start, duration = self.say("voice/s8g_03.mp3")

        total_reference = Line(
            [send_x, timeline_y + 0.42, 0],
            [last_token_x, timeline_y + 0.42, 0]
        )

        total_brace = Brace(
            total_reference,
            UP,
            color=C_TOTAL,
            buff=0.04
        )

        total_label_target = T(
            "Total latency",
            size=22,
            color=C_TOTAL,
            weight=BOLD
        ).next_to(
            total_brace,
            UP,
            buff=0.08
        )

        self.play(
            GrowFromCenter(total_brace),
            Transform(title, total_label_target),
            run_time=0.9
        )

        self.fill(start, duration)

        # ----- CÂU 04: TDS -----
        # Không dùng thanh TDS dài.
        # Các token được giao trực tiếp đến mắt người đọc.

        start, duration = self.say("voice/s8g_04.mp3")

        reader_eye = eye_icon(
            C_TDS,
            scale=0.95
        ).move_to([
            5.35,
            timeline_y,
            0
        ])

        tds_label = T(
            "TDS",
            size=20,
            color=C_TDS,
            weight=BOLD,
            vi=True
        ).next_to(
            reader_eye,
            DOWN,
            buff=0.28
        )

        tds_question = T(
            "đủ nhanh để đọc / nghe?",
            size=15,
            color=C_TDS,
            weight=BOLD,
            vi=True
        ).next_to(
            tds_label,
            DOWN,
            buff=0.05
        )

        delivery_paths = VGroup(*[
            ArcBetweenPoints(
                tokens[i].get_center(),
                reader_eye.get_center(),
                angle=-0.28 - 0.05 * (i - (token_count - 3)),
                color=C_TDS,
                stroke_width=2
            )
            for i in range(token_count - 3, token_count)
        ])

        self.play(
            FadeIn(reader_eye, scale=0.75),
            run_time=0.40
        )

        self.play(
            LaggedStart(
                *[
                    ShowPassingFlash(
                        path.copy().set_stroke(width=7),
                        time_width=0.28
                    )
                    for path in delivery_paths
                ],
                lag_ratio=0.18
            ),
            run_time=1.05
        )

        self.play(
            Flash(
                reader_eye,
                color=C_TDS,
                flash_radius=0.72,
                num_lines=10
            ),
            FadeIn(tds_label, shift=UP * 0.08),
            FadeIn(tds_question, shift=UP * 0.08),
            run_time=0.65
        )

        self.fill(start, duration)

        timeline_group = VGroup(
            title,
            axis,
            send_dot,
            send_label,
            tokens,
            ttft_brace,
            ttft_label,
            tpot_gap,
            tpot_label,
            total_brace,
            reader_eye,
            tds_label,
            tds_question
        )

        # ====================================================
        # CÂU 05: TPOT ↔ TDS
        # ====================================================

        start, duration = self.say("voice/s8g_05.mp3")

        self.play(
            FadeOut(timeline_group),
            run_time=0.45
        )

        relation_title = T(
            "Cùng một đầu ra — khác nhịp giao token",
            size=24,
            color=WHITE,
            weight=BOLD,
            vi=True
        ).move_to([0, 2.45, 0])

        top_y = 0.78
        bottom_y = -0.92

        divider = Line(
            [-5.7, -0.07, 0],
            [5.7, -0.07, 0],
            color=MUTED,
            stroke_width=1.5
        ).set_opacity(0.35)

        low_tpot = T(
            "TPOT thấp",
            size=20,
            color=C_TPOT,
            weight=BOLD,
            vi=True
        ).move_to([-5.15, top_y, 0])

        high_tpot = T(
            "TPOT cao",
            size=20,
            color=C_TPOT,
            weight=BOLD,
            vi=True
        ).move_to([-5.15, bottom_y, 0])

        dense_tokens = VGroup(*[
            Dot(radius=0.09, color=C_TDS)
            for _ in range(13)
        ]).arrange(
            RIGHT,
            buff=0.16
        ).move_to([
            -2.25,
            top_y,
            0
        ])

        sparse_tokens = VGroup(*[
            Dot(radius=0.09, color=RED)
            for _ in range(6)
        ]).arrange(
            RIGHT,
            buff=0.55
        ).move_to([
            -2.25,
            bottom_y,
            0
        ])

        top_eye = eye_icon(
            C_TDS,
            scale=0.72
        )

        top_tds_text = T(
            "TDS cao",
            size=20,
            color=C_TDS,
            weight=BOLD,
            vi=True
        )

        top_tds = VGroup(
            top_eye,
            top_tds_text
        ).arrange(
            RIGHT,
            buff=0.22
        ).move_to([
            1.75,
            top_y,
            0
        ])

        bottom_eye = eye_icon(
            RED,
            scale=0.72
        )

        bottom_tds_text = T(
            "TDS thấp",
            size=20,
            color=RED,
            weight=BOLD,
            vi=True
        )

        bottom_tds = VGroup(
            bottom_eye,
            bottom_tds_text
        ).arrange(
            RIGHT,
            buff=0.22
        ).move_to([
            1.75,
            bottom_y,
            0
        ])

        top_arrow = Arrow(
            dense_tokens.get_right() + RIGHT * 0.28,
            top_eye.get_left() + LEFT * 0.18,
            color=MUTED,
            stroke_width=3,
            buff=0
        )

        bottom_arrow = Arrow(
            sparse_tokens.get_right() + RIGHT * 0.28,
            bottom_eye.get_left() + LEFT * 0.18,
            color=MUTED,
            stroke_width=3,
            buff=0
        )

        top_result_arrow = Arrow(
            top_tds.get_right() + RIGHT * 0.18,
            [3.62, top_y, 0],
            color=C_TDS,
            stroke_width=3,
            buff=0
        )

        bottom_result_arrow = Arrow(
            bottom_tds.get_right() + RIGHT * 0.18,
            [3.62, bottom_y, 0],
            color=RED,
            stroke_width=3,
            buff=0
        )

        smooth = T(
            "MƯỢT",
            size=25,
            color=C_TDS,
            weight=BOLD,
            vi=True
        ).move_to([
            4.55,
            top_y,
            0
        ])

        choppy = T(
            "KHỰNG",
            size=25,
            color=RED,
            weight=BOLD,
            vi=True
        ).move_to([
            4.55,
            bottom_y,
            0
        ])

        self.play(
            FadeIn(relation_title, shift=DOWN * 0.10),
            Create(divider),
            run_time=0.45
        )

        self.play(
            FadeIn(low_tpot),
            LaggedStart(
                *[
                    FadeIn(token, scale=0.5)
                    for token in dense_tokens
                ],
                lag_ratio=0.045
            ),
            GrowArrow(top_arrow),
            FadeIn(top_tds, shift=RIGHT * 0.12),
            GrowArrow(top_result_arrow),
            FadeIn(smooth, shift=RIGHT * 0.12),
            run_time=1.05
        )

        self.play(
            FadeIn(high_tpot),
            LaggedStart(
                *[
                    FadeIn(token, scale=0.5)
                    for token in sparse_tokens
                ],
                lag_ratio=0.13
            ),
            GrowArrow(bottom_arrow),
            FadeIn(bottom_tds, shift=RIGHT * 0.12),
            GrowArrow(bottom_result_arrow),
            FadeIn(choppy, shift=RIGHT * 0.12),
            run_time=1.05
        )

        self.fill(start, duration)

        relation_group = VGroup(
            relation_title,
            divider,
            low_tpot,
            high_tpot,
            dense_tokens,
            sparse_tokens,
            top_arrow,
            bottom_arrow,
            top_tds,
            bottom_tds,
            top_result_arrow,
            bottom_result_arrow,
            smooth,
            choppy
        )

        # ====================================================
        # CÂU 06: CHỐT TRẢI NGHIỆM
        # ====================================================

        start, duration = self.say("voice/s8g_06.mp3")

        self.play(
            FadeOut(relation_group),
            run_time=0.45
        )

        synthesis_title = T(
            "Tối ưu latency",
            size=27,
            color=WHITE,
            weight=BOLD,
            vi=True
        ).move_to([0, 2.48, 0])

        fast_clock = clock_icon(
            C_TTFT,
            scale=1.05
        )

        fast_caption = metric_caption(
            "Xuất hiện sớm",
            "TTFT thấp",
            C_TTFT,
            size=20
        )

        fast_group = VGroup(
            fast_clock,
            fast_caption
        ).arrange(
            DOWN,
            buff=0.28
        ).move_to([
            -4.15,
            0.45,
            0
        ])

        fast_underline = Line(
            fast_group.get_left() + DOWN * 0.86,
            fast_group.get_right() + DOWN * 0.86,
            color=C_TTFT,
            stroke_width=4
        )

        rhythm_tokens = VGroup(*[
            Dot(radius=0.08, color=C_TDS)
            for _ in range(7)
        ]).arrange(
            RIGHT,
            buff=0.12
        )

        rhythm_eye = eye_icon(
            C_TDS,
            scale=0.78
        )

        rhythm_visual = VGroup(
            rhythm_tokens,
            rhythm_eye
        ).arrange(
            RIGHT,
            buff=0.28
        )

        rhythm_caption = metric_caption(
            "Chảy đúng nhịp",
            "TPOT thấp  •  TDS cao",
            C_TDS,
            size=20
        )

        rhythm_group = VGroup(
            rhythm_visual,
            rhythm_caption
        ).arrange(
            DOWN,
            buff=0.28
        ).move_to([
            0.20,
            0.45,
            0
        ])

        rhythm_underline = Line(
            rhythm_group.get_left() + DOWN * 0.86,
            rhythm_group.get_right() + DOWN * 0.86,
            color=C_TDS,
            stroke_width=4
        )

        smooth_wave = VMobject(
            color=GREEN,
            stroke_width=5
        )

        smooth_wave.set_points_smoothly([
            [-0.72, 0.00, 0],
            [-0.34, 0.16, 0],
            [0.00, -0.10, 0],
            [0.36, 0.12, 0],
            [0.72, 0.00, 0]
        ])

        smooth_text = T(
            "TRẢI NGHIỆM MƯỢT",
            size=22,
            color=GREEN,
            weight=BOLD,
            vi=True
        )

        smooth_group = VGroup(
            smooth_wave,
            smooth_text
        ).arrange(
            DOWN,
            buff=0.30
        ).move_to([
            4.28,
            0.45,
            0
        ])

        plus_sign = T(
            "+",
            size=40,
            color=WHITE,
            weight=BOLD
        ).move_to([
            -2.05,
            0.55,
            0
        ])

        equals_sign = T(
            "=",
            size=40,
            color=WHITE,
            weight=BOLD
        ).move_to([
            2.35,
            0.55,
            0
        ])

        punchline = T(
            "Phản hồi xuất hiện đúng lúc — và không để người dùng phải chờ",
            size=21,
            color=WHITE,
            weight=BOLD,
            vi=True
        ).move_to([
            0,
            -2.35,
            0
        ])

        self.play(
            FadeIn(synthesis_title, shift=DOWN * 0.10),
            run_time=0.35
        )

        self.play(
            FadeIn(fast_group, shift=RIGHT * 0.12),
            Create(fast_underline),
            run_time=0.65
        )

        self.play(
            FadeIn(plus_sign),
            FadeIn(rhythm_group, shift=RIGHT * 0.12),
            Create(rhythm_underline),
            run_time=0.70
        )

        self.play(
            FadeIn(equals_sign),
            Create(smooth_wave),
            FadeIn(smooth_text, shift=UP * 0.10),
            run_time=0.70
        )

        self.play(
            Write(punchline),
            run_time=0.85
        )

        self.fill(start, duration)

        synthesis_group = VGroup(
            synthesis_title,
            fast_group,
            fast_underline,
            plus_sign,
            rhythm_group,
            rhythm_underline,
            equals_sign,
            smooth_group,
            punchline
        )

        # ====================================================
        # CÂU 07: CHUYỂN SANG GPU MEMORY
        # ====================================================

        start, duration = self.say("voice/s8g_07.mp3")

        self.play(
            FadeOut(synthesis_group, shift=LEFT * 0.35),
            run_time=0.55
        )

        gpu_body = RoundedRectangle(
            width=2.85,
            height=2.15,
            corner_radius=0.24,
            stroke_color=C_MEMORY,
            stroke_width=4,
            fill_color=C_MEMORY,
            fill_opacity=0.08
        ).move_to([
            3.75,
            -0.10,
            0
        ])

        gpu_label = T(
            "GPU MEMORY",
            size=20,
            color=C_MEMORY,
            weight=BOLD
        ).next_to(
            gpu_body,
            UP,
            buff=0.18
        )

        pins = VGroup()

        for y_shift in [-0.68, -0.22, 0.22, 0.68]:
            left_pin = Rectangle(
                width=0.30,
                height=0.10,
                stroke_width=0,
                fill_color=C_MEMORY,
                fill_opacity=0.95
            ).next_to(
                gpu_body,
                LEFT,
                buff=0
            ).shift(UP * y_shift)

            right_pin = Rectangle(
                width=0.30,
                height=0.10,
                stroke_width=0,
                fill_color=C_MEMORY,
                fill_opacity=0.95
            ).next_to(
                gpu_body,
                RIGHT,
                buff=0
            ).shift(UP * y_shift)

            pins.add(left_pin, right_pin)

        memory_cells = VGroup(*[
            RoundedRectangle(
                width=0.48,
                height=0.38,
                corner_radius=0.06,
                stroke_color=C_MEMORY,
                stroke_width=1.4,
                fill_color=C_MEMORY,
                fill_opacity=0.10
            )
            for _ in range(12)
        ]).arrange_in_grid(
            rows=3,
            cols=4,
            buff=(0.14, 0.14)
        ).move_to(gpu_body)

        incoming_tokens = VGroup(*[
            Dot(
                [-4.75 + i * 0.46, -0.10, 0],
                radius=0.09,
                color=C_TDS
            )
            for i in range(9)
        ])

        flow_arrow = Arrow(
            incoming_tokens.get_right() + RIGHT * 0.72,
            [gpu_body.get_left()[0] - 0.48, -0.10, 0],
            color=C_MEMORY,
            stroke_width=4,
            buff=0
        )

        flow_caption = T(
            "dữ liệu phục vụ",
            size=16,
            color=MUTED,
            weight=BOLD,
            vi=True
        ).next_to(
            incoming_tokens,
            UP,
            buff=0.22
        )

        next_title = T(
            "THÁCH THỨC #2 — BỘ NHỚ GPU",
            size=27,
            color=C_MEMORY,
            weight=BOLD,
            vi=True
        ).move_to([
            0,
            -2.65,
            0
        ])

        self.play(
            LaggedStart(
                *[
                    FadeIn(token, scale=0.5)
                    for token in incoming_tokens
                ],
                lag_ratio=0.07
            ),
            FadeIn(flow_caption, shift=UP * 0.08),
            run_time=0.65
        )

        self.play(
            GrowArrow(flow_arrow),
            Create(gpu_body),
            FadeIn(pins),
            FadeIn(gpu_label, shift=UP * 0.08),
            run_time=0.75
        )

        self.play(
            LaggedStart(
                *[
                    cell.animate.set_fill(
                        C_MEMORY,
                        opacity=0.80
                    )
                    for cell in memory_cells
                ],
                lag_ratio=0.075
            ),
            run_time=1.0
        )

        self.play(
            FadeIn(next_title, shift=UP * 0.12),
            run_time=0.45
        )

        next_tag = self.make_node_label(
            "Bộ nhớ",
            C_MEMORY,
            vi=True
        )

        self.play(
            Transform(tag, next_tag),
            Indicate(
                gpu_body,
                color=WHITE,
                scale_factor=1.04
            ),
            run_time=0.65
        )

        self.fill(start, duration)
        self.wait(0.3)
