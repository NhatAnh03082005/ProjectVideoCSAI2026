from manim import *
from pathlib import Path
import json
import subprocess

# ============================================================
# PART 4 - SYSTEM OPTIMIZATIONS
# SCENE 20 - REQUEST SCHEDULING: CONTINUOUS BATCHING / CHUNKED PREFILL
#
# Render test:
#   py -m manim -pql --disable_caching main_p4_20.py Part4RequestScheduling
#
# Render dep:
#   py -m manim -pqh --disable_caching main_p4_20.py Part4RequestScheduling
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
    "voice/p4_20_01_intro.mp3": 20.0,
    "voice/p4_20_02_static_batching.mp3": 20.0,
    "voice/p4_20_03_partial_idle.mp3": 20.0,
    "voice/p4_20_04_iteration.mp3": 20.0,
    "voice/p4_20_05_conveyor.mp3": 20.0,
    "voice/p4_20_06_prefill_decode.mp3": 20.0,
    "voice/p4_20_07_long_prefill_blocks.mp3": 20.0,
    "voice/p4_20_08_chunked_prefill.mp3": 20.0,
    "voice/p4_20_09_priority_slo.mp3": 20.0,
    "voice/p4_20_10_disaggregation.mp3": 20.0,
    "voice/p4_20_11_full_timeline.mp3": 20.0,
    "voice/p4_20_12_summary_transition.mp3": 20.0,
}
CURRENT_SCALE = 1.0
TAIL_HOLD = 3.0

BASE_ANIMATION_DURATIONS = {
    "voice/p4_20_01_intro.mp3": 6.4,
    "voice/p4_20_02_static_batching.mp3": 6.2,
    "voice/p4_20_03_partial_idle.mp3": 5.9,
    "voice/p4_20_04_iteration.mp3": 6.8,
    "voice/p4_20_05_conveyor.mp3": 6.2,
    "voice/p4_20_06_prefill_decode.mp3": 6.0,
    "voice/p4_20_07_long_prefill_blocks.mp3": 6.0,
    "voice/p4_20_08_chunked_prefill.mp3": 6.4,
    "voice/p4_20_09_priority_slo.mp3": 5.8,
    "voice/p4_20_10_disaggregation.mp3": 6.2,
    "voice/p4_20_11_full_timeline.mp3": 6.6,
    "voice/p4_20_12_summary_transition.mp3": 6.0,
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


def block(label="", color=BLUE, width=0.45, height=0.34, fill=FILL_MEDIUM, size=12, stroke=1.6):
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


def mini_cross(color=RED, scale=1.0):
    x = VGroup(
        Line(LEFT*0.20+UP*0.20, RIGHT*0.20+DOWN*0.20, color=color, stroke_width=6),
        Line(LEFT*0.20+DOWN*0.20, RIGHT*0.20+UP*0.20, color=color, stroke_width=6),
    )
    x.scale(scale)
    return x


def user_icon(color=BLUE, label=""):
    head = Circle(radius=0.10, stroke_color=color, fill_color=color, fill_opacity=0.35, stroke_width=2).shift(UP*0.10)
    body = Arc(radius=0.20, start_angle=0, angle=PI, color=color, stroke_width=2.5).shift(DOWN*0.25)
    icon = VGroup(head, body)
    if label:
        txt = T(label, 13, WHITE_C, BOLD).next_to(icon, DOWN, buff=0.02)
        return VGroup(icon, txt)
    return icon


def gpu_chip(label="GPU", color=BLUE, width=1.50, height=0.92):
    body = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.10)
    pins = VGroup()
    for i in range(5):
        pins.add(Line(UP*0.06, DOWN*0.06, color=color, stroke_width=2).move_to(body.get_left()+RIGHT*0.08+UP*(0.28-i*0.14)))
        pins.add(Line(UP*0.06, DOWN*0.06, color=color, stroke_width=2).move_to(body.get_right()+LEFT*0.08+UP*(0.28-i*0.14)))
    text = T(label, 18, WHITE_C, BOLD).move_to(body)
    return VGroup(body, pins, text)


def timeline_row(name, prompt_width, output_width, color, y):
    label = chip(name, color, 16, 1.15, 0.40, 0.12).move_to(LEFT*4.90 + UP*y)
    prompt = bar("prompt", prompt_width, color, 0.38, 13, 0.20).next_to(label, RIGHT, buff=0.22)
    output = bar("output ?", output_width, YELLOW, 0.38, 13, 0.14).next_to(prompt, RIGHT, buff=0.12)
    return VGroup(label, prompt, output)


def slot_grid(rows=2, cols=4, filled=True):
    group = VGroup()
    colors = [BLUE, GREEN, ORANGE, PURPLE, TEAL, YELLOW, BLUE, GREEN]
    for i in range(rows * cols):
        group.add(block(chr(ord("A") + i) if filled else "", colors[i % len(colors)], 0.72, 0.48, 0.25 if filled else 0.06, 15))
    group.arrange_in_grid(rows=rows, cols=cols, buff=(0.14, 0.16))
    return group


class Part4RequestScheduling(Scene):
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
        self.scene_20_01_intro()
        self.scene_20_02_static_batching()
        self.scene_20_03_partial_idle()
        self.scene_20_04_iteration()
        self.scene_20_05_conveyor()
        self.scene_20_06_prefill_decode()
        self.scene_20_07_long_prefill_blocks()
        self.scene_20_08_chunked_prefill()
        self.scene_20_09_priority_slo()
        self.scene_20_10_disaggregation()
        self.scene_20_11_full_timeline()
        self.scene_20_12_summary_transition()

    def scene_20_01_intro(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_01_intro.mp3")
        title = title_text("Request Scheduling", "variable input, unknown output")
        rows = VGroup(
            timeline_row("Req A", 1.10, 1.05, BLUE, 0.95),
            timeline_row("Req B", 2.60, 1.40, GREEN, 0.25),
            timeline_row("Req C", 1.55, 2.10, ORANGE, -0.45),
            timeline_row("Req D", 3.25, 2.55, PURPLE, -1.15),
        )
        users = VGroup(*[user_icon([BLUE, GREEN, ORANGE, PURPLE][i], f"U{i+1}").next_to(rows[i][0], LEFT, buff=0.22) for i in range(4)])
        question = VGroup(*[T("?", 25, YELLOW, BOLD).next_to(rows[i][2], RIGHT, buff=0.12) for i in range(4)])
        note = chip("Variable input, unknown output", YELLOW, 22, 4.45, 0.60, 0.13).move_to(DOWN*2.30)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(u, shift=RIGHT*0.10) for u in users], lag_ratio=0.10), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(row[0]) for row in rows], lag_ratio=0.10), run_time=t(0.8))
        self.play(LaggedStart(*[GrowFromEdge(row[1], LEFT) for row in rows], lag_ratio=0.13), run_time=t(1.5))
        self.play(LaggedStart(*[GrowFromEdge(row[2], LEFT) for row in rows], lag_ratio=0.13), FadeIn(question), run_time=t(1.4))
        self.play(FadeIn(note, shift=UP), run_time=t(0.9))
        self.finish_audio_scene()

    def scene_20_02_static_batching(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_02_static_batching.mp3")
        title = title_text("Static Batching")
        batch = RoundedRectangle(width=8.80, height=2.85, corner_radius=0.18, stroke_color=BLUE, stroke_width=2.4, fill_color=BLUE, fill_opacity=0.06).move_to(UP*0.10)
        batch_label = T("Batch 1", 21, BLUE, BOLD).next_to(batch, UP, buff=0.14)
        labels = ["A", "B", "C", "D"]
        colors = [GREEN, TEAL, ORANGE, PURPLE]
        lengths = [2.0, 2.55, 4.15, 6.45]
        lines = VGroup()
        start_x = -3.15
        for i, (name, color, length) in enumerate(zip(labels, colors, lengths)):
            y = 0.90 - i * 0.55
            lab = chip(name, color, 17, 0.52, 0.36, 0.16).move_to(LEFT*3.95 + UP*y)
            ln = bar("", length, color, 0.30, 10, 0.28)
            ln.move_to([start_x + length/2, y, 0])
            done = T("done", 14, GREEN).next_to(ln, RIGHT, buff=0.08)
            lines.add(VGroup(lab, ln, done))
        new_req = chip("new requests wait", YELLOW, 19, 2.65, 0.52, 0.12).move_to(RIGHT*3.25+DOWN*1.75)
        wait_icon = VGroup(Arc(radius=0.28, start_angle=0, angle=TAU*0.82, color=YELLOW, stroke_width=4), T("...", 18, YELLOW, BOLD)).arrange(RIGHT, buff=0.10).next_to(new_req, LEFT, buff=0.20)
        tail = chip("tail latency", RED, 22, 2.10, 0.58, 0.14).move_to(DOWN*2.45)
        hold = SurroundingRectangle(
            VGroup(lines[0][1], lines[0][2], lines[1][1], lines[1][2]),
            color=RED,
            buff=0.08,
            corner_radius=0.08,
        )
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(batch), FadeIn(batch_label), run_time=t(0.8))
        self.play(LaggedStart(*[FadeIn(line[0]) for line in lines], lag_ratio=0.08), LaggedStart(*[GrowFromEdge(line[1], LEFT) for line in lines], lag_ratio=0.08), run_time=t(1.7))
        self.play(lines[0][1].animate.set_opacity(0.35), lines[1][1].animate.set_opacity(0.35), FadeIn(lines[0][2]), FadeIn(lines[1][2]), Create(hold), run_time=t(1.2))
        self.play(FadeIn(new_req, shift=LEFT), FadeIn(wait_icon), Flash(lines[3], color=PURPLE), run_time=t(1.0))
        self.play(FadeIn(tail, shift=UP), Circumscribe(lines[3], color=RED), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_20_03_partial_idle(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_03_partial_idle.mp3")
        title = title_text("Partial Idle")
        gpu = gpu_chip("GPU Batch Slots", BLUE, 3.00, 0.90).move_to(UP*1.35)
        slots = slot_grid().move_to(UP*0.15)
        frame = SurroundingRectangle(slots, color=MUTED, buff=0.20, corner_radius=0.12)
        idle_idx = [0, 1, 3, 5, 6]
        frozen = VGroup()
        for idx in idle_idx:
            frozen.add(slots[idx])
        cap = chip("unused capacity", RED, 22, 2.65, 0.58, 0.14).move_to(DOWN*1.55)
        util_full = bar("utilization high", 4.60, GREEN, 0.42, 16, 0.25).move_to(DOWN*2.35)
        util_low = bar("utilization drops", 2.30, RED, 0.42, 16, 0.25).move_to(DOWN*2.35+LEFT*1.15)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(gpu), FadeIn(frame), LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.04), run_time=t(1.5))
        self.play(FadeIn(util_full, shift=UP), run_time=t(0.7))
        self.play(*[slots[i].animate.set_opacity(0.25) for i in idle_idx], run_time=t(1.0))
        crosses = VGroup(*[mini_cross(scale=0.75).move_to(slots[i]) for i in idle_idx])
        self.play(FadeIn(crosses), FadeIn(cap, shift=UP), ReplacementTransform(util_full, util_low), run_time=t(1.4))
        self.play(Flash(frozen, color=RED), run_time=t(0.8))
        self.finish_audio_scene()

    def scene_20_04_iteration(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_04_iteration.mp3")
        title = title_text("Iteration-Level Scheduling", "continuous batching")
        col_labels = VGroup(*[chip(f"t{i}", YELLOW, 17, 0.75, 0.38, 0.12) for i in range(1, 5)]).arrange(RIGHT, buff=0.45).move_to(UP*1.35)
        row_y = [0.60, 0.00, -0.60]
        slots = VGroup()
        entries = [
            ["A", "B", "C"],
            ["A✓", "B", "C"],
            ["E", "B", "C"],
            ["E", "B✓", "F"],
        ]
        color_map = {"A": BLUE, "B": GREEN, "C": ORANGE, "E": PURPLE, "F": TEAL}
        for c in range(4):
            for r in range(3):
                raw = entries[c][r]
                key = raw.replace("✓", "")
                item = block(raw, color_map[key], 0.82, 0.44, 0.25, 15)
                item.move_to(col_labels[c].get_center() + DOWN*(0.75 + r*0.60))
                slots.add(item)
        queue = VGroup(chip("Queue", MUTED, 18, 1.25, 0.44, 0.10), chip("E", PURPLE, 18, 0.55, 0.42, 0.18), chip("F", TEAL, 18, 0.55, 0.42, 0.18)).arrange(DOWN, buff=0.15).move_to(RIGHT*4.25+DOWN*0.10)
        flow = chip("batch is a continuous flow", GREEN, 20, 3.95, 0.55, 0.12).move_to(DOWN*2.30)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(col_labels), FadeIn(queue, shift=LEFT), run_time=t(0.9))
        self.play(LaggedStart(*[FadeIn(slots[i]) for i in range(3)], lag_ratio=0.08), run_time=t(0.8))
        self.play(LaggedStart(*[FadeIn(slots[i]) for i in range(3, 6)], lag_ratio=0.08), Circumscribe(slots[3], color=GREEN), run_time=t(0.9))
        self.play(Create(arrow(queue[1].get_left(), slots[6].get_right(), PURPLE)), FadeIn(slots[6]), FadeIn(slots[7]), FadeIn(slots[8]), run_time=t(1.2))
        self.play(Create(arrow(queue[2].get_left(), slots[11].get_right(), TEAL)), FadeIn(slots[9]), FadeIn(slots[10]), FadeIn(slots[11]), run_time=t(1.2))
        self.play(FadeIn(flow, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_20_05_conveyor(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_05_conveyor.mp3")
        title = title_text("Continuous Batching", "băng chuyền không dừng")
        belt = RoundedRectangle(width=7.40, height=0.82, corner_radius=0.18, stroke_color=MUTED, stroke_width=2.4, fill_color=GRAY, fill_opacity=0.08).move_to(UP*0.45)
        rollers = VGroup(*[Circle(radius=0.14, stroke_color=MUTED, fill_color=MUTED, fill_opacity=0.25, stroke_width=1.8) for _ in range(8)]).arrange(RIGHT, buff=0.70).move_to(belt)
        reqs = VGroup(
            chip("A", BLUE, 18, 0.58, 0.42, 0.18),
            chip("B", GREEN, 18, 0.58, 0.42, 0.18),
            chip("C", ORANGE, 18, 0.58, 0.42, 0.18),
            chip("D", PURPLE, 18, 0.58, 0.42, 0.18),
        ).arrange(RIGHT, buff=0.65).move_to(UP*0.48)
        done = chip("done", GREEN, 15, 0.95, 0.38, 0.12).move_to(LEFT*4.45+DOWN*0.45)
        new = chip("E", TEAL, 18, 0.58, 0.42, 0.18).move_to(RIGHT*4.35+UP*0.48)
        pulse = chip("iteration tick", YELLOW, 18, 2.05, 0.50, 0.12).move_to(UP*1.55)
        util1 = chip("more utilization", GREEN, 22, 2.95, 0.62, 0.14).move_to(DOWN*1.65)
        count1 = chip("throughput +", YELLOW, 20, 2.10, 0.52, 0.12).move_to(DOWN*2.35)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(belt), FadeIn(rollers), FadeIn(reqs), run_time=t(1.2))
        self.play(FadeIn(pulse, shift=DOWN), Rotate(rollers, angle=PI/2), reqs.animate.shift(LEFT*0.55), run_time=t(1.1))
        self.play(reqs[0].animate.move_to(done.get_center()), FadeIn(done), FadeIn(new, shift=LEFT), run_time=t(1.1))
        self.play(new.animate.move_to(reqs[-1].get_center()+RIGHT*0.55), Rotate(rollers, angle=PI/2), run_time=t(1.0))
        self.play(FadeIn(util1, shift=UP), FadeIn(count1, shift=UP), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_20_06_prefill_decode(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_06_prefill_decode.mp3")
        title = title_text("Prefill vs Decode")
        request = chip("Request", YELLOW, 20, 1.65, 0.55, 0.13).move_to(LEFT*4.30+UP*0.40)
        prefill = bar("Prefill", 2.75, ORANGE, 0.78, 24, 0.22).move_to(LEFT*1.85+UP*0.40)
        decode_blocks = VGroup(*[block("D", BLUE, 0.48, 0.48, 0.22, 14) for _ in range(7)]).arrange(RIGHT, buff=0.08).move_to(RIGHT*1.90+UP*0.40)
        arr1 = arrow(request.get_right(), prefill.get_left(), ORANGE)
        arr2 = arrow(prefill.get_right(), decode_blocks.get_left(), BLUE)
        comp = chip("compute-heavy", ORANGE, 18, 2.25, 0.50, 0.12).next_to(prefill, DOWN, buff=0.35)
        mem = chip("memory / KV-heavy", BLUE, 18, 2.60, 0.50, 0.12).next_to(decode_blocks, DOWN, buff=0.35)
        kv = chip("KV Cache", TEAL, 20, 1.70, 0.54, 0.14).move_to(DOWN*1.65)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(request, shift=RIGHT), run_time=t(0.6))
        self.play(Create(arr1), GrowFromEdge(prefill, LEFT), FadeIn(comp, shift=UP), run_time=t(1.4))
        self.play(Create(arr2), LaggedStart(*[FadeIn(d, shift=RIGHT*0.06) for d in decode_blocks], lag_ratio=0.08), FadeIn(mem, shift=UP), run_time=t(1.5))
        self.play(FadeIn(kv, shift=UP), Create(arrow(prefill.get_bottom(), kv.get_top(), TEAL)), Create(arrow(kv.get_top()+RIGHT*0.65, decode_blocks.get_bottom(), TEAL)), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_20_07_long_prefill_blocks(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_07_long_prefill_blocks.mp3")
        title = title_text("Long Prefill Can Block Decode")
        streams = VGroup()
        colors = [BLUE, GREEN, PURPLE]
        for r in range(3):
            label = chip(f"Decode {r+1}", colors[r], 15, 1.35, 0.38, 0.12).move_to(LEFT*4.35+UP*(0.70-r*0.55))
            toks = VGroup(*[block("", colors[r], 0.32, 0.28, 0.23) for _ in range(8)]).arrange(RIGHT, buff=0.05).next_to(label, RIGHT, buff=0.25)
            streams.add(VGroup(label, toks))
        long_prefill = bar("LONG PREFILL", 5.80, ORANGE, 0.66, 22, 0.30).move_to(UP*1.85)
        stall = chip("streaming stalls", RED, 22, 2.75, 0.60, 0.14).move_to(DOWN*2.00)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(s[0]) for s in streams], lag_ratio=0.10), run_time=t(0.7))
        self.play(LaggedStart(*[LaggedStart(*[FadeIn(tok) for tok in s[1]], lag_ratio=0.04) for s in streams], lag_ratio=0.12), run_time=t(1.6))
        self.play(FadeIn(long_prefill, shift=DOWN), run_time=t(0.8))
        self.play(long_prefill.animate.move_to(RIGHT*1.55+UP*0.75), streams.animate.shift(DOWN*0.75), run_time=t(1.0))
        pause = VGroup(*[
            Line(s[1].get_left(), s[1].get_right(), color=RED, stroke_width=5).move_to(s[1])
            for s in streams
        ])
        self.play(FadeIn(pause), FadeIn(stall, shift=UP), Flash(long_prefill, color=RED), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_20_08_chunked_prefill(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_08_chunked_prefill.mp3")
        title = title_text("Chunked Prefill")
        prompt = bar("long prompt", 6.60, ORANGE, 0.62, 22, 0.22).move_to(UP*1.30)
        chunks = VGroup(*[bar(f"P{i}", 1.25, ORANGE, 0.48, 18, 0.24) for i in range(1, 5)]).arrange(RIGHT, buff=0.18).move_to(UP*0.45)
        timeline = VGroup(
            block("D", BLUE, 0.62, 0.44, 0.24, 15),
            bar("P1", 1.00, ORANGE, 0.44, 15, 0.24),
            block("D", BLUE, 0.62, 0.44, 0.24, 15),
            bar("P2", 1.00, ORANGE, 0.44, 15, 0.24),
            block("D", BLUE, 0.62, 0.44, 0.24, 15),
            bar("P3", 1.00, ORANGE, 0.44, 15, 0.24),
            block("D", BLUE, 0.62, 0.44, 0.24, 15),
            bar("P4", 1.00, ORANGE, 0.44, 15, 0.24),
        ).arrange(RIGHT, buff=0.12).move_to(DOWN*0.85)
        decode_stream = VGroup(*[block("", BLUE, 0.32, 0.26, 0.24) for _ in range(11)]).arrange(RIGHT, buff=0.05).move_to(DOWN*1.65)
        note = chip("interleave prefill with decode", GREEN, 20, 4.10, 0.55, 0.12).move_to(DOWN*2.35)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(prompt, shift=DOWN), run_time=t(0.8))
        self.play(ReplacementTransform(prompt.copy(), chunks), run_time=t(1.2))
        self.play(LaggedStart(*[FadeIn(item, shift=UP*0.10) for item in timeline], lag_ratio=0.08), run_time=t(1.8))
        self.play(LaggedStart(*[FadeIn(tok) for tok in decode_stream], lag_ratio=0.035), FadeIn(note, shift=UP), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_20_09_priority_slo(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_09_priority_slo.mp3")
        title = title_text("Scheduling Objectives", "throughput, latency, fairness, SLO")
        sched = chip("Scheduler", BLUE, 28, 2.35, 0.85, 0.16).move_to(ORIGIN)
        objs = [
            chip("Throughput", GREEN, 19, 1.90, 0.50, 0.12).move_to(LEFT*3.55+UP*1.15),
            chip("Latency", RED, 19, 1.55, 0.50, 0.12).move_to(RIGHT*3.55+UP*1.15),
            chip("Fairness", PURPLE, 19, 1.65, 0.50, 0.12).move_to(LEFT*3.55+DOWN*1.15),
            chip("SLO", YELLOW, 19, 1.10, 0.50, 0.12).move_to(RIGHT*3.55+DOWN*1.15),
        ]
        arrows = VGroup(*[DoubleArrow(sched.get_center(), obj.get_center(), buff=0.75, color=obj[0].get_stroke_color(), stroke_width=2.5) for obj in objs])
        slo_note = T("Service Level Objective", 16, MUTED).next_to(objs[3], DOWN, buff=0.10)
        scale = VGroup(chip("throughput", GREEN, 16, 1.55, 0.40, 0.12), DoubleArrow(LEFT, RIGHT, color=YELLOW).scale(0.60), chip("latency", RED, 16, 1.20, 0.40, 0.12)).arrange(RIGHT, buff=0.18).move_to(DOWN*2.35)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(sched, scale=1.05), run_time=t(0.8))
        self.play(LaggedStart(*[FadeIn(obj, shift=(obj.get_center()-sched.get_center())*0.08) for obj in objs], lag_ratio=0.10), run_time=t(1.2))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), FadeIn(slo_note), run_time=t(1.2))
        self.play(FadeIn(scale, shift=UP), Circumscribe(sched, color=YELLOW), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_20_10_disaggregation(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_10_disaggregation.mp3")
        title = title_text("Prefill-Decode Disaggregation")
        pre_cluster = VGroup(*[gpu_chip(f"P{i}", ORANGE, 1.05, 0.70) for i in range(3)]).arrange(RIGHT, buff=0.18)
        dec_cluster = VGroup(*[gpu_chip(f"D{i}", BLUE, 1.05, 0.70) for i in range(4)]).arrange_in_grid(rows=2, cols=2, buff=(0.18, 0.18))
        pre_box = VGroup(SurroundingRectangle(pre_cluster, color=ORANGE, buff=0.20, corner_radius=0.12), pre_cluster).move_to(LEFT*2.45+UP*0.25)
        dec_box = VGroup(SurroundingRectangle(dec_cluster, color=BLUE, buff=0.20, corner_radius=0.12), dec_cluster).move_to(RIGHT*2.95+UP*0.25)
        pre_label = T("Prefill Workers", 20, ORANGE, BOLD).next_to(pre_box, UP, buff=0.16)
        dec_label = T("Decode Workers", 20, BLUE, BOLD).next_to(dec_box, UP, buff=0.16)
        request = chip("request", YELLOW, 18, 1.25, 0.48, 0.14)
        request.next_to(pre_box, LEFT, buff=0.42)
        state = chip("KV/state", TEAL, 18, 1.30, 0.48, 0.14)
        state.next_to(pre_box, RIGHT, buff=0.38)
        output = chip("stream output", GREEN, 18, 1.85, 0.48, 0.14).move_to(RIGHT*5.35+UP*0.25)
        note = chip("more optimized, more complex", RED, 20, 4.00, 0.56, 0.13).move_to(DOWN*1.95)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(pre_box), FadeIn(dec_box), FadeIn(pre_label), FadeIn(dec_label), run_time=t(1.2))
        self.play(FadeIn(request, shift=RIGHT), Create(arrow(request.get_right(), pre_box.get_left(), ORANGE)), run_time=t(0.9))
        self.play(FadeIn(state, shift=RIGHT), Create(arrow(pre_box.get_right(), state.get_left(), TEAL)), run_time=t(1.0))
        self.play(Create(arrow(state.get_right(), dec_box.get_left(), TEAL)), FadeIn(output, shift=LEFT), Create(arrow(dec_box.get_right(), output.get_left(), GREEN)), run_time=t(1.2))
        self.play(FadeIn(note, shift=UP), Circumscribe(state, color=TEAL), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_20_11_full_timeline(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_11_full_timeline.mp3")
        title = title_text("Serving Loop", "queue -> prefill -> decode -> reusable slot")
        steps = VGroup(
            chip("Queue", MUTED, 19, 1.25, 0.58, 0.10),
            chip("Prefill", ORANGE, 19, 1.45, 0.58, 0.14),
            chip("Chunked\nPrefill", ORANGE, 17, 1.45, 0.72, 0.14),
            chip("Decode\nPool", BLUE, 18, 1.45, 0.72, 0.14),
            chip("Finish", GREEN, 19, 1.25, 0.58, 0.14),
            chip("Slot Pool", TEAL, 19, 1.45, 0.58, 0.14),
        ).arrange(RIGHT, buff=0.26).move_to(UP*0.40)
        arrows = VGroup(*[arrow(steps[i].get_right(), steps[i+1].get_left(), YELLOW, 2.4) for i in range(len(steps)-1)])
        req = Dot(steps[0].get_center(), color=YELLOW).scale(1.4)
        new_req = chip("new request", PURPLE, 17, 1.65, 0.46, 0.12).move_to(DOWN*1.25+LEFT*2.70)
        reusable = chip("slot reusable", GREEN, 20, 2.35, 0.55, 0.12).move_to(DOWN*2.20)
        loop_arrow = CurvedArrow(steps[-1].get_bottom(), steps[0].get_bottom(), angle=-PI/3, color=TEAL, stroke_width=3)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(s, shift=UP*0.10) for s in steps], lag_ratio=0.08), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), run_time=t(1.8))
        self.play(FadeIn(req), run_time=t(0.3))
        for i in range(1, len(steps)):
            self.play(req.animate.move_to(steps[i].get_center()), run_time=t(0.45))
        self.play(Create(loop_arrow), FadeIn(reusable, shift=UP), run_time=t(1.0))
        self.play(FadeIn(new_req, shift=RIGHT), Create(arrow(new_req.get_right(), steps[0].get_bottom()+DOWN*0.05, PURPLE)), run_time=t(1.1))
        self.finish_audio_scene()

    def scene_20_12_summary_transition(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_20_12_summary_transition.mp3")
        title = title_text("Request Scheduling - Summary")
        cards = VGroup(
            chip("Continuous\nBatching", BLUE, 19, 2.25, 0.86, 0.13),
            chip("Chunked\nPrefill", ORANGE, 19, 2.25, 0.86, 0.13),
            chip("Disaggregation", PURPLE, 19, 2.25, 0.86, 0.13),
        ).arrange(RIGHT, buff=0.35).move_to(UP*0.80)
        scheduler = chip("Scheduler", GREEN, 26, 3.00, 0.72, 0.15).move_to(DOWN*0.35)
        gpu = gpu_chip("GPU", BLUE, 2.15, 1.20).move_to(DOWN*1.70)
        kernel = chip("Next: Kernel Optimization", YELLOW, 23, 4.10, 0.62, 0.14).move_to(RIGHT*3.00+DOWN*2.80)
        down_arrow = arrow(scheduler.get_bottom(), gpu.get_top(), YELLOW, 3)
        next_arrow = arrow(gpu.get_bottom()+RIGHT*0.55, kernel.get_left(), YELLOW, 3)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.12) for card in cards], lag_ratio=0.16), run_time=t(1.4))
        self.play(TransformFromCopy(cards, scheduler), run_time=t(1.1))
        self.play(FadeIn(gpu, shift=UP), Create(down_arrow), run_time=t(1.1))
        self.play(Create(next_arrow), FadeIn(kernel, shift=LEFT), Flash(kernel, color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()
