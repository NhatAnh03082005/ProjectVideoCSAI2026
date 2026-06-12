# pyrefly: ignore [missing-import]
from manim import *
from mutagen.mp3 import MP3
import os
import sys

# Fix Unicode output on Windows console
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ============================================================
# MAIN.PY — PHẦN 4: SYSTEM OPTIMIZATIONS
# Scene hiện tại: Low-bit Quantization + voice sync
# Font + màu đã cố định để đồng nhất visual
# ============================================================

# ============================================================
# 1. THEME CHUNG — ĐỒNG BỘ VỚI CÁC THÀNH VIÊN
# ============================================================

# Font cố định
FONT = "Segoe UI"

# Nền
BG = "#0f172a"          # xanh đen/slate, hợp phong cách 3Blue1Brown

# Màu chữ
WHITE = "#e5e7eb"       # chữ chính
MUTED = "#94a3b8"       # chữ phụ, ghi chú nhỏ

# Màu nhấn
BLUE = "#38bdf8"        # concept chính / subtitle
GREEN = "#22c55e"       # trạng thái tốt / sau tối ưu
YELLOW = "#facc15"      # nhấn mạnh / mũi tên / lợi ích
RED = "#ef4444"         # cảnh báo / lỗi / bottleneck
PURPLE = "#a78bfa"      # token / node / phụ trợ
ORANGE = "#fb923c"      # INT4 / điểm nhấn phụ

# Độ mờ fill cố định
FILL_SOFT = 0.12
FILL_MEDIUM = 0.18
FILL_STRONG = 0.62

config.background_color = BG


# ============================================================
# 2. HELPER STYLE — DÙNG THAY CHO Text(...) TRỰC TIẾP
# ============================================================

def T(text, size=24, color=WHITE, weight=NORMAL, line_spacing=-1):
    """
    Hàm tạo Text thống nhất: tiếng Việt dùng Arial, tiếng Anh dùng font mặc định của Manim.
    """
    vietnamese_chars = "ăâđêôươáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
    is_vi = any(c.lower() in vietnamese_chars for c in text)
    
    if is_vi:
        return Text(
            text,
            font="Arial",
            font_size=size,
            color=color,
            weight=weight,
            line_spacing=line_spacing,
        )
    else:
        return Text(
            text,
            font_size=size,
            color=color,
            weight=weight,
            line_spacing=line_spacing,
        )


def resolve_audio_path(path):
    if os.path.exists(path):
        return path
    
    # Try relative to the main module / script directory
    import sys
    for arg in sys.argv:
        if arg.endswith('.py') and os.path.exists(arg):
            arg_dir = os.path.dirname(os.path.abspath(arg))
            alt_path = os.path.join(arg_dir, path)
            if os.path.exists(alt_path):
                return alt_path
                
    # Try relative to caller's file (walking stack frames)
    import inspect
    frame = inspect.currentframe()
    try:
        while frame:
            caller_file = frame.f_code.co_filename
            if caller_file and caller_file != __file__ and os.path.exists(caller_file):
                caller_dir = os.path.dirname(os.path.abspath(caller_file))
                alt_path = os.path.join(caller_dir, path)
                if os.path.exists(alt_path):
                    return alt_path
            frame = frame.f_back
    finally:
        del frame
        
    return path


def audio_duration(path):
    """
    Trả về thời lượng file mp3 tính bằng giây.
    Nếu file chưa tồn tại, trả về 0 để Manim không crash.
    """
    resolved = resolve_audio_path(path)
    if not os.path.exists(resolved):
        print(f"[WARNING] Không tìm thấy audio: {path} (đã thử phân giải thành {resolved})")
        return 0
    return MP3(resolved).info.length


# Monkey patch Scene.add_sound to automatically resolve path relative to source file
original_add_sound = Scene.add_sound

def patched_add_sound(self, sound_file, *args, **kwargs):
    resolved = resolve_audio_path(sound_file)
    return original_add_sound(self, resolved, *args, **kwargs)

Scene.add_sound = patched_add_sound


def make_title(text):
    title = T(text, size=42, color=WHITE, weight=BOLD)
    title.to_edge(UP, buff=0.35)
    return title


def make_subtitle(text, title):
    subtitle = T(text, size=23, color=BLUE)
    subtitle.next_to(title, DOWN, buff=0.22)
    return subtitle


# ============================================================
# SCENE 17 — LOW-BIT QUANTIZATION, CÓ VOICE SYNC
# ============================================================

class LowBitQuantizationAudioScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # -------------------------
        # Helper trong scene
        # -------------------------
        def precision_box(name, bits, color):
            box = RoundedRectangle(
                width=2.0,
                height=0.8,
                corner_radius=0.12,
                stroke_color=color,
                fill_color=color,
                fill_opacity=FILL_MEDIUM
            )
            t1 = T(name, size=22, color=WHITE, weight=BOLD)
            t2 = T(bits, size=16, color=color)
            t2.next_to(t1, DOWN, buff=0.05)
            return VGroup(box, t1, t2)

        def play_audio(path):
            """
            Bật audio nếu file tồn tại.
            """
            if os.path.exists(path):
                self.add_sound(path)
            else:
                print(f"[WARNING] Bỏ qua audio vì không tìm thấy: {path}")

        def wait_audio(path, visual_time):
            """
            Nếu audio dài hơn animation, giữ màn hình thêm cho đến khi audio đọc xong.
            Nếu audio không tồn tại hoặc thời gian chờ <= 0 thì bỏ qua,
            vì Manim không cho self.wait(0).
            """
            duration = audio_duration(path)
            remaining = duration - visual_time
            if remaining > 0.05:
                self.wait(remaining)

        # =====================================================
        # CẢNH 1 — INTRO
        # Audio: q01_intro.mp3
        # =====================================================

        title = make_title("Low-bit Quantization")
        subtitle = make_subtitle(
            "Không cắt mô hình — chỉ đổi cách biểu diễn số",
            title
        )

        audio = "voice/q01_intro.mp3"
        play_audio(audio)

        self.play(Write(title), run_time=1.4)
        self.play(FadeIn(subtitle, shift=UP), run_time=1.0)
        wait_audio(audio, visual_time=2.4)

        # =====================================================
        # CẢNH 2 — FP32 / FP16 / INT8 / INT4
        # Audio: q02_precision.mp3
        # =====================================================

        vram_box = RoundedRectangle(
            width=2.7,
            height=3.8,
            corner_radius=0.15,
            stroke_color=WHITE,
            stroke_width=2
        )
        vram_box.move_to(LEFT * 4.0 + DOWN * 0.35)

        vram_label = T("GPU VRAM", size=22, color=WHITE, weight=BOLD)
        vram_label.next_to(vram_box, UP, buff=0.18)

        weight_before = Rectangle(
            width=2.25,
            height=3.15,
            fill_color=RED,
            fill_opacity=FILL_STRONG,
            stroke_color=RED
        )
        weight_before.move_to(vram_box.get_center() + DOWN * 0.12)

        weight_text = T(
            "Model weights\nFP16 / FP32",
            size=20,
            color=WHITE,
            weight=BOLD
        )
        weight_text.move_to(weight_before.get_center())

        fp32 = precision_box("FP32", "32-bit", BLUE)
        fp16 = precision_box("FP16 / BF16", "16-bit", GREEN)
        int8 = precision_box("INT8 / FP8", "8-bit", YELLOW)
        int4 = precision_box("INT4", "4-bit", ORANGE)

        boxes = VGroup(fp32, fp16, int8, int4)
        boxes.arrange(DOWN, buff=0.22)
        boxes.move_to(RIGHT * 2.2 + DOWN * 0.35)

        arrow = Arrow(
            vram_box.get_right(),
            boxes.get_left(),
            color=YELLOW,
            buff=0.25
        )

        arrow_label = T("Đổi cách lưu số", size=22, color=YELLOW, weight=BOLD)
        arrow_label.next_to(arrow, UP, buff=0.18)

        audio = "voice/q02_precision.mp3"
        play_audio(audio)

        self.play(Create(vram_box), FadeIn(vram_label), run_time=1.0)
        self.play(FadeIn(weight_before), Write(weight_text), run_time=1.2)
        self.play(Create(arrow), Write(arrow_label), run_time=1.0)
        self.play(
            LaggedStart(
                FadeIn(fp32, shift=RIGHT),
                FadeIn(fp16, shift=RIGHT),
                FadeIn(int8, shift=RIGHT),
                FadeIn(int4, shift=RIGHT),
                lag_ratio=0.15
            ),
            run_time=2.0
        )
        wait_audio(audio, visual_time=5.2)

        # =====================================================
        # CẢNH 3 — MEMORY GIẢM SAU QUANTIZATION
        # Audio: q03_memory.mp3
        # =====================================================

        self.play(
            FadeOut(boxes),
            FadeOut(arrow),
            FadeOut(arrow_label),
            run_time=0.7
        )

        weight_after = Rectangle(
            width=2.25,
            height=1.55,
            fill_color=GREEN,
            fill_opacity=0.65,
            stroke_color=GREEN
        )
        weight_after.move_to(vram_box.get_center() + DOWN * 0.95)

        after_text = T(
            "Weights\nINT8 / INT4 / FP8",
            size=18,
            color=WHITE,
            weight=BOLD
        )
        after_text.move_to(weight_after.get_center())

        free_space = T(
            "Free space\nbatch + KV cache",
            size=18,
            color=GREEN,
            weight=BOLD
        )
        free_space.move_to(vram_box.get_center() + UP * 0.9)

        after_label = T("Sau quantization", size=23, color=GREEN, weight=BOLD)
        after_label.next_to(vram_box, DOWN, buff=0.22)

        audio = "voice/q03_memory.mp3"
        play_audio(audio)

        self.play(
            Transform(weight_before, weight_after),
            Transform(weight_text, after_text),
            FadeIn(after_label),
            run_time=1.5
        )
        self.play(Write(free_space), run_time=1.0)
        wait_audio(audio, visual_time=2.5)

        # =====================================================
        # CẢNH 4 — 3 LỢI ÍCH
        # Audio: q04_benefits.mp3
        # =====================================================

        benefits_title = T("Lợi ích", size=28, color=YELLOW, weight=BOLD)
        benefits_title.move_to(RIGHT * 2.7 + UP * 1.25)

        b1 = T("1. Giảm memory footprint", size=21, color=WHITE)
        b2 = T("2. Giảm băng thông đọc/ghi", size=21, color=WHITE)
        b3 = T("3. Có thể tăng tốc nếu hardware/kernel hỗ trợ", size=21, color=WHITE)

        benefits = VGroup(b1, b2, b3)
        benefits.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        benefits.next_to(benefits_title, DOWN, buff=0.35)
        benefits.scale_to_fit_width(5.4)

        audio = "voice/q04_benefits.mp3"
        play_audio(audio)

        self.play(Write(benefits_title), run_time=0.8)
        self.play(FadeIn(b1, shift=RIGHT), run_time=0.8)
        self.play(FadeIn(b2, shift=RIGHT), run_time=0.8)
        self.play(FadeIn(b3, shift=RIGHT), run_time=0.8)
        wait_audio(audio, visual_time=3.2)

        # =====================================================
        # CẢNH 5 — PTQ / QAT + WARNING
        # Audio: q05_warning.mp3
        # =====================================================

        self.play(
            FadeOut(vram_box),
            FadeOut(vram_label),
            FadeOut(weight_before),
            FadeOut(weight_text),
            FadeOut(free_space),
            FadeOut(after_label),
            FadeOut(benefits_title),
            FadeOut(benefits),
            run_time=0.8
        )

        trade_title = T(
            "Đánh đổi: ít bit hơn → có thể mất độ chính xác",
            size=28,
            color=YELLOW,
            weight=BOLD
        )
        trade_title.move_to(UP * 1.65)

        ptq_box = RoundedRectangle(
            width=4.7,
            height=1.35,
            corner_radius=0.15,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=FILL_SOFT
        )
        ptq_text = T(
            "PTQ\nQuantize sau khi train\ncó thể cần calibration",
            size=22,
            color=WHITE,
            weight=BOLD
        )
        ptq = VGroup(ptq_box, ptq_text)
        ptq.move_to(LEFT * 2.7 + DOWN * 0.15)

        qat_box = RoundedRectangle(
            width=4.7,
            height=1.35,
            corner_radius=0.15,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=FILL_SOFT
        )
        qat_text = T(
            "QAT\nĐưa quantization vào training\nmô hình thích nghi tốt hơn",
            size=22,
            color=WHITE,
            weight=BOLD
        )
        qat = VGroup(qat_box, qat_text)
        qat.move_to(RIGHT * 2.7 + DOWN * 0.15)

        warning_box = RoundedRectangle(
            width=10.3,
            height=0.9,
            corner_radius=0.15,
            stroke_color=RED,
            fill_color=RED,
            fill_opacity=0.15
        )
        warning_box.to_edge(DOWN, buff=0.55)

        warning_text = T(
            "Quantization không tự động nhanh: cần GPU và kernel hỗ trợ low-bit",
            size=21,
            color=RED,
            weight=BOLD
        )
        warning_text.move_to(warning_box.get_center())
        warning_text.scale_to_fit_width(9.6)

        audio = "voice/q05_warning.mp3"
        play_audio(audio)

        self.play(Write(trade_title), run_time=1.0)
        self.play(FadeIn(ptq, shift=UP), FadeIn(qat, shift=UP), run_time=1.2)
        self.play(Create(warning_box), Write(warning_text), run_time=1.2)
        self.play(Flash(warning_box, color=RED), run_time=0.6)
        wait_audio(audio, visual_time=4.0)

        # =====================================================
        # KẾT THÚC SCENE
        # =====================================================

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(trade_title),
            FadeOut(ptq),
            FadeOut(qat),
            FadeOut(warning_box),
            FadeOut(warning_text),
            run_time=1.0
        )


# ============================================================
# SCENE TEST NHANH, KHÔNG CẦN AUDIO
# Chạy lệnh:
# python -m manim -pql main.py TestScene
# ============================================================

class TestScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = T("LLM Serving", size=60, color=WHITE, weight=BOLD)
        subtitle = T("System Optimizations", size=34, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=1.0)
