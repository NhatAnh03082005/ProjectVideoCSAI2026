from manim import *
from pathlib import Path
import json
import subprocess

# ============================================================
# PART 4 - SYSTEM OPTIMIZATIONS
# SCENE 21 - KERNEL OPTIMIZATION: FUSION / FLASHATTENTION / COMPILATION
#
# Render test:
#   py -m manim -pql --disable_caching main_p4_21.py Part4KernelOptimization
#
# Render dep:
#   py -m manim -pqh --disable_caching main_p4_21.py Part4KernelOptimization
# ============================================================

FONT = None
VIETNAMESE_FONT = "Arial"
VIETNAMESE_CHARS = (
    "ăâđêôơư"
    "ĂÂĐÊÔƠƯ"
    "áàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩị"
    "óòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
    "ÁÀẢÃẠẤẦẨẪẬẮẰẲẴẶÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊ"
    "ÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ"
)
BG = "#0f172a"
WHITE_C = "#e5e7eb"
MUTED = "#94a3b8"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"
TEAL = "#2dd4bf"
GRAY = "#64748b"
FILL_SOFT = 0.12
FILL_MEDIUM = 0.22
config.background_color = BG


def text_font_for(text):
    return VIETNAMESE_FONT if any(ch in VIETNAMESE_CHARS for ch in str(text)) else FONT

try:
    from mutagen.mp3 import MP3
except Exception:
    MP3 = None

FALLBACK_SCENE_DURATIONS = {
    "voice/p4_21_01_intro.mp3": 20.0,
    "voice/p4_21_02_hbm_sram.mp3": 20.0,
    "voice/p4_21_03_fusion.mp3": 20.0,
    "voice/p4_21_04_prefill_attention.mp3": 20.0,
    "voice/p4_21_05_flashattention.mp3": 20.0,
    "voice/p4_21_06_decode_attention.mp3": 20.0,
    "voice/p4_21_07_variable_length.mp3": 20.0,
    "voice/p4_21_08_compilation.mp3": 20.0,
    "voice/p4_21_09_summary.mp3": 20.0,
}
CURRENT_SCALE = 1.0
TAIL_HOLD = 3.0

BASE_ANIMATION_DURATIONS = {
    "voice/p4_21_01_intro.mp3": 6.2,
    "voice/p4_21_02_hbm_sram.mp3": 6.2,
    "voice/p4_21_03_fusion.mp3": 6.4,
    "voice/p4_21_04_prefill_attention.mp3": 6.0,
    "voice/p4_21_05_flashattention.mp3": 6.6,
    "voice/p4_21_06_decode_attention.mp3": 6.3,
    "voice/p4_21_07_variable_length.mp3": 6.1,
    "voice/p4_21_08_compilation.mp3": 6.2,
    "voice/p4_21_09_summary.mp3": 6.0,
}


def get_mp3_duration_no_dependency(audio_path: str):
    try:
        data = Path(audio_path).read_bytes()
    except Exception:
        return None
    i = 0
    if len(data) > 10 and data[0:3] == b"ID3":
        size = (((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14) | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F))
        i = 10 + size
    bitrate_table = {
        ("1", "I"): [0,32,64,96,128,160,192,224,256,288,320,352,384,416,448],
        ("1", "II"): [0,32,48,56,64,80,96,112,128,160,192,224,256,320,384],
        ("1", "III"): [0,32,40,48,56,64,80,96,112,128,160,192,224,256,320],
        ("2", "I"): [0,32,48,56,64,80,96,112,128,144,160,176,192,224,256],
        ("2", "II"): [0,8,16,24,32,40,48,56,64,80,96,112,128,144,160],
        ("2", "III"): [0,8,16,24,32,40,48,56,64,80,96,112,128,144,160],
        ("2.5", "I"): [0,32,48,56,64,80,96,112,128,144,160,176,192,224,256],
        ("2.5", "II"): [0,8,16,24,32,40,48,56,64,80,96,112,128,144,160],
        ("2.5", "III"): [0,8,16,24,32,40,48,56,64,80,96,112,128,144,160],
    }
    sr_table = {"1": [44100,48000,32000], "2": [22050,24000,16000], "2.5": [11025,12000,8000]}
    version_map = {0b11: "1", 0b10: "2", 0b00: "2.5"}
    layer_map = {0b11: "I", 0b10: "II", 0b01: "III"}
    total = 0.0
    frames = 0
    n = len(data)
    while i + 4 <= n:
        if data[i] != 0xFF or (data[i + 1] & 0xE0) != 0xE0:
            i += 1
            continue
        header = int.from_bytes(data[i:i+4], "big")
        vb = (header >> 19) & 0b11
        lb = (header >> 17) & 0b11
        bi = (header >> 12) & 0b1111
        si = (header >> 10) & 0b11
        pad = (header >> 9) & 0b1
        if vb == 0b01 or lb == 0 or bi == 0 or bi == 0b1111 or si == 0b11:
            i += 1
            continue
        ver = version_map.get(vb)
        layer = layer_map.get(lb)
        if ver is None or layer is None:
            i += 1
            continue
        bitrate = bitrate_table[(ver, layer)][bi] * 1000
        sr = sr_table[ver][si]
        if layer == "I":
            frame_len = int((12 * bitrate / sr + pad) * 4)
            samples = 384
        elif layer == "III" and ver != "1":
            frame_len = int(72 * bitrate / sr + pad)
            samples = 576
        else:
            frame_len = int(144 * bitrate / sr + pad)
            samples = 1152
        if frame_len <= 0:
            i += 1
            continue
        total += samples / sr
        frames += 1
        i += frame_len
    return total if frames > 3 and total > 0 else None


def get_audio_duration(audio_path: str, fallback: float) -> float:
    path = Path(audio_path)
    if not path.exists():
        print(f"[WARN] Missing audio: {audio_path}. Using fallback {fallback:.2f}s")
        return fallback
    if MP3 is not None:
        try:
            return float(MP3(str(path)).info.length)
        except Exception:
            pass
    try:
        result = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)], capture_output=True, text=True, check=True)
        return float(json.loads(result.stdout)["format"]["duration"])
    except Exception:
        pass
    duration = get_mp3_duration_no_dependency(audio_path)
    return duration if duration is not None else fallback


def set_scene_timing(audio_path: str) -> float:
    global CURRENT_SCALE
    fallback = FALLBACK_SCENE_DURATIONS[audio_path]
    real = get_audio_duration(audio_path, fallback)
    base_anim = BASE_ANIMATION_DURATIONS.get(audio_path)
    if base_anim:
        CURRENT_SCALE = max((real - TAIL_HOLD) / base_anim, 0.25)
    else:
        CURRENT_SCALE = real / fallback
    print(f"[AUDIO] {audio_path}: {real:.2f}s | anim_scale={CURRENT_SCALE:.3f}")
    return real


def t(seconds: float) -> float:
    return seconds * CURRENT_SCALE


def T(text, size=28, color=WHITE_C, weight=NORMAL, **kwargs):
    if "line_spacing" not in kwargs and "\n" in text:
        kwargs["line_spacing"] = 0.75
    render_weight = SEMIBOLD if weight == BOLD else weight
    text_kwargs = dict(font_size=size, color=color, weight=render_weight, **kwargs)
    selected_font = text_font_for(text)
    if selected_font:
        text_kwargs["font"] = selected_font
    return Text(text, **text_kwargs)


def title_text(text, sub=None):
    title = T(text, size=40, color=WHITE_C, weight=BOLD)
    title.to_edge(UP, buff=0.34)
    if sub:
        subtitle = T(sub, size=23, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.10)
        return VGroup(title, subtitle)
    return title


def chip(text, color=BLUE, size=18, width=None, height=None, fill=FILL_SOFT):
    label = T(text, size=size, color=WHITE_C)
    box = RoundedRectangle(
        width=width if width else label.width + 0.52,
        height=height if height else label.height + 0.26,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=fill,
    )
    if label.width > box.width - 0.34:
        label.scale_to_fit_width(box.width - 0.34)
    if label.height > box.height - 0.16:
        label.scale_to_fit_height(box.height - 0.16)
    label.move_to(box)
    return VGroup(box, label)


def block(label="", color=BLUE, width=0.48, height=0.36, fill=FILL_MEDIUM, size=12, stroke=1.6):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.055,
        stroke_color=color,
        stroke_width=stroke,
        fill_color=color,
        fill_opacity=fill,
    )
    if not label:
        return VGroup(box)
    text = T(label, size=size, color=WHITE_C, weight=BOLD)
    if text.width > box.width - 0.08:
        text.scale_to_fit_width(box.width - 0.08)
    if text.height > box.height - 0.06:
        text.scale_to_fit_height(box.height - 0.06)
    text.move_to(box)
    return VGroup(box, text)


def bar(label, width, color, height=0.42, size=15, fill=FILL_MEDIUM):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.08, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill)
    text = T(label, size=size, color=WHITE_C, weight=BOLD)
    if text.width > box.width - 0.18:
        text.scale_to_fit_width(box.width - 0.18)
    if text.height > box.height - 0.08:
        text.scale_to_fit_height(box.height - 0.08)
    text.move_to(box)
    return VGroup(box, text)


def arrow(a, b, color=MUTED, width=3):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def gpu_chip(label="GPU", color=BLUE, width=1.70, height=1.00):
    body = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.10)
    pins = VGroup()
    for i in range(5):
        pins.add(Line(UP*0.06, DOWN*0.06, color=color, stroke_width=2).move_to(body.get_left()+RIGHT*0.08+UP*(0.28-i*0.14)))
        pins.add(Line(UP*0.06, DOWN*0.06, color=color, stroke_width=2).move_to(body.get_right()+LEFT*0.08+UP*(0.28-i*0.14)))
    text = T(label, 18, WHITE_C, BOLD).move_to(body)
    return VGroup(body, pins, text)


def matrix_grid(rows=6, cols=6, cell=0.28, colors=None):
    group = VGroup()
    for r in range(rows):
        for c in range(cols):
            color = colors(r, c) if colors else BLUE
            group.add(Square(side_length=cell, stroke_color=color, stroke_width=1.4, fill_color=color, fill_opacity=0.12))
    group.arrange_in_grid(rows=rows, cols=cols, buff=0.02)
    return group


def mini_cross(color=RED, scale=1.0):
    x = VGroup(
        Line(LEFT*0.20+UP*0.20, RIGHT*0.20+DOWN*0.20, color=color, stroke_width=6),
        Line(LEFT*0.20+DOWN*0.20, RIGHT*0.20+UP*0.20, color=color, stroke_width=6),
    )
    x.scale(scale)
    return x


class Part4KernelOptimization(Scene):
    def fade_clear(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.35)

    def start_audio_scene(self, audio_path):
        self._audio_scene_start = self.time
        self._audio_scene_duration = set_scene_timing(audio_path)
        path = Path(audio_path).resolve()
        if path.exists():
            self.renderer.file_writer.add_sound(str(path), time=self.time)

    def finish_audio_scene(self, pad=0.12):
        start = getattr(self, "_audio_scene_start", self.time)
        duration = getattr(self, "_audio_scene_duration", 0)
        remaining = start + duration + pad - self.time
        if remaining > 0.04:
            self.wait(remaining)

    def construct(self):
        self.camera.background_color = BG
        self.scene_21_01_intro()
        self.scene_21_02_hbm_sram()
        self.scene_21_03_fusion()
        self.scene_21_04_prefill_attention()
        self.scene_21_05_flashattention()
        self.scene_21_06_decode_attention()
        self.scene_21_07_variable_length()
        self.scene_21_08_compilation()
        self.scene_21_09_summary()

    def scene_21_01_intro(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_01_intro.mp3")
        title = title_text("Kernel Optimization")
        stack = VGroup(
            chip("Algorithm", PURPLE, 20, 2.35, 0.55, 0.10),
            chip("Serving System", GREEN, 20, 2.35, 0.55, 0.10),
            chip("Kernel", YELLOW, 22, 2.35, 0.62, 0.18),
            chip("Hardware", BLUE, 20, 2.35, 0.55, 0.10),
        ).arrange(DOWN, buff=0.12).move_to(LEFT*3.50+DOWN*0.10)
        focus = SurroundingRectangle(stack[2], color=YELLOW, buff=0.08, corner_radius=0.08)
        gpu = gpu_chip("GPU", BLUE, 3.55, 1.42).move_to(RIGHT*2.55+DOWN*0.10)
        gpu[2].set_opacity(0)
        gpu_label = T("GPU kernels", 16, BLUE, BOLD).next_to(gpu, UP, buff=0.12)
        kernels = VGroup(
            block("matmul", ORANGE, 0.95, 0.42, 0.25, 12),
            block("norm", GREEN, 0.86, 0.42, 0.25, 12),
            block("attn", PURPLE, 0.86, 0.42, 0.25, 12),
        ).arrange(RIGHT, buff=0.16).move_to(gpu)
        question = chip("data movement?", TEAL, 20, 3.15, 0.58, 0.13).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT*0.15) for s in stack], lag_ratio=0.12), run_time=t(1.4))
        self.play(Create(focus), stack.animate.shift(LEFT*0.25), run_time=t(0.9))
        self.play(FadeIn(gpu, shift=LEFT), FadeIn(gpu_label, shift=LEFT), Create(arrow(stack[2].get_right(), gpu.get_left(), YELLOW)), run_time=t(1.1))
        self.play(LaggedStart(*[FadeIn(k, scale=1.05) for k in kernels], lag_ratio=0.12), run_time=t(1.1))
        self.play(FadeIn(question, shift=UP), Flash(kernels, color=YELLOW), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_21_02_hbm_sram(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_02_hbm_sram.mp3")
        title = title_text("HBM vs SRAM")
        hbm = RoundedRectangle(width=2.65, height=2.95, corner_radius=0.16, stroke_color=BLUE, stroke_width=2.6, fill_color=BLUE, fill_opacity=0.08).move_to(LEFT*3.65+DOWN*0.10)
        hbm_label = T("HBM\nlarge / slower", 22, BLUE, BOLD).move_to(hbm)
        sram = RoundedRectangle(width=2.15, height=1.25, corner_radius=0.14, stroke_color=GREEN, stroke_width=2.6, fill_color=GREEN, fill_opacity=0.12).move_to(RIGHT*1.15+UP*0.60)
        sram_label = T("SRAM\nsmall / fast", 20, GREEN, BOLD).move_to(sram.get_center()+UP*0.13)
        core = gpu_chip("Compute", ORANGE, 1.75, 0.90).move_to(RIGHT*3.90+UP*0.45)
        data = VGroup(*[block("", YELLOW, 0.26, 0.22, 0.34) for _ in range(8)]).arrange(RIGHT, buff=0.04).move_to(LEFT*3.65+DOWN*1.25)
        sram_data_pos = sram.get_bottom()+UP*0.22
        arrows = VGroup(
            arrow(hbm.get_right()+DOWN*0.18, sram.get_left()+DOWN*0.28, YELLOW, 3.2),
            arrow(sram.get_right(), core.get_left(), GREEN, 3.2),
            CurvedArrow(core.get_bottom()+LEFT*0.20, hbm.get_right()+DOWN*0.98, angle=-PI/5, color=RED, stroke_width=3.2),
        )
        bottleneck = chip("memory movement matters", RED, 21, 4.25, 0.58, 0.14).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(hbm), FadeIn(hbm_label), FadeIn(data), run_time=t(1.0))
        self.play(FadeIn(sram), FadeIn(sram_label), FadeIn(core), run_time=t(1.0))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.18), run_time=t(1.5))
        self.play(data.animate.move_to(sram_data_pos), Flash(sram, color=GREEN), run_time=t(1.0))
        self.play(FadeIn(bottleneck, shift=UP), Circumscribe(arrows[2], color=RED), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_21_03_fusion(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_03_fusion.mp3")
        title = title_text("Kernel Fusion")
        before_title = T("Before", 24, RED, BOLD).move_to(LEFT*3.25+UP*1.65)
        after_title = T("After", 24, GREEN, BOLD).move_to(RIGHT*3.25+UP*1.65)
        before = VGroup(
            chip("Bias", ORANGE, 17, 1.05, 0.46, 0.14),
            chip("HBM", BLUE, 17, 0.95, 0.46, 0.10),
            chip("Act", PURPLE, 17, 1.05, 0.46, 0.14),
            chip("HBM", BLUE, 17, 0.95, 0.46, 0.10),
            chip("Residual", TEAL, 15, 1.20, 0.46, 0.14),
        ).arrange(RIGHT, buff=0.16).scale(0.88).move_to(LEFT*3.25+UP*0.35)
        before_arrows = VGroup(*[arrow(before[i].get_right(), before[i+1].get_left(), MUTED, 2.2) for i in range(len(before)-1)])
        fused = RoundedRectangle(width=3.55, height=1.08, corner_radius=0.16, stroke_color=GREEN, stroke_width=2.6, fill_color=GREEN, fill_opacity=0.13).move_to(RIGHT*3.25+UP*0.35)
        fused_label = T("Fused Kernel\nBias + Act + Residual", 19, WHITE_C, BOLD).move_to(fused)
        hbm_once = chip("write once to HBM", BLUE, 17, 2.20, 0.48, 0.10).next_to(fused, DOWN, buff=0.38)
        note = chip("less launch + less memory traffic", YELLOW, 20, 5.25, 0.55, 0.12).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(before_title), FadeIn(after_title), run_time=t(0.6))
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.10) for b in before], lag_ratio=0.10), LaggedStart(*[Create(a) for a in before_arrows], lag_ratio=0.10), run_time=t(1.7))
        self.play(FadeIn(fused), FadeIn(fused_label), run_time=t(1.0))
        self.play(Create(arrow(fused.get_bottom(), hbm_once.get_top(), GREEN)), FadeIn(hbm_once, shift=UP), run_time=t(1.0))
        self.play(FadeIn(note, shift=UP), Flash(before[1], color=RED), Flash(before[3], color=RED), Circumscribe(fused, color=GREEN), run_time=t(1.5))
        self.finish_audio_scene()

    def scene_21_04_prefill_attention(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_04_prefill_attention.mp3")
        title = title_text("Prefill Attention")
        small = matrix_grid(4, 4, 0.22).move_to(LEFT*2.65+UP*0.25)
        big = matrix_grid(9, 9, 0.18, lambda r, c: ORANGE if c <= r else BLUE).move_to(LEFT*0.60+UP*0.10)
        axes = VGroup(
            T("tokens", 17, MUTED).next_to(big, LEFT, buff=0.20).rotate(PI/2),
            T("tokens", 17, MUTED).next_to(big, UP, buff=0.14),
            T("L x L", 29, YELLOW, BOLD).next_to(big, RIGHT, buff=0.35),
        )
        hbm_frame = RoundedRectangle(width=1.10, height=2.75, corner_radius=0.12, stroke_color=BLUE, stroke_width=2.3, fill_color=BLUE, fill_opacity=0.05).move_to(RIGHT*3.90+UP*0.05)
        hbm_fill = Rectangle(width=0.86, height=0.62, fill_color=RED, fill_opacity=0.35, stroke_width=0).align_to(hbm_frame, DOWN).move_to([hbm_frame.get_center()[0], hbm_frame.get_bottom()[1]+0.31, 0])
        hbm_label = T("HBM", 19, BLUE, BOLD).next_to(hbm_frame, UP, buff=0.12)
        question = chip("Can we avoid storing it?", GREEN, 22, 4.35, 0.60, 0.13).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(small), run_time=t(0.8))
        self.play(ReplacementTransform(small, big), FadeIn(axes), run_time=t(1.4))
        self.play(FadeIn(hbm_frame), FadeIn(hbm_label), run_time=t(0.7))
        self.play(GrowFromEdge(hbm_fill, DOWN), Flash(big, color=RED), run_time=t(1.3))
        hbm_fill_big = Rectangle(width=0.86, height=2.35, fill_color=RED, fill_opacity=0.42, stroke_width=0).align_to(hbm_frame, DOWN).move_to([hbm_frame.get_center()[0], hbm_frame.get_bottom()[1]+1.175, 0])
        self.play(Transform(hbm_fill, hbm_fill_big), FadeIn(question, shift=UP), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_21_05_flashattention(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_05_flashattention.mp3")
        title = title_text("FlashAttention", "tile + online softmax")
        mat = matrix_grid(8, 8, 0.20, lambda r, c: ORANGE if (r//2 + c//2) % 2 == 0 else BLUE).move_to(LEFT*3.40+UP*0.25)
        mat_label = T("attention matrix", 18, MUTED).next_to(mat, UP, buff=0.16)
        tile = SurroundingRectangle(VGroup(*[mat[i] for i in [18, 19, 26, 27]]), color=YELLOW, buff=0.02, corner_radius=0.03)
        sram = chip("SRAM tile", GREEN, 20, 1.85, 0.72, 0.15).move_to(ORIGIN+UP*0.65)
        core = gpu_chip("Compute", ORANGE, 1.65, 0.86).move_to(RIGHT*2.35+UP*0.65)
        acc = chip("Output\naccumulator", TEAL, 18, 2.05, 0.78, 0.14).move_to(RIGHT*2.35+DOWN*0.75)
        no_full = chip("no full attention matrix in HBM", RED, 20, 4.90, 0.56, 0.13).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(mat_label), LaggedStart(*[FadeIn(c) for c in mat], lag_ratio=0.01), run_time=t(1.4))
        self.play(Create(tile), run_time=t(0.6))
        tile_copy = VGroup(*[block("", YELLOW, 0.24, 0.24, 0.35) for _ in range(4)]).arrange_in_grid(rows=2, cols=2, buff=0.04).move_to(tile)
        self.play(TransformFromCopy(tile, tile_copy), tile_copy.animate.move_to(sram), FadeIn(sram), run_time=t(1.1))
        self.play(Create(arrow(sram.get_right(), core.get_left(), GREEN)), FadeIn(core), run_time=t(0.9))
        self.play(Create(arrow(core.get_bottom(), acc.get_top(), TEAL)), FadeIn(acc, shift=UP), Flash(acc, color=TEAL), run_time=t(1.1))
        self.play(FadeIn(no_full, shift=UP), Circumscribe(mat, color=RED), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_21_06_decode_attention(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_06_decode_attention.mp3")
        title = title_text("Decode Attention")
        q = chip("Q new", YELLOW, 24, 1.35, 0.64, 0.18).move_to(LEFT*4.75+UP*0.30)
        kv_blocks = VGroup(*[
            block(f"KV{i+1}", [BLUE, GREEN, ORANGE, PURPLE, TEAL][i % 5], 0.62, 0.46, 0.22, 12)
            for i in range(12)
        ]).arrange(RIGHT, buff=0.08).move_to(RIGHT*0.85+UP*0.30)
        cache_box = SurroundingRectangle(kv_blocks, color=MUTED, buff=0.20, corner_radius=0.12)
        cache_label = T("long KV cache", 19, MUTED).next_to(cache_box, UP, buff=0.16)
        beam_targets = [1, 4, 7, 10]
        beams = VGroup(*[
            CurvedArrow(
                q.get_top()+RIGHT*0.20,
                kv_blocks[i].get_top()+UP*0.04,
                angle=-PI/5,
                color=YELLOW,
                stroke_width=1.9,
            )
            for i in beam_targets
        ])
        read_marks = VGroup(*[
            SurroundingRectangle(kv_blocks[i], color=YELLOW, buff=0.04, corner_radius=0.05)
            for i in beam_targets
        ])
        inc = chip("incremental decoding", BLUE, 20, 3.15, 0.55, 0.12).move_to(DOWN*1.15)
        names = VGroup(
            chip("PagedAttention", PURPLE, 15, 1.75, 0.42, 0.10),
            chip("FlashDecoding", ORANGE, 15, 1.75, 0.42, 0.10),
            chip("FlashInfer", TEAL, 15, 1.35, 0.42, 0.10),
        ).arrange(RIGHT, buff=0.20).move_to(DOWN*2.20)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(q, shift=RIGHT), FadeIn(cache_box), FadeIn(cache_label), LaggedStart(*[FadeIn(b) for b in kv_blocks], lag_ratio=0.035), run_time=t(1.7))
        self.play(LaggedStart(*[Create(b) for b in beams], lag_ratio=0.12), LaggedStart(*[Create(m) for m in read_marks], lag_ratio=0.12), run_time=t(1.3))
        self.play(FadeIn(inc, shift=UP), Flash(kv_blocks[3:8], color=YELLOW), run_time=t(1.0))
        self.play(FadeIn(names, shift=UP), Circumscribe(cache_box, color=TEAL), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_21_07_variable_length(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_07_variable_length.mp3")
        title = title_text("Variable Sequence Length")
        row_lengths = [8, 4, 2]
        colors = [BLUE, GREEN, ORANGE]
        before_rows = VGroup()
        pad_group = VGroup()
        for r, n in enumerate(row_lengths):
            row = VGroup()
            for c in range(8):
                if c < n:
                    row.add(block("", colors[r], 0.38, 0.30, 0.28))
                else:
                    pad_cell = block("pad", GRAY, 0.38, 0.30, 0.06, 8, 1.0)
                    row.add(pad_cell)
                    pad_group.add(pad_cell)
            row.arrange(RIGHT, buff=0.05)
            before_rows.add(row)
        before_rows.arrange(DOWN, buff=0.18).move_to(LEFT*2.95+UP*0.35)
        before_label = T("padding to max length", 19, RED, BOLD).next_to(before_rows, UP, buff=0.18)
        cross = VGroup(*[mini_cross(scale=0.35).move_to(cell) for cell in pad_group])
        packed = VGroup()
        for r, n in enumerate(row_lengths):
            seq = VGroup(*[block("", colors[r], 0.38, 0.30, 0.28) for _ in range(n)]).arrange(RIGHT, buff=0.05)
            packed.add(seq)
        packed.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT*2.75+UP*0.35)
        packed_label = T("packed / ragged", 19, GREEN, BOLD).next_to(packed, UP, buff=0.18)
        note = chip("less wasted compute", GREEN, 22, 3.45, 0.60, 0.14).move_to(DOWN*2.20)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(before_label), LaggedStart(*[FadeIn(row, shift=RIGHT*0.08) for row in before_rows], lag_ratio=0.10), run_time=t(1.4))
        self.play(FadeIn(cross), Flash(pad_group, color=RED), run_time=t(1.0))
        self.play(TransformFromCopy(VGroup(*[row[:n] for row, n in zip(before_rows, row_lengths)]), packed), FadeIn(packed_label), run_time=t(1.5))
        self.play(FadeIn(note, shift=UP), Circumscribe(packed, color=GREEN), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_21_08_compilation(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_08_compilation.mp3")
        title = title_text("Automatic Compilation")
        graph = VGroup(
            chip("MatMul", ORANGE, 16, 1.25, 0.45, 0.13),
            chip("Norm", GREEN, 16, 1.10, 0.45, 0.13),
            chip("Act", PURPLE, 16, 0.90, 0.45, 0.13),
        ).arrange(DOWN, buff=0.18).move_to(LEFT*4.30+UP*0.10)
        graph_arrows = VGroup(*[arrow(graph[i].get_bottom(), graph[i+1].get_top(), MUTED, 2.2) for i in range(2)])
        compiler = chip("Compiler\nTVM / Triton\nTorchInductor / MLIR", YELLOW, 18, 2.65, 1.22, 0.14).move_to(ORIGIN+UP*0.10)
        backends = VGroup(
            chip("NVIDIA GPU", GREEN, 16, 1.65, 0.46, 0.12),
            chip("AMD GPU", BLUE, 16, 1.45, 0.46, 0.12),
            chip("CPU", ORANGE, 16, 1.05, 0.46, 0.12),
            chip("Edge", PURPLE, 16, 1.05, 0.46, 0.12),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT*4.05+UP*0.10)
        arrows = VGroup(arrow(graph.get_right(), compiler.get_left(), YELLOW, 3), *[arrow(compiler.get_right(), b.get_left(), b[0].get_stroke_color(), 2.6) for b in backends])
        note = chip("hardware-aware codegen", TEAL, 21, 4.10, 0.58, 0.13).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(graph), LaggedStart(*[Create(a) for a in graph_arrows], lag_ratio=0.10), run_time=t(1.1))
        self.play(Create(arrows[0]), FadeIn(compiler, shift=RIGHT), run_time=t(1.1))
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT*0.10) for b in backends], lag_ratio=0.10), LaggedStart(*[Create(a) for a in arrows[1:]], lag_ratio=0.10), run_time=t(1.7))
        self.play(FadeIn(note, shift=UP), Circumscribe(compiler, color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_21_09_summary(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_21_09_summary.mp3")
        title = title_text("Kernel Optimization - Summary")
        cards = VGroup(
            chip("Fusion", GREEN, 19, 1.55, 0.58, 0.13),
            chip("FlashAttention", ORANGE, 18, 2.10, 0.58, 0.13),
            chip("Decode\nKernel", BLUE, 18, 1.65, 0.72, 0.13),
            chip("Variable\nLength", PURPLE, 18, 1.65, 0.72, 0.13),
            chip("Compilation", TEAL, 18, 1.75, 0.58, 0.13),
        ).arrange(RIGHT, buff=0.18).move_to(UP*0.75)
        kernel_layer = chip("Kernel Layer", YELLOW, 26, 3.20, 0.72, 0.16).move_to(DOWN*0.50)
        stack = VGroup(
            chip("Serving", GREEN, 16, 2.00, 0.42, 0.10),
            chip("Kernel", YELLOW, 18, 2.00, 0.48, 0.16),
            chip("Hardware", BLUE, 16, 2.00, 0.42, 0.10),
        ).arrange(DOWN, buff=0.08).move_to(LEFT*2.75+DOWN*1.85)
        next_box = chip("Next: Frameworks", ORANGE, 23, 3.45, 0.65, 0.14).move_to(RIGHT*2.65+DOWN*2.05)
        next_arrow = arrow(stack.get_right(), next_box.get_left(), YELLOW, 3)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.12) for card in cards], lag_ratio=0.12), run_time=t(1.6))
        self.play(TransformFromCopy(cards, kernel_layer), run_time=t(1.0))
        self.play(FadeIn(stack, shift=UP), Circumscribe(stack[1], color=YELLOW), run_time=t(1.1))
        self.play(Create(next_arrow), FadeIn(next_box, shift=LEFT), Flash(next_box, color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()
