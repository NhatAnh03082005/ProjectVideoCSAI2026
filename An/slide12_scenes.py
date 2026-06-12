from manim import *
from mutagen.mp3 import MP3
import os

# ============================================================
# SLIDE 12 — ACCURACY–EFFICIENCY TRADE-OFF + KẾT PHẦN 2 (7 cảnh)
# Style: 3Blue1Brown (biểu đồ thực, Dial speedometer, radial cân bằng). KHÔNG LaTeX.
# Render (đứng TRONG slide12_themed/):
#   PYTHONUTF8=1 manim -qh --disable_caching slide12_scenes.py Slide12aBridge
#   ... Slide12bChart Slide12cRead Slide12dDials Slide12eUseCases Slide12fRecap Slide12gToPart3
# ============================================================

FONT_VI = "Arial"
BG = "#0f172a"
WHITE = "#e5e7eb"; MUTED = "#94a3b8"; BLUE = "#38bdf8"; GREEN = "#22c55e"
YELLOW = "#facc15"; RED = "#ef4444"; PURPLE = "#a78bfa"; ORANGE = "#fb923c"
TEAL = "#2dd4bf"; MAROON = "#e11d48"; SLATE = "#64748b"; BROWN = "#b07a55"
config.background_color = BG
TEXT_SS = 4
ASSETS = "assets"


def T(text, size=24, color=WHITE, weight=NORMAL, line_spacing=-1, vi=False):
    kw = dict(font_size=size * TEXT_SS, color=color, weight=weight, line_spacing=line_spacing)
    if vi or any(ord(c) > 127 or c.isdigit() for c in text):
        kw["font"] = FONT_VI
    return Text(text, **kw).scale(1 / TEXT_SS)


def svg_icon(name, color, height=1.0, sw=3.0):
    m = SVGMobject(os.path.join(ASSETS, name + ".svg"))
    m.set_height(height); m.set_stroke(color=color, width=sw); m.set_fill(opacity=0)
    return m


def dial_arc(center, radius=0.9, arc_color=MUTED):
    arc = Arc(radius=radius, start_angle=210 * DEGREES, angle=-240 * DEGREES, arc_center=center)
    arc.set_stroke(arc_color, 3)
    ticks = VGroup(*[Line(center + 0.82 * (arc.point_from_proportion(a) - center),
                          arc.point_from_proportion(a)) for a in np.linspace(0, 1, 11)])
    ticks.set_stroke(arc_color, 2.5)
    return arc, ticks


# models: (name, speed, quality, price_radius, color, show_label)
MODELS = [
    ("Claude 3 Opus", 25, 93, 0.34, BROWN, True),
    ("Gemini 1.5 Pro", 58, 95, 0.17, GREEN, True),
    ("GPT-4o", 83, 100, 0.18, WHITE, True),
    ("Claude 3.5 Sonnet", 80, 98, 0.16, ORANGE, False),
    ("Llama 3 (70B)", 62, 83, 0.12, BLUE, True),
    ("Mixtral 8x22B", 58, 76, 0.15, PURPLE, False),
    ("GPT-4o mini", 130, 85, 0.11, MUTED, True),
    ("Gemini 1.5 Flash", 166, 84, 0.11, GREEN, True),
    ("Claude 3 Haiku", 127, 74, 0.11, BROWN, False),
    ("Llama 3 (8B)", 135, 64, 0.10, BLUE, False),
    ("GPT-3.5 Turbo", 78, 59, 0.11, SLATE, False),
]
FRONTIER = [(25, 93), (58, 95), (83, 100), (130, 85), (166, 84)]


def build_chart(faded=False):
    op = 0.25 if faded else 1.0
    ax = Axes(x_range=[0, 185, 20], y_range=[50, 112, 10], x_length=10.4, y_length=5.4,
              axis_config={"include_tip": False, "stroke_color": MUTED}).shift(DOWN * 0.4)
    xl = T("Output Speed (token/giây)", size=20, color=MUTED, vi=True).next_to(ax, DOWN, buff=0.25)
    yl = T("Quality", size=20, color=MUTED, vi=True).rotate(PI / 2).next_to(ax, LEFT, buff=0.1)
    ll = ax.c2p(95, 78); ur = ax.c2p(185, 112)
    region = Rectangle(width=ur[0] - ll[0], height=ur[1] - ll[1], stroke_width=0, fill_color=GREEN,
                       fill_opacity=0.10 * (0.6 if faded else 1)).move_to(
        [(ll[0] + ur[0]) / 2, (ll[1] + ur[1]) / 2, 0])
    dots = VGroup(); labels = VGroup()
    for nm, sp, q, r, col, show in MODELS:
        dt = Dot(ax.c2p(sp, q), radius=r, color=col, fill_opacity=0.75 * op, stroke_width=0)
        dots.add(dt)
        if show and not faded:
            labels.add(T(nm, size=15, color=WHITE).next_to(dt, UP, buff=0.08))
    return ax, xl, yl, region, dots, labels


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
        c = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.08, stroke_color=color,
                             fill_color=color, fill_opacity=1)
        label = T(name, size=22, color=color, weight=BOLD, vi=vi).next_to(c, RIGHT, buff=0.18)
        return VGroup(c, label).to_corner(UL, buff=0.45)


# ============================================================
# CẢNH 1 — BRIDGE: cán cân Nhanh·Rẻ ⇄ Chất lượng
# ============================================================
class Slide12aBridge(VoiceScene):
    def construct(self):
        s, d = self.say("voice/s12a_01.mp3")
        tagH = self.make_tag("Hardware", TEAL)
        self.add(tagH)
        tagT = self.make_tag("Trade-off", MAROON)
        self.play(FadeOut(tagH, shift=UP * 0.3), FadeIn(tagT, shift=UP * 0.3), run_time=0.8)
        title = T("Đánh đổi: Chất lượng ↔ Hiệu quả", size=30, color=WHITE, weight=BOLD,
                  vi=True).to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
        self.fill(s, d)

        s, d = self.say("voice/s12a_02.mp3")
        fulcrum = Triangle(color=WHITE, fill_opacity=1).scale(0.4).move_to(DOWN * 1.5)
        beam = Line(LEFT * 3.2, RIGHT * 3.2, color=WHITE, stroke_width=8).move_to(DOWN * 0.8)

        def pan(text, color):
            box = RoundedRectangle(width=2.7, height=0.95, corner_radius=0.12, stroke_color=color,
                                   fill_color=color, fill_opacity=0.2)
            box.add(T(text, size=19, color=color, weight=BOLD, vi=True).move_to(box))
            return box

        panL = pan("Nhanh · Rẻ", GREEN).move_to(beam.get_left() + DOWN * 0.6)
        panR = pan("Chất lượng", BLUE).move_to(beam.get_right() + DOWN * 0.6)
        scale_g = VGroup(beam, panL, panR)
        self.play(FadeIn(fulcrum), Create(beam), FadeIn(panL), FadeIn(panR), run_time=1.0)
        self.fill(s, d)

        s, d = self.say("voice/s12a_03.mp3")
        q = T("đánh đổi bao nhiêu chất lượng để lấy tốc độ / chi phí?", size=22, color=MAROON,
              weight=BOLD, vi=True).to_edge(DOWN, buff=0.5)
        self.play(Rotate(scale_g, -13 * DEGREES, about_point=fulcrum.get_top()), run_time=0.8)
        self.play(Rotate(scale_g, 26 * DEGREES, about_point=fulcrum.get_top()),
                  FadeIn(q, shift=UP * 0.15), run_time=1.1)
        self.play(Rotate(scale_g, -13 * DEGREES, about_point=fulcrum.get_top()), run_time=0.7)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 2 — BIỂU ĐỒ Quality vs Speed (bong bóng = giá)
# ============================================================
class Slide12bChart(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Trade-off", MAROON))
        ax, xl, yl, region, dots, labels = build_chart()
        src = T("ArtificialAnalysis.ai", size=16, color=MUTED).to_corner(UR, buff=0.4).shift(DOWN * 0.05)
        legend = VGroup(Dot(radius=0.18, color=MUTED, fill_opacity=0.5),
                        T("= giá / triệu token", size=15, color=MUTED, vi=True)
                        ).arrange(RIGHT, buff=0.15).to_corner(UL, buff=0.55).shift(DOWN * 0.9)

        # CÂU 01: tiêu đề + trục
        s, d = self.say("voice/s12b_01.mp3")
        title = T("Biểu đồ thực tế: Chất lượng vs Tốc độ", size=28, color=WHITE, weight=BOLD,
                  vi=True).to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.15), Create(ax), run_time=1.0)
        self.fill(s, d)

        # CÂU 02: nhãn trục + legend giá
        s, d = self.say("voice/s12b_02.mp3")
        self.play(FadeIn(xl), FadeIn(yl), FadeIn(legend), FadeIn(src), run_time=0.9)
        self.fill(s, d)

        # CÂU 03: chấm model
        s, d = self.say("voice/s12b_03.mp3")
        self.play(LaggedStart(*[GrowFromCenter(dt) for dt in dots], lag_ratio=0.12), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labels], lag_ratio=0.15), run_time=1.0)
        self.fill(s, d)

        # CÂU 04: trải khắp
        s, d = self.say("voice/s12b_04.mp3")
        self.play(LaggedStart(*[Indicate(dt, color=YELLOW, scale_factor=1.4) for dt in dots],
                  lag_ratio=0.06), run_time=1.4)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 3 — ĐỌC TRADE-OFF: vùng xanh + Pareto frontier
# ============================================================
class Slide12cRead(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Trade-off", MAROON))
        ax, xl, yl, region, dots, labels = build_chart()
        chart = VGroup(ax, xl, yl, dots, labels)
        self.add(chart)
        self.play(FadeIn(chart), run_time=0.4)

        # CÂU 01: vùng xanh hấp dẫn nhất
        s, d = self.say("voice/s12c_01.mp3")
        most = T("hấp dẫn nhất", size=20, color=GREEN, weight=BOLD, vi=True).move_to(
            region.get_top() + DOWN * 0.45)
        self.play(FadeIn(region), FadeIn(most), run_time=0.9)
        self.fill(s, d)

        # CÂU 02: ít model ở đó
        s, d = self.say("voice/s12c_02.mp3")
        self.play(Indicate(region, color=GREEN, scale_factor=1.02), run_time=0.9)
        self.fill(s, d)

        # CÂU 03: mạnh nhất ở trái-trên, chậm & đắt (Opus)
        s, d = self.say("voice/s12c_03.mp3")
        opus = dots[0]
        ring = Circle(radius=opus.width / 2 + 0.08, color=MAROON, stroke_width=4).move_to(opus)
        ol = T("chậm · đắt", size=17, color=MAROON, weight=BOLD, vi=True).next_to(opus, DOWN, buff=0.2)
        self.play(Create(ring), FadeIn(ol), run_time=0.9)
        self.fill(s, d)

        # CÂU 04: nhóm nhanh-rẻ thấp hơn (dots 6,7,8,9 = vùng phải-dưới)
        s, d = self.say("voice/s12c_04.mp3")
        grp = VGroup(dots[6], dots[7], dots[8], dots[9])
        br = SurroundingRectangle(VGroup(grp, labels[4], labels[5]), color=ORANGE, corner_radius=0.1, buff=0.18)
        gl = T("nhanh · rẻ · chất lượng thấp hơn", size=17, color=ORANGE, weight=BOLD, vi=True).next_to(
            br, DOWN, buff=0.15)
        self.play(Create(br), FadeIn(gl), run_time=0.9)
        self.fill(s, d)

        # CÂU 05: Pareto frontier + mũi tên — fade labels trước để tránh rối
        s, d = self.say("voice/s12c_05.mp3")
        curve = VMobject().set_points_smoothly([ax.c2p(x, y) for x, y in FRONTIER])
        curve = DashedVMobject(curve, num_dashes=40).set_stroke(MAROON, 4)
        # arrow route phía trên các bong bóng (y=106→89 thay vì 100→84)
        arr = CurvedArrow(ax.c2p(75, 106), ax.c2p(168, 89), color=MAROON, angle=-TAU / 10)
        # label đặt trên đường cong, tránh bong bóng
        al = T("nhanh hơn → chất lượng ↓", size=19, color=MAROON, weight=BOLD, vi=True).move_to(
            ax.c2p(118, 110))
        self.play(FadeOut(VGroup(ring, ol, br, gl, most)), FadeOut(labels), Create(curve), run_time=1.0)
        self.play(GrowArrow(arr) if isinstance(arr, Arrow) else Create(arr), FadeIn(al), run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 4 — ĐỒNG HỒ đánh đổi (Dial 3b1b) + lossless
# ============================================================
class Slide12dDials(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Trade-off", MAROON))

        def panel_card(label, icon_name, color, width=1.65):
            box = RoundedRectangle(width=width, height=0.56, corner_radius=0.12,
                                   stroke_color=color, stroke_width=2,
                                   fill_color=color, fill_opacity=0.10)
            ic = svg_icon(icon_name, color, 0.28).move_to(box.get_left() + RIGHT * 0.23)
            tx = T(label, size=14, color=WHITE, weight=BOLD, vi=True).next_to(ic, RIGHT, buff=0.16)
            return VGroup(box, ic, tx)

        def dial_plate(center, title, color):
            plate = RoundedRectangle(width=2.75, height=2.35, corner_radius=0.18,
                                     stroke_color=color, stroke_width=1.5,
                                     fill_color=color, fill_opacity=0.045).move_to(center + DOWN * 0.08)
            cap = T(title, size=17, color=color, weight=BOLD, vi=True).next_to(plate, UP, buff=0.12)
            return VGroup(plate, cap)

        # CÂU 01: title + 2 đồng hồ trung tính xuất hiện
        s, d = self.say("voice/s12d_01.mp3")
        title = T("Đẩy tốc độ / chi phí  →  chất lượng tụt", size=28, color=WHITE, weight=BOLD,
                  vi=True).to_edge(UP, buff=0.65)
        c1 = LEFT * 1.55 + UP * 0.2
        c2 = RIGHT * 2.75 + UP * 0.2
        a1, t1 = dial_arc(c1); a2, t2 = dial_arc(c2)
        spd = ValueTracker(0.5); qual = ValueTracker(0.82)

        # Tính endpoint kim từ toán học (không phụ thuộc arc object)
        _ARC_S = 210 * DEGREES; _ARC_W = -240 * DEGREES; _ARC_R = 0.9
        def _npt(ctr, t):
            a = _ARC_S + _ARC_W * min(max(t, 0.001), 0.999)
            return ctr + _ARC_R * np.array([np.cos(a), np.sin(a), 0])

        needle1 = always_redraw(lambda: Line(
            c1, _npt(c1, spd.get_value()), color=GREEN, stroke_width=7))
        needle2 = always_redraw(lambda: Line(
            c2, _npt(c2, qual.get_value()),
            color=(interpolate_color(ManimColor(MUTED), ManimColor(GREEN),
                                     min((qual.get_value() - 0.5) * 2, 1.0))
                   if qual.get_value() >= 0.5 else
                   interpolate_color(ManimColor(MUTED), ManimColor(RED),
                                     min((0.5 - qual.get_value()) * 2, 1.0))),
            stroke_width=7))
        hub1 = Dot(c1, radius=0.07, color=GREEN)
        hub2 = Dot(c2, radius=0.07, color=GREEN)
        l1 = T("Tốc độ / Chi phí ↑", size=20, color=GREEN, weight=BOLD, vi=True).next_to(a1, DOWN, buff=0.3)
        l2 = T("Chất lượng", size=20, color=GREEN, weight=BOLD, vi=True).next_to(a2, DOWN, buff=0.3)

        speed_plate = dial_plate(c1, "hiệu quả", GREEN)
        quality_plate = dial_plate(c2, "độ tin cậy", MUTED)
        neutral_hint = T("mỗi kỹ thuật đẩy một kim,\nnhưng thường kéo kim còn lại", size=16,
                         color=MUTED, vi=True).move_to(DOWN * 2.35)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(speed_plate), FadeIn(quality_plate),
                  Create(a1), Create(t1), Create(a2), Create(t2),
                  FadeIn(hub1), FadeIn(hub2), run_time=1.1)
        self.add(needle1, needle2)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(neutral_hint, shift=UP * 0.1), run_time=0.4)
        self.fill(s, d)

        # CÂU 02: icon kỹ thuật bơm tốc độ → kim vọt lên nhanh rồi settle
        s, d = self.say("voice/s12d_02.mp3")
        self.play(FadeOut(neutral_hint, shift=DOWN * 0.1), run_time=0.25)
        techs = [
            ("model nhỏ", "minimize-2"),
            ("lượng tử", "cpu"),
            ("tỉa tham số", "scissors"),
            ("thoát sớm", "door-open"),
            ("xếp tầng", "layers"),
        ]
        col = VGroup(*[panel_card(label, icon, BLUE, width=1.72) for label, icon in techs])
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT, buff=0.45).shift(UP * 0.1)
        feed = Arrow(col.get_right() + RIGHT * 0.08, c1 + LEFT * 1.02, color=BLUE, stroke_width=4, buff=0.18)
        packets = VGroup(*[
            Dot(col[i].get_right() + RIGHT * 0.08, radius=0.045, color=BLUE, fill_opacity=0.95)
            for i in range(len(col))
        ])
        speed_glow = Circle(radius=0.26, color=GREEN, stroke_width=3).move_to(c1).set_opacity(0)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.12) for r in col], lag_ratio=0.12),
                  GrowArrow(feed), run_time=0.95)
        self.add(packets, speed_glow)
        packet_moves = [
            MoveAlongPath(packets[i], Line(packets[i].get_center(), c1 + LEFT * 0.15 + UP * (0.12 - i * 0.05)))
            for i in range(len(packets))
        ]
        self.play(LaggedStart(*packet_moves, lag_ratio=0.10),
                  speed_glow.animate.set_opacity(1).scale(2.0),
                  spd.animate(rate_func=rush_into).set_value(0.93),
                  run_time=0.9)
        self.remove(packets)
        self.play(FadeOut(speed_glow), spd.animate(rate_func=smooth).set_value(0.86), run_time=0.35)
        self.play(Flash(c1, color=GREEN, line_length=0.2, num_lines=8, flash_radius=0.18), run_time=0.3)
        self.fill(s, d)

        # CÂU 03: mũi tên đỏ nối + dot chạy qua để thể hiện "truyền ảnh hưởng"
        s, d = self.say("voice/s12d_03.mp3")
        link = CurvedArrow(c1 + RIGHT * 1.02, c2 + LEFT * 1.02, color=RED, angle=-TAU / 8,
                           stroke_width=5)
        toll = T("không miễn phí", size=14, color=RED, weight=BOLD, vi=True).next_to(link, UP, buff=0.10)
        _tri = Triangle(stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.18).scale(0.22)
        _excl = T("!", size=15, color=RED, weight=BOLD).move_to(_tri.get_center() + DOWN * 0.025)
        warning = VGroup(_tri, _excl).move_to(link.get_center() + DOWN * 0.42)
        ripples = VGroup(*[Dot(link.get_start(), radius=0.06, color=RED) for _ in range(3)])
        self.play(Create(link), FadeIn(toll, shift=DOWN * 0.1), FadeIn(warning, scale=0.85), run_time=0.65)
        self.add(ripples)
        self.play(LaggedStart(*[MoveAlongPath(r, link) for r in ripples], lag_ratio=0.18),
                  Indicate(quality_plate, color=RED, scale_factor=1.02), run_time=0.9)
        self.remove(ripples)
        self.fill(s, d)

        # CÂU 04: kim chất lượng tụt + arc đỏ + label đổi màu + Flash
        s, d = self.say("voice/s12d_04.mp3")
        l2_red = T("Chất lượng ↓", size=20, color=RED, weight=BOLD, vi=True).move_to(l2)
        risks = VGroup(
            panel_card("câu khó", "message-circle", RED, width=1.5),
            panel_card("quant mạnh", "cpu", RED, width=1.75),
            panel_card("dừng sớm", "door-open", RED, width=1.62),
            panel_card("kiểm soát", "layers", RED, width=1.62),
        ).arrange(RIGHT, buff=0.14).move_to(DOWN * 1.85 + RIGHT * 1.25)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.12) for r in risks], lag_ratio=0.12), run_time=0.75)
        self.play(
            qual.animate(rate_func=rush_into).set_value(0.30),
            a2.animate.set_stroke(color=RED, width=4),
            hub2.animate.set_color(RED),
            Transform(l2, l2_red),
            run_time=0.8,
        )
        self.play(qual.animate(rate_func=rush_into).set_value(0.16),
                  Indicate(risks, color=RED, scale_factor=1.04), run_time=0.55)
        self.play(Flash(c2, color=RED, line_length=0.25, num_lines=10, flash_radius=0.22), run_time=0.35)
        self.fill(s, d)

        # CÂU 05: speculative decoding lossless — banner bay lên từ dưới
        s, d = self.say("voice/s12d_05.mp3")
        self.play(FadeOut(risks, shift=DOWN * 0.1), FadeOut(warning), run_time=0.35)
        spec = RoundedRectangle(width=10.4, height=1.70, corner_radius=0.18, stroke_color=GREEN,
                                stroke_width=2.2, fill_color=GREEN, fill_opacity=0.09).to_edge(DOWN, buff=0.28)
        # Title row — dùng arrange() để cân đối
        spec_ic = svg_icon("zap", GREEN, 0.42)
        spec_t = T("Speculative decoding: tăng tốc nhưng lossless", size=19,
                   color=GREEN, weight=BOLD, vi=True)
        title_row = VGroup(spec_ic, spec_t).arrange(RIGHT, buff=0.22).move_to(spec.get_center() + UP * 0.44)
        # Pipeline row — arrange 3 card + vẽ mũi tên sau
        draft = panel_card("draft nhanh", "zap", BLUE, width=1.78)
        verify = panel_card("model gốc kiểm", "gauge", GREEN, width=2.18)
        accept = panel_card("giữ chất lượng", "heart-pulse", GREEN, width=2.12)
        VGroup(draft, verify, accept).arrange(RIGHT, buff=0.95).move_to(spec.get_center() + DOWN * 0.40)
        pipe1 = Arrow(draft.get_right() + RIGHT * 0.08, verify.get_left() - RIGHT * 0.08,
                      color=MUTED, stroke_width=3.5, buff=0)
        pipe2 = Arrow(verify.get_right() + RIGHT * 0.08, accept.get_left() - RIGHT * 0.08,
                      color=GREEN, stroke_width=3.5, buff=0)
        l2_ok = VGroup(
            T("Chất lượng", size=15, color=GREEN, weight=BOLD, vi=True),
            T("giữ nguyên", size=15, color=GREEN, weight=BOLD, vi=True),
        ).arrange(DOWN, buff=0.03).move_to(l2.get_center() + DOWN * 0.03)
        self.play(FadeIn(spec, shift=UP * 0.18, scale=0.96),
                  FadeIn(title_row, shift=UP * 0.1), run_time=0.65)
        self.play(FadeIn(draft, shift=RIGHT * 0.15), GrowArrow(pipe1),
                  FadeIn(verify, shift=RIGHT * 0.15), run_time=0.65)
        self.play(GrowArrow(pipe2), FadeIn(accept, shift=RIGHT * 0.15),
                  qual.animate(rate_func=smooth).set_value(0.72),
                  a2.animate.set_stroke(color=GREEN, width=4), hub2.animate.set_color(GREEN),
                  FadeOut(l2), FadeIn(l2_ok, shift=UP * 0.05),
                  run_time=0.8)
        self.play(Indicate(accept, color=GREEN, scale_factor=1.12),
                  Flash(c2, color=GREEN, line_length=0.22, num_lines=10, flash_radius=0.28),
                  run_time=0.55)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 5 — KHÔNG one-size-fits-all (icon đặt lên biểu đồ)
# ============================================================
class Slide12eUseCases(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Trade-off", MAROON))

        # Chart chỉ có trục + nhãn — bỏ region và dots
        ax, xl, yl, _, _, _ = build_chart(faded=True)
        chart = VGroup(ax, xl, yl)
        title = T("Mỗi nhu cầu — một \"điểm ngọt\" khác nhau", size=26, color=WHITE, weight=BOLD,
                  vi=True).to_edge(UP, buff=0.55)

        # CÂU 01: chart sạch
        s, d = self.say("voice/s12e_01.mp3")
        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(chart), run_time=0.8)
        self.fill(s, d)

        def marker(icon, cap, color, sp, q, lbl_dir=DOWN):
            ic = svg_icon(icon, color, 0.52).move_to(ax.c2p(sp, q))
            halo = Circle(radius=0.44, color=color, stroke_width=3.5,
                          fill_color=color, fill_opacity=0.12).move_to(ic)
            lb = T(cap, size=16, color=color, weight=BOLD, vi=True).next_to(halo, lbl_dir, buff=0.14)
            return VGroup(halo, ic, lb), ax.c2p(sp, q)

        # CÂU 02: chatbot giải trí — vùng nhanh-rẻ phải-dưới
        s, d = self.say("voice/s12e_02.mp3")
        m1, p1 = marker("message-circle", "chatbot giải trí", GREEN, 155, 85, lbl_dir=UP)
        self.play(GrowFromCenter(m1), run_time=0.65)
        self.play(Flash(p1, color=GREEN, line_length=0.2, num_lines=8, flash_radius=0.52), run_time=0.35)
        self.fill(s, d)

        # CÂU 03: y tế · pháp lý + lập trình — vùng chất lượng cao
        s, d = self.say("voice/s12e_03.mp3")
        m2, p2 = marker("heart-pulse", "y tế · pháp lý", RED, 30, 91)
        m3, p3 = marker("code", "lập trình", BLUE, 76, 97, lbl_dir=UP)
        self.play(GrowFromCenter(m2), GrowFromCenter(m3), run_time=0.75)
        self.play(
            Flash(p2, color=RED, line_length=0.2, num_lines=8, flash_radius=0.52),
            Flash(p3, color=BLUE, line_length=0.2, num_lines=8, flash_radius=0.52),
            run_time=0.35,
        )
        self.fill(s, d)

        # CÂU 04: thiết bị vs cloud — ràng buộc khác nhau
        s, d = self.say("voice/s12e_04.mp3")
        m4, p4 = marker("smartphone", "trên thiết bị", YELLOW, 138, 64)
        m5, p5 = marker("cloud", "API cloud", TEAL, 52, 80)
        self.play(GrowFromCenter(m4), GrowFromCenter(m5), run_time=0.75)
        self.play(
            Flash(p4, color=YELLOW, line_length=0.2, num_lines=8, flash_radius=0.52),
            Flash(p5, color=TEAL, line_length=0.2, num_lines=8, flash_radius=0.52),
            run_time=0.35,
        )
        self.fill(s, d)

        # CÂU 05: Indicate tất cả theo thứ tự
        s, d = self.say("voice/s12e_05.mp3")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.15) for m in [m1, m2, m3, m4, m5]],
                  lag_ratio=0.18), run_time=1.4)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 6 — RECAP RADIAL: 5 bottleneck -> cân bằng
# ============================================================
class _Slide12fRecapOld(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Trade-off", MAROON))
        center = ORIGIN + UP * 0.25
        core = Circle(radius=0.95, color=WHITE, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(center)
        core_l = T("Cân bằng", size=22, color=WHITE, weight=BOLD, vi=True).move_to(core)
        nodes = [("Latency", RED), ("Memory", YELLOW), ("Throughput", GREEN),
                 ("Hardware", TEAL), ("Trade-off", MAROON)]
        n = len(nodes); ring = VGroup()
        for i, (nm, col) in enumerate(nodes):
            ang = PI / 2 + i * TAU / n
            pos = center + 2.7 * np.array([np.cos(ang), np.sin(ang), 0])
            chip = RoundedRectangle(width=2.2, height=0.85, corner_radius=0.14, stroke_color=col,
                                    fill_color=col, fill_opacity=0.18).move_to(pos)
            chip.add(T(nm, size=19, color=col, weight=BOLD, vi=True).move_to(chip))
            direction = normalize(chip.get_center() - center)
            line = Line(center + direction * 0.95, chip.get_center() - direction * 1.15,
                        color=col, stroke_width=3)
            ring.add(VGroup(line, chip))

        # CÂU 01: khép lại phần 2 -> lõi
        s, d = self.say("voice/s12f_01.mp3")
        self.play(FadeIn(core), FadeIn(core_l), run_time=0.7)
        self.fill(s, d)

        # CÂU 02: 5 nút
        s, d = self.say("voice/s12f_02.mp3")
        self.play(LaggedStart(*[FadeIn(g, shift=0.1 * normalize(g[1].get_center() - center))
                  for g in ring], lag_ratio=0.25), run_time=2.0)
        self.fill(s, d)

        # CÂU 03: ảnh hưởng lẫn nhau
        s, d = self.say("voice/s12f_03.mp3")
        self.play(LaggedStart(*[Indicate(g[1], scale_factor=1.1) for g in ring],
                  lag_ratio=0.1), run_time=1.1)
        self.fill(s, d)

        # CÂU 04: phương trình cân bằng
        s, d = self.say("voice/s12f_04.mp3")
        eq = T("Efficient LLM Serving = cân bằng 5 yếu tố", size=22, color=WHITE, weight=BOLD,
               vi=True).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(eq, shift=UP * 0.15), Indicate(VGroup(core, core_l), color=WHITE), run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 7 — CHUYỂN SANG PHẦN 3
# ============================================================
class Slide12fRecap(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Trade-off", MAROON))

        title = VGroup(
            T("KHÉP LẠI PHẦN 2", size=13, color=MUTED, weight=BOLD, vi=True),
            T("5 nút thắt • 1 hệ cân bằng", size=27, color=WHITE, weight=BOLD, vi=True),
        ).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.42)

        center = ORIGIN + DOWN * 0.08

        # Lõi trung tâm — đơn giản, rõ ràng
        core_ring = Circle(radius=0.70, color=BLUE, stroke_width=3,
                           fill_color=BG, fill_opacity=1).move_to(center)
        core_glow = Circle(radius=0.82, color=BLUE, stroke_width=14).set_stroke(opacity=0.09).move_to(center)
        core_lbl = VGroup(
            T("LLM", size=20, color=WHITE, weight=BOLD),
            T("Serving", size=12, color=MUTED, weight=BOLD, vi=True),
        ).arrange(DOWN, buff=0.04).move_to(center)
        core = VGroup(core_glow, core_ring, core_lbl)

        # 5 nút theo thứ tự pentagon, dùng svg_icon
        specs = [
            ("Độ trễ",      RED,    "gauge",       UP * 2.05),
            ("Bộ nhớ",      YELLOW, "layers",      RIGHT * 3.82 + UP * 0.68),
            ("Thông lượng", GREEN,  "zap",         RIGHT * 2.52 + DOWN * 1.88),
            ("Phần cứng",   TEAL,   "cpu",         LEFT * 2.52 + DOWN * 1.88),
            ("Chất lượng",  MAROON, "heart-pulse", LEFT * 3.82 + UP * 0.68),
        ]

        def make_node(label, color, icon_name):
            card = RoundedRectangle(width=2.10, height=0.72, corner_radius=0.16,
                                    stroke_color=color, stroke_width=2.5,
                                    fill_color=color, fill_opacity=0.12)
            ic = svg_icon(icon_name, color, 0.32).move_to(card.get_left() + RIGHT * 0.35)
            txt = T(label, size=16, color=color, weight=BOLD, vi=True).next_to(ic, RIGHT, buff=0.14)
            return VGroup(card, ic, txt)

        nodes = VGroup(*[make_node(lbl, col, icn).move_to(pos)
                         for lbl, col, icn, pos in specs])
        spokes = VGroup()
        for node, (_, col, _, _) in zip(nodes, specs):
            dirn = normalize(node.get_center() - center)
            spoke = Line(center + dirn * 0.72, node.get_center() - dirn * 1.07,
                         color=col, stroke_width=2.0)
            spoke.set_stroke(opacity=0.45)
            spokes.add(spoke)

        spokes.set_z_index(-1)
        core.set_z_index(2)
        nodes.set_z_index(3)

        # CÂU 01: title + lõi trung tâm xuất hiện
        s, d = self.say("voice/s12f_01.mp3")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.5)
        self.play(FadeIn(core_glow), DrawBorderThenFill(core_ring),
                  FadeIn(core_lbl), run_time=0.85)
        self.fill(s, d)

        # CÂU 02: 5 nút tỏa ra lần lượt + pulse hội tụ vào lõi
        s, d = self.say("voice/s12f_02.mp3")
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    Create(spokes[i]),
                    GrowFromCenter(nodes[i][0]),
                    FadeIn(nodes[i][1:], shift=0.08 * normalize(center - nodes[i].get_center())),
                )
                for i in range(5)
            ], lag_ratio=0.18),
            run_time=1.8,
        )
        pulses = VGroup(*[Dot(nodes[i].get_center(), radius=0.045,
                              color=specs[i][1], fill_opacity=0.9) for i in range(5)])
        self.add(pulses)
        self.play(
            LaggedStart(*[MoveAlongPath(pulses[i], Line(nodes[i].get_center(), center))
                          for i in range(5)], lag_ratio=0.08),
            run_time=0.9,
        )
        self.remove(pulses)
        self.play(Flash(center, color=BLUE, line_length=0.22, num_lines=12, flash_radius=0.85),
                  run_time=0.45)
        self.fill(s, d)

        # CÂU 03: Indicate từng nút — nhấn mạnh thứ tự 5 thách thức
        s, d = self.say("voice/s12f_03.mp3")
        self.play(
            LaggedStart(*[Indicate(nodes[i][0], scale_factor=1.10, color=specs[i][1])
                          for i in range(5)], lag_ratio=0.14),
            run_time=1.3,
        )
        self.fill(s, d)

        # CÂU 04: vòng xanh cân bằng + phương trình
        s, d = self.say("voice/s12f_04.mp3")
        eq_bg = RoundedRectangle(width=8.2, height=0.60, corner_radius=0.14,
                                 stroke_color=GREEN, stroke_width=1.8,
                                 fill_color=BG, fill_opacity=0.94).to_edge(DOWN, buff=0.35)
        eq = T("Efficient LLM Serving = cân bằng 5 yếu tố", size=20,
               color=WHITE, weight=BOLD, vi=True).move_to(eq_bg)
        stable_ring = Circle(radius=0.76, color=GREEN, stroke_width=3.5,
                             fill_color=BG, fill_opacity=1).move_to(center)
        self.play(
            Transform(core_ring, stable_ring),
            FadeIn(eq_bg, shift=UP * 0.12), FadeIn(eq, shift=UP * 0.12),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[Circumscribe(nodes[i][0], color=specs[i][1], buff=0.05, fade_out=True)
                          for i in range(5)], lag_ratio=0.10),
            run_time=1.2,
        )
        self.fill(s, d)
        self.wait(0.3)


class Slide12gToPart3(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Trade-off", MAROON))
        # CÂU 01: 5 nút nhỏ -> mũi tên
        s, d = self.say("voice/s12g_01.mp3")
        cols = [RED, YELLOW, GREEN, TEAL, MAROON]
        names = ["Latency", "Memory", "Throughput", "Hardware", "Trade-off"]
        chips = VGroup()
        for nm, c in zip(names, cols):
            b = RoundedRectangle(width=2.05, height=0.7, corner_radius=0.12, stroke_color=c,
                                 fill_color=c, fill_opacity=0.18)
            b.add(T(nm, size=17, color=c, weight=BOLD).move_to(b))
            chips.add(b)
        chips.arrange(RIGHT, buff=0.25).to_edge(UP, buff=1.3)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in chips], lag_ratio=0.1), run_time=1.0)
        arr = Arrow(chips.get_bottom(), DOWN * 0.6, color=WHITE, stroke_width=6, buff=0.3)
        self.play(GrowArrow(arr), run_time=0.6)
        self.fill(s, d)

        # CÂU 02: Phần 3 — Giải pháp (thuật toán -> hệ thống)
        s, d = self.say("voice/s12g_02.mp3")
        node = RoundedRectangle(width=6.6, height=1.5, corner_radius=0.18, stroke_color=BLUE,
                                fill_color=BLUE, fill_opacity=0.16).move_to(DOWN * 1.6)
        nt = VGroup(T("PHẦN 3 — GIẢI PHÁP", size=26, color=WHITE, weight=BOLD, vi=True),
                    T("tối ưu thuật toán  →  tối ưu hệ thống", size=20, color=BLUE, vi=True)
                    ).arrange(DOWN, buff=0.18).move_to(node)
        self.play(FadeIn(node, shift=UP * 0.15), FadeIn(nt), run_time=1.0)
        self.play(Indicate(node, color=BLUE, scale_factor=1.06), run_time=0.8)
        self.fill(s, d)
        self.wait(0.4)
