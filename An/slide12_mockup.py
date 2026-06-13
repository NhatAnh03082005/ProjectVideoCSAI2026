from manim import *
import os

# ============================================================
# SLIDE 12 — MOCKUP THIẾT KẾ MỚI (bỏ chữ, tăng hình; tận dụng 3b1b Dial)
# Render frame tĩnh: PYTHONUTF8=1 manim -qh -s slide12_mockup.py <Scene>
#   M3Pareto  M4Dials  M5UseCases  M6Recap
# ============================================================

FONT_VI = "Arial"
BG = "#0f172a"
WHITE = "#e5e7eb"; MUTED = "#94a3b8"; BLUE = "#38bdf8"; GREEN = "#22c55e"
YELLOW = "#facc15"; RED = "#ef4444"; PURPLE = "#a78bfa"; ORANGE = "#fb923c"
TEAL = "#2dd4bf"; MAROON = "#e11d48"; SLATE = "#64748b"; BROWN = "#b07a55"
config.background_color = BG
TEXT_SS = 4
ASSETS = "assets"


def T(text, size=24, color=WHITE, weight=NORMAL, vi=False):
    kw = dict(font_size=size * TEXT_SS, color=color, weight=weight)
    if vi or any(ord(c) > 127 or c.isdigit() for c in text):
        kw["font"] = FONT_VI
    return Text(text, **kw).scale(1 / TEXT_SS)


def svg_icon(name, color, height=1.0, sw=3.0):
    m = SVGMobject(os.path.join(ASSETS, name + ".svg"))
    m.set_height(height); m.set_stroke(color=color, width=sw); m.set_fill(opacity=0)
    return m


def make_dial(value, radius=0.9, needle_color=BLUE, arc_color=MUTED):
    # speedometer: value thấp -> kim trái, value cao -> kim phải (quét qua đỉnh)
    arc = Arc(radius=radius, start_angle=210 * DEGREES, angle=-240 * DEGREES)
    arc.set_stroke(arc_color, 3)
    ticks = VGroup(*[Line(0.82 * arc.point_from_proportion(a), arc.point_from_proportion(a))
                     for a in np.linspace(0, 1, 11)]).set_stroke(arc_color, 2.5)
    needle = Line(ORIGIN, arc.point_from_proportion(value), stroke_width=7, color=needle_color)
    hub = Dot(ORIGIN, radius=0.07, color=needle_color)
    return VGroup(arc, ticks, needle, hub)


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


def build_chart(faded=False):
    op = 0.25 if faded else 1.0
    ax = Axes(x_range=[0, 185, 20], y_range=[50, 112, 10], x_length=10.4, y_length=5.4,
              axis_config={"include_tip": False, "stroke_color": MUTED}).shift(DOWN * 0.4)
    xl = T("Output Speed (token/giây)", size=20, color=MUTED, vi=True).next_to(ax, DOWN, buff=0.25)
    yl = T("Quality", size=20, color=MUTED, vi=True).rotate(PI / 2).next_to(ax, LEFT, buff=0.1)
    ll = ax.c2p(95, 78); ur = ax.c2p(185, 112)
    region = Rectangle(width=ur[0] - ll[0], height=ur[1] - ll[1], stroke_width=0,
                       fill_color=GREEN, fill_opacity=0.10 * (0.6 if faded else 1)).move_to(
        [(ll[0] + ur[0]) / 2, (ll[1] + ur[1]) / 2, 0])
    dots = VGroup(); labels = VGroup()
    for nm, sp, q, r, col, show in MODELS:
        dt = Dot(ax.c2p(sp, q), radius=r, color=col, fill_opacity=0.75 * op, stroke_width=0)
        dots.add(dt)
        if show and not faded:
            labels.add(T(nm, size=15, color=WHITE).next_to(dt, UP, buff=0.08))
    return ax, xl, yl, region, dots, labels


# ============================================================
# MOCKUP C3 — Scatter + Pareto frontier + vùng xanh (đọc trade-off bằng HÌNH)
# ============================================================
class M3Pareto(Scene):
    def construct(self):
        self.add(make_tag("Trade-off", MAROON))
        ax, xl, yl, region, dots, labels = build_chart()
        self.add(ax, xl, yl, region, dots, labels)
        src = T("ArtificialAnalysis.ai", size=16, color=MUTED).to_corner(UR, buff=0.4).shift(DOWN * 0.1)
        legend = VGroup(Dot(radius=0.18, color=MUTED, fill_opacity=0.5),
                        T("= giá / triệu token", size=15, color=MUTED, vi=True)
                        ).arrange(RIGHT, buff=0.15).to_corner(UL, buff=0.55).shift(DOWN * 0.9)
        self.add(src, legend)
        # vùng xanh nhãn
        most = T("hấp dẫn nhất", size=18, color=GREEN, weight=BOLD, vi=True).move_to(
            region.get_top() + DOWN * 0.4)
        self.add(most)
        # Pareto frontier (đường biên tối ưu) — đỏ nét đứt
        fr_pts = [(25, 93), (58, 95), (83, 100), (130, 85), (166, 84)]
        curve = VMobject().set_points_smoothly([ax.c2p(x, y) for x, y in fr_pts])
        curve = DashedVMobject(curve, num_dashes=40).set_stroke(MAROON, 4)
        self.add(curve)
        # mũi tên trên frontier: nhanh hơn -> chất lượng giảm
        arr = CurvedArrow(ax.c2p(90, 100), ax.c2p(160, 84), color=MAROON, angle=-TAU / 8)
        al = T("nhanh hơn → chất lượng ↓", size=18, color=MAROON, weight=BOLD, vi=True).move_to(
            ax.c2p(140, 96))
        self.add(arr, al)


# ============================================================
# MOCKUP C4 — ĐỒNG HỒ ĐÁNH ĐỔI (3b1b Dial) thay cho list chữ "kỹ thuật→rủi ro"
# ============================================================
class M4Dials(Scene):
    def construct(self):
        self.add(make_tag("Trade-off", MAROON))
        title = T("Đẩy tốc độ / chi phí  →  chất lượng tụt", size=28, color=WHITE,
                  weight=BOLD, vi=True).to_edge(UP, buff=0.7)
        self.add(title)
        # 2 đồng hồ
        d1 = make_dial(0.86, needle_color=GREEN).move_to(LEFT * 1.2 + UP * 0.2)
        d1l = T("Tốc độ / Chi phí ↑", size=20, color=GREEN, weight=BOLD, vi=True).next_to(d1, DOWN, buff=0.25)
        d1u = svg_icon("zap", GREEN, 0.4).next_to(d1, UP, buff=0.1)
        d2 = make_dial(0.16, needle_color=RED).move_to(RIGHT * 3.2 + UP * 0.2)
        d2l = T("Chất lượng ↓", size=20, color=RED, weight=BOLD, vi=True).next_to(d2, DOWN, buff=0.25)
        d2u = svg_icon("gauge", RED, 0.4).next_to(d2, UP, buff=0.1)
        link = Arrow(d1.get_right(), d2.get_left(), color=RED, stroke_width=6, buff=0.3)
        self.add(d1, d1l, d1u, d2, d2l, d2u, link)
        # cột kỹ thuật (icon) đẩy đồng hồ tốc độ
        techs = [("minimize-2", "model nhỏ"), ("door-open", "thoát sớm"),
                 ("scissors", "tỉa"), ("layers", "xếp tầng")]
        col = VGroup()
        for ic, cap in techs:
            row = VGroup(svg_icon(ic, BLUE, 0.5),
                         T(cap, size=16, color=WHITE, vi=True)).arrange(RIGHT, buff=0.2)
            col.add(row)
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.7).shift(UP * 0.2)
        feed = Arrow(col.get_right(), d1.get_left(), color=BLUE, stroke_width=4, buff=0.3)
        self.add(col, feed)
        # speculative decoding = lossless (xanh, tách riêng)
        spec = RoundedRectangle(width=8.6, height=0.95, corner_radius=0.15, stroke_color=GREEN,
                                fill_color=GREEN, fill_opacity=0.1).to_edge(DOWN, buff=0.5)
        spec_ic = svg_icon("zap", GREEN, 0.5).move_to(spec.get_left() + RIGHT * 0.55)
        spec_t = T("Speculative decoding — không mất mát chất lượng (lossless)", size=20,
                   color=GREEN, weight=BOLD, vi=True).next_to(spec_ic, RIGHT, buff=0.3)
        self.add(spec, spec_ic, spec_t)


# ============================================================
# MOCKUP C5 — USE-CASE đặt ICON LÊN biểu đồ (thay câu chữ)
# ============================================================
class M5UseCases(Scene):
    def construct(self):
        self.add(make_tag("Trade-off", MAROON))
        ax, xl, yl, region, dots, labels = build_chart(faded=True)
        self.add(ax, xl, yl, region, dots)
        title = T("Mỗi nhu cầu — một \"điểm ngọt\" khác nhau", size=26, color=WHITE,
                  weight=BOLD, vi=True).to_edge(UP, buff=0.6)
        self.add(title)

        def marker(icon, cap, color, sp, q):
            ic = svg_icon(icon, color, 0.7).move_to(ax.c2p(sp, q))
            halo = Circle(radius=0.55, color=color, stroke_width=3).move_to(ic)
            lb = T(cap, size=16, color=color, weight=BOLD, vi=True).next_to(halo, DOWN, buff=0.12)
            return VGroup(halo, ic, lb)

        m1 = marker("message-circle", "chatbot giải trí", GREEN, 150, 80)
        m2 = marker("code", "lập trình", BLUE, 70, 99)
        m3 = marker("heart-pulse", "y tế · pháp lý", RED, 40, 94)
        m4 = marker("smartphone", "trên thiết bị", ORANGE, 140, 66)
        self.add(m1, m2, m3, m4)


# ============================================================
# MOCKUP C6 — RECAP 5 BOTTLENECK -> CÂN BẰNG (radial, ít chữ)
# ============================================================
class M6Recap(Scene):
    def construct(self):
        self.add(make_tag("Trade-off", MAROON))
        center = ORIGIN + UP * 0.2
        core = Circle(radius=0.95, color=WHITE, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(center)
        core_l = T("Cân bằng", size=22, color=WHITE, weight=BOLD, vi=True).move_to(core)
        self.add(core, core_l)
        nodes = [("Latency", RED), ("Memory", YELLOW), ("Throughput", GREEN),
                 ("Hardware", TEAL), ("Trade-off", MAROON)]
        n = len(nodes)
        ring = VGroup()
        for i, (nm, col) in enumerate(nodes):
            ang = PI / 2 + i * TAU / n
            pos = center + 2.7 * np.array([np.cos(ang), np.sin(ang), 0])
            chip = RoundedRectangle(width=2.2, height=0.85, corner_radius=0.14, stroke_color=col,
                                    fill_color=col, fill_opacity=0.18).move_to(pos)
            chip.add(T(nm, size=19, color=col, weight=BOLD, vi=True).move_to(chip))
            direction = normalize(chip.get_center() - core.get_center())
            line = Line(core.get_center() + direction * 0.95,
                        chip.get_center() - direction * 1.15, color=col, stroke_width=3)
            ring.add(VGroup(line, chip))
        self.add(ring)
        eq = T("Efficient LLM Serving = cân bằng 5 yếu tố", size=22, color=WHITE, weight=BOLD,
               vi=True).to_edge(DOWN, buff=0.5)
        self.add(eq)


def make_tag(name, color):
    c = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.08, stroke_color=color,
                         fill_color=color, fill_opacity=1)
    label = T(name, size=22, color=color, weight=BOLD, vi=True).next_to(c, RIGHT, buff=0.18)
    return VGroup(c, label).to_corner(UL, buff=0.45)
