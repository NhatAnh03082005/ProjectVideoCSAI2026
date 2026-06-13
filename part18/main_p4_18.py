from manim import *
from pathlib import Path
import json
import subprocess
import numpy as np

# ============================================================
# PART 4 — SYSTEM OPTIMIZATIONS
# SCENE 18 — PARALLEL COMPUTATION
#
# Render test:
#   py -m manim -pql --disable_caching main_p4_18.py Part4ParallelComputation
#
# Render đẹp:
#   py -m manim -pqh --disable_caching main_p4_18.py Part4ParallelComputation
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
FILL_SOFT = 0.12
FILL_MEDIUM = 0.20
config.background_color = BG


def text_font_for(text):
    return VIETNAMESE_FONT if any(ch in VIETNAMESE_CHARS for ch in str(text)) else FONT

try:
    from mutagen.mp3 import MP3
except Exception:
    MP3 = None

FALLBACK_SCENE_DURATIONS = {
    "voice/p4_18_01_problem.mp3": 20.0,
    "voice/p4_18_02_model_parallelism.mp3": 20.0,
    "voice/p4_18_03_tensor_parallel.mp3": 20.0,
    "voice/p4_18_04_tensor_tradeoff.mp3": 20.0,
    "voice/p4_18_05_pipeline_parallel.mp3": 20.0,
    "voice/p4_18_06_pipeline_bubble.mp3": 20.0,
    "voice/p4_18_07_sequence_parallel.mp3": 20.0,
    "voice/p4_18_08_sequence_communication.mp3": 20.0,
    "voice/p4_18_09_cloud_scaling.mp3": 20.0,
    "voice/p4_18_10_decentralized.mp3": 20.0,
    "voice/p4_18_11_which_parallelism.mp3": 20.0,
    "voice/p4_18_12_summary_transition.mp3": 20.0,
}
CURRENT_SCALE = 1.0
TAIL_HOLD = 3.0

BASE_ANIMATION_DURATIONS = {
    "voice/p4_18_01_problem.mp3": 6.6,
    "voice/p4_18_02_model_parallelism.mp3": 7.9,
    "voice/p4_18_03_tensor_parallel.mp3": 7.9,
    "voice/p4_18_04_tensor_tradeoff.mp3": 6.0,
    "voice/p4_18_05_pipeline_parallel.mp3": 6.1,
    "voice/p4_18_06_pipeline_bubble.mp3": 5.0,
    "voice/p4_18_07_sequence_parallel.mp3": 6.7,
    "voice/p4_18_08_sequence_communication.mp3": 5.7,
    "voice/p4_18_09_cloud_scaling.mp3": 5.6,
    "voice/p4_18_10_decentralized.mp3": 5.5,
    "voice/p4_18_11_which_parallelism.mp3": 5.85,
    "voice/p4_18_12_summary_transition.mp3": 5.5,
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
    box = RoundedRectangle(width=width if width else label.width + 0.52, height=height if height else label.height + 0.26, corner_radius=0.12, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill)
    if label.width > box.width - 0.36:
        label.scale_to_fit_width(box.width - 0.36)
    if label.height > box.height - 0.18:
        label.scale_to_fit_height(box.height - 0.18)
    label.move_to(box)
    return VGroup(box, label)


def gpu(name, width=1.65, height=1.00, color=BLUE):
    body = RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.10)
    label = T(name, size=19, color=WHITE_C, weight=BOLD)
    label.move_to(body.get_center() + UP * 0.16)
    return VGroup(body, label)


def arrow(a, b, color=MUTED, width=3):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def mini_cross(color=RED):
    return VGroup(Line(LEFT*0.20+UP*0.20, RIGHT*0.20+DOWN*0.20, color=color, stroke_width=6), Line(LEFT*0.20+DOWN*0.20, RIGHT*0.20+UP*0.20, color=color, stroke_width=6))


class Part4ParallelComputation(Scene):
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
        self.scene_18_01_problem()
        self.scene_18_02_model_parallelism()
        self.scene_18_03_tensor_parallel()
        self.scene_18_04_tensor_tradeoff()
        self.scene_18_05_pipeline_parallel()
        self.scene_18_06_pipeline_bubble()
        self.scene_18_07_sequence_parallel()
        self.scene_18_08_sequence_communication()
        self.scene_18_09_cloud_scaling()
        self.scene_18_10_decentralized()
        self.scene_18_11_choose_method()
        self.scene_18_12_summary_transition()

    def scene_18_01_problem(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_01_problem.mp3")
        title = title_text("Parallel Computation")
        one_gpu = gpu("GPU", 3.0, 1.60, BLUE).move_to(DOWN*0.10)
        vram = Rectangle(width=2.30, height=0.22, fill_color=RED, fill_opacity=0.75, stroke_width=0).move_to(one_gpu.get_center()+DOWN*0.28)
        vram_label = T("VRAM full", 18, RED, BOLD).next_to(one_gpu, DOWN, buff=0.12)
        llm = chip("Large LLM", YELLOW, 24, 4.80, 0.72, 0.12).move_to(UP*1.15)
        x = mini_cross().next_to(one_gpu, RIGHT, buff=0.30)
        b1 = chip("model too large", RED, 18, 2.30, 0.50).move_to(LEFT*2.45 + DOWN*1.35)
        b2 = chip("too many requests", ORANGE, 18, 2.55, 0.50).move_to(RIGHT*2.45 + DOWN*1.35)
        gpus = VGroup(*[gpu(f"GPU{i}", 1.25, 0.82, [BLUE,GREEN,PURPLE,ORANGE][i]) for i in range(4)]).arrange(RIGHT, buff=0.28).move_to(DOWN*0.10)
        taxonomy = VGroup(chip("model parallelism", BLUE, 15, 2.20, 0.44), chip("sequence parallelism", GREEN, 15, 2.40, 0.44), chip("cloud scaling", YELLOW, 15, 1.75, 0.44), chip("decentralized inference", PURPLE, 15, 2.65, 0.44)).arrange(RIGHT, buff=0.18).move_to(DOWN*2.35)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(llm), FadeIn(one_gpu), FadeIn(vram), run_time=t(1.2))
        self.play(FadeIn(x, scale=1.15), FadeIn(vram_label), run_time=t(0.9))
        self.play(FadeIn(b1, shift=UP), FadeIn(b2, shift=UP), run_time=t(1.1))
        self.play(FadeOut(one_gpu), FadeOut(vram), FadeOut(vram_label), FadeOut(x), FadeOut(llm), FadeIn(gpus), run_time=t(1.2))
        self.play(FadeIn(taxonomy, shift=UP), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_18_02_model_parallelism(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_02_model_parallelism.mp3")
        title = title_text("Model Parallelism")
        table = RoundedRectangle(width=3.2, height=0.34, corner_radius=0.06, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.10).move_to(DOWN*0.75)
        table_label = T("one GPU table", 18, BLUE).next_to(table, DOWN, buff=0.10)
        book = RoundedRectangle(width=5.2, height=1.15, corner_radius=0.12, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.14).move_to(UP*0.55)
        book_text = T("Huge LLM Book", 25, WHITE_C, BOLD).move_to(book)
        big_book = VGroup(book, book_text)
        over = mini_cross().next_to(book, RIGHT, buff=0.25)
        vols = VGroup(chip("Volume A", BLUE, 19, 1.65, 0.72), chip("Volume B", GREEN, 19, 1.65, 0.72), chip("Volume C", ORANGE, 19, 1.65, 0.72)).arrange(RIGHT, buff=0.25).move_to(UP*0.35)
        gpu_tables = VGroup(gpu("GPU0",1.55,0.85,BLUE), gpu("GPU1",1.55,0.85,GREEN), gpu("GPU2",1.55,0.85,ORANGE)).arrange(RIGHT,buff=0.45).move_to(DOWN*0.95)
        note = chip("parameters / layers are split", PURPLE, 19, 3.95, 0.54).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(table), FadeIn(table_label), FadeIn(big_book, shift=DOWN), run_time=t(1.3))
        self.play(FadeIn(over, scale=1.15), Flash(big_book, color=RED), run_time=t(1.0))
        self.play(ReplacementTransform(big_book, vols), FadeOut(over), run_time=t(1.3))
        self.play(FadeIn(gpu_tables, shift=UP), FadeOut(table), FadeOut(table_label), run_time=t(1.0))
        self.play(*[vols[i].animate.next_to(gpu_tables[i], UP, buff=0.12) for i in range(3)], run_time=t(1.3))
        self.play(FadeIn(note, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_18_03_tensor_parallel(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_03_tensor_parallel.mp3")
        title = title_text("Tensor Parallelism")
        x = chip("x", BLUE, 28, 1.20, 0.70).move_to(LEFT*3.6+UP*1.10)
        w = chip("W", YELLOW, 30, 2.10, 1.25).move_to(UP*1.10)
        y = chip("y", GREEN, 28, 1.20, 0.70).move_to(RIGHT*3.6+UP*1.10)
        eq = T("x × W = y", 28, WHITE_C, BOLD).move_to(UP*2.05)
        arrows = VGroup(arrow(x.get_right(), w.get_left()), arrow(w.get_right(), y.get_left()))
        w1 = chip("W1", BLUE, 22, 1.05, 0.85).move_to(w.get_center()+LEFT*0.55)
        w2 = chip("W2", ORANGE, 22, 1.05, 0.85).move_to(w.get_center()+RIGHT*0.55)
        g0 = gpu("GPU0",2.15,1.20,BLUE).move_to(LEFT*2.0+DOWN*0.65)
        g1 = gpu("GPU1",2.15,1.20,ORANGE).move_to(RIGHT*2.0+DOWN*0.65)
        p1 = chip("partial y1", BLUE, 18, 1.55, 0.45).move_to(g0.get_center()+DOWN*0.22)
        p2 = chip("partial y2", ORANGE, 18, 1.55, 0.45).move_to(g1.get_center()+DOWN*0.22)
        final = chip("all-reduce / concat → final y", GREEN, 18, 3.55, 0.55).move_to(DOWN*2.05)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(eq), FadeIn(x), FadeIn(w), FadeIn(y), Create(arrows), run_time=t(1.5))
        self.play(ReplacementTransform(w.copy(), VGroup(w1,w2)), run_time=t(1.1))
        self.play(FadeIn(g0), FadeIn(g1), run_time=t(1.0))
        self.play(w1.animate.next_to(g0, UP, buff=0.12), w2.animate.next_to(g1, UP, buff=0.12), run_time=t(1.2))
        self.play(FadeIn(p1, shift=UP), FadeIn(p2, shift=UP), run_time=t(0.9))
        self.play(Create(arrow(p1.get_bottom(), final.get_top()+LEFT*0.65)), Create(arrow(p2.get_bottom(), final.get_top()+RIGHT*0.65)), FadeIn(final, shift=UP), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_18_04_tensor_tradeoff(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_04_tensor_tradeoff.mp3")
        title = title_text("Tensor Parallel Trade-off", "compute saved vs communication cost")
        board = RoundedRectangle(width=4.80, height=1.40, corner_radius=0.12, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.08).move_to(UP*0.85)
        divider = Line(UP*0.60, DOWN*0.60, color=YELLOW, stroke_width=3).move_to(board)
        left_half = T("half A", 22, BLUE).move_to(board.get_center()+LEFT*1.2)
        right_half = T("half B", 22, ORANGE).move_to(board.get_center()+RIGHT*1.2)
        worker1 = VGroup(Circle(radius=0.20, color=BLUE, fill_color=BLUE, fill_opacity=0.40), Line(DOWN*0.2, DOWN*0.75, color=BLUE, stroke_width=4)).move_to(LEFT*2.2+DOWN*0.70)
        worker2 = VGroup(Circle(radius=0.20, color=ORANGE, fill_color=ORANGE, fill_opacity=0.40), Line(DOWN*0.2, DOWN*0.75, color=ORANGE, stroke_width=4)).move_to(RIGHT*2.2+DOWN*0.70)
        fast = VGroup(DoubleArrow(LEFT, RIGHT, color=GREEN, stroke_width=5).scale(1.15), T("NVLink fast", 20, GREEN, BOLD)).arrange(DOWN,buff=0.10).move_to(DOWN*0.55)
        slow = VGroup(DoubleArrow(LEFT, RIGHT, color=RED, stroke_width=3).scale(1.15), T("slow network delay", 20, RED, BOLD)).arrange(DOWN,buff=0.10).move_to(DOWN*0.55)
        balance = VGroup(chip("compute saved", GREEN, 18, 2.20, 0.50), DoubleArrow(LEFT, RIGHT, color=YELLOW).scale(0.70), chip("comm cost", RED, 18, 1.70, 0.50)).arrange(RIGHT, buff=0.25).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(board), Create(divider), FadeIn(left_half), FadeIn(right_half), FadeIn(worker1), FadeIn(worker2), run_time=t(1.5))
        self.play(FadeIn(fast), run_time=t(1.0))
        self.play(Transform(fast, slow), worker2.animate.shift(RIGHT*0.8), run_time=t(1.2))
        self.play(FadeIn(balance, shift=UP), Circumscribe(balance, color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_18_05_pipeline_parallel(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_05_pipeline_parallel.mp3")
        title = title_text("Pipeline Parallelism")
        stages = VGroup(chip("Layers 1–10", BLUE, 20, 2.15, 0.70), chip("Layers 11–20", GREEN, 20, 2.25, 0.70), chip("Layers 21–30", ORANGE, 20, 2.25, 0.70)).arrange(RIGHT, buff=0.50).move_to(UP*0.80)
        gpus = VGroup(gpu("GPU1",2.15,1.00,BLUE), gpu("GPU2",2.15,1.00,GREEN), gpu("GPU3",2.15,1.00,ORANGE)).arrange(RIGHT,buff=0.50).move_to(DOWN*0.55)
        arrows = VGroup(arrow(stages[0].get_right(), stages[1].get_left()), arrow(stages[1].get_right(), stages[2].get_left()))
        act = Dot(stages[0].get_left()+LEFT*0.40, color=YELLOW).scale(1.2)
        act_label = T("activation", 19, YELLOW).next_to(act, UP, buff=0.12)
        note = chip("factory-like stages", PURPLE, 20, 2.80, 0.54).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(stages), FadeIn(gpus), Create(arrows), run_time=t(1.4))
        self.play(FadeIn(act), FadeIn(act_label), run_time=t(0.6))
        for i in range(3):
            self.play(act.animate.move_to(stages[i].get_center()), act_label.animate.next_to(stages[i], UP, buff=0.15), run_time=t(0.7))
        self.play(FadeIn(note, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_18_06_pipeline_bubble(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_06_pipeline_bubble.mp3")
        title = title_text("Pipeline Bubble")
        row_labels = VGroup(T("GPU1",20,BLUE), T("GPU2",20,GREEN), T("GPU3",20,ORANGE)).arrange(DOWN,buff=0.34).move_to(LEFT*4.50+UP*0.15)
        cells = VGroup(); bubbles = VGroup(); colors = [BLUE,GREEN,ORANGE]
        schedule = {(0,0):"MB1",(1,1):"MB1",(2,2):"MB1",(0,1):"MB2",(1,2):"MB2",(2,3):"MB2",(0,2):"MB3",(1,3):"MB3",(2,4):"MB3"}
        start = LEFT*3.45+UP*0.75
        for r in range(3):
            for c in range(5):
                pos = start + RIGHT*c*1.15 + DOWN*r*0.70
                if (r,c) in schedule:
                    cell = chip(schedule[(r,c)], colors[r], 15, 0.88, 0.44, fill=0.18)
                else:
                    cell = RoundedRectangle(width=0.88,height=0.44,corner_radius=0.08,stroke_color=RED,fill_color=RED,fill_opacity=0.05,stroke_width=1.8)
                    bubbles.add(cell)
                cell.move_to(pos); cells.add(cell)
        bubble_label = chip("bubble", RED, 18, 1.28, 0.48).move_to(RIGHT*3.55+DOWN*0.10)
        note = chip("more micro-batches fill gaps", GREEN, 19, 3.45, 0.54).move_to(DOWN*2.20)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(row_labels), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.025), run_time=t(2.0))
        self.play(Flash(bubbles, color=RED), FadeIn(bubble_label), run_time=t(1.0))
        self.play(FadeIn(note, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_18_07_sequence_parallel(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_07_sequence_parallel.mp3")
        title = title_text("Sequence Parallelism")
        scroll = RoundedRectangle(width=9.40,height=0.70,corner_radius=0.14,stroke_color=YELLOW,fill_color=YELLOW,fill_opacity=0.08).move_to(UP*1.25)
        scroll_label = T("long context: 100k tokens",22,YELLOW,BOLD).move_to(scroll)
        chunks = VGroup(
            chip("chunk A", BLUE, 18, 1.70, 0.72, 1.00),
            chip("chunk B", GREEN, 18, 1.70, 0.72, 1.00),
            chip("chunk C", ORANGE, 18, 1.70, 0.72, 1.00),
            chip("chunk D", PURPLE, 18, 1.70, 0.72, 1.00),
        ).arrange(RIGHT,buff=0.28).move_to(UP*0.35)
        gpus = VGroup(*[gpu(f"GPU{i}",1.55,0.88,[BLUE,GREEN,ORANGE,PURPLE][i]) for i in range(4)]).arrange(RIGHT,buff=0.42).move_to(DOWN*1.05)
        gpus.set_z_index(1)
        chunks.set_z_index(5)
        load = chip("compute + storage distributed by sequence length", TEAL, 19, 5.60, 0.55).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(scroll), FadeIn(scroll_label), run_time=t(1.1))
        self.play(ReplacementTransform(scroll.copy(), chunks), run_time=t(1.2))
        self.play(FadeIn(gpus, shift=UP), run_time=t(1.0))
        self.play(*[chunks[i].animate.move_to(gpus[i].get_center()) for i in range(4)], run_time=t(1.4))
        self.play(FadeIn(load, shift=UP), run_time=t(1.0))
        self.finish_audio_scene()

    def scene_18_08_sequence_communication(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_08_sequence_communication.mp3")
        title = title_text("Sequence Parallel Communication")
        colors = [BLUE,GREEN,ORANGE,PURPLE]
        positions = [LEFT*2.55+UP*0.80, RIGHT*2.55+UP*0.80, RIGHT*2.55+DOWN*0.90, LEFT*2.55+DOWN*0.90]
        nodes = VGroup(*[gpu(f"GPU{i}",1.75,0.90,colors[i]).move_to(positions[i]) for i in range(4)])
        chunks = VGroup(*[chip(f"tokens {i+1}",colors[i],15,1.30,0.36).move_to(positions[i]+DOWN*0.22) for i in range(4)])
        ring = VGroup(CurvedArrow(positions[0],positions[1],angle=-PI/5,color=YELLOW,stroke_width=3), CurvedArrow(positions[1],positions[2],angle=-PI/5,color=YELLOW,stroke_width=3), CurvedArrow(positions[2],positions[3],angle=-PI/5,color=YELLOW,stroke_width=3), CurvedArrow(positions[3],positions[0],angle=-PI/5,color=YELLOW,stroke_width=3))
        gather = chip("ring / all-gather", YELLOW, 20, 2.55, 0.54).move_to(ORIGIN)
        attn = chip("full attention context", GREEN, 20, 3.25, 0.54).move_to(DOWN*2.20)
        warn = chip("not independent summarization", RED, 18, 3.55, 0.50).move_to(UP*2.05)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(nodes), FadeIn(chunks), run_time=t(1.2))
        self.play(LaggedStart(*[Create(a) for a in ring], lag_ratio=0.12), FadeIn(gather), run_time=t(1.5))
        self.play(FadeIn(warn, shift=DOWN), run_time=t(0.8))
        self.play(FadeIn(attn, shift=UP), Circumscribe(attn, color=GREEN), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_18_09_cloud_scaling(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_09_cloud_scaling.mp3")
        title = title_text("Cloud Scaling")
        axes = Axes(x_range=[0,10,2], y_range=[0,5,1], x_length=5.6, y_length=2.5, axis_config={"color":MUTED,"include_ticks":False}).move_to(LEFT*2.40+UP*0.20)
        curve = axes.plot(lambda x: 1.1 + 3.0*np.exp(-0.5*(x-7.0)**2), color=YELLOW)
        curve_label = T("requests over time",20,YELLOW).next_to(axes, UP, buff=0.18)
        small_cluster = VGroup(gpu("GPU0",1.10,0.70,BLUE),gpu("GPU1",1.10,0.70,BLUE)).arrange(RIGHT,buff=0.15).move_to(RIGHT*2.90+UP*0.75)
        big_cluster = VGroup(*[gpu(f"G{i}",0.82,0.58,GREEN) for i in range(6)]).arrange_in_grid(rows=2,cols=3,buff=(0.18,0.18)).move_to(RIGHT*2.90+DOWN*0.35)
        scale_up = chip("scale up at peak", GREEN, 18, 2.25, 0.50).next_to(big_cluster, DOWN, buff=0.18)
        spot = chip("spot / preemptible cost ↓", YELLOW, 18, 3.05, 0.50).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(Create(axes), Create(curve), FadeIn(curve_label), run_time=t(1.5))
        self.play(FadeIn(small_cluster, shift=UP), run_time=t(0.9))
        self.play(ReplacementTransform(small_cluster.copy(), big_cluster), FadeIn(scale_up, shift=UP), run_time=t(1.3))
        self.play(FadeIn(spot, shift=UP), run_time=t(0.9))
        self.finish_audio_scene()

    def scene_18_10_decentralized(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_10_decentralized.mp3")
        title = title_text("Decentralized Inference")
        center = chip("central data center", BLUE, 20, 3.20, 0.72).move_to(UP*1.20)
        world = RoundedRectangle(width=8.80,height=2.80,corner_radius=0.25,stroke_color=PURPLE,fill_color=PURPLE,fill_opacity=0.06).move_to(DOWN*0.15)
        node_pos = [LEFT*3.2+UP*0.65, LEFT*1.6+DOWN*0.25, ORIGIN+UP*0.65, RIGHT*1.4+DOWN*0.45, RIGHT*3.1+UP*0.35, LEFT*0.2+DOWN*1.05]
        nodes = VGroup(*[Dot(p, color=[BLUE,GREEN,ORANGE,PURPLE,TEAL,YELLOW][i]).scale(1.4) for i,p in enumerate(node_pos)])
        labels = VGroup(*[T(f"N{i}",14,WHITE_C).next_to(nodes[i], DOWN, buff=0.05) for i in range(len(nodes))])
        links = VGroup(*[DashedLine(node_pos[i], node_pos[(i+1)%len(node_pos)], color=MUTED, dash_length=0.08, stroke_width=2) for i in range(len(node_pos))])
        shards = VGroup(*[chip(f"S{i}",[BLUE,GREEN,ORANGE,PURPLE][i%4],14,0.55,0.36).move_to(node_pos[i]+UP*0.28) for i in range(4)])
        warns = VGroup(chip("latency",RED,16,1.20,0.42), chip("bandwidth",ORANGE,16,1.45,0.42), chip("heterogeneous",PURPLE,15,1.80,0.42), chip("privacy",YELLOW,16,1.18,0.42)).arrange(RIGHT,buff=0.18).move_to(DOWN*2.25)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(center), run_time=t(0.8))
        self.play(Transform(center, world), Create(links), FadeIn(nodes), FadeIn(labels), run_time=t(1.5))
        self.play(FadeIn(shards, shift=UP), run_time=t(1.0))
        self.play(FadeIn(warns, shift=UP), Circumscribe(warns, color=RED), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_18_11_choose_method(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_11_which_parallelism.mp3")
        title = title_text("Chọn kỹ thuật theo nút thắt", "không có giải pháp vạn năng")
        rows = [("layer too large","Tensor Parallel",BLUE), ("model too deep","Pipeline Parallel",GREEN), ("long context","Sequence Parallel",ORANGE), ("traffic spike","Cloud Scaling",YELLOW), ("scattered GPUs","Decentralized",PURPLE)]
        board = VGroup()
        for left, right, color in rows:
            l = chip(left,color,18,2.45,0.46); r = chip(right,color,18,2.65,0.46); ar = Arrow(l.get_right(), r.get_left(), buff=0.15, color=color, stroke_width=3)
            board.add(VGroup(l,ar,r).arrange(RIGHT,buff=0.24))
        board.arrange(DOWN,buff=0.22).move_to(DOWN*0.05)
        icons = VGroup(chip("communication",RED,15,1.80,0.40), chip("latency",ORANGE,15,1.05,0.40), chip("cost",YELLOW,15,0.90,0.40)).arrange(RIGHT,buff=0.18).move_to(DOWN*2.40)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(r, shift=UP*0.10) for r in board], lag_ratio=0.15), run_time=t(2.2))
        for row in board:
            self.play(Circumscribe(row, color=YELLOW), run_time=t(0.35))
        self.play(FadeIn(icons, shift=UP), run_time=t(0.9))
        self.finish_audio_scene()

    def scene_18_12_summary_transition(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_18_12_summary_transition.mp3")
        title = title_text("Parallel Computation — Summary")
        model = chip("LLM workload", YELLOW, 26, 4.40, 0.78).move_to(UP*0.85)
        gpus = VGroup(*[gpu(f"GPU{i}",1.25,0.78,[BLUE,GREEN,ORANGE,PURPLE][i]) for i in range(4)]).arrange(RIGHT,buff=0.35).move_to(DOWN*0.25)
        wires = VGroup(*[DoubleArrow(gpus[i].get_right(), gpus[i+1].get_left(), buff=0.08, color=MUTED, stroke_width=2) for i in range(3)])
        costs = VGroup(chip("sync",RED,16,0.85,0.40), chip("scheduling",ORANGE,16,1.45,0.40), chip("state",PURPLE,16,0.90,0.40)).arrange(RIGHT,buff=0.18).move_to(DOWN*1.35)
        mem = RoundedRectangle(width=4.70,height=0.62,corner_radius=0.10,stroke_color=BLUE,fill_color=BLUE,fill_opacity=0.08).move_to(DOWN*2.28)
        kv = Rectangle(width=1.25,height=0.62,stroke_width=0,fill_color=YELLOW,fill_opacity=0.65).align_to(mem, RIGHT)
        kv.move_to([mem.get_right()[0]-kv.width/2, mem.get_center()[1], 0])
        next_label = T("Next: Memory Management / KV Cache",22,YELLOW,BOLD)
        next_label.next_to(mem, UP, buff=0.10)
        mem_label = T("memory + KV cache",16,WHITE_C,BOLD).move_to(mem)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(model), FadeIn(gpus, shift=UP), run_time=t(1.2))
        self.play(Create(wires), run_time=t(0.9))
        self.play(FadeIn(costs, shift=UP), run_time=t(1.0))
        self.play(FadeIn(next_label), FadeIn(mem), FadeIn(kv), FadeIn(mem_label), Flash(kv, color=YELLOW), run_time=t(1.4))
        self.finish_audio_scene()
