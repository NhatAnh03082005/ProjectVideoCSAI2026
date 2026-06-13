from manim import *
from pathlib import Path
import json
import subprocess


# ============================================================
# PART 4 - SYSTEM OPTIMIZATIONS
# SCENE 17 - LOW-BIT QUANTIZATION
#
# Render test:
#   py -m manim -pql main_p4_17_quantization.py Part4LowBitQuantization
#
# Audio expected by the new script:
#   voice/p4_17_01_hook.mp3 ... voice/p4_17_12_summary_transition.mp3
# ============================================================


# ------------------------------------------------------------
# Theme
# ------------------------------------------------------------
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
WHITE = "#e5e7eb"
MUTED = "#94a3b8"

BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"
TEAL = "#2dd4bf"

FILL_SOFT = 0.12
FILL_MEDIUM = 0.18
FILL_STRONG = 0.74

config.background_color = BG


def text_font_for(content):
    return VIETNAMESE_FONT if any(ch in VIETNAMESE_CHARS for ch in str(content)) else FONT


# ------------------------------------------------------------
# Audio timing
# ------------------------------------------------------------
try:
    from mutagen.mp3 import MP3
except Exception:
    MP3 = None


FALLBACK_SCENE_DURATIONS = {
    "voice/p4_17_01_hook.mp3": 20.0,
    "voice/p4_17_02_numbers_inside_model.mp3": 20.0,
    "voice/p4_17_03_precision_as_ruler.mp3": 20.0,
    "voice/p4_17_04_bucket_mapping.mp3": 20.0,
    "voice/p4_17_05_tiny_example.mp3": 20.0,
    "voice/p4_17_06_not_pruning.mp3": 20.0,
    "voice/p4_17_07_precision_levels.mp3": 20.0,
    "voice/p4_17_08_memory_example.mp3": 20.0,
    "voice/p4_17_09_bandwidth.mp3": 20.0,
    "voice/p4_17_10_speed_hardware_kernel.mp3": 20.0,
    "voice/p4_17_11_ptq_qat.mp3": 20.0,
    "voice/p4_17_12_summary_transition.mp3": 20.0,
}

CURRENT_SCALE = 1.0
CURRENT_ANIM_STRETCH = 1.0
CURRENT_WAIT_STRETCH = 1.0

TAIL_WAIT_ARGS = {
    "voice/p4_17_01_hook.mp3": 10.8,
    "voice/p4_17_02_numbers_inside_model.mp3": 9.7,
    "voice/p4_17_03_precision_as_ruler.mp3": 9.3,
    "voice/p4_17_04_bucket_mapping.mp3": 9.7,
    "voice/p4_17_05_tiny_example.mp3": 9.4,
    "voice/p4_17_06_not_pruning.mp3": 10.4,
    "voice/p4_17_07_precision_levels.mp3": 10.4,
    "voice/p4_17_08_memory_example.mp3": 11.5,
    "voice/p4_17_09_bandwidth.mp3": 9.5,
    "voice/p4_17_10_speed_hardware_kernel.mp3": 10.1,
    "voice/p4_17_11_ptq_qat.mp3": 11.3,
    "voice/p4_17_12_summary_transition.mp3": 11.7,
}

TARGET_TAIL_HOLD = 3.0


def get_mp3_duration_no_dependency(audio_path: str):
    try:
        data = Path(audio_path).read_bytes()
    except Exception:
        return None

    i = 0
    if len(data) > 10 and data[0:3] == b"ID3":
        size = (
            ((data[6] & 0x7F) << 21)
            | ((data[7] & 0x7F) << 14)
            | ((data[8] & 0x7F) << 7)
            | (data[9] & 0x7F)
        )
        i = 10 + size

    bitrate_table = {
        ("1", "I"): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
        ("1", "II"): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
        ("1", "III"): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
        ("2", "I"): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
        ("2", "II"): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
        ("2", "III"): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
        ("2.5", "I"): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
        ("2.5", "II"): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
        ("2.5", "III"): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
    }
    sample_rate_table = {
        "1": [44100, 48000, 32000],
        "2": [22050, 24000, 16000],
        "2.5": [11025, 12000, 8000],
    }
    version_map = {0b11: "1", 0b10: "2", 0b00: "2.5"}
    layer_map = {0b11: "I", 0b10: "II", 0b01: "III"}

    total_duration = 0.0
    frame_count = 0
    n = len(data)

    while i + 4 <= n:
        if data[i] != 0xFF or (data[i + 1] & 0xE0) != 0xE0:
            i += 1
            continue

        header = int.from_bytes(data[i:i + 4], "big")
        version_bits = (header >> 19) & 0b11
        layer_bits = (header >> 17) & 0b11
        bitrate_idx = (header >> 12) & 0b1111
        sr_idx = (header >> 10) & 0b11
        padding = (header >> 9) & 0b1

        if version_bits == 0b01 or layer_bits == 0b00:
            i += 1
            continue
        if bitrate_idx == 0 or bitrate_idx == 0b1111 or sr_idx == 0b11:
            i += 1
            continue

        version = version_map.get(version_bits)
        layer = layer_map.get(layer_bits)
        if version is None or layer is None:
            i += 1
            continue

        bitrate = bitrate_table[(version, layer)][bitrate_idx] * 1000
        sample_rate = sample_rate_table[version][sr_idx]

        if layer == "I":
            frame_length = int((12 * bitrate / sample_rate + padding) * 4)
            samples_per_frame = 384
        elif layer == "III" and version != "1":
            frame_length = int(72 * bitrate / sample_rate + padding)
            samples_per_frame = 576
        else:
            frame_length = int(144 * bitrate / sample_rate + padding)
            samples_per_frame = 1152

        if frame_length <= 0:
            i += 1
            continue

        total_duration += samples_per_frame / sample_rate
        frame_count += 1
        i += frame_length

    if frame_count > 3 and total_duration > 0:
        return total_duration
    return None


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
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception:
        pass

    duration = get_mp3_duration_no_dependency(audio_path)
    if duration is not None:
        return duration

    print(f"[WARN] Could not read audio duration: {audio_path}. Using fallback {fallback:.2f}s")
    return fallback


def set_scene_timing(audio_path: str) -> float:
    global CURRENT_SCALE, CURRENT_ANIM_STRETCH, CURRENT_WAIT_STRETCH
    fallback = FALLBACK_SCENE_DURATIONS[audio_path]
    real_duration = get_audio_duration(audio_path, fallback)
    CURRENT_SCALE = real_duration / fallback

    wait_arg = TAIL_WAIT_ARGS.get(audio_path)
    if wait_arg is None:
        CURRENT_ANIM_STRETCH = 1.0
        CURRENT_WAIT_STRETCH = 1.0
    else:
        anim_arg = fallback - wait_arg
        CURRENT_WAIT_STRETCH = TARGET_TAIL_HOLD / wait_arg
        CURRENT_ANIM_STRETCH = (fallback - TARGET_TAIL_HOLD) / anim_arg

    print(
        f"[AUDIO] {audio_path}: {real_duration:.2f}s | "
        f"scale = {CURRENT_SCALE:.3f} | anim = {CURRENT_ANIM_STRETCH:.3f} | wait = {CURRENT_WAIT_STRETCH:.3f}"
    )
    return real_duration


def t(seconds: float) -> float:
    return seconds * CURRENT_SCALE * CURRENT_ANIM_STRETCH


def tw(seconds: float) -> float:
    return seconds * CURRENT_SCALE * CURRENT_WAIT_STRETCH


# ------------------------------------------------------------
# Visual helpers
# ------------------------------------------------------------
def txt(content, font_size=32, color=WHITE, weight=NORMAL, **kwargs):
    kwargs.setdefault("line_spacing", 0.75)
    render_weight = SEMIBOLD if weight == BOLD else weight
    text_kwargs = dict(
        font_size=font_size,
        color=color,
        weight=render_weight,
        **kwargs,
    )
    selected_font = text_font_for(content)
    if selected_font:
        text_kwargs["font"] = selected_font
    return Text(
        content,
        **text_kwargs,
    )


def title_text(content, font_size=40):
    title = txt(content, font_size=font_size, weight=BOLD)
    max_width = config.frame_width - 1.90
    if title.width > max_width:
        title.scale_to_fit_width(max_width)
    title.to_edge(UP, buff=0.42)
    return title


def chip(content, color=BLUE, font_size=22, width=None, height=None, fill_opacity=0.14, label_weight=NORMAL):
    lines = [line.strip() for line in str(content).splitlines() if line.strip()]
    if len(lines) > 1:
        label = VGroup(*[txt(line, font_size=font_size, weight=label_weight) for line in lines]).arrange(DOWN, buff=0.08)
    else:
        label = txt(content, font_size=font_size, weight=label_weight)

    rect_width = width if width else label.width + 0.55
    rect_height = height if height else label.height + 0.34
    rect_width = max(rect_width, label.width + 0.45)
    rect_height = max(rect_height, label.height + 0.32)

    rect = RoundedRectangle(
        corner_radius=0.16,
        width=rect_width,
        height=rect_height,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    if label.width > rect.width - 0.35:
        label.scale_to_fit_width(rect.width - 0.35)
    if label.height > rect.height - 0.22:
        label.scale_to_fit_height(rect.height - 0.22)
    label.move_to(rect)
    return VGroup(rect, label)


def small_note(content, color=MUTED, font_size=19):
    return txt(content, font_size=font_size, color=color)


def gpu_block(width=5.6, height=3.1, title="GPU VRAM", color=BLUE):
    body = RoundedRectangle(
        corner_radius=0.22,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=3,
        fill_color=color,
        fill_opacity=FILL_SOFT,
    )
    label = txt(title, font_size=25, color=color, weight=BOLD)
    label.next_to(body.get_top(), DOWN, buff=0.20)
    return VGroup(body, label)


def network_block(width=3.35, height=1.35, title="LLM"):
    body = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        stroke_color=YELLOW,
        stroke_width=2.5,
        fill_color=YELLOW,
        fill_opacity=0.14,
    )
    nodes = VGroup()
    edges = VGroup()
    layers = []
    for li, count in enumerate([3, 4, 3]):
        x = -width * 0.30 + li * width * 0.30
        layer = []
        for j in range(count):
            y = (j - (count - 1) / 2) * 0.25
            dot = Dot([x, y, 0], radius=0.035, color=YELLOW)
            layer.append(dot)
            nodes.add(dot)
        layers.append(layer)
    for left_layer, right_layer in zip(layers[:-1], layers[1:]):
        for a in left_layer:
            for b in right_layer:
                edges.add(Line(a.get_center(), b.get_center(), color=YELLOW, stroke_width=1, stroke_opacity=0.35))
    net = VGroup(edges, nodes)
    label = txt(title, font_size=28, weight=BOLD)
    label.next_to(net, DOWN, buff=0.10)
    content = VGroup(net, label).move_to(body)
    return VGroup(body, content)


def vram_bar(fill_ratio=0.5, width=5.4, height=0.42, label="VRAM", fill_color=RED, percent=True):
    name = txt(label, font_size=20, color=MUTED, weight=BOLD)
    outline = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=WHITE,
        stroke_width=1.8,
        fill_opacity=0,
    )
    fill = Rectangle(
        width=max(width * fill_ratio, 0.01),
        height=height,
        stroke_width=0,
        fill_color=fill_color,
        fill_opacity=0.84,
    )
    fill.move_to(outline)
    fill.align_to(outline, LEFT)
    name.next_to(outline, LEFT, buff=0.24)
    pct = txt(f"{int(round(fill_ratio * 100))}%", font_size=18, color=fill_color, weight=BOLD)
    pct.next_to(outline, RIGHT, buff=0.18)
    if not percent:
        pct.set_opacity(0)
    return VGroup(name, fill, outline, pct)


def number_grid(rows=4, cols=6, cell_w=0.78, cell_h=0.42, values=None, font_size=14, color=BLUE):
    if values is None:
        values = ["0.7312", "-1.2846", "0.0049", "1.1027", "-0.3821", "0.1984"]

    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            rect = RoundedRectangle(
                corner_radius=0.04,
                width=cell_w,
                height=cell_h,
                stroke_color=color,
                stroke_width=1.2,
                fill_color=color,
                fill_opacity=0.12,
            )
            label = txt(values[(r * cols + c) % len(values)], font_size=font_size, color=WHITE)
            cell = VGroup(rect, label)
            cell.move_to([c * cell_w, -r * cell_h, 0])
            cells.add(cell)
    cells.arrange_in_grid(rows=rows, cols=cols, buff=0.03)
    return cells


def simple_axis(x_range=(-1, 1, 0.5), length=9.5, y=0.0, color=WHITE):
    axis = NumberLine(
        x_range=[x_range[0], x_range[1], x_range[2]],
        length=length,
        include_numbers=False,
        include_ticks=False,
        color=color,
    )
    axis.move_to([0, y, 0])
    return axis


def axis_tick_group(axis, values, height=0.22, color=BLUE, stroke_width=2):
    ticks = VGroup()
    for value in values:
        p = axis.n2p(value)
        ticks.add(Line(p + UP * height / 2, p + DOWN * height / 2, color=color, stroke_width=stroke_width))
    return ticks


def bucket_group(axis, centers, bucket_width, color=GREEN, labels=None, height=0.72):
    buckets = VGroup()
    for i, center in enumerate(centers):
        x0 = axis.n2p(center - bucket_width / 2)[0]
        x1 = axis.n2p(center + bucket_width / 2)[0]
        rect = Rectangle(
            width=abs(x1 - x0),
            height=height,
            stroke_color=color,
            stroke_width=1.8,
            fill_color=color,
            fill_opacity=0.12,
        )
        rect.move_to([axis.n2p(center)[0], axis.get_center()[1], 0])
        if labels:
            label = txt(labels[i], font_size=18, color=color, weight=BOLD)
            label.next_to(rect, DOWN, buff=0.10)
            buckets.add(VGroup(rect, label))
        else:
            buckets.add(rect)
    return buckets


def storage_block(label, value, width, color):
    text = txt(f"{label}  {value}", font_size=22, weight=BOLD)
    box_width = max(width, text.width + 0.58)
    rect = RoundedRectangle(
        corner_radius=0.14,
        width=box_width,
        height=0.62,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.18,
    )
    text.move_to(rect)
    return VGroup(rect, text)


def bit_format_box(name, bits, subtitle, color, width):
    rect = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=2.05,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=0.13,
    )
    name_text = txt(name, font_size=24, weight=BOLD)
    bit_text = txt(f"{bits}-bit", font_size=21, color=color, weight=BOLD)
    sub_text = txt(subtitle, font_size=15, color=MUTED)

    block_count = min(bits, 32)
    cols = 8
    rows = max(1, int((block_count + cols - 1) / cols))
    squares = VGroup()
    for i in range(block_count):
        sq = Square(side_length=0.105, stroke_width=0, fill_color=color, fill_opacity=0.86)
        squares.add(sq)
    squares.arrange_in_grid(rows=rows, cols=cols, buff=0.035)
    squares.scale_to_fit_width(min(width - 0.50, 1.25))

    content = VGroup(name_text, bit_text, squares, sub_text).arrange(DOWN, buff=0.12)
    content.move_to(rect)
    return VGroup(rect, content)


def flow_arrow(a, b, color=MUTED):
    return Arrow(
        a.get_right(),
        b.get_left(),
        buff=0.10,
        color=color,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.16,
    )


def gpu_cluster(scale=1.0):
    cards = VGroup()
    for r in range(2):
        for c in range(3):
            gpu = gpu_block(width=1.55, height=0.92, title="GPU", color=BLUE).scale(0.65)
            gpu.move_to([c * 1.13, -r * 0.78, 0])
            cards.add(gpu)
    cards.arrange_in_grid(rows=2, cols=3, buff=0.26)
    links = VGroup()
    for i in range(len(cards) - 1):
        if i % 3 != 2:
            links.add(Line(cards[i].get_right(), cards[i + 1].get_left(), color=GREEN, stroke_width=2))
    for i in range(3):
        links.add(Line(cards[i].get_bottom(), cards[i + 3].get_top(), color=GREEN, stroke_width=2))
    return VGroup(links, cards).scale(scale)


# ------------------------------------------------------------
# Main Scene
# ------------------------------------------------------------
class Part4LowBitQuantization(Scene):
    def fade_clear(self, run_time=0.35):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=run_time)

    def start_audio_scene(self, audio_path: str):
        set_scene_timing(audio_path)
        audio_file = Path(audio_path).resolve()
        if not audio_file.exists():
            print(f"[WARN] Missing audio for scene: {audio_path}")
            return
        self.renderer.file_writer.add_sound(str(audio_file), time=self.time)

    def construct(self):
        self.scene_17_01_hook()
        self.scene_17_02_numbers_inside_model()
        self.scene_17_03_precision_ruler()
        self.scene_17_04_bucket_mapping()
        self.scene_17_05_tiny_example()
        self.scene_17_06_not_pruning()
        self.scene_17_07_precision_levels()
        self.scene_17_08_memory_footprint()
        self.scene_17_09_bandwidth()
        self.scene_17_10_speed_hardware_kernel()
        self.scene_17_11_ptq_qat()
        self.scene_17_12_summary_transition()

    # --------------------------------------------------------
    # Scene 17.01 - System Optimizations hook
    # --------------------------------------------------------
    def scene_17_01_hook(self):
        self.start_audio_scene("voice/p4_17_01_hook.mp3")

        chapter = title_text("PART 4: SYSTEM OPTIMIZATIONS", font_size=43)
        quant_title = title_text("LOW-BIT QUANTIZATION", font_size=43)

        gpu = gpu_block(width=6.6, height=3.55, title="GPU VRAM")
        gpu.move_to(DOWN * 0.25)

        model = network_block(width=3.85, height=1.55, title="Large LLM")
        model.move_to(gpu.get_center() + UP * 0.20)

        bar_20 = vram_bar(0.20, width=5.20, label="VRAM", fill_color=GREEN)
        bar_20.next_to(gpu, DOWN, buff=0.34)
        bar_95 = vram_bar(0.95, width=5.20, label="VRAM", fill_color=RED)
        bar_95.move_to(bar_20)

        warning = VGroup(
            Triangle(stroke_color=RED, fill_color=RED, fill_opacity=0.22, stroke_width=3).scale(0.32),
            txt("!", font_size=30, color=RED, weight=BOLD),
        )
        warning.move_to(gpu.get_corner(UR) + LEFT * 0.55 + DOWN * 0.55)

        metrics = VGroup(
            chip("latency", color=ORANGE, width=2.25, font_size=22),
            chip("memory", color=RED, width=2.25, font_size=22),
            chip("throughput", color=GREEN, width=2.75, font_size=22),
        ).arrange(RIGHT, buff=0.30)
        metrics.next_to(bar_20, DOWN, buff=0.30)

        self.play(FadeIn(gpu, scale=0.94), FadeIn(model, shift=UP * 0.15), run_time=t(1.7))
        self.play(FadeIn(bar_20, shift=UP * 0.10), run_time=t(0.8))
        self.play(
            Transform(bar_20[1], bar_95[1]),
            Transform(bar_20[3], bar_95[3]),
            FadeIn(warning, scale=1.25),
            run_time=t(2.0),
        )
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in metrics], lag_ratio=0.18), run_time=t(1.6))
        self.play(FadeIn(chapter, shift=DOWN * 0.10), run_time=t(1.0))
        self.play(FadeOut(chapter, shift=UP * 0.08), run_time=t(0.35))
        self.play(FadeIn(quant_title, shift=DOWN * 0.08), Indicate(model, color=YELLOW), run_time=t(1.45))
        self.wait(tw(10.8))

    # --------------------------------------------------------
    # Scene 17.02 - Numbers inside the model
    # --------------------------------------------------------
    def scene_17_02_numbers_inside_model(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_02_numbers_inside_model.mp3")

        title = title_text("Bên trong model là rất nhiều con số", font_size=38)

        model = network_block(width=4.35, height=1.75, title="LLM")
        model.move_to(UP * 0.65)

        grid = number_grid(rows=5, cols=8, cell_w=0.72, cell_h=0.38, font_size=12, color=BLUE)
        grid.move_to(UP * 0.48)

        vram = gpu_block(width=10.4, height=2.0, title="GPU memory full of weights")
        vram.move_to(DOWN * 1.65)

        bricks = number_grid(
            rows=3,
            cols=12,
            cell_w=0.58,
            cell_h=0.32,
            font_size=10,
            color=YELLOW,
            values=["0.73", "-1.28", "0.00", "1.10", "-0.38", "0.19"],
        )
        bricks.scale(0.88)
        bricks.move_to(vram.get_center() + DOWN * 0.15)

        bar_35 = vram_bar(0.35, width=8.2, label="memory", fill_color=ORANGE)
        bar_35.to_edge(DOWN, buff=0.38)
        bar_78 = vram_bar(0.78, width=8.2, label="memory", fill_color=RED)
        bar_78.move_to(bar_35)

        note = chip("billions of weights", color=YELLOW, width=3.35, font_size=23)
        note.to_edge(RIGHT, buff=0.62).shift(UP * 1.05)

        self.play(Write(title), FadeIn(model, scale=0.95), run_time=t(1.5))
        self.play(model.animate.scale(1.18), run_time=t(0.9))
        self.play(ReplacementTransform(model, grid), run_time=t(2.0))
        self.play(FadeIn(vram, shift=UP * 0.10), FadeIn(bar_35, shift=UP * 0.10), run_time=t(1.2))
        self.play(ReplacementTransform(grid.copy(), bricks), FadeIn(note, shift=LEFT), run_time=t(2.2))
        self.play(Transform(bar_35[1], bar_78[1]), Transform(bar_35[3], bar_78[3]), run_time=t(1.5))
        self.play(Indicate(bricks, color=YELLOW), run_time=t(1.0))
        self.wait(tw(9.7))

    # --------------------------------------------------------
    # Scene 17.03 - Precision as ruler granularity
    # --------------------------------------------------------
    def scene_17_03_precision_ruler(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_03_precision_as_ruler.mp3")

        title = title_text("Precision là độ mịn của thước đo", font_size=39)
        axis = simple_axis(x_range=(-1, 1, 0.5), length=10.4, y=0.45)
        left_label = txt("-1", font_size=22, color=MUTED).next_to(axis.get_left(), DOWN, buff=0.25)
        right_label = txt("1", font_size=22, color=MUTED).next_to(axis.get_right(), DOWN, buff=0.25)

        fp32_ticks = axis_tick_group(axis, [x / 16 for x in range(-16, 17)], height=0.55, color=BLUE, stroke_width=1.4)
        fp16_ticks = axis_tick_group(axis, [x / 8 for x in range(-8, 9)], height=0.50, color=TEAL, stroke_width=2.0)
        int8_buckets = bucket_group(axis, [-0.875, -0.625, -0.375, -0.125, 0.125, 0.375, 0.625, 0.875], 0.25, color=GREEN)
        int4_buckets = bucket_group(axis, [-0.75, -0.25, 0.25, 0.75], 0.50, color=ORANGE)

        mode_label = chip("FP32: rất nhiều vạch nhỏ", color=BLUE, width=4.15, font_size=23)
        mode_label.move_to(DOWN * 1.35)
        fp16_label = chip("FP16 / BF16: ít vạch hơn", color=TEAL, width=4.15, font_size=23).move_to(mode_label)
        int8_label = chip("INT8: các ô rời rạc", color=GREEN, width=4.15, font_size=23).move_to(mode_label)
        int4_label = chip("INT4: ít ô lớn hơn", color=ORANGE, width=4.15, font_size=23).move_to(mode_label)

        self.play(Write(title), Create(axis), FadeIn(left_label), FadeIn(right_label), run_time=t(1.6))
        self.play(Create(fp32_ticks), FadeIn(mode_label, shift=UP * 0.10), run_time=t(2.0))
        self.play(ReplacementTransform(fp32_ticks, fp16_ticks), Transform(mode_label, fp16_label), run_time=t(2.0))
        self.play(ReplacementTransform(fp16_ticks, int8_buckets), Transform(mode_label, int8_label), run_time=t(2.0))
        self.play(ReplacementTransform(int8_buckets, int4_buckets), Transform(mode_label, int4_label), run_time=t(2.0))
        self.play(Indicate(int4_buckets, color=ORANGE), run_time=t(1.1))
        self.wait(tw(9.3))

    # --------------------------------------------------------
    # Scene 17.04 - Bucket mapping
    # --------------------------------------------------------
    def scene_17_04_bucket_mapping(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_04_bucket_mapping.mp3")

        title = title_text("Quantization: đưa số vào các ô rời rạc", font_size=38)
        axis = simple_axis(x_range=(-2.5, 2.5, 0.5), length=10.2, y=0.30)
        labels = ["q = -2", "q = -1", "q = 0", "q = 1", "q = 2"]
        buckets = bucket_group(axis, [-2, -1, 0, 1, 2], 1.0, color=GREEN, labels=labels, height=0.86)

        raw_values = [-1.76, -0.72, -0.18, 0.43, 1.66]
        raw_dots = VGroup()
        drop_lines = VGroup()
        for i, value in enumerate(raw_values):
            start = axis.n2p(value) + UP * (2.10 + 0.15 * (i % 2))
            end = axis.n2p(value) + UP * 0.48
            dot = Dot(start, color=YELLOW, radius=0.075)
            raw_dots.add(dot)
            drop_lines.add(DashedLine(start + DOWN * 0.10, end, color=YELLOW, stroke_width=2))

        snapped_values = [-2, -1, 0, 0, 2]
        snapped_dots = VGroup()
        for dot, q in zip(raw_dots, snapped_values):
            snapped_dots.add(Dot(axis.n2p(q) + UP * 0.48, color=YELLOW, radius=0.075))

        formula = chip("x ≈ s × q", color=YELLOW, width=2.85, font_size=30)
        formula.move_to(DOWN * 2.25)
        scale = chip("scale = s", color=PURPLE, width=2.35, font_size=23)
        scale.next_to(formula, RIGHT, buff=0.35)

        self.play(Write(title), Create(axis), run_time=t(1.4))
        self.play(LaggedStart(*[FadeIn(dot) for dot in raw_dots], lag_ratio=0.12), run_time=t(1.0))
        self.play(Create(drop_lines), raw_dots.animate.shift(DOWN * 1.65), run_time=t(1.8))
        self.play(FadeIn(buckets, shift=UP * 0.10), run_time=t(1.6))
        self.play(Transform(raw_dots, snapped_dots), run_time=t(2.0))
        self.play(FadeIn(formula, shift=UP), FadeIn(scale, shift=UP), run_time=t(1.5))
        self.play(Circumscribe(formula, color=YELLOW), run_time=t(1.0))
        self.wait(tw(9.7))

    # --------------------------------------------------------
    # Scene 17.05 - Tiny numerical example
    # --------------------------------------------------------
    def scene_17_05_tiny_example(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_05_tiny_example.mp3")

        title = title_text("Ví dụ nhỏ: 0.73 thành 0.70", font_size=40)
        axis = simple_axis(x_range=(0, 1, 0.1), length=8.6, y=0.35)
        ticks = axis_tick_group(axis, [i / 10 for i in range(11)], height=0.30, color=MUTED, stroke_width=1.7)
        zero = txt("0.0", font_size=18, color=MUTED).next_to(axis.n2p(0), DOWN, buff=0.25)
        one = txt("1.0", font_size=18, color=MUTED).next_to(axis.n2p(1), DOWN, buff=0.25)

        dot = Dot(axis.n2p(0.73) + UP * 0.45, color=YELLOW, radius=0.09)
        original_label = txt("0.73", font_size=28, color=YELLOW, weight=BOLD).next_to(dot, UP, buff=0.14)
        target_dot = Dot(axis.n2p(0.70) + UP * 0.45, color=GREEN, radius=0.09)

        scale_chip = chip("scale = 0.1", color=PURPLE, width=2.65, font_size=23)
        scale_chip.move_to(LEFT * 3.75 + UP * 1.55)

        q_chip = chip("q = 7", color=GREEN, width=1.65, font_size=25)
        q_chip.next_to(scale_chip, DOWN, buff=0.22)

        error_line = Line(axis.n2p(0.70) + UP * 0.08, axis.n2p(0.73) + UP * 0.08, color=RED, stroke_width=6)
        error_label = txt("error = 0.03", font_size=20, color=RED, weight=BOLD)
        error_label.next_to(error_line, UP, buff=0.12)

        table = VGroup(
            chip("original  0.73", color=BLUE, width=3.15, font_size=21),
            chip("q  =  7", color=GREEN, width=3.15, font_size=21),
            chip("reconstructed  0.70", color=YELLOW, width=3.15, font_size=20),
            chip("error  0.03", color=RED, width=3.15, font_size=21),
        ).arrange(DOWN, buff=0.17)
        table.to_edge(RIGHT, buff=0.70).shift(DOWN * 0.42)

        self.play(Write(title), Create(axis), Create(ticks), FadeIn(zero), FadeIn(one), run_time=t(1.5))
        self.play(FadeIn(dot), FadeIn(original_label), run_time=t(1.1))
        self.play(FadeIn(scale_chip, shift=RIGHT), run_time=t(1.0))
        self.play(dot.animate.move_to(target_dot), original_label.animate.next_to(target_dot, UP, buff=0.14), run_time=t(1.6))
        new_label = txt("0.70", font_size=28, color=GREEN, weight=BOLD).move_to(original_label)
        self.play(Transform(original_label, new_label), FadeIn(q_chip, shift=DOWN), run_time=t(1.2))
        self.play(Create(error_line), FadeIn(error_label), run_time=t(1.2))
        self.play(LaggedStart(*[FadeIn(row, shift=LEFT) for row in table], lag_ratio=0.15), run_time=t(2.0))
        self.play(Circumscribe(table[2], color=YELLOW), run_time=t(1.0))
        self.wait(tw(9.4))

    # --------------------------------------------------------
    # Scene 17.06 - Quantization is not pruning
    # --------------------------------------------------------
    def scene_17_06_not_pruning(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_06_not_pruning.mp3")

        title = title_text("Quantization không phải pruning", font_size=40)
        divider = DashedLine(UP * 2.55, DOWN * 2.45, color=MUTED, stroke_opacity=0.65)

        left_title = txt("Pruning", font_size=32, color=RED, weight=BOLD).move_to(LEFT * 3.70 + UP * 2.25)
        right_title = txt("Quantization", font_size=32, color=GREEN, weight=BOLD).move_to(RIGHT * 3.50 + UP * 2.25)

        trunk = Line(DOWN * 1.30, UP * 0.75, color=GREEN, stroke_width=10)
        branch_a = Line(UP * 0.25, LEFT * 0.90 + UP * 1.25, color=GREEN, stroke_width=7)
        branch_b = Line(UP * 0.25, RIGHT * 0.90 + UP * 1.25, color=GREEN, stroke_width=7)
        branch_c = Line(DOWN * 0.35, LEFT * 0.72 + UP * 0.20, color=GREEN, stroke_width=6)
        tree = VGroup(trunk, branch_a, branch_b, branch_c).move_to(LEFT * 3.75 + DOWN * 0.05)
        cut = VGroup(
            Line(branch_b.get_center() + LEFT * 0.25 + UP * 0.25, branch_b.get_center() + RIGHT * 0.25 + DOWN * 0.25, color=RED, stroke_width=8),
            Line(branch_b.get_center() + LEFT * 0.25 + DOWN * 0.25, branch_b.get_center() + RIGHT * 0.25 + UP * 0.25, color=RED, stroke_width=8),
        )
        cut.move_to(LEFT * 3.23 + UP * 0.58)
        pruning_note = small_note("cắt bớt cấu trúc", color=RED, font_size=22).next_to(tree, DOWN, buff=0.38)

        long_grid = number_grid(
            rows=3,
            cols=4,
            cell_w=0.86,
            cell_h=0.50,
            values=["0.7312", "-1.2846", "0.0049", "1.1027"],
            font_size=15,
            color=BLUE,
        )
        long_grid.move_to(RIGHT * 3.55 + DOWN * 0.08)
        q_grid = number_grid(
            rows=3,
            cols=4,
            cell_w=0.86,
            cell_h=0.50,
            values=["q=7", "q=-13", "q=0", "q=11"],
            font_size=18,
            color=GREEN,
        )
        q_grid.move_to(long_grid)
        same_note = chip("same structure,\nfewer bits", color=GREEN, width=3.25, height=0.92, font_size=22)
        same_note.next_to(long_grid, DOWN, buff=0.34)

        self.play(Write(title), Create(divider), FadeIn(left_title), FadeIn(right_title), run_time=t(1.5))
        self.play(Create(tree), run_time=t(1.4))
        self.play(FadeIn(cut, scale=1.20), FadeIn(pruning_note, shift=UP), run_time=t(1.2))
        self.play(FadeIn(long_grid, shift=LEFT), run_time=t(1.4))
        self.play(Transform(long_grid, q_grid), run_time=t(2.0))
        self.play(FadeIn(same_note, shift=UP), run_time=t(1.1))
        self.play(Circumscribe(same_note, color=GREEN), run_time=t(1.0))
        self.wait(tw(10.4))

    # --------------------------------------------------------
    # Scene 17.07 - Precision levels
    # --------------------------------------------------------
    def scene_17_07_precision_levels(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_07_precision_levels.mp3")

        title = title_text("Các mức bit phổ biến", font_size=42)
        boxes = VGroup(
            bit_format_box("FP32", 32, "chính xác, tốn bộ nhớ", BLUE, 3.0),
            bit_format_box("FP16 / BF16", 16, "phổ biến trong deep learning", TEAL, 2.75),
            bit_format_box("INT8 / FP8", 8, "cùng 8-bit, khác kiểu số", GREEN, 2.45),
            bit_format_box("INT4", 4, "nhỏ hơn, thô hơn", ORANGE, 2.05),
        ).arrange(RIGHT, buff=0.30, aligned_edge=DOWN)
        boxes.move_to(UP * 0.25)

        size_arrow = Arrow(LEFT * 4.75 + DOWN * 1.72, RIGHT * 4.75 + DOWN * 1.72, color=MUTED, stroke_width=4)
        size_label = small_note("ít bit hơn  →  ít byte hơn, biểu diễn thô hơn", color=MUTED, font_size=22)
        size_label.next_to(size_arrow, UP, buff=0.14)
        warning = chip("FP8 ≠ INT4", color=RED, width=3.05, font_size=28)
        warning.next_to(size_arrow, DOWN, buff=0.18)

        self.play(Write(title), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(box, shift=UP * 0.15) for box in boxes], lag_ratio=0.16), run_time=t(2.5))
        self.play(Create(size_arrow), FadeIn(size_label), run_time=t(1.2))
        self.play(Circumscribe(boxes[2], color=GREEN), run_time=t(1.3))
        self.play(Circumscribe(boxes[3], color=ORANGE), run_time=t(1.3))
        self.play(FadeIn(warning, shift=UP), run_time=t(1.1))
        self.play(Flash(warning, color=RED), run_time=t(1.2))
        self.wait(tw(10.4))

    # --------------------------------------------------------
    # Scene 17.08 - Memory footprint
    # --------------------------------------------------------
    def scene_17_08_memory_footprint(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_08_memory_example.mp3")

        title = title_text("Lợi ích 1: giảm memory footprint", font_size=39)
        param_card = chip("7B params", color=YELLOW, width=2.55, font_size=28)
        param_card.move_to(LEFT * 4.65 + UP * 1.35)

        dots = VGroup()
        for r in range(5):
            for c in range(7):
                dots.add(Dot(radius=0.025, color=YELLOW).move_to([c * 0.16, -r * 0.16, 0]))
        dots.arrange_in_grid(rows=5, cols=7, buff=0.07)
        dots.next_to(param_card, DOWN, buff=0.34)

        fp16 = storage_block("FP16", "≈ 14 GB", 6.2, BLUE)
        int8 = storage_block("INT8", "≈ 7 GB", 3.25, GREEN)
        int4 = storage_block("INT4", "≈ 3.5 GB + overhead", 2.25, ORANGE)
        bars = VGroup(fp16, int8, int4).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        bars.move_to(RIGHT * 1.15 + UP * 0.35)

        freed = VGroup(
            RoundedRectangle(
                corner_radius=0.13,
                width=6.2,
                height=0.74,
                stroke_color=WHITE,
                stroke_width=2,
                fill_opacity=0,
            ),
        )
        weight = Rectangle(width=2.25, height=0.74, stroke_width=0, fill_color=ORANGE, fill_opacity=0.82)
        cache = Rectangle(width=1.70, height=0.74, stroke_width=0, fill_color=PURPLE, fill_opacity=0.72)
        free = Rectangle(width=2.25, height=0.74, stroke_width=0, fill_color=GREEN, fill_opacity=0.72)
        segs = VGroup(weight, cache, free).arrange(RIGHT, buff=0).move_to(freed[0])
        weight_label = txt("weights", font_size=17, color=WHITE).move_to(weight)
        cache_label = txt("KV cache", font_size=17, color=WHITE).move_to(cache)
        free_label = txt("batch", font_size=17, color=WHITE).move_to(free)
        freed_group = VGroup(segs, freed[0], weight_label, cache_label, free_label)
        freed_group.move_to(DOWN * 2.25)
        freed_title = txt("VRAM còn chỗ cho batch / KV cache", font_size=24, color=GREEN, weight=BOLD)
        freed_title.next_to(freed_group, UP, buff=0.20)

        self.play(Write(title), FadeIn(param_card, shift=RIGHT), FadeIn(dots), run_time=t(1.5))
        self.play(FadeIn(fp16, shift=LEFT), run_time=t(1.2))
        self.play(ReplacementTransform(fp16.copy(), int8), run_time=t(1.4))
        self.play(ReplacementTransform(int8.copy(), int4), run_time=t(1.4))
        self.play(FadeIn(freed_group, shift=UP), FadeIn(freed_title, shift=UP), run_time=t(1.6))
        self.play(Indicate(free, color=GREEN), Indicate(cache, color=PURPLE), run_time=t(1.4))
        self.wait(tw(11.5))

    # --------------------------------------------------------
    # Scene 17.09 - Memory bandwidth
    # --------------------------------------------------------
    def scene_17_09_bandwidth(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_09_bandwidth.mp3")

        title = title_text("Lợi ích 2: giảm băng thông bộ nhớ", font_size=38)

        hbm = chip("HBM\nmemory", color=BLUE, width=2.05, height=1.18, font_size=24)
        hbm.move_to(LEFT * 4.75 + UP * 0.45)
        compute = chip("Tensor\nCore", color=YELLOW, width=2.25, height=1.18, font_size=24)
        compute.move_to(RIGHT * 4.75 + UP * 0.45)

        road_top = Line(hbm.get_right() + RIGHT * 0.25 + UP * 0.18, compute.get_left() + LEFT * 0.25 + UP * 0.18, color=MUTED, stroke_width=5)
        road_bottom = Line(hbm.get_right() + RIGHT * 0.25 + DOWN * 0.18, compute.get_left() + LEFT * 0.25 + DOWN * 0.18, color=MUTED, stroke_width=5)
        road = VGroup(road_top, road_bottom)

        def truck(label, width, color):
            body = RoundedRectangle(
                corner_radius=0.08,
                width=width,
                height=0.50,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.28,
            )
            cab = Rectangle(width=0.32, height=0.38, stroke_width=0, fill_color=color, fill_opacity=0.70)
            cab.next_to(body, RIGHT, buff=-0.05)
            wheels = VGroup(
                Circle(radius=0.07, fill_color=WHITE, fill_opacity=1, stroke_width=0).next_to(body, DOWN, buff=-0.06).shift(LEFT * width * 0.25),
                Circle(radius=0.07, fill_color=WHITE, fill_opacity=1, stroke_width=0).next_to(body, DOWN, buff=-0.06).shift(RIGHT * width * 0.25),
            )
            text = txt(label, font_size=17, color=WHITE, weight=BOLD).move_to(body)
            return VGroup(body, cab, wheels, text)

        fp16_truck = truck("FP16", 1.55, RED).move_to(LEFT * 2.70 + UP * 0.45)
        int8_truck = truck("INT8", 1.05, GREEN).move_to(LEFT * 2.70 + UP * 0.45)
        int4_truck = truck("INT4", 0.72, ORANGE).move_to(LEFT * 2.70 + UP * 0.45)

        meter_box = RoundedRectangle(
            corner_radius=0.10,
            width=6.2,
            height=0.55,
            stroke_color=WHITE,
            stroke_width=2,
            fill_opacity=0,
        )
        meter_box.move_to(DOWN * 2.20)
        meter_high = Rectangle(width=5.55, height=0.55, stroke_width=0, fill_color=RED, fill_opacity=0.82)
        meter_high.move_to(meter_box).align_to(meter_box, LEFT)
        meter_low = Rectangle(width=2.25, height=0.55, stroke_width=0, fill_color=GREEN, fill_opacity=0.82)
        meter_low.move_to(meter_box).align_to(meter_box, LEFT)
        meter_label = txt("bytes moved per token", font_size=21, color=MUTED, weight=BOLD)
        meter_label.next_to(meter_box, UP, buff=0.22)

        self.play(Write(title), FadeIn(hbm), FadeIn(compute), Create(road), run_time=t(1.6))
        self.play(FadeIn(fp16_truck), FadeIn(meter_box), FadeIn(meter_high), FadeIn(meter_label), run_time=t(1.2))
        self.play(fp16_truck.animate.move_to(RIGHT * 2.70 + UP * 0.45), run_time=t(1.8))
        int8_truck.move_to(LEFT * 2.70 + UP * 0.45)
        self.play(FadeOut(fp16_truck), FadeIn(int8_truck), run_time=t(0.7))
        self.play(int8_truck.animate.move_to(RIGHT * 2.70 + UP * 0.45), Transform(meter_high, meter_low), run_time=t(1.8))
        int4_truck.move_to(LEFT * 2.70 + UP * 0.45)
        base_packet = int4_truck.copy().scale(0.68)
        packets = VGroup(*[base_packet.copy() for _ in range(3)]).arrange(RIGHT, buff=0.08)
        packets.move_to(LEFT * 2.30 + UP * 0.45)
        self.play(FadeOut(int8_truck), FadeIn(packets), run_time=t(0.8))
        self.play(packets.animate.move_to(RIGHT * 2.55 + UP * 0.45), run_time=t(1.6))
        self.play(Indicate(meter_high, color=GREEN), run_time=t(1.0))
        self.wait(tw(9.5))

    # --------------------------------------------------------
    # Scene 17.10 - Speed needs hardware and kernels
    # --------------------------------------------------------
    def scene_17_10_speed_hardware_kernel(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_10_speed_hardware_kernel.mp3")

        title = title_text("Lợi ích 3: tốc độ phụ thuộc hardware + kernel", font_size=36)

        fast = VGroup(
            chip("INT8 / FP8", color=GREEN, width=2.05, font_size=20),
            chip("low-bit kernel", color=GREEN, width=2.55, font_size=20),
            chip("Tensor Core", color=YELLOW, width=2.30, font_size=20),
            chip("output nhanh", color=GREEN, width=2.25, font_size=20),
        ).arrange(RIGHT, buff=0.28)
        fast.move_to(RIGHT * 0.45 + UP * 1.35)
        good_title = txt("Đường tốt", font_size=27, color=GREEN, weight=BOLD)
        good_title.next_to(fast[0], UP, buff=0.24).align_to(fast[0], LEFT)
        fast_arrows = VGroup(*[flow_arrow(fast[i], fast[i + 1], color=GREEN) for i in range(len(fast) - 1)])
        check = txt("✓", font_size=46, color=GREEN, weight=BOLD).next_to(fast[-1], RIGHT, buff=0.20)

        slow = VGroup(
            chip("INT4 stored", color=ORANGE, width=2.05, font_size=19),
            chip("dequantize", color=RED, width=2.10, font_size=19),
            chip("FP16 GEMM", color=BLUE, width=2.12, font_size=19),
            chip("output", color=MUTED, width=1.70, font_size=19),
        ).arrange(RIGHT, buff=0.25)
        slow.move_to(RIGHT * 0.40 + DOWN * 0.65)
        bad_title = txt("Đường tốn overhead", font_size=27, color=RED, weight=BOLD)
        bad_title.next_to(slow[0], UP, buff=0.24).align_to(slow[0], LEFT)
        slow_arrows = VGroup(*[flow_arrow(slow[i], slow[i + 1], color=ORANGE) for i in range(len(slow) - 1)])
        warn = txt("!", font_size=34, color=RED, weight=BOLD).next_to(slow[1], DOWN, buff=0.10)

        warning = chip("memory saving ≠ always faster", color=RED, width=4.65, font_size=25)
        warning.move_to(DOWN * 2.35)

        self.play(Write(title), run_time=t(1.0))
        self.play(FadeIn(good_title), LaggedStart(*[FadeIn(x, shift=UP * 0.10) for x in fast], lag_ratio=0.12), run_time=t(1.7))
        self.play(LaggedStart(*[Create(a) for a in fast_arrows], lag_ratio=0.18), FadeIn(check, scale=1.25), run_time=t(1.2))
        self.play(FadeIn(bad_title), LaggedStart(*[FadeIn(x, shift=DOWN * 0.10) for x in slow], lag_ratio=0.12), run_time=t(1.7))
        self.play(LaggedStart(*[Create(a) for a in slow_arrows], lag_ratio=0.18), FadeIn(warn, scale=1.25), run_time=t(1.2))
        self.play(Circumscribe(slow[1], color=RED), run_time=t(1.0))
        self.play(FadeIn(warning, shift=UP), run_time=t(1.1))
        self.play(Flash(warning, color=RED), run_time=t(1.0))
        self.wait(tw(10.1))

    # --------------------------------------------------------
    # Scene 17.11 - PTQ and QAT
    # --------------------------------------------------------
    def scene_17_11_ptq_qat(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_11_ptq_qat.mp3")

        title = title_text("PTQ và QAT", font_size=42)
        divider = DashedLine(UP * 2.55, DOWN * 2.45, color=MUTED, stroke_opacity=0.65)

        ptq_title = txt("PTQ", font_size=34, color=BLUE, weight=BOLD).move_to(LEFT * 3.60 + UP * 2.18)
        qat_title = txt("QAT", font_size=34, color=GREEN, weight=BOLD).move_to(RIGHT * 3.45 + UP * 2.18)

        trained = chip("trained model", color=BLUE, width=3.00, font_size=22)
        calibration = chip("calibration data", color=YELLOW, width=3.00, font_size=22)
        ptq_model = chip("quantized model", color=GREEN, width=3.00, font_size=22)
        ptq_flow = VGroup(trained, calibration, ptq_model).arrange(DOWN, buff=0.38)
        ptq_flow.move_to(LEFT * 3.60 + UP * 0.22)
        ptq_arrows = VGroup(
            Arrow(trained.get_bottom(), calibration.get_top(), buff=0.10, color=MUTED),
            Arrow(calibration.get_bottom(), ptq_model.get_top(), buff=0.10, color=MUTED),
        )
        ptq_note = chip("nhanh, sau train", color=BLUE, width=3.10, font_size=20)
        ptq_note.next_to(ptq_flow, DOWN, buff=0.28)

        loop_box = RoundedRectangle(
            corner_radius=0.20,
            width=3.70,
            height=1.45,
            stroke_color=GREEN,
            stroke_width=2.4,
            fill_color=GREEN,
            fill_opacity=0.13,
        )
        loop_text = VGroup(
            txt("training loop", font_size=24, weight=BOLD),
            txt("+ fake quantization", font_size=19, color=MUTED),
        ).arrange(DOWN, buff=0.12)
        loop = VGroup(loop_box, loop_text).move_to(RIGHT * 3.45 + UP * 0.55)
        loop_arrow = Arc(radius=0.38, start_angle=0.25, angle=TAU * 0.78, color=GREEN, stroke_width=4)
        loop_arrow.move_to(loop.get_corner(UR) + LEFT * 0.34 + DOWN * 0.24)

        qat_model = chip("QAT model", color=GREEN, width=3.00, font_size=22)
        qat_model.next_to(loop, DOWN, buff=0.38)
        qat_arrow = Arrow(loop.get_bottom(), qat_model.get_top(), buff=0.10, color=MUTED)
        qat_note = chip("tốn công hơn,\ngiữ chất lượng tốt hơn", color=GREEN, width=3.35, height=0.88, font_size=19)
        qat_note.next_to(qat_model, DOWN, buff=0.26)

        tradeoff = chip("PTQ: tiện hơn     QAT: quality hơn", color=YELLOW, width=5.25, font_size=22)
        tradeoff.move_to(DOWN * 3.02)

        self.play(Write(title), Create(divider), FadeIn(ptq_title), FadeIn(qat_title), run_time=t(1.4))
        self.play(FadeIn(trained), run_time=t(0.7))
        self.play(Create(ptq_arrows[0]), FadeIn(calibration), run_time=t(0.9))
        self.play(Create(ptq_arrows[1]), FadeIn(ptq_model), FadeIn(ptq_note, shift=UP), run_time=t(1.1))
        self.play(FadeIn(loop, scale=0.94), Create(loop_arrow), run_time=t(1.3))
        self.play(Create(qat_arrow), FadeIn(qat_model), FadeIn(qat_note, shift=UP), run_time=t(1.2))
        self.play(FadeIn(tradeoff, shift=UP), run_time=t(1.1))
        self.play(Circumscribe(tradeoff, color=YELLOW), run_time=t(1.0))
        self.wait(tw(11.3))

    # --------------------------------------------------------
    # Scene 17.12 - Summary and transition
    # --------------------------------------------------------
    def scene_17_12_summary_transition(self):
        self.fade_clear()
        self.start_audio_scene("voice/p4_17_12_summary_transition.mp3")

        title = title_text("Low-bit Quantization - tổng kết", font_size=39)

        recap = VGroup(
            chip("Memory ↓", color=BLUE, width=2.85, font_size=25),
            chip("Bandwidth ↓", color=TEAL, width=3.05, font_size=25),
            chip("Speed ? depends", color=YELLOW, width=3.45, font_size=24),
        ).arrange(RIGHT, buff=0.35)
        recap.move_to(UP * 1.48)

        warnings = VGroup(
            chip("quality trade-off", color=RED, width=3.30, font_size=22),
            chip("hardware-aware kernels", color=ORANGE, width=4.05, font_size=22),
        ).arrange(RIGHT, buff=0.35)
        warnings.move_to(UP * 0.35)

        single = gpu_block(width=3.55, height=2.05, title="one GPU")
        single.move_to(LEFT * 2.85 + DOWN * 1.25)
        cluster = gpu_cluster(scale=1.20)
        cluster.move_to(RIGHT * 2.50 + DOWN * 1.25)

        arrow = Arrow(single.get_right() + RIGHT * 0.18, cluster.get_left() + LEFT * 0.18, color=GREEN, stroke_width=6)
        next_text = txt("Next: Parallel Computation", font_size=31, color=GREEN, weight=BOLD)
        next_text.to_edge(DOWN, buff=0.35)

        self.play(Write(title), run_time=t(1.0))
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in recap], lag_ratio=0.18), run_time=t(1.6))
        self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.12) for w in warnings], lag_ratio=0.18), run_time=t(1.4))
        self.play(FadeIn(single, scale=0.95), run_time=t(1.1))
        self.play(Create(arrow), ReplacementTransform(single.copy(), cluster), run_time=t(2.0))
        self.play(FadeIn(next_text, shift=UP), run_time=t(1.2))
        self.play(Indicate(cluster, color=GREEN), run_time=t(1.0))
        self.wait(tw(11.7))
