from manim import *
from mutagen.mp3 import MP3
import os

# ============================================================
# SLIDE 10 — SCALABILITY & THROUGHPUT (7 cảnh)
# Style: 3Blue1Brown (số chạy, dòng token, lưới GPU, cân) + theme Phần 2.
# Icon: SVG Lucide (assets/), recolor theo palette. KHÔNG dùng LaTeX (chỉ Text).
# Render (đứng TRONG slide10_themed/):
#   PYTHONUTF8=1 manim -qh --disable_caching slide10_scenes.py Slide10aArch
#   ... Slide10bLatVsTp Slide10cRequests Slide10dOutput
#   ... Slide10eBatching Slide10fTension Slide10gOutro
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

FILL_SOFT = 0.12
FILL_MEDIUM = 0.18

# Quy ước màu Slide 10
C_TP = GREEN       # throughput / GPU bận / gom batch
C_LAT = RED        # latency / chờ lâu / kẹt
C_PROMPT = BLUE    # prompt đã biết độ dài
C_OUT = YELLOW     # output chưa biết độ dài

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


def small_box(title, color, w=1.95, h=1.15, fs=19):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12,
                           stroke_color=color, fill_color=color, fill_opacity=0.16)
    box.add(T(title, size=fs, color=WHITE, weight=BOLD, vi=True).move_to(box))
    return box


# ============================================================
# CẢNH 1 — BRIDGE + KIẾN TRÚC SERVING
# ============================================================
class Slide10aArch(VoiceScene):
    def construct(self):
        # CÂU 01: bridge Memory#2 -> Throughput#3
        s, d = self.say("voice/s10a_01.mp3")
        tagM = self.make_tag("Memory", YELLOW)
        self.add(tagM)
        tagT = self.make_tag("Throughput", GREEN)
        self.play(FadeOut(tagM, shift=UP * 0.3), FadeIn(tagT, shift=UP * 0.3), run_time=0.8)
        self.fill(s, d)

        # CÂU 02: phục vụ 1 người -> toàn cảnh
        s, d = self.say("voice/s10a_02.mp3")
        intro = T("Phục vụ 1 người  →  phục vụ HÀNG NGHÌN người", size=28, color=WHITE,
                  weight=BOLD, vi=True).move_to(UP * 0.3)
        self.play(FadeIn(intro, shift=UP * 0.2), run_time=0.8)
        self.fill(s, d)
        self.play(FadeOut(intro), run_time=0.4)

        # CÂU 03: apps -> server
        s, d = self.say("voice/s10a_03.mp3")
        apps = VGroup(*[svg_icon("app-window", PURPLE, height=0.55) for _ in range(4)]
                      ).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.7).shift(UP * 0.2)
        apps_lbl = T("End Users", size=20, color=PURPLE, weight=BOLD, vi=True).next_to(apps, UP, buff=0.25)
        server = RoundedRectangle(width=8.2, height=4.3, corner_radius=0.18, stroke_color=BLUE,
                                  fill_color=BLUE, fill_opacity=0.05).shift(RIGHT * 1.4 + UP * 0.2)
        server_lbl = T("Server", size=20, color=BLUE, weight=BOLD, vi=True).next_to(
            server.get_corner(UL), DR, buff=0.18)
        req_arr = Arrow(apps.get_right(), server.get_left() + UP * 1.2, color=WHITE,
                        buff=0.2, stroke_width=4)
        req_lbl = T("Yêu cầu (HTTP/gRPC)", size=17, color=MUTED, vi=True).next_to(
            req_arr, UP, buff=0.08)
        self.play(FadeIn(apps_lbl), LaggedStart(*[FadeIn(a, shift=RIGHT * 0.15) for a in apps],
                  lag_ratio=0.12), run_time=0.9)
        self.play(Create(server), FadeIn(server_lbl), GrowArrow(req_arr), FadeIn(req_lbl),
                  run_time=1.0)
        self.fill(s, d)

        # CÂU 04: engine boxes + hardware
        s, d = self.say("voice/s10a_04.mp3")
        eng_lbl = T("Engine", size=18, color=TEAL, weight=BOLD, vi=True)
        b_q = small_box("Hàng đợi\n+ Lập lịch", TEAL)
        b_b = small_box("Dynamic\nBatching", GREEN)
        b_m = small_box("Model\n(backends)", BLUE)
        engine = VGroup(b_q, b_b, b_m).arrange(RIGHT, buff=0.45).move_to(server.get_center() + UP * 0.55)
        eng_lbl.next_to(engine, UP, buff=0.18)
        a1 = Arrow(b_q.get_right(), b_b.get_left(), color=WHITE, buff=0.08, stroke_width=3)
        a2 = Arrow(b_b.get_right(), b_m.get_left(), color=WHITE, buff=0.08, stroke_width=3)
        hw = RoundedRectangle(width=7.4, height=0.7, corner_radius=0.1, stroke_color=ORANGE,
                              fill_color=ORANGE, fill_opacity=0.14).move_to(server.get_center() + DOWN * 1.25)
        hw.add(T("Hardware (GPU / CPU)", size=19, color=ORANGE, weight=BOLD, vi=True).move_to(hw))
        self.play(FadeIn(eng_lbl), LaggedStart(FadeIn(b_q, shift=UP * 0.1), GrowArrow(a1),
                  FadeIn(b_b, shift=UP * 0.1), GrowArrow(a2), FadeIn(b_m, shift=UP * 0.1),
                  lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(hw, shift=UP * 0.1), run_time=0.6)
        self.fill(s, d)

        # CÂU 05: metrics + response
        s, d = self.say("voice/s10a_05.mp3")
        resp_arr = Arrow(server.get_left() + DOWN * 1.2, apps.get_right() + DOWN * 0.3,
                         color=MUTED, buff=0.2, stroke_width=4)
        resp_lbl = T("Phản hồi", size=16, color=MUTED, vi=True).next_to(resp_arr, DOWN, buff=0.05)
        metrics = RoundedRectangle(width=7.4, height=0.55, corner_radius=0.1, stroke_color=WHITE,
                                   fill_color=WHITE, fill_opacity=0.05).next_to(hw, DOWN, buff=0.18)
        metrics.add(T("Metrics:  Throughput · Latency", size=18, color=WHITE, vi=True).move_to(metrics))
        self.play(GrowArrow(resp_arr), FadeIn(resp_lbl), run_time=0.6)
        self.play(FadeIn(metrics, shift=UP * 0.1),
                  Indicate(metrics, color=GREEN, scale_factor=1.05), run_time=0.9)
        self.fill(s, d)

        # CÂU 06: chốt
        s, d = self.say("voice/s10a_06.mp3")
        self.play(Circumscribe(server, color=GREEN, run_time=1.4))
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 2 — LATENCY vs THROUGHPUT
# ============================================================
# ============================================================
# CẢNH 2 — LATENCY vs THROUGHPUT (BẢN THIẾT KẾ LẠI V2)
# Thay toàn bộ class Slide10bLatVsTp cũ bằng class này.
# Giữ nguyên 5 câu voice: s10b_01 -> s10b_05.
# ============================================================
class Slide10bLatVsTp(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Throughput", GREEN))

        # ----------------------------------------------------
        # Helpers: vẽ bằng primitive của Manim, không cần ảnh ngoài
        # ----------------------------------------------------
        def make_user(color=WHITE):
            head = Circle(
                radius=0.27,
                stroke_color=color,
                stroke_width=3,
                fill_opacity=0,
            ).shift(UP * 0.43)

            shoulders = Arc(
                radius=0.62,
                start_angle=20 * DEGREES,
                angle=140 * DEGREES,
                stroke_color=color,
                stroke_width=3,
            ).rotate(PI).shift(DOWN * 0.23)

            left_side = Line(
                shoulders.get_left() + UP * 0.02,
                shoulders.get_left() + DOWN * 0.34,
                color=color,
                stroke_width=3,
            )
            right_side = Line(
                shoulders.get_right() + UP * 0.02,
                shoulders.get_right() + DOWN * 0.34,
                color=color,
                stroke_width=3,
            )
            return VGroup(head, shoulders, left_side, right_side)

        def make_clock(center, phase):
            glow_1 = Circle(radius=0.63, stroke_color=RED, stroke_width=15)
            glow_1.set_stroke(opacity=0.055)
            glow_2 = Circle(radius=0.61, stroke_color=RED, stroke_width=8)
            glow_2.set_stroke(opacity=0.10)

            ring = Circle(
                radius=0.56,
                stroke_color=RED,
                stroke_width=3.2,
                fill_color=RED,
                fill_opacity=0.025,
            )

            # Crown: stem chạm viền trên, button ngang ở đỉnh stem
            _top = ring.get_top()
            crown = VGroup(
                Line(_top, _top + UP * 0.16, color=RED, stroke_width=3),
                Line(_top + UP * 0.16 + LEFT * 0.13, _top + UP * 0.16 + RIGHT * 0.13,
                     color=RED, stroke_width=3),
            )

            hub = Dot(radius=0.043, color=RED)
            clock = VGroup(glow_1, glow_2, ring, crown, hub)
            clock.move_to(center)

            # always_redraw phải dùng tọa độ tuyệt đối (không ORIGIN)
            # vì mỗi frame tạo Line mới, VGroup.move_to không giữ được shift
            _c = np.array(center, dtype=float)
            minute_hand = always_redraw(
                lambda: Line(
                    _c,
                    _c + rotate_vector(UP * 0.36, -TAU * phase.get_value()),
                    color=RED,
                    stroke_width=3.2,
                )
            )
            return clock, ring, minute_hand

        def make_token(
            phase_value,
            y_value,
            left_x,
            right_x,
            speed_tracker,
            opacity_tracker,
        ):
            halo = Dot(radius=0.145, color=GREEN).set_opacity(0.10)
            core = Dot(radius=0.078, color=GREEN)
            token = VGroup(halo, core)

            token.move_to([
                interpolate(left_x, right_x, phase_value),
                y_value,
                0,
            ])

            def flow(mob, dt):
                mob.shift(RIGHT * speed_tracker.get_value() * dt)

                if mob.get_x() > right_x:
                    mob.set_x(left_x + mob.get_x() - right_x)

                progress = (mob.get_x() - left_x) / (right_x - left_x)
                edge = min(
                    1.0,
                    max(0.0, progress * 8.0),
                    max(0.0, (1.0 - progress) * 8.0),
                )
                mob.set_opacity(opacity_tracker.get_value() * edge)

            token.add_updater(flow)
            return token

        # ----------------------------------------------------
        # Layout cố định
        # ----------------------------------------------------
        x_left = -3.55
        x_right = 3.55

        lat_title = T(
            "Latency",
            size=31,
            color=RED,
            weight=BOLD,
        ).move_to([x_left, 2.23, 0])

        tp_title = T(
            "Throughput",
            size=31,
            color=GREEN,
            weight=BOLD,
        ).move_to([x_right, 2.23, 0])

        # Đường chia được ngắt tại huy hiệu ≠, không còn chồng mũi tên.
        divider_top = DashedLine(
            [0, 1.93, 0],
            [0, 0.58, 0],
            dash_length=0.10,
            dashed_ratio=0.45,
            color=MUTED,
            stroke_width=1.8,
        ).set_opacity(0.60)

        divider_bottom = DashedLine(
            [0, -0.05, 0],
            [0, -2.10, 0],
            dash_length=0.10,
            dashed_ratio=0.45,
            color=MUTED,
            stroke_width=1.8,
        ).set_opacity(0.60)

        neq_outer = Circle(
            radius=0.37,
            stroke_color=BLUE,
            stroke_width=1.8,
            fill_color=BG,
            fill_opacity=1,
        )
        neq_inner = Circle(
            radius=0.31,
            stroke_color=WHITE,
            stroke_width=0.8,
        ).set_opacity(0.16)
        # Vẽ ≠ thủ công bằng Lines để tránh Pango render slash sai màu
        _eq_top  = Line(LEFT * 0.19, RIGHT * 0.19, color=WHITE, stroke_width=2.6).shift(UP  * 0.09)
        _eq_bot  = Line(LEFT * 0.19, RIGHT * 0.19, color=WHITE, stroke_width=2.6).shift(DOWN * 0.09)
        _slash   = Line(LEFT * 0.10 + DOWN * 0.20, RIGHT * 0.10 + UP * 0.20,
                        color=WHITE, stroke_width=2.6)
        neq_symbol = VGroup(_eq_top, _eq_bot, _slash)
        neq = VGroup(neq_outer, neq_inner, neq_symbol).move_to([0, 0.26, 0])

        # ====================================================
        # CÂU 01 — Phân biệt hai khái niệm
        # ====================================================
        s, d = self.say("voice/s10b_01.mp3")

        self.play(
            LaggedStart(
                FadeIn(lat_title, shift=DOWN * 0.15),
                FadeIn(tp_title, shift=DOWN * 0.15),
                Create(divider_top),
                Create(divider_bottom),
                FadeIn(neq, scale=0.72),
                lag_ratio=0.12,
            ),
            run_time=1.15,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 02 — Latency: một người chờ từ request đến phản hồi
        # ====================================================
        s, d = self.say("voice/s10b_02.mp3")

        user = svg_icon("user", WHITE, height=1.0).move_to([x_left - 1.15, 0.70, 0])

        clock_phase = ValueTracker(0.08)
        clock_phase.add_updater(
            lambda tracker, dt: tracker.increment_value(dt * 0.10)
        )
        clock, clock_ring, minute_hand = make_clock(
            [x_left + 1.15, 0.70, 0],
            clock_phase,
        )

        rail_y = -0.72
        rail_left = x_left - 2.05
        rail_right = x_left + 2.05

        rail = Line(
            [rail_left, rail_y, 0],
            [rail_right, rail_y, 0],
            color=MUTED,
            stroke_width=3,
        ).set_opacity(0.32)

        nodes = VGroup()
        node_count = 9
        for i in range(node_count):
            alpha = i / (node_count - 1)
            point = [
                interpolate(rail_left, rail_right, alpha),
                rail_y,
                0,
            ]
            nodes.add(
                Dot(
                    point,
                    radius=0.052,
                    color=MUTED,
                ).set_opacity(0.55)
            )

        latency_tracker = ValueTracker(0.0)
        latency_number = DecimalNumber(
            0,
            num_decimal_places=1,
            color=RED,
            font_size=42,
        ).move_to([x_left - 0.25, -1.63, 0])
        latency_number.add_updater(
            lambda number: number.set_value(latency_tracker.get_value())
        )

        latency_unit = always_redraw(
            lambda: T("s / request", size=23, color=RED)
            .next_to(latency_number, RIGHT, buff=0.14)
            .align_to(latency_number, DOWN)
        )

        request_dot = VGroup(
            Dot(radius=0.13, color=RED).set_opacity(0.14),
            Dot(radius=0.058, color=WHITE),
        ).move_to(nodes[0])

        self.play(
            FadeIn(user, shift=UP * 0.10),
            FadeIn(clock, scale=0.84),
            FadeIn(minute_hand, scale=0.84),
            Create(rail),
            LaggedStart(
                *[FadeIn(node, scale=0.70) for node in nodes],
                lag_ratio=0.05,
            ),
            run_time=0.95,
        )
        self.add(latency_number, latency_unit, request_dot)

        latency_path = Line(nodes[0].get_center(), nodes[4].get_center())
        self.play(
            MoveAlongPath(
                request_dot,
                latency_path,
                rate_func=linear,
            ),
            LaggedStart(
                *[
                    nodes[i].animate
                    .set_color(RED)
                    .set_opacity(1)
                    .scale(1.22)
                    for i in range(5)
                ],
                lag_ratio=0.10,
            ),
            latency_tracker.animate.set_value(1.8),
            run_time=1.55,
        )

        self.play(
            Flash(
                request_dot.get_center(),
                color=RED,
                line_length=0.13,
                flash_radius=0.25,
            ),
            Indicate(clock_ring, color=RED, scale_factor=1.08),
            run_time=0.55,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 03 — Throughput: token chạy liên tục và cách đều
        # ====================================================
        s, d = self.say("voice/s10b_03.mp3")

        pipe = RoundedRectangle(
            width=4.55,
            height=1.05,
            corner_radius=0.30,
            stroke_color=GREEN,
            stroke_width=2.5,
            fill_color=GREEN,
            fill_opacity=0.018,
        ).move_to([x_right, 0.54, 0])

        pipe_inner = RoundedRectangle(
            width=4.29,
            height=0.79,
            corner_radius=0.23,
            stroke_color=WHITE,
            stroke_width=0.7,
            fill_opacity=0,
        ).move_to(pipe).set_opacity(0.10)

        pipe_glow_1 = pipe.copy().set_stroke(
            GREEN,
            width=14,
            opacity=0.045,
        )
        pipe_glow_2 = pipe.copy().set_stroke(
            GREEN,
            width=7,
            opacity=0.085,
        )

        streaks = VGroup(
            Line(LEFT * 0.52, LEFT * 0.08, color=GREEN, stroke_width=2.8),
            Line(LEFT * 0.42, LEFT * 0.03, color=GREEN, stroke_width=2.0),
            Line(LEFT * 0.31, ORIGIN, color=GREEN, stroke_width=1.7),
        ).arrange(DOWN, buff=0.105)
        streaks.next_to(pipe, LEFT, buff=0.12)
        streaks.set_opacity(0.65)

        speed = ValueTracker(0.92)
        base_opacity = ValueTracker(1.0)
        extra_opacity = ValueTracker(0.0)

        token_left = pipe.get_left()[0] + 0.28
        token_right = pipe.get_right()[0] - 0.28
        token_y = pipe.get_center()[1]

        # 9 token cơ sở: cùng một hàng, giãn đều tuyệt đối.
        base_tokens = VGroup()
        for i in range(9):
            base_tokens.add(
                make_token(
                    phase_value=i / 9,
                    y_value=token_y,
                    left_x=token_left,
                    right_x=token_right,
                    speed_tracker=speed,
                    opacity_tracker=base_opacity,
                )
            )

        # Token phụ nằm chính giữa các token cơ sở.
        extra_tokens = VGroup()
        for i in range(9):
            extra_tokens.add(
                make_token(
                    phase_value=(i + 0.5) / 9,
                    y_value=token_y,
                    left_x=token_left,
                    right_x=token_right,
                    speed_tracker=speed,
                    opacity_tracker=extra_opacity,
                )
            )

        throughput_tracker = ValueTracker(0)
        throughput_number = Integer(
            0,
            color=GREEN,
            font_size=43,
        ).move_to([x_right - 0.25, -1.48, 0])
        throughput_number.add_updater(
            lambda number: number.set_value(
                int(throughput_tracker.get_value())
            )
        )

        throughput_unit = always_redraw(
            lambda: T("tok/s", size=19, color=GREEN)
            .next_to(throughput_number, RIGHT, buff=0.14)
            .align_to(throughput_number, DOWN)
        )

        self.play(
            FadeIn(pipe_glow_1),
            FadeIn(pipe_glow_2),
            Create(pipe),
            FadeIn(pipe_inner),
            FadeIn(streaks, shift=RIGHT * 0.10),
            run_time=0.85,
        )

        self.add(
            base_tokens,
            extra_tokens,
            throughput_number,
            throughput_unit,
        )

        self.play(
            throughput_tracker.animate.set_value(1850),
            run_time=1.25,
            rate_func=smooth,
        )

        self.play(
            ShowPassingFlash(
                pipe.copy().set_stroke(GREEN, width=5),
                time_width=0.35,
            ),
            run_time=0.55,
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 04 — Liên quan nhưng không cùng đại lượng
        # ====================================================
        s, d = self.say("voice/s10b_04.mp3")
        self.play(
            Circumscribe(neq_outer, color=BLUE, buff=0.08, stroke_width=2.5, run_time=0.90),
        )
        self.fill(s, d)

        # ====================================================
        # CÂU 05 — Tăng batch làm throughput tăng,
        # nhưng request đơn lẻ có thể phải chờ lâu hơn.
        # ====================================================
        s, d = self.say("voice/s10b_05.mp3")

        batch_title = T(
            "BATCH",
            size=15,
            color=MUTED,
            weight=BOLD,
        ).move_to([0, -2.26, 0])

        batch_values = ["1", "2", "4", "8", "16", "32"]
        batch_nodes = VGroup()

        for value in batch_values:
            circle = Circle(
                radius=0.20,
                stroke_color=BLUE,
                stroke_width=1.5,
                fill_color=BG,
                fill_opacity=1,
            )
            number = T(
                value,
                size=13,
                color=MUTED,
                weight=BOLD,
            ).move_to(circle)
            batch_nodes.add(VGroup(circle, number))

        batch_nodes.arrange(RIGHT, buff=0.30)
        batch_nodes.move_to([0, -2.70, 0])

        active_ring = Circle(
            radius=0.255,
            stroke_color=WHITE,
            stroke_width=2.2,
        ).move_to(batch_nodes[2])

        active_dot = Dot(
            batch_nodes[2].get_center(),
            radius=0.055,
            color=GREEN,
        )

        batch_line = Line(
            batch_nodes[0].get_center(),
            batch_nodes[-1].get_center(),
            color=BLUE,
            stroke_width=1.7,
        ).set_opacity(0.45)
        batch_line.set_z_index(-1)

        self.play(
            FadeIn(batch_title, shift=UP * 0.08),
            Create(batch_line),
            LaggedStart(
                *[FadeIn(node, scale=0.75) for node in batch_nodes],
                lag_ratio=0.07,
            ),
            FadeIn(active_ring, scale=0.75),
            FadeIn(active_dot),
            run_time=1.0,
        )

        new_ring = active_ring.copy().move_to(batch_nodes[4])
        new_dot = active_dot.copy().move_to(batch_nodes[4])

        latency_end_path = Line(
            request_dot.get_center(),
            nodes[7].get_center(),
        )

        self.play(
            Transform(active_ring, new_ring),
            Transform(active_dot, new_dot),

            MoveAlongPath(
                request_dot,
                latency_end_path,
                rate_func=smooth,
            ),

            LaggedStart(
                *[
                    nodes[i].animate
                    .set_color(RED)
                    .set_opacity(1)
                    .scale(1.15)
                    for i in range(5, 8)
                ],
                lag_ratio=0.11,
            ),

            latency_tracker.animate.set_value(3.4),
            throughput_tracker.animate.set_value(6420),

            speed.animate.set_value(1.85),
            extra_opacity.animate.set_value(0.92),

            run_time=1.85,
            rate_func=smooth,
        )

        self.play(
            Flash(
                request_dot.get_center(),
                color=RED,
                line_length=0.13,
                flash_radius=0.25,
            ),
            ShowPassingFlash(
                pipe.copy().set_stroke(GREEN, width=6),
                time_width=0.30,
            ),
            run_time=0.70,
        )

        self.fill(s, d)
        self.wait(0.35)

# ============================================================
# CẢNH 3 — REQUEST KHÔNG ĐỒNG NHẤT
# ============================================================
class Slide10cRequests(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Throughput", GREEN))
        title = T("Yêu cầu đến liên tục — và RẤT khác nhau", size=30, color=WHITE,
                  weight=BOLD, vi=True).to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        # Hàng đợi bên phải (mở rộng để chứa trọn các chuỗi token)
        queue = RoundedRectangle(width=7.2, height=4.4, corner_radius=0.15, stroke_color=MUTED,
                                 fill_color=MUTED, fill_opacity=0.05).move_to(RIGHT * 1.3 + DOWN * 0.3)
        q_lbl = T("Hàng đợi", size=20, color=MUTED, weight=BOLD, vi=True).next_to(
            queue, UP, buff=0.12)

        # Người dùng bên trái
        users = VGroup(*[svg_icon("user", WHITE, height=0.65) for _ in range(3)]
                       ).arrange(DOWN, buff=1.0).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)

        # CÂU 01: nhiều user bắn request
        s, d = self.say("voice/s10c_01.mp3")
        self.play(Create(queue), FadeIn(q_lbl), LaggedStart(*[FadeIn(u, shift=RIGHT*0.2) for u in users],
                  lag_ratio=0.15), run_time=1.0)
        self.fill(s, d)

        def make_token_stream(num_tokens, color, text):
            tokens = VGroup(*[
                RoundedRectangle(
                    width=0.16, height=0.35, corner_radius=0.04,
                    stroke_color=color, stroke_width=1.5,
                    fill_color=color, fill_opacity=0.4
                ) for _ in range(num_tokens)
            ]).arrange(RIGHT, buff=0.06)
            lbl = T(text, size=17, color=color, vi=True)
            lbl.next_to(tokens, UP, buff=0.1).align_to(tokens, LEFT)
            return VGroup(lbl, tokens)

        def animate_req(user_idx, num_tokens, color, text, y_offset):
            bar_group = make_token_stream(num_tokens, color, text)
            target_pos = queue.get_top() + DOWN * y_offset
            target_left = queue.get_left() + RIGHT * 0.3
            bar_group.move_to(target_pos)
            shift_x = target_left[0] - bar_group[1].get_left()[0]
            bar_group.shift(RIGHT * shift_x)
            self.play(Indicate(users[user_idx], color=color, scale_factor=1.2), run_time=0.4)
            self.play(
                FadeIn(bar_group[0], shift=DOWN*0.1),
                LaggedStart(*[FadeIn(t, shift=RIGHT*0.15, scale=0.6) for t in bar_group[1]], lag_ratio=0.03),
                run_time=min(1.0, 0.4 + num_tokens * 0.02)
            )
            return bar_group

        # CÂU 02: User A ngắn
        s, d = self.say("voice/s10c_02.mp3")
        reqA = animate_req(0, 6, TEAL, "\"2 + 2 = ?\"", 1.0)
        self.fill(s, d)

        # CÂU 03: User B dài, User C rất dài
        s, d = self.say("voice/s10c_03.mp3")
        reqB = animate_req(1, 16, ORANGE, "\"Viết bài phân tích 2000 chữ\"", 2.35)
        reqC = animate_req(2, 26, RED, "\"Tóm tắt tài liệu 30 trang\"", 3.7)
        self.fill(s, d)

        # CÂU 04: chênh độ dài — brace neo ngoài queue box
        s, d = self.say("voice/s10c_04.mp3")
        brace_x = queue.get_right()[0] + 0.25
        ref_line = Line(
            np.array([brace_x, reqA[1].get_center()[1], 0]),
            np.array([brace_x, reqC[1].get_center()[1], 0]),
            stroke_width=0
        )
        brace = Brace(ref_line, RIGHT, color=YELLOW)
        bl = T("chênh lệch\nrất xa", size=18, color=YELLOW, weight=BOLD, vi=True).next_to(
            brace, RIGHT, buff=0.12)
        self.play(GrowFromCenter(brace), FadeIn(bl, shift=LEFT*0.1), run_time=0.8)
        self.play(
            LaggedStart(*[Indicate(t, color=YELLOW, scale_factor=1.2) for t in reqC[1]], lag_ratio=0.03),
            run_time=1.2
        )
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 4 — OUTPUT KHÔNG BIẾT TRƯỚC
# ============================================================
class Slide10dOutput(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Throughput", GREEN))
        # CÂU 01: điểm khó nhất
        s, d = self.say("voice/s10d_01.mp3")
        title = T("Điểm khó nhất: độ dài ĐẦU RA không biết trước", size=30, color=WHITE,
                  weight=BOLD, vi=True).to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.fill(s, d)

        # CÂU 02: prompt biết, output không
        s, d = self.say("voice/s10d_02.mp3")
        prompt = RoundedRectangle(width=3.2, height=0.85, corner_radius=0.1, stroke_color=BLUE,
                                  fill_color=BLUE, fill_opacity=0.4).move_to(LEFT * 2.5 + UP * 0.4)
        p_lbl = T("Prompt — ĐÃ biết độ dài", size=20, color=BLUE, weight=BOLD, vi=True).next_to(
            prompt, UP, buff=0.2)
        out = DashedVMobject(RoundedRectangle(width=4.0, height=0.85, corner_radius=0.1,
                             stroke_color=YELLOW).move_to(RIGHT * 1.5 + UP * 0.4), num_dashes=40)
        q = T("?", size=44, color=YELLOW, weight=BOLD).move_to(out)
        o_lbl = T("Output — CHƯA biết độ dài", size=20, color=YELLOW, weight=BOLD, vi=True).next_to(
            out, UP, buff=0.2)
        self.play(FadeIn(prompt, shift=RIGHT * 0.1), FadeIn(p_lbl), run_time=0.7)
        self.play(Create(out), FadeIn(q, scale=0.6), FadeIn(o_lbl), run_time=0.9)
        self.fill(s, d)

        # CÂU 03: vài chữ hoặc vài nghìn chữ -> output co giãn
        s, d = self.say("voice/s10d_03.mp3")
        for w in (2.0, 5.5, 3.2):
            new_out = DashedVMobject(RoundedRectangle(width=w, height=0.85, corner_radius=0.1,
                                     stroke_color=YELLOW), num_dashes=int(w * 10))
            new_out.move_to(prompt.get_right() + RIGHT * (0.2 + w / 2))
            self.play(Transform(out, new_out), q.animate.move_to(new_out), run_time=0.5)
        self.fill(s, d)

        # CÂU 04: inference truyền thống cố định
        s, d = self.say("voice/s10d_04.mp3")
        trad = VGroup(
            T("Inference truyền thống:", size=20, color=MUTED, vi=True),
            RoundedRectangle(width=2.2, height=0.7, corner_radius=0.1, stroke_color=MUTED,
                             fill_color=MUTED, fill_opacity=0.2).add(
                T("cố định", size=18, color=WHITE, vi=True)),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1.6)
        self.play(FadeIn(trad, shift=UP * 0.2), run_time=0.8)
        self.fill(s, d)

        # CÂU 05: dấu hỏi co giãn -> khó lập lịch
        s, d = self.say("voice/s10d_05.mp3")
        hard = T("→ lập lịch & gom batch khó hơn rất nhiều", size=24, color=RED, weight=BOLD,
                 vi=True).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(hard, shift=UP * 0.2), Indicate(q, color=YELLOW, scale_factor=1.4),
                  run_time=1.0)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 5 — BATCHING
# ============================================================
class Slide10eBatching(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Throughput", GREEN))
        # CÂU 01: gom bát
        s, d = self.say("voice/s10e_01.mp3")
        title = T("Batching — gom nhiều yêu cầu xử lý chung", size=30, color=GREEN,
                  weight=BOLD, vi=True).to_edge(UP, buff=0.8)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        reqs = VGroup(*[RoundedRectangle(width=1.4, height=0.45, corner_radius=0.08,
                        stroke_color=WHITE, fill_color=WHITE, fill_opacity=0.18)
                        for _ in range(8)]).arrange_in_grid(rows=4, cols=2, buff=0.25).to_edge(
                        LEFT, buff=1.2).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in reqs], lag_ratio=0.06),
                  run_time=0.9)
        self.fill(s, d)

        # lưới slot GPU (kiểu MachineWithDials)
        grid = VGroup(*[Square(0.5, stroke_color=MUTED, stroke_width=2, fill_color=MUTED,
                        fill_opacity=0.1) for _ in range(8)]).arrange_in_grid(rows=4, cols=2, buff=0.18)
        gpu = RoundedRectangle(width=2.4, height=3.4, corner_radius=0.14, stroke_color=ORANGE,
                               fill_color=ORANGE, fill_opacity=0.06)
        grid.move_to(gpu)
        gpu_g = VGroup(gpu, grid).move_to(RIGHT * 3.2 + DOWN * 0.3)
        gpu_lbl = T("GPU", size=20, color=ORANGE, weight=BOLD, vi=True).next_to(gpu_g, UP, buff=0.2)
        cnt = ValueTracker(120)
        counter = always_redraw(lambda: T(f"{int(cnt.get_value())} tok/s", size=26, color=GREEN,
                                          weight=BOLD, vi=True).next_to(gpu_g, DOWN, buff=0.3))

        # CÂU 02: thay vì chạy lẻ -> xếp nhiều vào 1 lượt
        s, d = self.say("voice/s10e_02.mp3")
        batch_box = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.1, stroke_color=GREEN,
                                     fill_color=GREEN, fill_opacity=0.16).move_to(UP * 0.3)
        batch_box.add(T("Dynamic\nBatching", size=18, color=GREEN, weight=BOLD, vi=True).move_to(batch_box))
        self.play(FadeIn(gpu, shift=LEFT * 0.1), FadeIn(grid), FadeIn(gpu_lbl), run_time=0.7)
        self.add(counter)
        self.play(reqs.animate.scale(0.7).move_to(batch_box).set_opacity(0.0),
                  FadeIn(batch_box), run_time=1.0)
        self.fill(s, d)

        # CÂU 03: GPU bận hiệu quả -> tok/s tăng vọt
        s, d = self.say("voice/s10e_03.mp3")
        self.play(LaggedStart(*[c.animate.set_stroke(GREEN).set_fill(GREEN, 0.6) for c in grid],
                  lag_ratio=0.08), cnt.animate.set_value(5200), run_time=1.6)
        busy = T("GPU bận hiệu quả", size=22, color=GREEN, weight=BOLD, vi=True).next_to(
            title, DOWN, buff=0.3)
        self.play(FadeIn(busy, shift=DOWN * 0.1), run_time=0.5)
        self.fill(s, d)

        # CÂU 04: chỉ là cơ bản, kỹ thuật sâu để sau
        s, d = self.say("voice/s10e_04.mp3")
        note = T("(kỹ thuật gom thông minh hơn: để dành phần sau)", size=20, color=MUTED,
                 vi=True).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), FadeIn(batch_box), run_time=0.8)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 6 — CĂNG THẲNG LATENCY <-> THROUGHPUT (CENTERPIECE)
# ============================================================
class Slide10fTension(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Throughput", GREEN))
        # CÂU 01: căng thẳng cốt lõi
        s, d = self.say("voice/s10f_01.mp3")
        title = T("Căng thẳng cốt lõi: Latency  ↔  Throughput", size=30, color=WHITE,
                  weight=BOLD, vi=True).to_edge(UP, buff=0.7)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.fill(s, d)

        # CÂU 02: muốn gom nhiều -> throughput cao
        s, d = self.say("voice/s10f_02.mp3")
        up_arr = T("gom nhiều  →  throughput ↑", size=23, color=GREEN, weight=BOLD, vi=True
                   ).move_to(UP * 1.9)
        self.play(FadeIn(up_arr, shift=RIGHT * 0.2), run_time=0.7)
        self.fill(s, d)

        # CÂU 03: request ngắn kẹt sau dài -> latency
        s, d = self.say("voice/s10f_03.mp3")
        long_bar = RoundedRectangle(width=4.4, height=0.55, corner_radius=0.08, stroke_color=RED,
                                    fill_color=RED, fill_opacity=0.4).move_to(LEFT * 2.4 + UP * 0.5)
        long_bar.add(T("yêu cầu rất dài", size=16, color=WHITE, vi=True).move_to(long_bar))
        short_bar = RoundedRectangle(width=1.2, height=0.55, corner_radius=0.08, stroke_color=TEAL,
                                     fill_color=TEAL, fill_opacity=0.5)
        short_bar.add(T("2+2?", size=15, color=WHITE, vi=True).move_to(short_bar))
        short_bar.next_to(long_bar, RIGHT, buff=0.2)
        timer = svg_icon("timer", RED, height=0.7).next_to(short_bar, RIGHT, buff=0.3)
        kt = ValueTracker(0)
        tcount = always_redraw(lambda: T(f"chờ: {kt.get_value():.1f}s", size=18, color=RED,
                                         weight=BOLD, vi=True).next_to(timer, RIGHT, buff=0.15))
        self.play(FadeIn(long_bar, shift=LEFT * 0.1), FadeIn(short_bar), FadeIn(timer), run_time=0.7)
        self.add(tcount)
        self.play(kt.animate.set_value(8.0), Indicate(short_bar, color=RED, scale_factor=1.1),
                  run_time=1.3)
        self.fill(s, d)

        # CÂU 04: batch không đều -> GPU rảnh
        s, d = self.say("voice/s10f_04.mp3")
        grid = VGroup(*[Square(0.42, stroke_color=GREEN, stroke_width=2, fill_color=GREEN,
                        fill_opacity=0.6) for _ in range(8)]).arrange_in_grid(
                        rows=2, cols=4, buff=0.14).move_to(RIGHT * 3.6 + DOWN * 1.2)
        util = ValueTracker(100)
        ulbl = always_redraw(lambda: T(f"GPU: {int(util.get_value())}%", size=20,
                             color=interpolate_color(ManimColor(RED), ManimColor(GREEN),
                             util.get_value() / 100), weight=BOLD, vi=True).next_to(grid, UP, buff=0.25))
        self.play(FadeIn(grid), run_time=0.4)
        self.add(ulbl)
        idle = [1, 3, 4, 6]
        self.play(*[grid[i].animate.set_stroke(SLATE).set_fill(SLATE, 0.12) for i in idle],
                  util.animate.set_value(50), run_time=1.2)
        idle_lbl = T("slot trống → lãng phí", size=18, color=SLATE, vi=True).next_to(grid, DOWN, buff=0.25)
        self.play(FadeIn(idle_lbl), run_time=0.4)
        self.fill(s, d)

        # CÂU 05: cái cân
        s, d = self.say("voice/s10f_05.mp3")
        self.play(FadeOut(VGroup(long_bar, short_bar, timer, tcount, grid, ulbl, idle_lbl, up_arr)),
                  run_time=0.5)
        fulcrum = Triangle(color=WHITE, fill_opacity=1).scale(0.4).move_to(DOWN * 1.6)
        beam = Line(LEFT * 3, RIGHT * 3, color=WHITE, stroke_width=8).move_to(DOWN * 0.9)

        def pan(text, color):
            box = RoundedRectangle(width=2.3, height=0.9, corner_radius=0.12, stroke_color=color,
                                   fill_color=color, fill_opacity=0.2)
            lbl = T(text, size=18, color=color, weight=BOLD).move_to(box)
            return VGroup(box, lbl)

        panL = pan("THROUGHPUT", GREEN).move_to(beam.get_left() + DOWN * 0.6)
        panR = pan("LATENCY", RED).move_to(beam.get_right() + DOWN * 0.6)
        scale_g = VGroup(beam, panL, panR)
        self.play(FadeIn(fulcrum), Create(beam), FadeIn(panL), FadeIn(panR), run_time=1.0)
        # dao động
        self.play(Rotate(scale_g, -12 * DEGREES, about_point=fulcrum.get_top()), run_time=0.7)
        self.play(Rotate(scale_g, 24 * DEGREES, about_point=fulcrum.get_top()), run_time=1.0)
        self.play(Rotate(scale_g, -12 * DEGREES, about_point=fulcrum.get_top()), run_time=0.7)
        self.fill(s, d)

        # CÂU 06: đẩy bên này bên kia thiệt
        s, d = self.say("voice/s10f_06.mp3")
        self.play(Rotate(scale_g, -16 * DEGREES, about_point=fulcrum.get_top()), run_time=0.8)
        push = T("đẩy bên này — bên kia thiệt", size=24, color=YELLOW, weight=BOLD, vi=True
                 ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(push, shift=UP * 0.2), run_time=0.6)
        self.fill(s, d)
        self.wait(0.3)


# ============================================================
# CẢNH 7 — TỔNG KẾT -> HARDWARE
# ============================================================
class Slide10gOutro(VoiceScene):
    def construct(self):
        self.add(self.make_tag("Throughput", GREEN))
        # CÂU 01: 1 người đã khó
        s, d = self.say("voice/s10g_01.mp3")
        one = svg_icon("user", WHITE, height=1.3).move_to(UP * 1.6)
        one_lbl = T("1 người dùng — đã khó", size=22, color=WHITE, vi=True).next_to(one, DOWN, buff=0.25)
        self.play(FadeIn(one, scale=0.7), FadeIn(one_lbl), run_time=0.7)
        self.fill(s, d)

        # CÂU 02: hàng nghìn người còn khó hơn
        s, d = self.say("voice/s10g_02.mp3")
        crowd = VGroup(*[svg_icon("user", MUTED, height=0.5) for _ in range(24)]
                       ).arrange_in_grid(rows=3, cols=8, buff=0.3).move_to(UP * 1.5)
        crowd_lbl = T("hàng nghìn người — khó hơn nhiều", size=22, color=YELLOW, weight=BOLD,
                      vi=True).next_to(crowd, DOWN, buff=0.25)
        self.play(FadeOut(one_lbl), ReplacementTransform(VGroup(one), crowd),
                  FadeIn(crowd_lbl), run_time=1.1)
        self.fill(s, d)

        # CÂU 03: không chỉ "thêm GPU" -> mà TỔ CHỨC (hình, ít chữ)
        s, d = self.say("voice/s10g_03.mp3")
        self.play(FadeOut(VGroup(crowd, crowd_lbl)), run_time=0.4)
        # (a) "+ GPU" bị gạch chéo
        gpus = VGroup(*[svg_icon("cpu", MUTED, height=0.8) for _ in range(4)]
                      ).arrange(RIGHT, buff=0.25).move_to(UP * 1.7)
        plus = T("+", size=30, color=MUTED, weight=BOLD).next_to(gpus, LEFT, buff=0.2)
        gx = Cross(VGroup(plus, gpus), stroke_color=RED, stroke_width=8).scale(1.05)
        self.play(FadeIn(plus), LaggedStart(*[FadeIn(g, shift=RIGHT * 0.1) for g in gpus],
                  lag_ratio=0.1), run_time=0.8)
        self.play(Create(gx), run_time=0.6)
        # (b) thay vào đó: tổ chức -> bộ 3 icon nhỏ (1 từ mỗi cái)
        q_icon = VGroup(*[RoundedRectangle(width=w, height=0.16, corner_radius=0.04, stroke_width=0,
                          fill_color=WHITE, fill_opacity=0.6) for w in (1.0, 0.55, 1.3)]
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        g_icon = VGroup(*[Square(0.26, stroke_width=0, fill_color=GREEN, fill_opacity=0.6)
                          for _ in range(4)]).arrange_in_grid(rows=2, cols=2, buff=0.08)
        beam = Line(LEFT * 0.55, RIGHT * 0.55, color=WHITE, stroke_width=5).rotate(8 * DEGREES)
        ful = Triangle(color=WHITE, fill_opacity=1).scale(0.16).next_to(beam, DOWN, buff=-0.02)
        sc_icon = VGroup(beam, ful)
        m1 = VGroup(q_icon, T("request", size=17, color=WHITE, weight=BOLD, vi=True).next_to(
            q_icon, DOWN, buff=0.25))
        m2 = VGroup(g_icon, T("batch", size=17, color=GREEN, weight=BOLD, vi=True).next_to(
            g_icon, DOWN, buff=0.25))
        m3 = VGroup(sc_icon, T("cân bằng", size=17, color=YELLOW, weight=BOLD, vi=True).next_to(
            sc_icon, DOWN, buff=0.3))
        triad = VGroup(m1, m2, m3).arrange(RIGHT, buff=1.4).move_to(DOWN * 0.9)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in triad], lag_ratio=0.25),
                  run_time=1.5)
        self.fill(s, d)

        # CÂU 04: vẫn chạy trên phần cứng -> Hardware #4
        s, d = self.say("voice/s10g_04.mp3")
        self.play(FadeOut(VGroup(plus, gpus, gx, triad)), run_time=0.4)
        punch = T("Mở rộng quy mô = tổ chức thông minh,\nkhông chỉ là thêm phần cứng.",
                  size=28, color=WHITE, weight=BOLD, vi=True, line_spacing=0.9).move_to(UP * 0.6)
        self.play(Write(punch), run_time=1.3)
        self.play(punch.animate.set_color(GREEN), run_time=0.5)
        nxt = RoundedRectangle(width=3.2, height=0.95, corner_radius=0.15, stroke_color=TEAL,
                               fill_color=TEAL, fill_opacity=0.18)
        nxt.add(T("Hardware", size=24, color=WHITE, weight=BOLD).move_to(nxt))
        num4 = T("4", size=26, color=TEAL, weight=BOLD).next_to(nxt, UP, buff=0.12).shift(LEFT * 1.3)
        grp = VGroup(nxt, num4).to_edge(DOWN, buff=0.7)
        arr = Arrow(punch.get_bottom(), nxt.get_top(), color=TEAL, buff=0.25, stroke_width=5)
        self.play(GrowArrow(arr), FadeIn(grp, shift=UP * 0.2), run_time=1.0)
        self.play(Indicate(nxt, color=TEAL, scale_factor=1.1), run_time=0.7)
        self.fill(s, d)
        self.wait(0.4)
