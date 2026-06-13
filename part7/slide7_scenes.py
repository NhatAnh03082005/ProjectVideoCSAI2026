from manim import *
from mutagen.mp3 import MP3
import os

# ============================================================
# SLIDE 7 — VIGNETTE 5 YẾU TỐ (trừ Intro), THEME ĐỒNG BỘ + VOICE SYNC
# Dựa trên template/main_segoe_theme.py (font Segoe UI, bảng màu, audio sync).
#
# Render HD (chạy TỪ TRONG thư mục slide7_themed để voice/ đúng đường dẫn):
#   manim -qh slide7_scenes.py Slide7aLatency
#   manim -qh slide7_scenes.py Slide7bMemory
#   manim -qh slide7_scenes.py Slide7cThroughput
#   manim -qh slide7_scenes.py Slide7dHardware
#   manim -qh slide7_scenes.py Slide7eTradeoff
#   manim -qh slide7_scenes.py Slide7fOutro
# ============================================================

# ---------- THEME ----------
# Dùng Arial cho cả Anh + Việt: kerning sạch, đủ glyph tiếng Việt.
# (DejaVu Sans Bold cỡ nhỏ bị giãn chữ bất thường trong manim -> bỏ.)
FONT_VI = "Arial"
FONT_EN = "Arial"
BG = "#0f172a"

WHITE = "#e5e7eb"
MUTED = "#94a3b8"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"
# Hai màu bổ sung cho đủ 5 yếu tố (giữ đúng quy ước Slide 7).
TEAL = "#2dd4bf"      # Hardware
MAROON = "#e11d48"    # Accuracy–Efficiency

FILL_SOFT = 0.12
FILL_MEDIUM = 0.18
FILL_STRONG = 0.62

# Quy ước màu 5 yếu tố
C_LATENCY = RED
C_MEMORY = YELLOW
C_THROUGHPUT = GREEN
C_HARDWARE = TEAL
C_ACCURACY = MAROON

NAMES_5 = ["Latency", "Memory", "Throughput", "Hardware", "Accuracy/\nEfficiency"]
COLORS_5 = [C_LATENCY, C_MEMORY, C_THROUGHPUT, C_HARDWARE, C_ACCURACY]

config.background_color = BG


# ---------- HELPER ----------
# Render chữ ở cỡ LỚN (size*TEXT_SS) rồi thu nhỏ lại 1/TEXT_SS:
# ManimPango bố trí glyph ở cỡ nhỏ hay sinh "hở chữ" (vd "M odel") do làm tròn sub-pixel;
# tính layout ở cỡ lớn thì chính xác hơn, scale hình học xuống (Text là vector) vẫn sạch.
TEXT_SS = 4

def T(text, size=24, color=WHITE, weight=NORMAL, line_spacing=-1, vi=False):
    # HYBRID + số dùng Arial:
    #  - chữ tiếng Anh thuần (chỉ chữ cái ASCII) -> font MẶC ĐỊNH serif giống Slide7Intro
    #  - có dấu tiếng Việt / ký hiệu (ngoài ASCII), HOẶC có chữ SỐ -> Arial (dễ đọc, không vỡ dấu)
    #  - vi=True: ÉP Arial dù chuỗi thuần ASCII. Dùng cho TỪ tiếng Việt KHÔNG dấu
    #    (vd "nhanh") khi câu tiếng Việt được tách render TỪNG TỪ -> tránh 1 từ rơi về serif
    #    lạc lõng giữa các từ Arial.
    kwargs = dict(font_size=size * TEXT_SS, color=color, weight=weight, line_spacing=line_spacing)
    if vi or any(ord(ch) > 127 or ch.isdigit() for ch in text):
        kwargs["font"] = FONT_VI
    return Text(text, **kwargs).scale(1 / TEXT_SS)


def T_nokern(text, size=24, color=WHITE, weight=NORMAL, tracking=0.035):
    return T(text, size=size, color=color, weight=weight)


def audio_duration(path):
    if not os.path.exists(path):
        print(f"[WARNING] Không tìm thấy audio: {path}")
        return 0
    return MP3(path).info.length


class VoiceScene(Scene):
    """Scene cha: gói sẵn play_audio / wait_audio để mọi vignette đồng bộ giọng."""

    def play_audio(self, path):
        if os.path.exists(path):
            self.add_sound(path)
        else:
            print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path}")

    def wait_audio(self, path, visual_time):
        remaining = audio_duration(path) - visual_time
        if remaining > 0.05:
            self.wait(remaining)

    def hold_to_audio_end(self, path, tail=0.4):
        """Giữ cảnh đúng tới khi giọng đọc xong, dựa trên THỜI GIAN THẬT đã trôi
        (self.renderer.time) — không phải đoán visual_time. Tránh cắt audio / dư hình.
        Dùng kèm các updater/always_redraw để màn hình vẫn chuyển động trong lúc giữ."""
        elapsed = self.renderer.time
        remaining = audio_duration(path) - elapsed + tail
        if remaining > 0.05:
            self.wait(remaining)

    # ----- Đồng bộ "nói tới đâu, hiện tới đó" theo TỪNG CÂU -----
    def say(self, path):
        """Phát 1 câu, trả về (thời điểm bắt đầu, thời lượng câu)."""
        self.add_sound(path)
        return self.renderer.time, audio_duration(path)

    def fill(self, start, dur, pad=0.18):
        """Giữ cho hết câu hiện tại trước khi sang câu sau (khớp hình ↔ tiếng)."""
        rem = dur + pad - (self.renderer.time - start)
        if rem > 0.05:
            self.wait(rem)

    def make_node_label(self, name, color, vi=False):
        """Tên yếu tố nhỏ ở góc trên — neo người xem vào yếu tố đang nói."""
        chip = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.08,
                                stroke_color=color, fill_color=color, fill_opacity=1)
        label = T(name, size=22, color=color, weight=BOLD, vi=vi).next_to(chip, RIGHT, buff=0.18)
        g = VGroup(chip, label).to_corner(UL, buff=0.45)
        return g


# ============================================================
# 7A — LATENCY (đỏ): "màn hình im lặng"
# ============================================================
class Slide7aLatency(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Latency", C_LATENCY)
        self.add(tag)

        # ===== Dựng khung tĩnh (chưa hiện) =====
        phone = RoundedRectangle(width=4.2, height=4.9, corner_radius=0.35,
                                 stroke_color=MUTED, stroke_width=4).move_to(LEFT * 3.6 + UP * 0.25)
        notch = RoundedRectangle(width=1.1, height=0.18, corner_radius=0.09,
                                 stroke_width=0, fill_color=MUTED, fill_opacity=0.7
                                 ).next_to(phone.get_top(), DOWN, buff=0.12)
        user_b = RoundedRectangle(width=3.0, height=0.8, corner_radius=0.2, stroke_width=0,
                                  fill_color=BLUE, fill_opacity=0.85
                                  ).move_to(phone.get_top() + DOWN * 0.95 + RIGHT * 0.4)
        user_t = T("Tóm tắt bài báo này…", size=18, color="#0b1220").move_to(user_b)
        answer_box = RoundedRectangle(width=3.1, height=1.95, corner_radius=0.2,
                                      stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.08
                                      ).move_to(phone.get_center() + DOWN * 0.55 + LEFT * 0.2)

        sw_c = RIGHT * 3.4 + UP * 1.05
        ring = Circle(radius=1.0, color=MUTED, stroke_width=8).move_to(sw_c)
        clk = ValueTracker(0.0)   # đồng hồ điều khiển bằng tay → 0..8 trong lúc chờ, rồi giữ = TTFT

        def cc(frac):
            return interpolate_color(ManimColor(MUTED), ManimColor(RED), min(frac, 1))

        def hand_dir():
            a = clk.get_value() / 8 * TAU
            return np.array([np.sin(a), np.cos(a), 0])

        hand = always_redraw(lambda: Line(sw_c + 0.55 * hand_dir(), sw_c + 0.92 * hand_dir(),
                                          color=cc(clk.get_value() / 8), stroke_width=7))
        num = always_redraw(lambda: T(f"{clk.get_value():.1f}s", size=30,
                                      color=cc(clk.get_value() / 8), weight=BOLD
                                      ).move_to(sw_c + DOWN * 0.42))

        # Thanh latency dưới đáy
        bar_y = DOWN * 3.25
        bar_left = LEFT * 4.6
        ttft_w = 3.4
        track = Line(bar_left + bar_y, RIGHT * 4.6 + bar_y, stroke_color=MUTED, stroke_width=3)
        ttft_seg = Rectangle(width=ttft_w, height=0.34, fill_color=YELLOW, fill_opacity=0.9,
                             stroke_width=0).move_to(bar_left + bar_y + RIGHT * ttft_w / 2)
        ttft_lbl = T("TTFT", size=20, color=YELLOW, weight=BOLD, vi=True).next_to(ttft_seg, UP, buff=0.16)
        # TPOT × N: căn NGANG HÀNG với TTFT (cùng độ cao), nằm giữa vùng pip teal
        pip_mid_x = (bar_left + RIGHT * (ttft_w + 1.1))[0]
        tpot_lbl = T("TPOT × N", size=20, color=TEAL, weight=BOLD)
        tpot_lbl.move_to([pip_mid_x, ttft_lbl.get_y(), 0])

        # ===== CÂU 01: gõ prompt, gửi, màn hình im lặng =====
        s, d = self.say("voice/s7a_01.mp3")
        self.play(Create(phone), FadeIn(notch), run_time=1.0)
        self.play(FadeIn(user_b, shift=UP * 0.2), Write(user_t), run_time=1.1)
        dots = VGroup(*[Dot(radius=0.11, color=MUTED) for _ in range(3)]
                      ).arrange(RIGHT, buff=0.22).move_to(answer_box.get_center() + UP * 0.2)
        self.play(FadeIn(answer_box), FadeIn(dots), run_time=0.7)
        self.fill(s, d)

        # ===== CÂU 02: đồng hồ chạy, viền đỏ dần = "độ trễ" =====
        s, d = self.say("voice/s7a_02.mp3")
        self.play(Create(ring), run_time=0.6)
        self.add(hand, num)
        phone.add_updater(lambda m: m.set_stroke(cc(clk.get_value() / 8)))
        self.play(clk.animate.set_value(4.5),
                  dots.animate.set_opacity(0.3), run_time=max(d - 0.6, 1.0), rate_func=linear)
        self.fill(s, d)

        # ===== CÂU 03: hiện thanh latency, "gồm 2 phần" =====
        s, d = self.say("voice/s7a_03.mp3")
        boundary = bar_left + bar_y + RIGHT * ttft_w
        divider = DashedLine(boundary + UP * 0.45, boundary + DOWN * 0.45, color=WHITE, stroke_width=2)
        self.play(Create(track), run_time=0.6)
        self.play(clk.animate.set_value(8.0), run_time=max(d - 1.0, 1.0), rate_func=linear)
        self.play(FadeIn(divider), run_time=0.4)
        self.fill(s, d)

        # ===== CÂU 04: TTFT — token đầu tiên =====
        s, d = self.say("voice/s7a_04.mp3")
        phone.clear_updaters()
        first_w = T("Bài", size=20, color=WHITE, vi=True)
        first_w.move_to(answer_box.get_corner(UL) + RIGHT * (first_w.width / 2 + 0.25) + DOWN * 0.32)
        self.play(GrowFromEdge(ttft_seg, LEFT), FadeIn(ttft_lbl, shift=UP * 0.15), run_time=1.0)
        self.play(FadeOut(dots),
                  Flash(first_w.get_center(), color=GREEN, flash_radius=0.7),
                  FadeIn(first_w, scale=1.5), run_time=0.7)
        self.fill(s, d)

        # ===== CÂU 05: TTFT phụ thuộc prompt + prefill =====
        s, d = self.say("voice/s7a_05.mp3")
        prefill = Arrow(user_b.get_bottom(), first_w.get_top() + UP * 0.1,
                        color=YELLOW, stroke_width=4, buff=0.12)
        prefill_lbl = T("prefill", size=16, color=YELLOW).next_to(prefill, RIGHT, buff=0.1)
        self.play(Indicate(user_b, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.play(GrowArrow(prefill), FadeIn(prefill_lbl), run_time=0.9)
        self.fill(s, d)
        self.play(FadeOut(prefill), FadeOut(prefill_lbl), run_time=0.3)

        # ===== CÂU 06: TPOT — mỗi token tiếp theo =====
        s, d = self.say("voice/s7a_06.mp3")
        self.play(FadeIn(tpot_lbl, shift=UP * 0.15), run_time=0.6)
        pip0 = Rectangle(width=0.14, height=0.34, fill_color=TEAL, fill_opacity=0.9,
                         stroke_width=0).move_to(bar_left + bar_y + RIGHT * (ttft_w + 0.1))
        self.play(FadeIn(pip0, scale=0.6), run_time=0.5)
        self.fill(s, d)

        # ===== CÂU 07: stream các token còn lại (mỗi token = 1 pip) =====
        s, d = self.say("voice/s7a_07.mp3")
        words = ["báo", "đề", "xuất", "cách", "phục", "vụ", "nhanh", "và", "rẻ", "hơn"]
        # bố trí từ cuộn dòng trong answer_box, bắt đầu sau "Bài"
        x0 = first_w.get_right()[0] + 0.18
        y0 = first_w.get_center()[1]
        line_x, line_y = x0, y0
        right_lim = answer_box.get_right()[0] - 0.2
        word_mobs = []
        for w in words:
            m = T(w, size=20, color=WHITE, vi=True)
            if line_x + m.width > right_lim:
                line_x = answer_box.get_left()[0] + 0.25
                line_y -= 0.45
            m.move_to([line_x + m.width / 2, line_y, 0])
            line_x += m.width + 0.16
            word_mobs.append(m)
        pip_x = ttft_w + 0.1 + 0.17
        step = max((d - 0.2) / len(words), 0.28)
        for m in word_mobs:
            pip = Rectangle(width=0.14, height=0.34, fill_color=TEAL, fill_opacity=0.9,
                            stroke_width=0).move_to(bar_left + bar_y + RIGHT * (pip_x + 0.08))
            pip_x += 0.17
            self.play(FadeIn(m, shift=UP * 0.1), FadeIn(pip, scale=0.6), run_time=step)
        self.fill(s, d)

        # ===== CÂU 08: con số ví dụ — 8.0s & 50ms =====
        s, d = self.say("voice/s7a_08.mp3")
        n_ttft = T("8.0s", size=20, color=YELLOW, weight=BOLD).next_to(ttft_seg, DOWN, buff=0.18)
        # ≈ 50ms/token: căn NGANG HÀNG với "8.0s" (cùng độ cao dưới thanh), không sát pip teal
        callout = T("≈ 50 ms/token", size=18, color=TEAL, weight=BOLD)
        callout.move_to([pip_mid_x, n_ttft.get_y(), 0])
        self.play(FadeIn(n_ttft, shift=UP * 0.1), Indicate(ttft_seg, color=WHITE), run_time=0.9)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.8)
        self.fill(s, d)

        # ===== CÂU 09: tổng độ trễ = TTFT + TPOT × N =====
        s, d = self.say("voice/s7a_09.mp3")
        whole = SurroundingRectangle(VGroup(ttft_seg, *[track]), color=WHITE, buff=0.12)
        total_lbl = T("Tổng độ trễ = TTFT + TPOT × N", size=20, color=WHITE, weight=BOLD
                      ).next_to(track, UP, buff=0.9).shift(RIGHT * 1.0)
        self.play(Create(whole), run_time=0.8)
        self.play(FadeIn(total_lbl, shift=UP * 0.15), run_time=0.8)
        self.play(Indicate(num, color=RED, scale_factor=1.2), run_time=0.7)
        self.fill(s, d)

        # ===== CÂU 10: chuyển tiếp sang Memory (7B) =====
        s, d = self.say("voice/s7a_10.mp3")
        self.play(FadeOut(whole), Indicate(tag, color=RED, scale_factor=1.15), run_time=0.9)
        self.fill(s, d)


# ============================================================
# 7B — MEMORY / KV CACHE (vàng): "chiếc cốc tràn"
# ============================================================
class Slide7bMemory(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Memory", C_MEMORY)
        self.add(tag)

        # ===== Khung tĩnh: cốc "GPU Memory" =====
        bar_w, bar_h = 2.6, 5.4
        outline = Rectangle(width=bar_w, height=bar_h, stroke_color=WHITE, stroke_width=2)
        outline.move_to(LEFT * 3.4 + DOWN * 0.15)
        cap = T("GPU Memory", size=22, color=WHITE, weight=BOLD).next_to(outline, UP, buff=0.18)
        inner_w = bar_w - 0.1
        col_x = outline.get_center()[0]
        bottom_y = outline.get_bottom()[1]
        top_y = outline.get_top()[1]
        oom_y = top_y - 0.55
        oom = DashedLine([col_x - bar_w / 2, oom_y, 0], [col_x + bar_w / 2, oom_y, 0], color=RED)
        oom_lbl = T("OOM", size=18, color=RED, weight=BOLD).next_to(oom, RIGHT, buff=0.12)

        # ===== CÂU 01: trọng số chiếm phần lớn bộ nhớ =====
        s, d = self.say("voice/s7b_01.mp3")
        self.play(Create(outline), FadeIn(cap), run_time=1.0)
        w_h = 1.5
        weights = Rectangle(width=inner_w, height=w_h, fill_color=BLUE, fill_opacity=FILL_STRONG,
                            stroke_width=0).move_to([col_x, bottom_y + w_h / 2 + 0.05, 0])
        wtext = T("Model Weights", size=18, color=WHITE).move_to(weights)
        self.play(GrowFromEdge(weights, DOWN), Write(wtext), run_time=1.3)
        self.fill(s, d)

        # ===== CÂU 02: trọng số CỐ ĐỊNH =====
        s, d = self.say("voice/s7b_02.mp3")
        fixed = T("cố định", size=18, color=BLUE, weight=BOLD).next_to(weights, RIGHT, buff=0.5)
        self.play(Indicate(weights, color=WHITE, scale_factor=1.0), FadeIn(fixed, shift=LEFT * 0.2),
                  run_time=1.0)
        self.fill(s, d)

        # chuẩn bị tham số KV
        base_y = weights.get_top()[1]
        kv_h = 0.82
        kv_blocks = VGroup()
        avatars = VGroup()

        def add_user(idx, gb):
            """Một user kết nối -> 1 khối KV dâng lên."""
            av = VGroup(Circle(radius=0.24, color=YELLOW, fill_opacity=FILL_MEDIUM, stroke_color=YELLOW),
                        T(f"U{idx}", size=15, color=YELLOW))
            av.move_to(RIGHT * 1.8 + UP * (1.7 - (idx - 1) * 0.95))
            y = base_y + len(kv_blocks) * kv_h + kv_h / 2
            block = Rectangle(width=inner_w, height=kv_h, fill_color=YELLOW, fill_opacity=0.55,
                              stroke_color=BG, stroke_width=1).move_to([col_x, y, 0])
            # nhãn +N GB đặt cạnh avatar (nguồn) để KHÔNG bị đầu mũi tên (ở phía block) đè
            gbt = T(f"+{gb} GB", size=17, color=YELLOW, weight=BOLD).next_to(av, LEFT, buff=0.3)
            arrow = Arrow(av.get_left(), block.get_right(), buff=0.12, color=YELLOW, stroke_width=3)
            self.play(FadeIn(av, shift=LEFT * 0.3), run_time=0.4)
            self.play(GrowArrow(arrow), FadeIn(block, shift=UP * 0.2), FadeIn(gbt), run_time=0.7)
            self.play(FadeOut(arrow), FadeOut(gbt), run_time=0.25)
            kv_blocks.add(block)
            avatars.add(av)
            return block

        # ===== CÂU 03: user đầu -> KV cache xuất hiện =====
        s, d = self.say("voice/s7b_03.mp3")
        b1 = add_user(1, 4)
        kv_lbl = T("KV Cache", size=18, color=YELLOW, weight=BOLD).next_to(b1, LEFT, buff=0.3)
        self.play(FadeIn(kv_lbl, shift=RIGHT * 0.2), run_time=0.5)
        self.fill(s, d)

        # ===== CÂU 04: KV lưu key/value mỗi token =====
        s, d = self.say("voice/s7b_04.mp3")
        kvtag = VGroup(T("k", size=16, color=BG, weight=BOLD), T("v", size=16, color=BG, weight=BOLD)
                       ).arrange(RIGHT, buff=0.12).move_to(b1)
        # cụm minh hoạ dời hẳn sang phải, có mũi tên nối, để KHÔNG đè viền khung memory
        toks = VGroup(*[Square(0.12, color=YELLOW, fill_opacity=0.8, stroke_width=0) for _ in range(5)]
                      ).arrange(RIGHT, buff=0.08).next_to(b1, RIGHT, buff=1.7)
        tok_arrow = Arrow(b1.get_right(), toks.get_left(), buff=0.18, color=MUTED, stroke_width=2)
        tok_lbl = T("mỗi token → (k, v)", size=16, color=MUTED).next_to(toks, UP, buff=0.18)
        self.play(FadeIn(kvtag), GrowArrow(tok_arrow),
                  LaggedStart(*[FadeIn(t) for t in toks], lag_ratio=0.2),
                  FadeIn(tok_lbl), run_time=1.4)
        self.fill(s, d)
        self.play(FadeOut(toks), FadeOut(tok_lbl), FadeOut(kvtag), FadeOut(tok_arrow), run_time=0.3)

        # ===== CÂU 05: thêm user / hội thoại dài -> dâng cao =====
        s, d = self.say("voice/s7b_05.mp3")
        add_user(2, 8)
        add_user(3, 12)
        self.fill(s, d)

        # ===== CÂU 06: phình ~ tuyến tính =====
        s, d = self.say("voice/s7b_06.mp3")
        growth = Arrow([col_x + bar_w / 2 + 0.5, base_y, 0],
                       [col_x + bar_w / 2 + 0.5, kv_blocks.get_top()[1], 0],
                       color=ORANGE, buff=0.0, stroke_width=5)
        glbl = T("~ tuyến tính", size=18, color=ORANGE, weight=BOLD).next_to(growth, RIGHT, buff=0.15)
        self.play(GrowArrow(growth), FadeIn(glbl), run_time=1.0)
        self.fill(s, d)

        # ===== CÂU 07: chạm OOM =====
        s, d = self.say("voice/s7b_07.mp3")
        self.play(Create(oom), FadeIn(oom_lbl), run_time=0.7)
        b4 = add_user(4, 16)   # khối này chạm vạch OOM
        self.play(Flash(oom, color=RED, flash_radius=1.4),
                  kv_blocks.animate.set_color(RED), run_time=0.9)
        self.fill(s, d)

        # ===== CÂU 08: hết chỗ -> từ chối yêu cầu =====
        s, d = self.say("voice/s7b_08.mp3")
        reject = VGroup(Circle(radius=0.24, color=RED, fill_opacity=FILL_MEDIUM, stroke_color=RED),
                        T("U5", size=15, color=RED)).move_to(RIGHT * 1.8 + UP * (1.7 - 4 * 0.95))
        cross = Cross(reject, stroke_color=RED, stroke_width=5).scale(0.7)
        self.play(FadeIn(reject), run_time=0.4)
        self.play(Create(cross), Indicate(oom_lbl, color=RED, scale_factor=1.3), run_time=0.7)
        rej_lbl = T("từ chối request", size=18, color=RED, weight=BOLD).next_to(reject, DOWN, buff=0.3)
        self.play(FadeIn(rej_lbl, shift=UP * 0.1), run_time=0.5)
        self.fill(s, d)

        # ===== CÂU 09: chuyển tiếp sang Throughput (7C) =====
        s, d = self.say("voice/s7b_09.mp3")
        self.play(Indicate(VGroup(outline, kv_blocks), color=RED, scale_factor=1.03), run_time=1.0)
        self.play(Indicate(tag, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.fill(s, d)


# ============================================================
# 7C — THROUGHPUT (xanh lá): "băng chuyền / batch"
# ============================================================
class Slide7cThroughput(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Throughput", C_THROUGHPUT)
        self.add(tag)

        gpu = RoundedRectangle(width=1.8, height=3.0, corner_radius=0.18,
                               stroke_color=GREEN, fill_color=GREEN, fill_opacity=FILL_SOFT
                               ).move_to(RIGHT * 4.3 + DOWN * 0.1)
        gpu_lbl = T("GPU", size=24, color=GREEN, weight=BOLD).move_to(gpu)

        # ===== CÂU 01: hàng nghìn request + GPU =====
        s, d = self.say("voice/s7c_01.mp3")
        self.play(FadeIn(gpu), Write(gpu_lbl), run_time=0.8)
        widths = [0.7, 2.0, 1.3, 0.5, 1.6]
        rcols = [BLUE, PURPLE, ORANGE, YELLOW, TEAL]
        reqs = VGroup()
        for w, c in zip(widths, rcols):
            reqs.add(RoundedRectangle(width=w, height=0.42, corner_radius=0.08,
                                      stroke_color=c, fill_color=c, fill_opacity=0.6))
        reqs.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(LEFT * 4.3 + DOWN * 0.1)
        qlbl = T("requests", size=18, color=MUTED).next_to(reqs, UP, buff=0.25)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in reqs], lag_ratio=0.18),
                  FadeIn(qlbl), run_time=1.6)
        self.fill(s, d)

        # ===== Lưới batch (xây sẵn toạ độ) =====
        cols, rows, cell = 7, 5, 0.5
        gx0, gy0 = -2.0, 1.2
        lengths = [3, 7, 5, 2, 6]  # độ dài mỗi request (số ô)

        def cpos(r, c):
            return np.array([gx0 + c * cell, gy0 - r * cell, 0])

        # ===== CÂU 02: gom thành batch -> vào GPU, hiện lưới =====
        s, d = self.say("voice/s7c_02.mp3")
        bracket = SurroundingRectangle(reqs, color=GREEN, buff=0.18)
        blbl = T("1 batch", size=18, color=GREEN, weight=BOLD).next_to(bracket, UP, buff=0.15)
        self.play(Create(bracket), FadeIn(blbl), run_time=0.8)
        self.play(VGroup(reqs, bracket, blbl, qlbl).animate.move_to(gpu).scale(0.4).set_opacity(0),
                  run_time=0.9)
        filled, empties = VGroup(), []
        outline_cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(cell, stroke_color=MUTED, stroke_width=1, fill_opacity=0).move_to(cpos(r, c))
                outline_cells.add(sq)
        self.play(Create(outline_cells), run_time=1.0)
        self.fill(s, d)

        # ===== CÂU 03: request dài ngắn khác nhau (đổ ô xanh theo độ dài) =====
        s, d = self.say("voice/s7c_03.mp3")
        row_anims = []
        for r in range(rows):
            for c in range(lengths[r]):
                sq = Square(cell, stroke_color=BG, stroke_width=1,
                            fill_color=rcols[r], fill_opacity=0.75).move_to(cpos(r, c))
                filled.add(sq)
                row_anims.append(FadeIn(sq))
        self.play(LaggedStart(*row_anims, lag_ratio=0.03), run_time=1.6)
        long_start = sum(lengths[:1])          # hàng dài nhất là hàng index 1 (7 ô)
        self.play(Indicate(VGroup(*[filled[i] for i in range(long_start, long_start + lengths[1])]),
                           color=WHITE), run_time=0.7)
        self.fill(s, d)

        # ===== CÂU 04: ngắn xong sớm, chờ request dài nhất =====
        s, d = self.say("voice/s7c_04.mp3")
        sweep = Line(cpos(0, 0) + UP * cell / 2 + LEFT * cell / 2,
                     cpos(rows - 1, 0) + DOWN * cell / 2 + LEFT * cell / 2,
                     color=YELLOW, stroke_width=4)
        self.play(FadeIn(sweep), run_time=0.3)
        self.play(sweep.animate.shift(RIGHT * cols * cell), run_time=1.6, rate_func=linear)
        self.play(FadeOut(sweep), run_time=0.2)
        self.fill(s, d)

        # ===== CÂU 05: ô trống = lãng phí =====
        s, d = self.say("voice/s7c_05.mp3")
        waste = VGroup()
        for r in range(rows):
            for c in range(lengths[r], cols):
                sq = Square(cell, stroke_color=RED, stroke_width=2,
                            fill_color=RED, fill_opacity=0.18).move_to(cpos(r, c))
                waste.add(sq)
        wlbl = T("ô trống = GPU rảnh = lãng phí", size=19, color=RED, weight=BOLD
                 ).next_to(outline_cells, DOWN, buff=0.4)
        self.play(LaggedStartMap(FadeIn, waste, lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(wlbl, shift=UP * 0.1), run_time=0.6)
        self.fill(s, d)

        # ===== CÂU 06: xếp khéo -> lấp ô trống -> tokens/s tăng =====
        s, d = self.say("voice/s7c_06.mp3")
        thr = T("1200 tokens/s", size=26, color=GREEN, weight=BOLD).next_to(gpu, DOWN, buff=0.55)
        self.play(FadeIn(thr), run_time=0.5)
        fill_in = []
        for r in range(rows):
            for c in range(lengths[r], cols):
                sq = Square(cell, stroke_color=BG, stroke_width=1,
                            fill_color=GREEN, fill_opacity=0.75).move_to(cpos(r, c))
                fill_in.append(GrowFromCenter(sq))
        self.play(FadeOut(waste, run_time=0.3))
        self.play(LaggedStart(*fill_in, lag_ratio=0.04),
                  Transform(thr, T("3100 tokens/s", size=26, color=GREEN, weight=BOLD
                                   ).next_to(gpu, DOWN, buff=0.55)),
                  Indicate(thr, color=YELLOW), run_time=1.8)
        self.fill(s, d)

        # ===== CÂU 07: chuyển tiếp sang Hardware (7D) =====
        s, d = self.say("voice/s7c_07.mp3")
        self.play(FadeOut(wlbl), Indicate(tag, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.play(Indicate(gpu, color=TEAL, scale_factor=1.05), run_time=0.7)
        self.fill(s, d)


# ============================================================
# 7D — HARDWARE (teal): "một phích cắm, nhiều loại ổ"
# ============================================================
class Slide7dHardware(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Hardware", C_HARDWARE, vi=True)
        self.add(tag)

        plug = RoundedRectangle(width=2.2, height=1.0, corner_radius=0.15, stroke_color=TEAL,
                                fill_color=TEAL, fill_opacity=FILL_MEDIUM)
        # cỡ 30 (≥30): dưới ngưỡng này chữ nhỏ hay dính artifact hở "M odel" của ManimPango ở vài vị trí
        model = VGroup(plug, T("Model", size=30, color=WHITE, weight=BOLD, vi=True).move_to(plug)
                       ).to_edge(UP, buff=1.1)
        plats = [("NVIDIA", GREEN), ("AMD", ORANGE), ("TPU", BLUE),
                 ("CPU", MUTED), ("Mobile", PURPLE), ("Edge", YELLOW)]
        runtimes = ["CUDA", "ROCm", "XLA", "oneDNN", "NNAPI", "TFLite"]
        sockets = VGroup()
        for nm, c in plats:
            box = RoundedRectangle(width=1.7, height=1.0, corner_radius=0.12, stroke_color=c,
                                   fill_color=c, fill_opacity=FILL_SOFT)
            sockets.add(VGroup(box, T(nm, size=20, color=WHITE, vi=True).move_to(box)))
        sockets.arrange(RIGHT, buff=0.28).to_edge(DOWN, buff=1.5)

        # ===== CÂU 01: cùng model chạy nhiều phần cứng =====
        s, d = self.say("voice/s7d_01.mp3")
        # KHÔNG dùng shift= (nội suy vị trí VGroup chứa Text -> lệch glyph "M odel"); chỉ mờ dần.
        self.play(FadeIn(model), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.3) for m in sockets], lag_ratio=0.12),
                  run_time=1.4)
        self.fill(s, d)

        # ===== CÂU 02: liệt kê nền tảng (nhấn lần lượt) =====
        s, d = self.say("voice/s7d_02.mp3")
        self.play(LaggedStart(*[Indicate(sk, color=WHITE, scale_factor=1.1) for sk in sockets],
                              lag_ratio=0.25), run_time=2.0)
        self.fill(s, d)

        # ===== CÂU 03: NVIDIA khớp (CUDA), mỗi ổ một runtime =====
        s, d = self.say("voice/s7d_03.mp3")
        nv = sockets[0]
        # Dời bằng .animate.shift (tịnh tiến ĐỀU) thay vì .animate.next_to:
        # .animate.next_to nội suy từng-điểm trên VGroup chứa Text làm glyph bị lệch -> hở chữ
        # ("M odel"). shift một vector đều thì nội suy thuần tịnh tiến, không méo glyph.
        mv_tgt = model.copy().next_to(nv, UP, buff=0.5)
        self.play(model.animate.shift(mv_tgt.get_center() - model.get_center()), run_time=0.8)
        # dấu check VẼ bằng hình (không phụ thuộc glyph font ✓)
        ok = VMobject(stroke_color=GREEN, stroke_width=7)
        ok.set_points_as_corners([[-0.13, 0.02, 0], [-0.02, -0.15, 0], [0.2, 0.22, 0]])
        ok.next_to(nv, UP, buff=0.08).shift(RIGHT * 0.5)
        cuda = T("CUDA", size=20, color=GREEN, weight=BOLD, vi=True).next_to(nv, UP, buff=0.1).shift(LEFT * 0.4)
        self.play(nv[0].animate.set_fill(GREEN, opacity=0.4), Create(ok),
                  FadeIn(cuda), run_time=0.8)
        self.fill(s, d)

        # ===== CÂU 04: phải gắn runtime + biên dịch lại (ổ khác) =====
        s, d = self.say("voice/s7d_04.mp3")
        op = [None, 0.4, 0.3, 0.16, 0.26, 0.2]   # độ sáng khác nhau = hiệu năng khác nhau
        adapters = []
        for i in range(1, len(sockets)):
            # cỡ chữ ~16 để tránh artifact hở chữ ("RO Cm") khi rasterize ở cỡ quá nhỏ;
            # khung adapter tự co theo bề rộng nhãn.
            al = T(runtimes[i], size=20, color=YELLOW, weight=BOLD, vi=True)
            ad = RoundedRectangle(width=al.width + 0.28, height=0.46, corner_radius=0.08,
                                  stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.55
                                  ).next_to(sockets[i], UP, buff=0.1)
            al.move_to(ad)
            adapters.append(AnimationGroup(FadeIn(ad, shift=DOWN * 0.1), FadeIn(al),
                                           sockets[i][0].animate.set_fill(plats[i][1], opacity=op[i])))
        # cỡ ≥26 để tránh khoảng hở không đều giữa các âm tiết tiếng Việt khi bold ở cỡ nhỏ
        recompile = T("phải biên dịch/tối ưu lại", size=26, color=TEAL, weight=BOLD).move_to(UP * 0.2)
        self.play(FadeIn(recompile), run_time=0.5)
        self.play(LaggedStart(*adapters, lag_ratio=0.2), run_time=2.2)
        self.fill(s, d)

        # ===== CÂU 05: chốt — không hề đơn giản =====
        s, d = self.say("voice/s7d_05.mp3")
        msg = T("Không phải 'viết một lần, chạy mọi nơi'", size=26, color=TEAL, weight=BOLD).move_to(DOWN * 0.6)
        self.play(Transform(recompile, msg), run_time=0.7)
        self.play(Indicate(tag, color=TEAL, scale_factor=1.15), run_time=0.8)
        self.fill(s, d)


# ============================================================
# 7E — ACCURACY–EFFICIENCY (maroon): "cái cân / thanh trượt"
# ============================================================
class Slide7eTradeoff(VoiceScene):
    def construct(self):
        tag = self.make_node_label("Accuracy/Efficiency", C_ACCURACY)
        self.add(tag)

        pivot = Triangle(color=MUTED, fill_color=MUTED, fill_opacity=0.5).scale(0.5).move_to(DOWN * 1.7)
        beam = Line(LEFT * 3.2, RIGHT * 3.2, stroke_color=WHITE, stroke_width=6).next_to(pivot, UP, buff=0.0)

        def pan(text, color):
            plate = Arc(radius=0.95, start_angle=PI, angle=PI, color=color, stroke_width=4)
            lbl = T(text, size=20, color=color, weight=BOLD).next_to(plate, DOWN, buff=0.12)
            return VGroup(plate, lbl)

        left = pan("Chất lượng", MAROON).move_to(beam.get_left() + DOWN * 0.6)
        right = pan("Tốc độ + Chi phí", GREEN).move_to(beam.get_right() + DOWN * 0.6)
        scale_group = VGroup(beam, left, right)

        # ===== CÂU 01: có kỹ thuật giúp nhanh + rẻ =====
        s, d = self.say("voice/s7e_01.mp3")
        self.play(Create(pivot), Create(beam), run_time=0.8)
        self.play(FadeIn(left, shift=DOWN * 0.2), FadeIn(right, shift=DOWN * 0.2), run_time=0.9)
        acc = T("accuracy 92%", size=26, color=MAROON, weight=BOLD).to_corner(UL, buff=0.9).shift(RIGHT * 1.6)
        self.play(Write(acc), run_time=0.6)
        self.fill(s, d)

        # ===== CÂU 02: quantize / prune / distill =====
        s, d = self.say("voice/s7e_02.mp3")
        chips = VGroup(
            *[RoundedRectangle(width=2.0, height=0.55, corner_radius=0.12, stroke_color=GREEN,
                               fill_color=GREEN, fill_opacity=0.18) for _ in range(3)])
        names = ["Quantize", "Prune", "Distill"]
        chip_g = VGroup()
        for ch, nm in zip(chips, names):
            chip_g.add(VGroup(ch, T(nm, size=18, color=WHITE, weight=BOLD).move_to(ch)))
        chip_g.arrange(DOWN, buff=0.2).to_corner(UR, buff=0.7)
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.3) for m in chip_g], lag_ratio=0.2),
                  run_time=1.4)
        self.fill(s, d)

        # ===== CÂU 03: không có bữa trưa miễn phí =====
        s, d = self.say("voice/s7e_03.mp3")
        nfl = T("không có bữa trưa miễn phí", size=22, color=YELLOW, weight=BOLD).move_to(UP * 1.2)
        self.play(FadeIn(nfl, scale=1.1), run_time=0.8)
        self.fill(s, d)

        # ===== CÂU 04: nén -> chất lượng giảm (cân nghiêng) =====
        s, d = self.say("voice/s7e_04.mp3")
        weight = T("nén", size=20, color=GREEN, weight=BOLD).move_to(right[0].get_center() + UP * 0.15)
        self.play(chip_g.animate.scale(0.5).move_to(right[0].get_center() + UP * 0.1).set_opacity(0.0),
                  FadeIn(weight), run_time=0.9)
        self.play(Rotate(scale_group, angle=-20 * DEGREES, about_point=pivot.get_top()),
                  weight.animate.shift(DOWN * 0.5 + RIGHT * 0.1), run_time=1.2)
        self.fill(s, d)

        # ===== CÂU 05: accuracy 92 -> 88 =====
        s, d = self.say("voice/s7e_05.mp3")
        self.play(Transform(acc, T("accuracy 92% → 88%", size=26, color=ORANGE, weight=BOLD
                                    ).to_corner(UL, buff=0.9).shift(RIGHT * 2.0)), run_time=0.9)
        self.play(Indicate(acc, color=RED, scale_factor=1.2), run_time=0.7)
        self.fill(s, d)

        # ===== CÂU 06: chuyển tiếp — gộp lại 5 thách thức (dẫn sang Outro 7F) =====
        s, d = self.say("voice/s7e_06.mp3")
        self.play(FadeOut(VGroup(scale_group, pivot, weight, nfl, acc)), run_time=0.6)
        recap_names = ["Latency", "Memory", "Throughput", "Hardware", "Trade-off"]
        recap_cols = [C_LATENCY, C_MEMORY, C_THROUGHPUT, C_HARDWARE, C_ACCURACY]
        chips5 = VGroup()
        for nm, c in zip(recap_names, recap_cols):
            b = RoundedRectangle(width=2.1, height=0.75, corner_radius=0.12, stroke_color=c,
                                 fill_color=c, fill_opacity=0.85)
            chips5.add(VGroup(b, T(nm, size=18, color=(BG if c == YELLOW else WHITE),
                                   weight=BOLD).move_to(b)))
        chips5.arrange(RIGHT, buff=0.28)
        if chips5.width > 13:
            chips5.scale_to_fit_width(13)
        chips5.move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips5], lag_ratio=0.25),
                  run_time=2.2)
        self.play(Indicate(chips5, color=WHITE, scale_factor=1.03), run_time=0.7)
        self.fill(s, d)


# ============================================================
# 7F — OUTRO: ghép lại "bản đồ bottleneck", đẩy về node Latency
# ============================================================
class Slide7fOutro(VoiceScene):
    def construct(self):
        audio = "voice/s7f_outro.mp3"
        self.play_audio(audio)

        # LLM Server ở giữa
        server = RoundedRectangle(width=3.0, height=1.5, corner_radius=0.2,
                                  stroke_color=BLUE, fill_color=BLUE, fill_opacity=FILL_MEDIUM)
        server_lbl = T("LLM Server", size=30, color=WHITE, weight=BOLD).move_to(server)
        server_group = VGroup(server, server_lbl)
        self.play(FadeIn(server_group, scale=0.85), run_time=0.8)

        # 5 node quanh server
        nodes = VGroup()
        arrows = VGroup()
        rx, ry = 4.6, 2.7
        for i, (nm, col) in enumerate(zip(NAMES_5, COLORS_5)):
            angle = TAU / 5 * i + PI / 2
            pos = np.array([rx * np.cos(angle), ry * np.sin(angle), 0])
            box = RoundedRectangle(width=2.3, height=1.05, corner_radius=0.15,
                                   stroke_color=col, fill_color=col, fill_opacity=0.85)
            lbl_color = BG if col == YELLOW else WHITE
            node = VGroup(box, T(nm, size=22, color=lbl_color, weight=BOLD).move_to(box)).move_to(pos)
            nodes.add(node)
            d = pos - server.get_center()
            d = d / np.linalg.norm(d)
            arrows.add(Arrow(server.get_boundary_point(d), box.get_boundary_point(-d),
                             buff=0.12, stroke_width=4, color=col))

        self.play(LaggedStart(*[FadeIn(n, scale=0.8) for n in nodes], lag_ratio=0.12),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=2.0)

        # 5 node + mũi tên cùng nhấp nháy
        title = T("5 bottleneck của LLM Serving", size=30, color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2),
                  *[Indicate(a, color=YELLOW) for a in arrows], run_time=1.2)
        self.wait(0.5)

        # Đẩy nhẹ về node Latency (đỏ) để nối sang Slide 8
        latency_node = nodes[0]
        rest = VGroup(*nodes[1:], *arrows[:], server_group, title)
        self.play(FadeOut(rest), run_time=0.8)
        self.play(latency_node.animate.move_to(ORIGIN).scale(1.8), run_time=1.0)

        self.wait_audio(audio, visual_time=9.0)
        self.play(FadeOut(latency_node), run_time=0.6)
