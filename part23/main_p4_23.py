from manim import *
from pathlib import Path
import json
import subprocess

# ============================================================
# PART 4 - SYSTEM OPTIMIZATIONS
# SCENE 23 - FUTURE DIRECTIONS AND CONCLUSION
#
# Render test:
#   py -m manim -pql --disable_caching --progress_bar none main_p4_23.py Part4FutureDirectionsConclusion
#
# Render dep:
#   py -m manim -pqh --disable_caching --progress_bar none main_p4_23.py Part4FutureDirectionsConclusion
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
    "voice/p4_23_01_full_stack.mp3": 15.0,
    "voice/p4_23_02_future_directions.mp3": 15.0,
    "voice/p4_23_03_no_one_size.mp3": 15.0,
    "voice/p4_23_04_final.mp3": 15.0,
}
CURRENT_SCALE = 1.0
TAIL_HOLD = 2.2

BASE_ANIMATION_DURATIONS = {
    "voice/p4_23_01_full_stack.mp3": 6.0,
    "voice/p4_23_02_future_directions.mp3": 6.2,
    "voice/p4_23_03_no_one_size.mp3": 5.8,
    "voice/p4_23_04_final.mp3": 6.0,
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
    title = T(text, size=39, color=WHITE_C, weight=BOLD)
    title.to_edge(UP, buff=0.34)
    if sub:
        subtitle = T(sub, size=22, color=BLUE)
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


def arrow(a, b, color=MUTED, width=3):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def stack_layer(text, color, width=3.25):
    return chip(text, color, 17, width, 0.46, 0.12)


def workload_card(title, metric, color):
    top = chip(title, color, 19, 2.45, 0.56, 0.15)
    bottom = chip(metric, color, 15, 2.45, 0.46, 0.08)
    return VGroup(top, bottom).arrange(DOWN, buff=0.10)


class Part4FutureDirectionsConclusion(Scene):
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
        self.scene_23_01_full_stack()
        self.scene_23_02_future_directions()
        self.scene_23_03_no_one_size()
        self.scene_23_04_final()

    def scene_23_01_full_stack(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_23_01_full_stack.mp3")
        title = title_text("Full-Stack Optimization")
        left_layers = VGroup(
            stack_layer("Token algorithm", PURPLE),
            stack_layer("Model architecture", ORANGE),
            stack_layer("Quantization", YELLOW),
            stack_layer("Parallelism", GREEN),
        ).arrange(DOWN, buff=0.13).move_to(LEFT*2.45+UP*0.18)
        right_layers = VGroup(
            stack_layer("Memory management", BLUE),
            stack_layer("Request scheduling", TEAL),
            stack_layer("Kernel + compiler", RED),
            stack_layer("Hardware", GRAY),
        ).arrange(DOWN, buff=0.13).move_to(RIGHT*2.45+UP*0.18)
        bridge = chip("LLM Serving System", WHITE_C, 24, 3.70, 0.66, 0.06).move_to(DOWN*1.78)
        arrows = VGroup(
            arrow(left_layers.get_bottom()+DOWN*0.05, bridge.get_left()+UP*0.05, YELLOW, 2.5),
            arrow(right_layers.get_bottom()+DOWN*0.05, bridge.get_right()+UP*0.05, YELLOW, 2.5),
        )
        warning = chip("ignore one layer -> bottleneck", RED, 20, 4.40, 0.56, 0.14).move_to(DOWN*2.55)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(layer, shift=RIGHT*0.10) for layer in left_layers], lag_ratio=0.10), run_time=t(1.4))
        self.play(LaggedStart(*[FadeIn(layer, shift=LEFT*0.10) for layer in right_layers], lag_ratio=0.10), run_time=t(1.4))
        self.play(FadeIn(bridge, shift=UP), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.12), run_time=t(1.2))
        self.play(FadeIn(warning, shift=UP), Flash(VGroup(left_layers, right_layers), color=YELLOW), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_23_02_future_directions(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_23_02_future_directions.mp3")
        title = title_text("Future Directions")
        hub = VGroup(
            Circle(radius=0.34, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.18),
            Dot(color=YELLOW).scale(1.15),
        ).move_to(ORIGIN+UP*0.05)
        center_label = chip("Future LLM Serving", YELLOW, 19, 3.05, 0.52, 0.10).next_to(hub, DOWN, buff=0.22)
        cards = VGroup(
            chip("Accelerators", ORANGE, 17, 2.05, 0.50, 0.12).move_to(LEFT*4.05+UP*1.25),
            chip("Speculative\nInference", GREEN, 16, 2.05, 0.68, 0.12).move_to(ORIGIN+UP*1.65),
            chip("Long Context", BLUE, 17, 2.05, 0.50, 0.12).move_to(RIGHT*4.05+UP*1.25),
            chip("New\nArchitectures", PURPLE, 16, 2.05, 0.68, 0.12).move_to(LEFT*3.05+DOWN*1.45),
            chip("Edge / Hybrid\nDecentralized", TEAL, 15, 2.45, 0.68, 0.12).move_to(RIGHT*3.05+DOWN*1.45),
        )
        spokes = VGroup(*[
            Arrow(
                hub.get_center(),
                card.get_center(),
                buff=0.48,
                color=card[0].get_stroke_color(),
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.12,
            )
            for card in cards
        ])
        horizon = chip("efficiency across hardware, context, and deployment", GREEN, 18, 6.55, 0.52, 0.11).move_to(DOWN*2.55)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(hub, scale=1.05), FadeIn(center_label, shift=UP*0.08), run_time=t(0.8))
        self.play(LaggedStart(*[Create(s) for s in spokes], lag_ratio=0.08), LaggedStart(*[FadeIn(c, shift=(c.get_center()-hub.get_center())*0.08) for c in cards], lag_ratio=0.08), run_time=t(2.0))
        self.play(FadeIn(horizon, shift=UP), Circumscribe(VGroup(hub, center_label), color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_23_03_no_one_size(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_23_03_no_one_size.mp3")
        title = title_text("No One-Size-Fits-All")
        cards = VGroup(
            workload_card("Realtime\nChatbot", "low latency", BLUE),
            workload_card("Offline\nBatch", "high throughput", GREEN),
            workload_card("Edge\nDevice", "memory + power", ORANGE),
        ).arrange(RIGHT, buff=0.55).move_to(UP*0.55)
        knobs = VGroup(
            chip("scheduler", TEAL, 15, 1.40, 0.42, 0.10),
            chip("KV cache", BLUE, 15, 1.25, 0.42, 0.10),
            chip("kernels", YELLOW, 15, 1.10, 0.42, 0.10),
            chip("offload", ORANGE, 15, 1.15, 0.42, 0.10),
        ).arrange(RIGHT, buff=0.18).move_to(DOWN*1.00)
        arrows = VGroup(
            arrow(cards[0].get_bottom(), knobs[0].get_top(), BLUE, 2.2),
            arrow(cards[1].get_bottom(), knobs[1].get_top(), GREEN, 2.2),
            arrow(cards[2].get_bottom(), knobs[3].get_top(), ORANGE, 2.2),
        )
        conclusion = chip("optimize for the actual goal", RED, 22, 4.60, 0.60, 0.14).move_to(DOWN*2.30)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.12) for card in cards], lag_ratio=0.16), run_time=t(1.5))
        self.play(LaggedStart(*[FadeIn(k, shift=UP*0.08) for k in knobs], lag_ratio=0.10), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.12), run_time=t(1.5))
        self.play(FadeIn(conclusion, shift=UP), Circumscribe(cards, color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_23_04_final(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_23_04_final.mp3")
        title = title_text("Conclusion")
        center = chip("Serve LLMs\nat real scale", YELLOW, 28, 3.55, 1.00, 0.16).move_to(UP*0.35)
        goals = VGroup(
            chip("faster", GREEN, 20, 1.45, 0.52, 0.13),
            chip("cheaper", BLUE, 20, 1.55, 0.52, 0.13),
            chip("stable", PURPLE, 20, 1.45, 0.52, 0.13),
            chip("fit real needs", ORANGE, 18, 2.05, 0.52, 0.13),
        ).arrange(RIGHT, buff=0.24).move_to(DOWN*0.95)
        system = VGroup(
            chip("model", MUTED, 14, 0.95, 0.34, 0.07),
            chip("memory", BLUE, 14, 1.05, 0.34, 0.08),
            chip("schedule", GREEN, 14, 1.10, 0.34, 0.08),
            chip("kernel", YELLOW, 14, 0.95, 0.34, 0.08),
            chip("hardware", ORANGE, 14, 1.10, 0.34, 0.08),
        ).arrange(RIGHT, buff=0.12).move_to(DOWN*2.05)
        final_line = T("Build systems that can actually serve users.", 24, WHITE_C, BOLD).move_to(UP*1.85)
        arrows = VGroup(*[arrow(center.get_bottom(), goal.get_top(), goal[0].get_stroke_color(), 2.2) for goal in goals])
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(final_line, shift=DOWN), FadeIn(center, scale=1.04), run_time=t(1.2))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), LaggedStart(*[FadeIn(g, shift=UP*0.10) for g in goals], lag_ratio=0.10), run_time=t(1.6))
        self.play(FadeIn(system, shift=UP), Circumscribe(center, color=YELLOW), run_time=t(1.2))
        self.play(Flash(system, color=GREEN), run_time=t(1.0))
        self.finish_audio_scene()
