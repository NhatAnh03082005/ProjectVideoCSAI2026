from manim import *
from pathlib import Path
import json
import subprocess

# ============================================================
# PART 4 - SYSTEM OPTIMIZATIONS
# SCENE 19 - MEMORY MANAGEMENT: KV CACHE / PAGEDATTENTION / OFFLOADING
#
# Render test:
#   py -m manim -pql --disable_caching main_p4_19.py Part4MemoryManagement
#
# Render dep:
#   py -m manim -pqh --disable_caching main_p4_19.py Part4MemoryManagement
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
    "voice/p4_19_01_memory_intro.mp3": 20.0,
    "voice/p4_19_02_autoregressive.mp3": 20.0,
    "voice/p4_19_03_kv_memory.mp3": 20.0,
    "voice/p4_19_04_growth.mp3": 20.0,
    "voice/p4_19_05_naive_allocation.mp3": 20.0,
    "voice/p4_19_06_hotel_old.mp3": 20.0,
    "voice/p4_19_07_paged_intro.mp3": 20.0,
    "voice/p4_19_08_block_table.mp3": 20.0,
    "voice/p4_19_09_benefit.mp3": 20.0,
    "voice/p4_19_10_not_quality.mp3": 20.0,
    "voice/p4_19_11_offloading_intro.mp3": 20.0,
    "voice/p4_19_12_offload_types.mp3": 20.0,
    "voice/p4_19_13_offload_tradeoff.mp3": 20.0,
    "voice/p4_19_14_integration.mp3": 20.0,
    "voice/p4_19_15_summary.mp3": 20.0,
}
CURRENT_SCALE = 1.0
TAIL_HOLD = 3.0

BASE_ANIMATION_DURATIONS = {
    "voice/p4_19_01_memory_intro.mp3": 6.5,
    "voice/p4_19_02_autoregressive.mp3": 6.4,
    "voice/p4_19_03_kv_memory.mp3": 6.8,
    "voice/p4_19_04_growth.mp3": 6.3,
    "voice/p4_19_05_naive_allocation.mp3": 5.8,
    "voice/p4_19_06_hotel_old.mp3": 6.8,
    "voice/p4_19_07_paged_intro.mp3": 6.5,
    "voice/p4_19_08_block_table.mp3": 6.2,
    "voice/p4_19_09_benefit.mp3": 5.9,
    "voice/p4_19_10_not_quality.mp3": 5.8,
    "voice/p4_19_11_offloading_intro.mp3": 5.9,
    "voice/p4_19_12_offload_types.mp3": 6.2,
    "voice/p4_19_13_offload_tradeoff.mp3": 6.0,
    "voice/p4_19_14_integration.mp3": 6.2,
    "voice/p4_19_15_summary.mp3": 5.9,
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


def memory_segment(label, width, color, height=0.72, size=17, fill=FILL_MEDIUM):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=fill,
    )
    text = T(label, size=size, color=WHITE_C, weight=BOLD)
    if text.width > box.width - 0.22:
        text.scale_to_fit_width(box.width - 0.22)
    text.move_to(box)
    return VGroup(box, text)


def block_cell(label="", color=BLUE, width=0.48, height=0.36, fill=FILL_MEDIUM, size=12, stroke=1.6):
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


def token_box(text, color=BLUE, width=0.92):
    return chip(text, color=color, size=18, width=width, height=0.54, fill=0.16)


def arrow(a, b, color=MUTED, width=3):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def mini_cross(color=RED, scale=1.0):
    x = VGroup(
        Line(LEFT*0.20+UP*0.20, RIGHT*0.20+DOWN*0.20, color=color, stroke_width=6),
        Line(LEFT*0.20+DOWN*0.20, RIGHT*0.20+UP*0.20, color=color, stroke_width=6),
    )
    x.scale(scale)
    return x


def notebook(width=2.20, height=1.45):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=BLUE, stroke_width=2.4, fill_color=BLUE, fill_opacity=0.10)
    lines = VGroup(*[
        Line(LEFT*(width/2-0.22), RIGHT*(width/2-0.22), color=BLUE, stroke_width=1.6).move_to(UP*y)
        for y in [0.20, -0.05, -0.30]
    ])
    label = T("KV Cache", 20, BLUE, BOLD).move_to(UP*0.48)
    group = VGroup(box, lines, label)
    return group


def simple_gear(label, color):
    ring = Circle(radius=0.72, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.08)
    inner = Circle(radius=0.22, stroke_color=color, stroke_width=2, fill_opacity=0)
    spokes = VGroup(*[
        Line(ORIGIN, RIGHT*0.62, color=color, stroke_width=3).rotate(k * PI / 4)
        for k in range(8)
    ])
    teeth = VGroup(*[
        RoundedRectangle(width=0.20, height=0.15, corner_radius=0.03, stroke_color=color, fill_color=color, fill_opacity=0.35, stroke_width=1.2)
        .move_to(RIGHT*0.82)
        .rotate(k * PI / 4, about_point=ORIGIN)
        for k in range(8)
    ])
    moving = VGroup(ring, inner, spokes, teeth)
    text = T(label, 18, WHITE_C, BOLD)
    if text.width > 1.15:
        text.scale_to_fit_width(1.15)
    text.move_to(ORIGIN)
    return VGroup(moving, text)


class Part4MemoryManagement(Scene):
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
        self.scene_19_01_memory_intro()
        self.scene_19_02_autoregressive()
        self.scene_19_03_kv_memory()
        self.scene_19_04_growth()
        self.scene_19_05_naive_allocation()
        self.scene_19_06_hotel_old()
        self.scene_19_07_paged_intro()
        self.scene_19_08_block_table()
        self.scene_19_09_benefit()
        self.scene_19_10_not_quality()
        self.scene_19_11_offloading_intro()
        self.scene_19_12_offload_types()
        self.scene_19_13_offload_tradeoff()
        self.scene_19_14_integration()
        self.scene_19_15_summary()

    def scene_19_01_memory_intro(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_01_memory_intro.mp3")
        title = title_text("Memory Management", "GPU không chỉ chứa model")
        vram = RoundedRectangle(width=9.60, height=1.20, corner_radius=0.14, stroke_color=MUTED, stroke_width=2.4, fill_color=GRAY, fill_opacity=0.06).move_to(UP*0.10)
        vram_label = T("GPU VRAM", 21, MUTED, BOLD).next_to(vram, UP, buff=0.15)
        weights = memory_segment("Model weights", 2.70, YELLOW, 0.76, 16, 0.20)
        workspace = memory_segment("Workspace", 1.45, PURPLE, 0.76, 15, 0.20)
        kv_small = memory_segment("KV cache", 1.35, BLUE, 0.76, 15, 0.25)
        left = vram.get_left()[0] + 0.30
        y = vram.get_center()[1]
        weights.move_to([left + weights.width/2, y, 0])
        workspace.move_to([weights.get_right()[0] + 0.12 + workspace.width/2, y, 0])
        kv_small.move_to([workspace.get_right()[0] + 0.12 + kv_small.width/2, y, 0])
        kv_big = memory_segment("KV cache grows", 4.25, BLUE, 0.76, 16, 0.35)
        kv_big.move_to([workspace.get_right()[0] + 0.12 + kv_big.width/2, y, 0])
        state = chip("Serving = model + state + memory management", TEAL, 20, 5.95, 0.58, 0.13).move_to(DOWN*1.55)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(vram), FadeIn(vram_label), run_time=t(0.9))
        self.play(FadeIn(weights, shift=RIGHT*0.15), run_time=t(1.0))
        self.play(FadeIn(workspace, shift=RIGHT*0.15), run_time=t(0.8))
        self.play(FadeIn(kv_small, shift=RIGHT*0.15), run_time=t(0.8))
        self.play(Transform(kv_small, kv_big), Flash(kv_small, color=BLUE), run_time=t(1.4))
        self.play(FadeIn(state, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_19_02_autoregressive(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_02_autoregressive.mp3")
        title = title_text("Autoregressive Decoding")
        words = ["Thủ", "đô", "Việt", "Nam", "là", "?"]
        colors = [BLUE, BLUE, GREEN, GREEN, ORANGE, YELLOW]
        tokens = VGroup(*[token_box(w, colors[i], 0.86) for i, w in enumerate(words)]).arrange(RIGHT, buff=0.15).move_to(UP*0.50)
        prefix_box = SurroundingRectangle(VGroup(*tokens[:5]), color=BLUE, buff=0.12, corner_radius=0.10)
        next_label = T("next token", 17, YELLOW).next_to(tokens[-1], UP, buff=0.18)
        arrows = VGroup(*[
            CurvedArrow(tokens[-1].get_top()+LEFT*0.05, tokens[i].get_top()+UP*0.03, angle=PI/4, color=MUTED, stroke_width=2)
            for i in range(5)
        ])
        recompute = chip("recompute everything?", RED, 20, 3.25, 0.55, 0.13).move_to(DOWN*1.15)
        cross = mini_cross(scale=1.4).next_to(recompute, RIGHT, buff=0.18)
        cache = chip("cache previous K,V", GREEN, 21, 3.30, 0.58, 0.14).move_to(DOWN*1.15)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(tok, shift=UP*0.18) for tok in tokens[:5]], lag_ratio=0.18), run_time=t(1.7))
        self.play(FadeIn(tokens[-1], shift=UP*0.18), FadeIn(next_label), Create(prefix_box), run_time=t(0.9))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), run_time=t(1.2))
        self.play(FadeIn(recompute, shift=UP), FadeIn(cross, scale=1.1), run_time=t(0.9))
        self.play(ReplacementTransform(recompute, cache), FadeOut(cross), run_time=t(1.1))
        self.finish_audio_scene()

    def scene_19_03_kv_memory(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_03_kv_memory.mp3")
        title = title_text("KV Cache")
        layer = RoundedRectangle(width=2.30, height=1.25, corner_radius=0.16, stroke_color=PURPLE, stroke_width=2.4, fill_color=PURPLE, fill_opacity=0.12).move_to(ORIGIN)
        layer_label = T("Transformer\nLayer", 22, WHITE_C, BOLD).move_to(layer)
        old_tok = token_box("old tokens", BLUE, 1.55).move_to(LEFT*3.60+UP*0.70)
        new_tok = token_box("new token", YELLOW, 1.55).move_to(LEFT*3.60+DOWN*0.85)
        k = chip("K", BLUE, 28, 0.68, 0.56, 0.20).move_to(RIGHT*1.75+UP*0.52)
        v = chip("V", GREEN, 28, 0.68, 0.56, 0.20).move_to(RIGHT*1.75+DOWN*0.12)
        q = chip("Q", YELLOW, 28, 0.68, 0.56, 0.20).move_to(RIGHT*1.75+DOWN*1.05)
        cache = notebook().move_to(RIGHT*3.80+UP*0.10)
        reuse = chip("reuse, do not recompute", GREEN, 19, 3.65, 0.55, 0.12).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(layer), FadeIn(layer_label), FadeIn(old_tok, shift=RIGHT), run_time=t(1.1))
        self.play(Create(arrow(old_tok.get_right(), layer.get_left(), BLUE)), run_time=t(0.7))
        self.play(FadeIn(k, shift=RIGHT), FadeIn(v, shift=RIGHT), run_time=t(0.9))
        self.play(Create(arrow(k.get_right(), cache.get_left()+UP*0.28, BLUE)), Create(arrow(v.get_right(), cache.get_left()+DOWN*0.20, GREEN)), FadeIn(cache, shift=LEFT), run_time=t(1.2))
        self.play(FadeIn(new_tok, shift=RIGHT), Create(arrow(new_tok.get_right(), layer.get_left()+DOWN*0.35, YELLOW)), FadeIn(q, shift=RIGHT), run_time=t(1.1))
        self.play(Create(arrow(q.get_right(), cache.get_left()+DOWN*0.58, YELLOW)), FadeIn(reuse, shift=UP), run_time=t(1.1))
        self.finish_audio_scene()

    def scene_19_04_growth(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_04_growth.mp3")
        title = title_text("KV Cache Growth")
        rows = []
        colors = [BLUE, GREEN, ORANGE]
        names = ["Request A", "Request B", "Request C"]
        lengths = [7, 5, 6]
        y_positions = [0.95, 0.15, -0.65]
        for name, color, n, y in zip(names, colors, lengths, y_positions):
            label = chip(name, color, 16, 1.55, 0.43, 0.13).move_to(LEFT*4.20 + UP*y)
            blocks = VGroup(*[block_cell("", color, 0.42, 0.34, 0.25) for _ in range(n)]).arrange(RIGHT, buff=0.06)
            blocks.next_to(label, RIGHT, buff=0.28)
            rows.append((label, blocks))
        token_clock = chip("t grows", YELLOW, 20, 1.85, 0.54, 0.12).move_to(RIGHT*3.65+UP*1.15)
        layer_hint = chip("layers x K,V", PURPLE, 18, 2.25, 0.50, 0.12).move_to(RIGHT*3.65+UP*0.35)
        warn = chip("long context + large batch = large KV cache", RED, 19, 5.85, 0.55, 0.12).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(*[FadeIn(label, shift=RIGHT*0.12) for label, _ in rows], run_time=t(0.8))
        for _, blocks in rows:
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT*0.05) for b in blocks], lag_ratio=0.08), run_time=t(1.0))
        self.play(FadeIn(token_clock, shift=DOWN), FadeIn(layer_hint, shift=DOWN), run_time=t(0.9))
        self.play(Flash(VGroup(*[b for _, blocks in rows for b in blocks[-2:]]), color=BLUE), FadeIn(warn, shift=UP), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_19_05_naive_allocation(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_05_naive_allocation.mp3")
        title = title_text("Naive Allocation")
        frame = RoundedRectangle(width=9.40, height=0.94, corner_radius=0.12, stroke_color=MUTED, stroke_width=2.2, fill_color=GRAY, fill_opacity=0.05).move_to(UP*0.25)
        used = memory_segment("used ~200", 1.15, BLUE, 0.62, 14, 0.35)
        unused = memory_segment("reserved but unused", 7.35, GRAY, 0.62, 18, 0.11)
        used.move_to([frame.get_left()[0] + 0.20 + used.width/2, frame.get_center()[1], 0])
        unused.move_to([used.get_right()[0] + 0.08 + unused.width/2, frame.get_center()[1], 0])
        max_label = T("max length reservation: 2048 tokens", 22, YELLOW, BOLD).next_to(frame, UP, buff=0.22)
        req = chip("Request A", BLUE, 18, 1.65, 0.50, 0.14).move_to(LEFT*3.75+DOWN*1.05)
        waste = chip("wasted VRAM", RED, 22, 2.25, 0.58, 0.14).move_to(RIGHT*2.50+DOWN*1.05)
        cross = mini_cross(scale=1.25).next_to(waste, RIGHT, buff=0.16)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(max_label), FadeIn(frame), run_time=t(0.9))
        self.play(FadeIn(req, shift=UP), FadeIn(used, shift=RIGHT*0.15), run_time=t(1.0))
        self.play(FadeIn(unused, shift=RIGHT*0.15), run_time=t(1.0))
        self.play(Flash(unused, color=RED), FadeIn(waste, shift=UP), FadeIn(cross, scale=1.1), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_19_06_hotel_old(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_06_hotel_old.mp3")
        title = title_text("Hotel Analogy")
        rows, cols = 3, 8
        occupied = {(0,0),(0,2),(0,4),(0,7),(1,1),(1,2),(1,5),(2,0),(2,3),(2,6)}
        rooms = VGroup()
        free_rooms = VGroup()
        for r in range(rows):
            for c in range(cols):
                used = (r, c) in occupied
                cell = block_cell("", ORANGE if used else GRAY, 0.58, 0.45, 0.28 if used else 0.08, stroke=1.7)
                rooms.add(cell)
                if not used:
                    free_rooms.add(cell)
        rooms.arrange_in_grid(rows=rows, cols=cols, buff=(0.08, 0.10)).move_to(UP*0.20)
        hotel = SurroundingRectangle(rooms, color=PURPLE, buff=0.16, corner_radius=0.14)
        guests = VGroup(*[Dot(color=YELLOW).scale(1.15) for _ in range(5)]).arrange(RIGHT, buff=0.15).move_to(DOWN*1.40)
        guests_label = T("need 5 contiguous rooms", 20, YELLOW, BOLD).next_to(guests, DOWN, buff=0.12)
        def window(row, start):
            return VGroup(*[rooms[row*cols + c] for c in range(start, start+5)])
        scan = SurroundingRectangle(window(0, 0), color=YELLOW, buff=0.05, corner_radius=0.08)
        oom = chip("OOM due to fragmentation", RED, 21, 3.85, 0.58, 0.14).move_to(DOWN*2.35)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(hotel), LaggedStart(*[FadeIn(room) for room in rooms], lag_ratio=0.02), run_time=t(1.4))
        self.play(FadeIn(guests, shift=UP), FadeIn(guests_label), run_time=t(0.8))
        self.play(Create(scan), run_time=t(0.5))
        for row, start in [(0, 1), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3)]:
            self.play(scan.animate.move_to(window(row, start).get_center()), run_time=t(0.25))
        self.play(Flash(free_rooms, color=GREEN), FadeIn(oom, shift=UP), FadeIn(mini_cross(scale=1.15).next_to(guests, RIGHT, buff=0.25)), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_19_07_paged_intro(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_07_paged_intro.mp3")
        title = title_text("PagedAttention", "block rời rạc + block table")
        assigned = {2: ("A0", BLUE), 7: ("A1", BLUE), 13: ("A2", BLUE), 18: ("A3", BLUE)}
        grid = VGroup()
        for i in range(24):
            if i in assigned:
                label, color = assigned[i]
                grid.add(block_cell(label, color, 0.50, 0.38, 0.34, 11))
            else:
                grid.add(block_cell(f"B{i}", GRAY, 0.50, 0.38, 0.06, 9, stroke=1.2))
        grid.arrange_in_grid(rows=3, cols=8, buff=(0.07, 0.08)).move_to(LEFT*2.25+UP*0.05)
        grid_label = T("physical KV blocks", 19, MUTED).next_to(grid, UP, buff=0.18)
        rows = VGroup(
            chip("A: tokens 0-15  ->  B2", BLUE, 15, 2.65, 0.42, 0.13),
            chip("A: tokens 16-31 ->  B7", BLUE, 15, 2.65, 0.42, 0.13),
            chip("A: tokens 32-47 -> B13", BLUE, 15, 2.65, 0.42, 0.13),
            chip("A: tokens 48-63 -> B18", BLUE, 15, 2.65, 0.42, 0.13),
        ).arrange(DOWN, buff=0.12)
        table_title = chip("Block Table", YELLOW, 18, 2.65, 0.50, 0.12)
        table = VGroup(table_title, rows).arrange(DOWN, buff=0.18).move_to(RIGHT*3.05+UP*0.10)
        arrows = VGroup(*[
            arrow(rows[i].get_left(), grid[idx].get_right(), BLUE, 2.2)
            for i, idx in enumerate([2, 7, 13, 18])
        ])
        note = chip("no contiguous allocation required", GREEN, 20, 4.25, 0.55, 0.12).move_to(DOWN*2.30)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(grid_label), LaggedStart(*[FadeIn(cell) for cell in grid], lag_ratio=0.015), run_time=t(1.5))
        self.play(FadeIn(table, shift=LEFT), run_time=t(1.0))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.10), run_time=t(1.2))
        self.play(FadeIn(note, shift=UP), Circumscribe(table, color=YELLOW), run_time=t(1.1))
        self.finish_audio_scene()

    def scene_19_08_block_table(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_08_block_table.mp3")
        title = title_text("Block Table", "logical order -> physical blocks")
        header = VGroup(chip("logical", YELLOW, 16, 1.35, 0.42, 0.12), chip("physical", YELLOW, 16, 1.35, 0.42, 0.12)).arrange(RIGHT, buff=0.14)
        table_rows = VGroup()
        mappings = [("0: tokens 0-15", "B3", 3), ("1: tokens 16-31", "B9", 9), ("2: tokens 32-47", "B1", 1)]
        for logical, physical, _ in mappings:
            table_rows.add(VGroup(chip(logical, BLUE, 14, 1.75, 0.40, 0.12), chip(physical, GREEN, 16, 0.85, 0.40, 0.14)).arrange(RIGHT, buff=0.18))
        table_rows.arrange(DOWN, buff=0.10)
        table = VGroup(header, table_rows).arrange(DOWN, buff=0.16).move_to(LEFT*2.45+UP*0.05)
        phys = {
            3: block_cell("B3", GREEN, 0.75, 0.50, 0.24, 15).move_to(RIGHT*2.45+UP*0.95),
            9: block_cell("B9", GREEN, 0.75, 0.50, 0.24, 15).move_to(RIGHT*3.45+DOWN*0.10),
            1: block_cell("B1", GREEN, 0.75, 0.50, 0.24, 15).move_to(RIGHT*2.15+DOWN*1.10),
        }
        physical_blocks = VGroup(*phys.values())
        cloud = SurroundingRectangle(physical_blocks, color=MUTED, buff=0.30, corner_radius=0.16)
        cloud_label = T("scattered physical memory", 19, MUTED).next_to(cloud, UP, buff=0.16)
        order = chip("logical order is preserved by table", TEAL, 20, 4.80, 0.55, 0.12).move_to(DOWN*2.30)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(table, shift=RIGHT), FadeIn(cloud), FadeIn(cloud_label), FadeIn(physical_blocks), run_time=t(1.4))
        arrows = VGroup()
        for i, (_, _, block_no) in enumerate(mappings):
            ar = arrow(table_rows[i].get_right(), phys[block_no].get_left(), YELLOW, 2.6)
            arrows.add(ar)
            self.play(Circumscribe(table_rows[i], color=YELLOW), Create(ar), Flash(phys[block_no], color=YELLOW), run_time=t(0.9))
        self.play(FadeIn(order, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_19_09_benefit(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_09_benefit.mp3")
        title = title_text("PagedAttention Benefit", "giảm lãng phí, tăng batch")
        before_title = T("Before", 24, RED, BOLD).move_to(LEFT*3.05+UP*1.65)
        after_title = T("After", 24, GREEN, BOLD).move_to(RIGHT*3.05+UP*1.65)
        free_positions = {1, 4, 6, 9, 12, 14}
        before = VGroup()
        after = VGroup()
        for i in range(16):
            before.add(block_cell("", GRAY if i in free_positions else ORANGE, 0.44, 0.34, 0.06 if i in free_positions else 0.25))
            if i in free_positions:
                after.add(block_cell("N", GREEN, 0.44, 0.34, 0.30, 11))
            else:
                after.add(block_cell("", ORANGE, 0.44, 0.34, 0.22))
        before.arrange_in_grid(rows=2, cols=8, buff=(0.07, 0.08)).move_to(LEFT*3.05+UP*0.25)
        after.arrange_in_grid(rows=2, cols=8, buff=(0.07, 0.08)).move_to(RIGHT*3.05+UP*0.25)
        before_cross = mini_cross(scale=2.3).move_to(before)
        reused = chip("reused blocks", GREEN, 18, 2.10, 0.50, 0.12).move_to(RIGHT*3.05+DOWN*0.80)
        batch_old = chip("batch size: 3", YELLOW, 22, 2.35, 0.58, 0.12).move_to(DOWN*1.75)
        batch_new = chip("batch size: 7 (illustrative)", YELLOW, 22, 3.45, 0.58, 0.12).move_to(DOWN*1.75)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(before_title), FadeIn(after_title), FadeIn(before), FadeIn(after), run_time=t(1.3))
        self.play(FadeIn(before_cross, scale=1.05), Flash(before, color=RED), run_time=t(0.9))
        self.play(FadeIn(reused, shift=UP), Flash(VGroup(*[after[i] for i in free_positions]), color=GREEN), run_time=t(1.0))
        self.play(FadeIn(batch_old, shift=UP), run_time=t(0.7))
        self.play(ReplacementTransform(batch_old, batch_new), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_19_10_not_quality(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_10_not_quality.mp3")
        title = title_text("System Optimization")
        left_model = chip("Same model", BLUE, 22, 2.20, 0.68, 0.14).move_to(LEFT*3.00+UP*0.85)
        right_model = chip("Same model", BLUE, 22, 2.20, 0.68, 0.14).move_to(RIGHT*3.00+UP*0.85)
        left_cache = memory_segment("contiguous cache", 2.45, GRAY, 0.45, 13, 0.12).next_to(left_model, DOWN, buff=0.22)
        right_blocks = VGroup(block_cell("K,V", GREEN, 0.60, 0.38, 0.22, 10), block_cell("K,V", GREEN, 0.60, 0.38, 0.22, 10), block_cell("K,V", GREEN, 0.60, 0.38, 0.22, 10)).arrange(RIGHT, buff=0.18).next_to(right_model, DOWN, buff=0.25)
        table = chip("block table", YELLOW, 14, 1.45, 0.36, 0.10).next_to(right_blocks, DOWN, buff=0.12)
        out1 = chip('"Hà Nội"', ORANGE, 24, 1.85, 0.64, 0.15).move_to(LEFT*3.00+DOWN*1.00)
        out2 = chip('"Hà Nội"', ORANGE, 24, 1.85, 0.64, 0.15).move_to(RIGHT*3.00+DOWN*1.00)
        eq = T("=", 44, WHITE_C, BOLD).move_to(DOWN*1.00)
        same = chip("same semantics", GREEN, 20, 2.45, 0.55, 0.12).move_to(DOWN*2.05)
        better = chip("better memory utilization", TEAL, 20, 3.60, 0.55, 0.12).next_to(same, RIGHT, buff=0.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(left_model), FadeIn(right_model), run_time=t(0.8))
        self.play(FadeIn(left_cache, shift=UP), FadeIn(right_blocks, shift=UP), FadeIn(table), run_time=t(1.1))
        self.play(Create(arrow(left_model.get_bottom(), out1.get_top(), BLUE)), Create(arrow(right_model.get_bottom(), out2.get_top(), BLUE)), FadeIn(out1), FadeIn(out2), run_time=t(1.2))
        self.play(FadeIn(eq), FadeIn(same, shift=UP), run_time=t(0.9))
        self.play(FadeIn(better, shift=UP), Circumscribe(better, color=TEAL), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_19_11_offloading_intro(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_11_offloading_intro.mp3")
        title = title_text("Offloading")
        gpu = memory_segment("GPU HBM\nfast / small / expensive", 3.20, BLUE, 0.78, 15, 0.18).move_to(UP*1.05)
        ram = memory_segment("CPU RAM\nlarger / slower", 4.55, GREEN, 0.78, 15, 0.14).move_to(UP*0.00)
        disk = memory_segment("Disk / NVMe\nlargest / slowest", 6.00, ORANGE, 0.78, 15, 0.12).move_to(DOWN*1.05)
        data = chip("weights / KV", YELLOW, 18, 1.75, 0.50, 0.16).move_to(gpu.get_right()+RIGHT*1.00)
        down = Arrow(gpu.get_bottom(), ram.get_top(), buff=0.08, color=RED, stroke_width=3)
        down2 = Arrow(ram.get_bottom(), disk.get_top(), buff=0.08, color=RED, stroke_width=3)
        up = Arrow(disk.get_top()+RIGHT*1.20, gpu.get_bottom()+RIGHT*1.20, buff=0.08, color=GREEN, stroke_width=3)
        off = T("offload", 19, RED, BOLD).next_to(down, LEFT, buff=0.15)
        pre = T("prefetch", 19, GREEN, BOLD).next_to(up, RIGHT, buff=0.15)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(gpu, shift=DOWN), FadeIn(ram), FadeIn(disk, shift=UP), run_time=t(1.3))
        self.play(FadeIn(data, shift=LEFT), run_time=t(0.7))
        self.play(Create(down), Create(down2), FadeIn(off), data.animate.move_to(disk.get_right()+RIGHT*0.75), run_time=t(1.5))
        self.play(Create(up), FadeIn(pre), data.animate.move_to(gpu.get_right()+RIGHT*1.00), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_19_12_offload_types(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_12_offload_types.mp3")
        title = title_text("What Gets Offloaded?", "weights và KV cache là hai kiểu khác nhau")
        divider = Line(UP*1.65, DOWN*1.70, color=MUTED, stroke_width=2)
        left_title = T("Weight Offload", 25, YELLOW, BOLD).move_to(LEFT*3.05+UP*1.55)
        right_title = T("KV Cache Offload", 25, BLUE, BOLD).move_to(RIGHT*3.05+UP*1.55)
        gpu_l = chip("GPU", BLUE, 18, 1.20, 0.46, 0.14).move_to(LEFT*4.15+UP*0.55)
        cpu_l = chip("CPU RAM", GREEN, 18, 1.55, 0.46, 0.14).move_to(LEFT*1.95+DOWN*0.75)
        layers = VGroup(*[chip(f"L{i}", YELLOW, 16, 0.64, 0.42, 0.16) for i in range(1, 5)]).arrange(RIGHT, buff=0.14).move_to(LEFT*3.22+DOWN*0.02)
        layer_l1_target = cpu_l.get_left() + LEFT*0.40
        gpu_r = chip("GPU", BLUE, 18, 1.20, 0.46, 0.14).move_to(RIGHT*1.95+UP*0.55)
        cpu_r = chip("CPU RAM", GREEN, 18, 1.55, 0.46, 0.14).move_to(RIGHT*4.15+DOWN*0.75)
        cache_blocks = VGroup(*[block_cell("", [BLUE, ORANGE, PURPLE, TEAL][i % 4], 0.38, 0.32, 0.27) for i in range(10)]).arrange(RIGHT, buff=0.05).move_to(RIGHT*3.05+DOWN*0.05)
        note = chip("different data, same idea: relieve GPU memory", TEAL, 20, 5.85, 0.55, 0.12).move_to(DOWN*2.02)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(Create(divider), FadeIn(left_title), FadeIn(right_title), run_time=t(0.9))
        self.play(FadeIn(gpu_l), FadeIn(cpu_l), FadeIn(layers, shift=UP), FadeIn(gpu_r), FadeIn(cpu_r), FadeIn(cache_blocks, shift=UP), run_time=t(1.4))
        self.play(Create(arrow(gpu_l.get_right(), layer_l1_target + UP*0.20, YELLOW)), layers[0].animate.move_to(layer_l1_target), run_time=t(1.1))
        self.play(Create(arrow(gpu_r.get_right(), cpu_r.get_left(), BLUE)), cache_blocks[-3:].animate.next_to(cpu_r, UP, buff=0.12), run_time=t(1.1))
        self.play(FadeIn(note, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_19_13_offload_tradeoff(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_13_offload_tradeoff.mp3")
        title = title_text("Offloading Trade-off")
        gpu = chip("GPU\nwaiting", BLUE, 24, 2.10, 1.05, 0.14).move_to(LEFT*2.75+UP*0.35)
        cpu = chip("CPU RAM", GREEN, 20, 1.95, 0.62, 0.14).move_to(RIGHT*1.05+UP*0.90)
        disk = chip("Disk / NVMe", ORANGE, 20, 2.25, 0.62, 0.12).move_to(RIGHT*2.35+DOWN*0.65)
        data = chip("data", YELLOW, 18, 1.00, 0.42, 0.16).move_to(disk)
        clock = VGroup(Circle(radius=0.35, color=RED, stroke_width=3), Line(ORIGIN, UP*0.25, color=RED, stroke_width=3), Line(ORIGIN, RIGHT*0.20, color=RED, stroke_width=3)).next_to(gpu, DOWN, buff=0.25)
        latency = T("latency ↑", 24, RED, BOLD).next_to(clock, RIGHT, buff=0.18)
        trade = VGroup(chip("fit larger model", GREEN, 18, 2.25, 0.50, 0.12), DoubleArrow(LEFT, RIGHT, color=YELLOW, stroke_width=3).scale(0.70), chip("higher latency", RED, 18, 2.05, 0.50, 0.12)).arrange(RIGHT, buff=0.25).move_to(DOWN*2.25)
        not_free = chip("not free", RED, 20, 1.55, 0.55, 0.14).move_to(UP*2.05)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(gpu), FadeIn(cpu), FadeIn(disk), run_time=t(1.0))
        self.play(FadeIn(data), Create(arrow(disk.get_left(), cpu.get_right(), ORANGE)), data.animate.move_to(cpu), run_time=t(1.2))
        self.play(Create(arrow(cpu.get_left(), gpu.get_right(), GREEN)), data.animate.move_to(gpu), FadeIn(clock), FadeIn(latency), run_time=t(1.4))
        self.play(FadeIn(trade, shift=UP), FadeIn(not_free, shift=DOWN), Circumscribe(trade, color=YELLOW), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_19_14_integration(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_14_integration.mp3")
        title = title_text("Memory + Scheduling")
        mem = simple_gear("Memory\nManager", BLUE).move_to(LEFT*2.10+UP*0.15)
        sched = simple_gear("Request\nScheduler", GREEN).move_to(RIGHT*2.10+UP*0.15)
        link1 = DoubleArrow(mem.get_right(), sched.get_left(), buff=0.18, color=YELLOW, stroke_width=3)
        info = VGroup(
            chip("batch size", YELLOW, 16, 1.45, 0.40, 0.12),
            chip("KV cache", BLUE, 16, 1.30, 0.40, 0.12),
            chip("prefetch", GREEN, 16, 1.22, 0.40, 0.12),
        ).arrange(RIGHT, buff=0.18).move_to(DOWN*1.35)
        teaser = chip("Next: Request Scheduling", ORANGE, 22, 3.65, 0.60, 0.13).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(mem), FadeIn(sched), run_time=t(1.0))
        self.play(Create(link1), Rotate(mem[0], angle=PI/3), Rotate(sched[0], angle=-PI/3), run_time=t(1.4))
        self.play(FadeIn(info, shift=UP), Rotate(mem[0], angle=PI/3), Rotate(sched[0], angle=-PI/3), run_time=t(1.2))
        self.play(FadeIn(teaser, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_19_15_summary(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_19_15_summary.mp3")
        title = title_text("Memory Management — Summary")
        cards = VGroup(
            chip("KV Cache\ntemporary memory", BLUE, 19, 2.55, 0.88, 0.13),
            chip("PagedAttention\nblock table", GREEN, 19, 2.55, 0.88, 0.13),
            chip("Offloading\nlatency trade-off", ORANGE, 19, 2.55, 0.88, 0.13),
        ).arrange(RIGHT, buff=0.35).move_to(UP*0.55)
        stack_label = chip("Memory Management", PURPLE, 24, 3.75, 0.70, 0.15).move_to(DOWN*0.75)
        next_box = chip("Request Scheduling", YELLOW, 24, 3.55, 0.70, 0.15).move_to(RIGHT*2.70+DOWN*2.05)
        stack = VGroup(
            chip("KV Cache\ntemporary memory", BLUE, 16, 2.35, 0.62, 0.13),
            chip("PagedAttention\nblock table", GREEN, 16, 2.35, 0.62, 0.13),
            chip("Offloading\nlatency trade-off", ORANGE, 16, 2.35, 0.62, 0.13),
        ).arrange(DOWN, buff=0.08).move_to(LEFT*3.18+DOWN*1.80)
        next_arrow = arrow(stack.get_right(), next_box.get_left(), YELLOW, 3.2)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.12) for card in cards], lag_ratio=0.18), run_time=t(1.6))
        self.play(TransformFromCopy(cards, stack), FadeIn(stack_label, shift=UP), run_time=t(1.2))
        self.play(Create(next_arrow), FadeIn(next_box, shift=LEFT), Flash(next_box, color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()
