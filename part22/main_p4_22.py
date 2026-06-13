from manim import *
from pathlib import Path
import json
import subprocess

# ============================================================
# PART 4 - SYSTEM OPTIMIZATIONS
# SCENE 22 - FRAMEWORKS AND CASE STUDY
#
# Render test:
#   py -m manim -pql --disable_caching --progress_bar none main_p4_22.py Part4FrameworksCaseStudy
#
# Render dep:
#   py -m manim -pqh --disable_caching --progress_bar none main_p4_22.py Part4FrameworksCaseStudy
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
    "voice/p4_22_01_intro.mp3": 20.0,
    "voice/p4_22_02_vllm.mp3": 20.0,
    "voice/p4_22_03_tensorrt_deepspeed.mp3": 20.0,
    "voice/p4_22_04_other_frameworks.mp3": 20.0,
    "voice/p4_22_05_workload_choice.mp3": 20.0,
    "voice/p4_22_06_summary.mp3": 20.0,
}
CURRENT_SCALE = 1.0
TAIL_HOLD = 3.0

BASE_ANIMATION_DURATIONS = {
    "voice/p4_22_01_intro.mp3": 6.4,
    "voice/p4_22_02_vllm.mp3": 6.4,
    "voice/p4_22_03_tensorrt_deepspeed.mp3": 6.2,
    "voice/p4_22_04_other_frameworks.mp3": 6.1,
    "voice/p4_22_05_workload_choice.mp3": 6.3,
    "voice/p4_22_06_summary.mp3": 6.0,
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


def block(label="", color=BLUE, width=0.50, height=0.36, fill=FILL_MEDIUM, size=12, stroke=1.6):
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


def arrow(a, b, color=MUTED, width=3):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def gpu_chip(label="GPU", color=BLUE, width=1.50, height=0.92):
    body = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.10)
    pins = VGroup()
    for i in range(5):
        pins.add(Line(UP*0.06, DOWN*0.06, color=color, stroke_width=2).move_to(body.get_left()+RIGHT*0.08+UP*(0.28-i*0.14)))
        pins.add(Line(UP*0.06, DOWN*0.06, color=color, stroke_width=2).move_to(body.get_right()+LEFT*0.08+UP*(0.28-i*0.14)))
    text = T(label, 18, WHITE_C, BOLD).move_to(body)
    return VGroup(body, pins, text)


def mini_server(label, color):
    box = RoundedRectangle(width=1.25, height=0.74, corner_radius=0.10, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.12)
    lights = VGroup(*[Dot(radius=0.035, color=YELLOW).move_to(box.get_left()+RIGHT*0.18+UP*y) for y in [0.18, 0.0, -0.18]])
    text = T(label, 14, WHITE_C, BOLD)
    if text.width > 0.78:
        text.scale_to_fit_width(0.78)
    text.move_to(box.get_center()+RIGHT*0.13)
    return VGroup(box, lights, text)


class Part4FrameworksCaseStudy(Scene):
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
        self.scene_22_01_intro()
        self.scene_22_02_vllm()
        self.scene_22_03_tensorrt_deepspeed()
        self.scene_22_04_other_frameworks()
        self.scene_22_05_workload_choice()
        self.scene_22_06_summary()

    def scene_22_01_intro(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_22_01_intro.mp3")
        title = title_text("Serving Frameworks")
        techniques = VGroup(
            chip("Quantization", ORANGE, 16, 1.80, 0.44, 0.11),
            chip("Parallelism", PURPLE, 16, 1.72, 0.44, 0.11),
            chip("Memory", BLUE, 16, 1.35, 0.44, 0.11),
            chip("Scheduling", GREEN, 16, 1.60, 0.44, 0.11),
            chip("Kernels", YELLOW, 16, 1.35, 0.44, 0.11),
        ).arrange(DOWN, buff=0.13).move_to(LEFT*4.05+DOWN*0.05)
        framework = chip("Serving\nFramework", TEAL, 28, 2.80, 1.10, 0.16).move_to(ORIGIN+UP*0.05)
        players = VGroup(
            chip("memory\nmanager", BLUE, 15, 1.35, 0.62, 0.11).move_to(RIGHT*3.60+UP*1.15),
            chip("scheduler", GREEN, 15, 1.25, 0.44, 0.11).move_to(RIGHT*3.95+UP*0.35),
            chip("kernel\nbackend", YELLOW, 15, 1.32, 0.62, 0.11).move_to(RIGHT*3.60+DOWN*0.50),
            chip("distributed\nruntime", PURPLE, 14, 1.45, 0.62, 0.11).move_to(RIGHT*3.95+DOWN*1.35),
        )
        arrows = VGroup(*[arrow(t.get_right(), framework.get_left(), t[0].get_stroke_color(), 2.4) for t in techniques])
        out_arrows = VGroup(*[arrow(framework.get_right(), p.get_left(), p[0].get_stroke_color(), 2.4) for p in players])
        note = chip("not one trick: a coordinated system", ORANGE, 20, 5.35, 0.58, 0.13).move_to(DOWN*2.35)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT*0.10) for x in techniques], lag_ratio=0.10), run_time=t(1.3))
        self.play(FadeIn(framework, scale=1.04), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), run_time=t(1.4))
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT*0.10) for p in players], lag_ratio=0.10), LaggedStart(*[Create(a) for a in out_arrows], lag_ratio=0.08), run_time=t(1.5))
        self.play(FadeIn(note, shift=UP), Circumscribe(framework, color=TEAL), run_time=t(1.2))
        self.finish_audio_scene()

    def scene_22_02_vllm(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_22_02_vllm.mp3")
        title = title_text("vLLM", "memory và throughput")
        vllm = chip("vLLM", BLUE, 31, 1.95, 0.78, 0.18).move_to(LEFT*4.25+DOWN*0.20)
        kv_blocks = VGroup(*[
            block(f"B{i+1}", [BLUE, GREEN, ORANGE, PURPLE, TEAL][i % 5], 0.43, 0.32, 0.24, 9)
            for i in range(16)
        ]).arrange_in_grid(rows=2, cols=8, buff=(0.08, 0.08)).move_to(RIGHT*0.15+UP*0.55)
        kv_label = T("PagedAttention\nKV blocks", 18, BLUE, BOLD).next_to(kv_blocks, UP, buff=0.18)
        queue = VGroup(*[chip(f"Req {c}", [GREEN, ORANGE, PURPLE, TEAL][i], 14, 0.92, 0.38, 0.12) for i, c in enumerate(["A", "B", "C", "D"])]).arrange(DOWN, buff=0.10).move_to(RIGHT*4.35+UP*0.80)
        batch = chip("continuous\nbatching", GREEN, 17, 1.80, 0.74, 0.13).move_to(RIGHT*4.35+DOWN*0.95)
        throughput = chip("throughput high", YELLOW, 22, 3.10, 0.60, 0.14).move_to(DOWN*2.30)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(vllm, shift=RIGHT), run_time=t(0.8))
        self.play(FadeIn(kv_label), LaggedStart(*[FadeIn(b) for b in kv_blocks], lag_ratio=0.025), run_time=t(1.6))
        self.play(FadeIn(queue, shift=LEFT), run_time=t(0.9))
        q_to_batch = arrow(queue.get_bottom(), batch.get_top(), GREEN, 2.6)
        batch_to_kv = CurvedArrow(batch.get_left()+UP*0.08, kv_blocks.get_bottom()+RIGHT*0.80, angle=-PI/4, color=GREEN, stroke_width=2.8)
        vllm_to_kv = arrow(vllm.get_right(), kv_blocks.get_left(), BLUE, 2.5)
        self.play(Create(vllm_to_kv), Create(q_to_batch), Create(batch_to_kv), FadeIn(batch, shift=UP), run_time=t(1.2))
        self.play(FadeIn(throughput, shift=UP), Flash(kv_blocks, color=BLUE), Circumscribe(batch, color=GREEN), run_time=t(1.4))
        self.finish_audio_scene()

    def scene_22_03_tensorrt_deepspeed(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_22_03_tensorrt_deepspeed.mp3")
        title = title_text("TensorRT-LLM & DeepSpeed", "phần cứng và hạ tầng quyết định")
        divider = Line(UP*1.85, DOWN*1.95, color=MUTED, stroke_width=2)
        trt_title = chip("TensorRT-LLM", GREEN, 21, 2.35, 0.58, 0.14).move_to(LEFT*3.25+UP*1.40)
        ds_title = chip("DeepSpeed\nInference", PURPLE, 20, 2.35, 0.78, 0.14).move_to(RIGHT*3.25+UP*1.40)
        gpu = gpu_chip("NVIDIA", GREEN, 1.85, 1.00).move_to(LEFT*4.05+UP*0.20)
        tensor = chip("Tensor Core", YELLOW, 15, 1.50, 0.42, 0.11).move_to(LEFT*2.25+UP*0.65)
        kernel = chip("optimized\nkernels", ORANGE, 15, 1.45, 0.62, 0.11).move_to(LEFT*2.25+DOWN*0.15)
        triton = chip("Triton\nintegration", TEAL, 15, 1.45, 0.62, 0.11).move_to(LEFT*2.25+DOWN*0.95)
        nodes = VGroup(
            mini_server("GPU 1", BLUE),
            mini_server("GPU 2", BLUE),
            mini_server("GPU 3", BLUE),
            mini_server("GPU 4", BLUE),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.30, 0.28)).move_to(RIGHT*3.25+DOWN*0.15)
        parallel = chip("parallelism + offloading", YELLOW, 18, 3.15, 0.52, 0.12).move_to(RIGHT*3.25+DOWN*1.70)
        note = chip("choose by hardware and infrastructure", ORANGE, 20, 5.55, 0.58, 0.13).move_to(DOWN*2.45)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(Create(divider), FadeIn(trt_title), FadeIn(ds_title), run_time=t(0.8))
        self.play(FadeIn(gpu), FadeIn(tensor), FadeIn(kernel), FadeIn(triton), run_time=t(1.3))
        self.play(Create(arrow(gpu.get_right(), tensor.get_left(), GREEN, 2.4)), Create(arrow(gpu.get_right(), kernel.get_left(), ORANGE, 2.4)), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(n, shift=UP*0.08) for n in nodes], lag_ratio=0.10), run_time=t(1.1))
        links = VGroup(*[Line(nodes[i].get_center(), nodes[j].get_center(), color=PURPLE, stroke_width=2) for i, j in [(0, 1), (0, 2), (1, 3), (2, 3)]])
        self.play(Create(links), FadeIn(parallel, shift=UP), run_time=t(1.2))
        self.play(FadeIn(note, shift=UP), Circumscribe(VGroup(nodes, parallel), color=PURPLE), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_22_04_other_frameworks(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_22_04_other_frameworks.mp3")
        title = title_text("Other Frameworks")
        cards = VGroup(
            chip("FlexGen / ZeRO\nOffloading", ORANGE, 17, 2.20, 0.78, 0.13),
            chip("TGI\nDeployment", GREEN, 18, 2.00, 0.78, 0.13),
            chip("LightLLM\nToken KV", BLUE, 18, 2.00, 0.78, 0.13),
            chip("MLC-LLM\nMulti-backend", PURPLE, 17, 2.20, 0.78, 0.13),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.40)).move_to(UP*0.25)
        gpu = chip("GPU HBM", BLUE, 15, 1.25, 0.40, 0.10).move_to(LEFT*4.50+DOWN*1.65)
        cpu = chip("CPU RAM", GREEN, 15, 1.25, 0.40, 0.10).move_to(LEFT*2.80+DOWN*1.65)
        disk = chip("Disk", ORANGE, 15, 0.95, 0.40, 0.10).move_to(LEFT*1.35+DOWN*1.65)
        deploy = chip("API / container", TEAL, 15, 1.75, 0.40, 0.10).move_to(RIGHT*1.20+DOWN*1.65)
        backend = chip("many devices", PURPLE, 15, 1.75, 0.40, 0.10).move_to(RIGHT*3.70+DOWN*1.65)
        note = chip("integration, offload, KV layout, portability", YELLOW, 19, 5.95, 0.55, 0.12).move_to(DOWN*2.45)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.10) for c in cards], lag_ratio=0.13), run_time=t(1.6))
        self.play(FadeIn(gpu), FadeIn(cpu), FadeIn(disk), Create(arrow(gpu.get_right(), cpu.get_left(), ORANGE, 2.4)), Create(arrow(cpu.get_right(), disk.get_left(), ORANGE, 2.4)), run_time=t(1.2))
        self.play(FadeIn(deploy, shift=UP), FadeIn(backend, shift=UP), run_time=t(0.9))
        self.play(Create(arrow(cards[1].get_bottom(), deploy.get_top(), GREEN, 2.2)), Create(arrow(cards[3].get_bottom(), backend.get_top(), PURPLE, 2.2)), FadeIn(note, shift=UP), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_22_05_workload_choice(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_22_05_workload_choice.mp3")
        title = title_text("Case Study", "chọn framework theo workload")
        workload = chip("Workload", YELLOW, 28, 2.25, 0.78, 0.16).move_to(LEFT*4.15+UP*0.20)
        choices = VGroup(
            chip("many users\nbatching + KV", GREEN, 16, 2.20, 0.70, 0.12),
            chip("model too large\nparallel/offload", ORANGE, 16, 2.20, 0.70, 0.12),
            chip("low latency\nspeculative + kernel", BLUE, 16, 2.20, 0.70, 0.12),
            chip("many platforms\ncompiler/backend", PURPLE, 16, 2.20, 0.70, 0.12),
        ).arrange(DOWN, buff=0.16).move_to(LEFT*1.05+UP*0.05)
        frameworks = VGroup(
            chip("vLLM / TGI", GREEN, 16, 1.75, 0.45, 0.12),
            chip("DeepSpeed\nFlexGen", ORANGE, 16, 1.75, 0.62, 0.12),
            chip("TensorRT-LLM", BLUE, 16, 1.90, 0.45, 0.12),
            chip("MLC-LLM", PURPLE, 16, 1.45, 0.45, 0.12),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT*3.55+UP*0.05)
        arrows = VGroup(*[
            arrow(choices[i].get_right(), frameworks[i].get_left(), choices[i][0].get_stroke_color(), 2.4)
            for i in range(4)
        ])
        start = arrow(workload.get_right(), choices.get_left(), YELLOW, 3)
        note = chip("start from workload, not from hype", RED, 21, 4.95, 0.58, 0.13).move_to(DOWN*2.35)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(FadeIn(workload, shift=RIGHT), Create(start), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*0.10) for c in choices], lag_ratio=0.10), run_time=t(1.4))
        self.play(LaggedStart(*[FadeIn(f, shift=LEFT*0.10) for f in frameworks], lag_ratio=0.10), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.10), run_time=t(1.6))
        self.play(FadeIn(note, shift=UP), Circumscribe(workload, color=YELLOW), run_time=t(1.3))
        self.finish_audio_scene()

    def scene_22_06_summary(self):
        self.fade_clear(); self.start_audio_scene("voice/p4_22_06_summary.mp3")
        title = title_text("Frameworks - Summary")
        cards = VGroup(
            chip("vLLM\nKV + throughput", BLUE, 16, 1.90, 0.72, 0.13),
            chip("TensorRT-LLM\nNVIDIA", GREEN, 16, 1.90, 0.72, 0.13),
            chip("FlexGen\nmemory limit", ORANGE, 16, 1.75, 0.72, 0.13),
            chip("TGI\ndeployment", TEAL, 16, 1.60, 0.72, 0.13),
            chip("MLC-LLM\nportable", PURPLE, 16, 1.70, 0.72, 0.13),
        ).arrange(RIGHT, buff=0.16).move_to(UP*0.90)
        tradeoffs = chip("Framework = a bundle of trade-offs", YELLOW, 25, 5.50, 0.72, 0.15).move_to(DOWN*0.35)
        workload = chip("best choice = fit your workload", GREEN, 23, 4.85, 0.65, 0.14).move_to(DOWN*1.55)
        next_box = chip("End of System Optimizations", ORANGE, 22, 4.60, 0.62, 0.13).move_to(DOWN*2.45)
        self.play(FadeIn(title, shift=DOWN), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(card, shift=UP*0.12) for card in cards], lag_ratio=0.12), run_time=t(1.6))
        self.play(TransformFromCopy(cards, tradeoffs), run_time=t(1.2))
        self.play(FadeIn(workload, shift=UP), Circumscribe(tradeoffs, color=YELLOW), run_time=t(1.2))
        self.play(FadeIn(next_box, shift=UP), Flash(workload, color=GREEN), run_time=t(1.2))
        self.finish_audio_scene()
