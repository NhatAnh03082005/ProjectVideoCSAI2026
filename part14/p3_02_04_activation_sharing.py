# -*- coding: utf-8 -*-

from manim import *
from mutagen.mp3 import MP3
from pathlib import Path
import os


config.background_color = "#0f172a"

BG = "#0f172a"
WHITE = "#e5e7eb"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"
PURPLE = "#a78bfa"
ORANGE = "#fb923c"
MUTED = "#94a3b8"
VI_FONT = "Arial"
FONT = None

_MANIM_TEXT = Text


def has_vietnamese(text):
    vietnamese_chars = (
        "ăâđêôơư"
        "áàảãạấầẩẫậắằẳẵặ"
        "éèẻẽẹếềểễệ"
        "íìỉĩị"
        "óòỏõọốồổỗộớờởỡợ"
        "úùủũụứừửữự"
        "ýỳỷỹỵ"
    )
    lowered = str(text).lower()
    return any(ch in lowered for ch in vietnamese_chars)


def Text(text, *args, font=None, **kwargs):
    if font is None:
        if has_vietnamese(text):
            kwargs["font"] = VI_FONT
    else:
        kwargs["font"] = font
    return _MANIM_TEXT(text, *args, **kwargs)


def audio_duration(path, fallback=10.0):
    if not os.path.exists(path):
        print("[WARNING] Không tìm thấy audio:", path)
        return fallback
    try:
        return MP3(path).info.length
    except Exception:
        return fallback


def fit_text(text, width, height=None):
    if text.width > width:
        text.scale_to_fit_width(width)
    if height is not None and text.height > height:
        text.scale_to_fit_height(height)
    return text


def make_box(text, color, width=2.6, height=0.72, font_size=21, fill=0.13):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.3,
        fill_color=color,
        fill_opacity=fill,
    )

    label = Text(
        text,
        font=FONT,
        font_size=font_size,
        color=WHITE,
        line_spacing=0.82,
    )

    fit_text(label, width - 0.24, height - 0.16)
    label.move_to(box.get_center())

    return VGroup(box, label)


def token_box(text, color=BLUE, width=1.10, height=0.45, font_size=16):
    return make_box(
        text,
        color=color,
        width=width,
        height=height,
        font_size=font_size,
    )


class SceneP3ActivationSharing(Scene):
    def construct(self):
        self.camera.background_color = BG

        root = Path(__file__).resolve().parents[1]
        voice_dir = root / "voice"

        active_mobs = []

        def get_audio_path(filename):
            return str(voice_dir / filename)

        def section_title(text, subtitle, color=WHITE, font_size=28):
            t = Text(text, font=FONT, font_size=font_size, color=color)
            fit_text(t, 10.9)
            t.next_to(subtitle, DOWN, buff=0.30)
            return t

        def bottom_note(text, color=YELLOW, font_size=21, y=-2.28):
            note = Text(text, font=FONT, font_size=font_size, color=color)
            fit_text(note, 10.9)
            note.move_to(DOWN * abs(y))
            return note

        def cache_cells(count, color, cell_width=0.34, cell_height=0.34):
            cells = VGroup()
            for _ in range(count):
                cell = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    stroke_color=color,
                    stroke_width=1.8,
                    fill_color=color,
                    fill_opacity=0.20,
                )
                cells.add(cell)
            cells.arrange(RIGHT, buff=0.06)
            return cells

        def clear_active(play_func, run_time=0.18):
            nonlocal active_mobs
            mobs = [m for m in active_mobs if m is not None]
            if mobs:
                play_func(*[FadeOut(m) for m in mobs], run_time=run_time)
            active_mobs = []

        def set_active(*mobs):
            nonlocal active_mobs
            active_mobs = [m for m in mobs if m is not None]

        def play_segment(filename, fallback_duration, visual_func):
            audio_path = get_audio_path(filename)
            duration = audio_duration(audio_path, fallback=fallback_duration)

            if os.path.exists(audio_path):
                self.add_sound(audio_path)
            else:
                print("[WARNING] Bỏ qua audio vì không tìm thấy:", audio_path)

            local_time = 0.0

            def wait_to(ratio):
                nonlocal local_time
                target = duration * ratio
                delay = max(0, target - local_time)
                if delay > 0:
                    self.wait(delay)
                    local_time += delay

            def play_func(*animations, run_time=0.35, **kwargs):
                nonlocal local_time
                self.play(*animations, run_time=run_time, **kwargs)
                local_time += run_time

            visual_func(wait_to, play_func, duration)

            remain = max(0, duration - local_time)
            if remain > 0:
                self.wait(remain)

        # =====================================================
        # HEADER
        # =====================================================
        title = Text(
            "Activation Sharing: MQA và GQA",
            font=FONT,
            font_size=37,
            color=WHITE,
        )
        fit_text(title, 11.2)
        title.to_edge(UP, buff=0.30)

        subtitle = Text(
            "Giảm KV cache khi serving",
            font=FONT,
            font_size=23,
            color=BLUE,
        )
        fit_text(subtitle, 10.8)
        subtitle.next_to(title, DOWN, buff=0.14)

        # =====================================================
        # 1) INTRO
        # =====================================================
        def visual_intro(wait_to, play, duration):
            mqa = make_box(
                "MQA",
                GREEN,
                width=2.35,
                height=0.88,
                font_size=30,
            )

            gqa = make_box(
                "GQA",
                BLUE,
                width=2.35,
                height=0.88,
                font_size=30,
            )

            pair = VGroup(mqa, gqa)
            pair.arrange(RIGHT, buff=0.80)
            pair.move_to(UP * 0.35)

            kv_focus = make_box(
                "Liên quan trực tiếp\nđến KV cache khi serving",
                PURPLE,
                width=5.40,
                height=0.90,
                font_size=22,
            )
            kv_focus.next_to(pair, DOWN, buff=0.55)

            play(Write(title), run_time=0.55)

            wait_to(0.10)
            play(FadeIn(subtitle, shift=UP), run_time=0.25)

            wait_to(0.35)
            play(FadeIn(pair, shift=UP), run_time=0.35)

            wait_to(0.78)
            play(FadeIn(kv_focus, shift=UP), run_time=0.35)

            set_active(pair, kv_focus)

        play_segment(
            "p3_02_04_01_intro.mp3",
            fallback_duration=12.0,
            visual_func=visual_intro,
        )

        # =====================================================
        # 2) KV CACHE
        # =====================================================
        def visual_kv_cache(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            kv_title = section_title(
                "KV cache là gì?",
                subtitle,
                color=YELLOW,
            )

            qkv_label = Text(
                "Attention dùng ba thành phần",
                font=FONT,
                font_size=23,
                color=WHITE,
            )
            fit_text(qkv_label, 10.5)
            qkv_label.move_to(UP * 1.05)

            q_box = make_box("Query\nQ", BLUE, width=1.45, height=0.72, font_size=20)
            k_box = make_box("Key\nK", GREEN, width=1.45, height=0.72, font_size=20)
            v_box = make_box("Value\nV", PURPLE, width=1.45, height=0.72, font_size=20)

            qkv = VGroup(q_box, k_box, v_box)
            qkv.arrange(RIGHT, buff=0.42)
            qkv.move_to(UP * 0.35)

            old_token = token_box(
                "token cũ",
                BLUE,
                width=1.35,
                height=0.50,
                font_size=16,
            )
            old_token.move_to(LEFT * 4.30 + UP * 0.15)

            kv_pair = make_box(
                "Key / Value\nđã tính",
                YELLOW,
                width=2.05,
                height=0.70,
                font_size=18,
            )
            kv_pair.move_to(LEFT * 2.20 + UP * 0.15)

            cache_frame = RoundedRectangle(
                width=2.55,
                height=1.28,
                corner_radius=0.16,
                stroke_color=YELLOW,
                stroke_width=2.6,
                fill_color=YELLOW,
                fill_opacity=0.08,
            )
            cache_frame.move_to(RIGHT * 0.25 + UP * 0.15)

            cache_label = Text(
                "KV Cache",
                font=FONT,
                font_size=21,
                color=YELLOW,
            )
            cache_label.move_to(cache_frame.get_center() + UP * 0.35)

            cache_data = cache_cells(4, YELLOW, cell_width=0.38)
            cache_data.move_to(cache_frame.get_center() + DOWN * 0.22)

            cache_group = VGroup(cache_frame, cache_label, cache_data)

            next_token = make_box(
                "sinh token\ntiếp theo",
                GREEN,
                width=2.00,
                height=0.72,
                font_size=18,
            )
            next_token.move_to(RIGHT * 4.20 + UP * 0.15)

            new_token = token_box(
                "token mới",
                GREEN,
                width=1.35,
                height=0.50,
                font_size=16,
            )
            new_token.move_to(RIGHT * 4.20 + DOWN * 1.12)

            query_new = make_box(
                "Query mới",
                GREEN,
                width=1.70,
                height=0.56,
                font_size=18,
            )
            query_new.move_to(RIGHT * 2.45 + DOWN * 1.12)

            a_old = Arrow(
                old_token.get_right(),
                kv_pair.get_left(),
                color=MUTED,
                buff=0.12,
            )

            a_cache = Arrow(
                kv_pair.get_right(),
                cache_frame.get_left(),
                color=YELLOW,
                buff=0.12,
            )

            a_next = Arrow(
                cache_frame.get_right(),
                next_token.get_left(),
                color=GREEN,
                buff=0.12,
            )

            a_new_query = Arrow(
                new_token.get_left(),
                query_new.get_right(),
                color=GREEN,
                buff=0.12,
            )

            a_query_cache = Arrow(
                query_new.get_left(),
                cache_frame.get_bottom(),
                color=GREEN,
                buff=0.12,
            )

            kv_note = bottom_note(
                "Lưu Key/Value của token cũ để không tính lại từ đầu",
                color=YELLOW,
                font_size=20,
                y=-2.28,
            )

            wait_to(0.02)
            play(FadeIn(kv_title, shift=UP), run_time=0.24)

            wait_to(0.12)
            play(
                Write(qkv_label),
                FadeIn(qkv, shift=UP),
                run_time=0.45,
            )

            wait_to(0.32)
            play(
                FadeOut(qkv_label),
                FadeOut(qkv),
                run_time=0.20,
            )

            wait_to(0.36)
            play(
                FadeIn(old_token, shift=RIGHT),
                FadeIn(kv_pair, shift=RIGHT),
                Create(a_old),
                run_time=0.42,
            )

            wait_to(0.50)
            play(
                Create(cache_frame),
                Write(cache_label),
                FadeIn(cache_data, shift=UP),
                Create(a_cache),
                FadeIn(kv_note, shift=UP),
                run_time=0.55,
            )

            wait_to(0.72)
            play(
                FadeIn(new_token, shift=LEFT),
                FadeIn(query_new, shift=LEFT),
                Create(a_new_query),
                Create(a_query_cache),
                run_time=0.45,
            )

            wait_to(0.86)
            play(
                FadeIn(next_token, shift=LEFT),
                Create(a_next),
                run_time=0.38,
            )

            set_active(
                kv_title,
                old_token,
                kv_pair,
                cache_group,
                next_token,
                new_token,
                query_new,
                a_old,
                a_cache,
                a_next,
                a_new_query,
                a_query_cache,
                kv_note,
            )

        play_segment(
            "p3_02_04_02_kv_cache.mp3",
            fallback_duration=35.0,
            visual_func=visual_kv_cache,
        )

        # =====================================================
        # 3) KV CACHE PROBLEM
        # =====================================================
        def visual_kv_problem(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            problem_title = section_title(
                "Vấn đề: KV cache phình to",
                subtitle,
                color=RED,
            )

            many_tokens = make_box(
                "Càng nhiều token",
                BLUE,
                width=2.70,
                height=0.72,
                font_size=21,
            )
            many_tokens.move_to(LEFT * 3.75 + UP * 0.55)

            many_requests = make_box(
                "Càng nhiều request",
                PURPLE,
                width=3.00,
                height=0.72,
                font_size=21,
            )
            many_requests.move_to(LEFT * 3.75 + DOWN * 0.45)

            growing_cache = make_box(
                "KV cache\nlớn dần",
                RED,
                width=2.45,
                height=1.05,
                font_size=23,
            )
            growing_cache.move_to(LEFT * 0.55 + UP * 0.05)

            gpu = RoundedRectangle(
                width=3.15,
                height=2.0,
                corner_radius=0.16,
                stroke_color=WHITE,
                stroke_width=2.0,
                fill_color=WHITE,
                fill_opacity=0.04,
            )
            gpu.move_to(RIGHT * 3.25 + UP * 0.05)

            gpu_label = Text(
                "GPU memory",
                font=FONT,
                font_size=22,
                color=WHITE,
            )
            gpu_label.next_to(gpu, UP, buff=0.16)

            blocks = VGroup()
            for _ in range(12):
                blocks.add(
                    Rectangle(
                        width=0.38,
                        height=0.30,
                        stroke_color=RED,
                        fill_color=RED,
                        fill_opacity=0.30,
                    )
                )
            blocks.arrange_in_grid(rows=3, cols=4, buff=0.12)
            blocks.move_to(gpu.get_center())

            p1 = Arrow(
                many_tokens.get_right(),
                growing_cache.get_left(),
                color=BLUE,
                buff=0.14,
            )

            p2 = Arrow(
                many_requests.get_right(),
                growing_cache.get_left(),
                color=PURPLE,
                buff=0.14,
            )

            p3 = Arrow(
                growing_cache.get_right(),
                gpu.get_left(),
                color=RED,
                buff=0.14,
            )

            problem_note = bottom_note(
                "Serving cần giảm kích thước KV cache",
                color=YELLOW,
                font_size=21,
                y=-2.28,
            )

            wait_to(0.02)
            play(FadeIn(problem_title, shift=UP), run_time=0.25)

            wait_to(0.16)
            play(
                FadeIn(many_tokens, shift=RIGHT),
                Create(p1),
                run_time=0.35,
            )

            wait_to(0.30)
            play(
                FadeIn(growing_cache, scale=0.96),
                run_time=0.32,
            )

            wait_to(0.52)
            play(
                FadeIn(many_requests, shift=RIGHT),
                Create(p2),
                run_time=0.35,
            )

            wait_to(0.72)
            play(
                Create(gpu),
                Write(gpu_label),
                Create(p3),
                FadeIn(blocks, shift=UP),
                FadeIn(problem_note, shift=UP),
                run_time=0.55,
            )

            set_active(
                problem_title,
                many_tokens,
                many_requests,
                growing_cache,
                gpu,
                gpu_label,
                blocks,
                p1,
                p2,
                p3,
                problem_note,
            )

        play_segment(
            "p3_02_04_03_kv_problem.mp3",
            fallback_duration=16.0,
            visual_func=visual_kv_problem,
        )

        # =====================================================
        # 4) MHA
        # =====================================================
        def visual_mha(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            mha_title = section_title(
                "MHA: mỗi head có K/V riêng",
                subtitle,
                color=RED,
            )

            head_rows = VGroup()
            for i, y in enumerate([0.88, 0.30, -0.28, -0.86], start=1):
                q = make_box(
                    f"Q{i}",
                    BLUE,
                    width=1.00,
                    height=0.46,
                    font_size=18,
                )
                kv = make_box(
                    f"K{i}, V{i}",
                    RED,
                    width=1.55,
                    height=0.46,
                    font_size=17,
                )

                q.move_to(LEFT * 2.85 + UP * y)
                kv.move_to(LEFT * 0.55 + UP * y)

                arr = Arrow(
                    q.get_right(),
                    kv.get_left(),
                    color=MUTED,
                    buff=0.12,
                    stroke_width=2.1,
                )

                head_rows.add(VGroup(q, arr, kv))

            mha_cache = cache_cells(10, RED, cell_width=0.28)
            mha_cache.move_to(RIGHT * 3.35 + DOWN * 0.15)

            mha_cache_label = Text(
                "KV cache lớn",
                font=FONT,
                font_size=21,
                color=RED,
            )
            mha_cache_label.next_to(mha_cache, UP, buff=0.20)

            mha_note = bottom_note(
                "Biểu diễn phong phú, nhưng tốn nhiều KV cache",
                color=RED,
                font_size=21,
                y=-2.28,
            )

            wait_to(0.02)
            play(FadeIn(mha_title, shift=UP), run_time=0.25)

            wait_to(0.18)
            play(FadeIn(head_rows[0], shift=RIGHT), run_time=0.28)

            wait_to(0.30)
            play(FadeIn(head_rows[1], shift=RIGHT), run_time=0.28)

            wait_to(0.42)
            play(FadeIn(head_rows[2], shift=RIGHT), run_time=0.28)

            wait_to(0.54)
            play(FadeIn(head_rows[3], shift=RIGHT), run_time=0.28)

            wait_to(0.72)
            play(
                FadeIn(mha_cache_label, shift=UP),
                FadeIn(mha_cache, shift=UP),
                FadeIn(mha_note, shift=UP),
                run_time=0.45,
            )

            set_active(
                mha_title,
                head_rows,
                mha_cache,
                mha_cache_label,
                mha_note,
            )

        play_segment(
            "p3_02_04_04_mha.mp3",
            fallback_duration=13.0,
            visual_func=visual_mha,
        )

        # =====================================================
        # 5) MQA
        # =====================================================
        def visual_mqa(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            mqa_title = section_title(
                "MQA: nhiều Query head dùng chung K/V",
                subtitle,
                color=GREEN,
                font_size=27,
            )

            q_heads = VGroup()
            for i in range(1, 5):
                q_heads.add(
                    make_box(
                        f"Q{i}",
                        BLUE,
                        width=1.05,
                        height=0.46,
                        font_size=18,
                    )
                )

            q_heads.arrange(DOWN, buff=0.16)
            q_heads.move_to(LEFT * 3.25 + DOWN * 0.05)

            shared_kv = make_box(
                "Chung\nK, V",
                GREEN,
                width=1.95,
                height=0.96,
                font_size=23,
            )
            shared_kv.move_to(RIGHT * 0.05 + DOWN * 0.05)

            shared_arrows = VGroup()
            for q in q_heads:
                shared_arrows.add(
                    Arrow(
                        q.get_right(),
                        shared_kv.get_left(),
                        color=GREEN,
                        buff=0.12,
                        stroke_width=2.0,
                    )
                )

            mqa_cache = cache_cells(4, GREEN, cell_width=0.32)
            mqa_cache.move_to(RIGHT * 3.45 + DOWN * 0.15)

            mqa_cache_label = Text(
                "KV cache nhỏ hơn",
                font=FONT,
                font_size=21,
                color=GREEN,
            )
            mqa_cache_label.next_to(mqa_cache, UP, buff=0.20)

            mqa_note = bottom_note(
                "Số lượng Key/Value cần lưu giảm mạnh",
                color=GREEN,
                font_size=21,
                y=-2.28,
            )

            wait_to(0.02)
            play(FadeIn(mqa_title, shift=UP), run_time=0.25)

            wait_to(0.22)
            play(FadeIn(q_heads, shift=RIGHT), run_time=0.32)

            wait_to(0.48)
            play(
                FadeIn(shared_kv, scale=0.96),
                Create(shared_arrows),
                run_time=0.45,
            )

            wait_to(0.72)
            play(
                FadeIn(mqa_cache_label, shift=UP),
                FadeIn(mqa_cache, shift=UP),
                FadeIn(mqa_note, shift=UP),
                run_time=0.45,
            )

            set_active(
                mqa_title,
                q_heads,
                shared_kv,
                shared_arrows,
                mqa_cache,
                mqa_cache_label,
                mqa_note,
            )

        play_segment(
            "p3_02_04_05_mqa.mp3",
            fallback_duration=13.0,
            visual_func=visual_mqa,
        )

        # =====================================================
        # 6) GQA
        # =====================================================
        def visual_gqa(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            gqa_title = section_title(
                "GQA: Query head chia thành nhóm",
                subtitle,
                color=BLUE,
                font_size=27,
            )

            q1 = make_box("Q1", BLUE, width=1.00, height=0.44, font_size=17)
            q2 = make_box("Q2", BLUE, width=1.00, height=0.44, font_size=17)
            q3 = make_box("Q3", BLUE, width=1.00, height=0.44, font_size=17)
            q4 = make_box("Q4", BLUE, width=1.00, height=0.44, font_size=17)

            group_a = VGroup(q1, q2)
            group_b = VGroup(q3, q4)
            group_a.arrange(DOWN, buff=0.14)
            group_b.arrange(DOWN, buff=0.14)
            group_a.move_to(LEFT * 3.20 + UP * 0.55)
            group_b.move_to(LEFT * 3.20 + DOWN * 0.75)

            kv_a = make_box(
                "K,V\nnhóm 1",
                YELLOW,
                width=1.95,
                height=0.72,
                font_size=19,
            )
            kv_b = make_box(
                "K,V\nnhóm 2",
                YELLOW,
                width=1.95,
                height=0.72,
                font_size=19,
            )

            kv_a.move_to(RIGHT * 0.10 + UP * 0.55)
            kv_b.move_to(RIGHT * 0.10 + DOWN * 0.75)

            ga_box = SurroundingRectangle(
                VGroup(group_a, kv_a),
                color=YELLOW,
                buff=0.18,
                corner_radius=0.12,
                stroke_width=1.8,
            )

            gb_box = SurroundingRectangle(
                VGroup(group_b, kv_b),
                color=YELLOW,
                buff=0.18,
                corner_radius=0.12,
                stroke_width=1.8,
            )

            ga_arrows = VGroup(
                Arrow(q1.get_right(), kv_a.get_left(), color=YELLOW, buff=0.12, stroke_width=2.0),
                Arrow(q2.get_right(), kv_a.get_left(), color=YELLOW, buff=0.12, stroke_width=2.0),
            )

            gb_arrows = VGroup(
                Arrow(q3.get_right(), kv_b.get_left(), color=YELLOW, buff=0.12, stroke_width=2.0),
                Arrow(q4.get_right(), kv_b.get_left(), color=YELLOW, buff=0.12, stroke_width=2.0),
            )

            gqa_cache = cache_cells(6, YELLOW, cell_width=0.30)
            gqa_cache.move_to(RIGHT * 3.45 + DOWN * 0.10)

            gqa_cache_label = Text(
                "KV cache trung gian",
                font=FONT,
                font_size=20,
                color=YELLOW,
            )
            gqa_cache_label.next_to(gqa_cache, UP, buff=0.20)

            gqa_note = bottom_note(
                "Tiết kiệm hơn MHA, linh hoạt hơn MQA",
                color=YELLOW,
                font_size=21,
                y=-2.28,
            )

            wait_to(0.02)
            play(FadeIn(gqa_title, shift=UP), run_time=0.25)

            wait_to(0.32)
            play(
                FadeIn(group_a, shift=RIGHT),
                FadeIn(kv_a, shift=LEFT),
                Create(ga_arrows),
                Create(ga_box),
                run_time=0.48,
            )

            wait_to(0.62)
            play(
                FadeIn(group_b, shift=RIGHT),
                FadeIn(kv_b, shift=LEFT),
                Create(gb_arrows),
                Create(gb_box),
                run_time=0.48,
            )

            wait_to(0.80)
            play(
                FadeIn(gqa_cache_label, shift=UP),
                FadeIn(gqa_cache, shift=UP),
                FadeIn(gqa_note, shift=UP),
                run_time=0.45,
            )

            set_active(
                gqa_title,
                group_a,
                group_b,
                kv_a,
                kv_b,
                ga_box,
                gb_box,
                ga_arrows,
                gb_arrows,
                gqa_cache,
                gqa_cache_label,
                gqa_note,
            )

        play_segment(
            "p3_02_04_06_gqa.mp3",
            fallback_duration=14.0,
            visual_func=visual_gqa,
        )

        # =====================================================
        # 7) PRINTER ANALOGY
        # =====================================================
        def visual_printer(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            printer_title = section_title(
                "Ví dụ máy in",
                subtitle,
                color=ORANGE,
            )

            def printer_card(title_text, desc_text, color, x):
                header = make_box(
                    title_text,
                    color,
                    width=2.35,
                    height=0.55,
                    font_size=20,
                )
                header.move_to(RIGHT * x + UP * 0.95)

                desc = Text(
                    desc_text,
                    font=FONT,
                    font_size=17,
                    color=WHITE,
                    line_spacing=0.80,
                )
                fit_text(desc, 2.70, 1.80)
                desc.next_to(header, DOWN, buff=0.22)

                outline = SurroundingRectangle(
                    VGroup(header, desc),
                    color=color,
                    buff=0.18,
                    corner_radius=0.12,
                    stroke_width=1.7,
                )

                return VGroup(outline, header, desc)

            col_mha = printer_card(
                "MHA",
                "Mỗi nhân viên\nmột máy in\n\nLinh hoạt\nnhưng tốn chỗ",
                RED,
                -4.0,
            )

            col_mqa = printer_card(
                "MQA",
                "Cả công ty\nmột máy in\n\nRất tiết kiệm\nnhưng hạn chế hơn",
                GREEN,
                0.0,
            )

            col_gqa = printer_card(
                "GQA",
                "Mỗi phòng ban\nmột máy in\n\nCân bằng hơn",
                BLUE,
                4.0,
            )

            printer_note = bottom_note(
                "MHA: nhiều K/V   |   MQA: một K/V   |   GQA: K/V theo nhóm",
                color=YELLOW,
                font_size=19,
                y=-2.28,
            )

            wait_to(0.02)
            play(FadeIn(printer_title, shift=UP), run_time=0.25)

            wait_to(0.16)
            play(FadeIn(col_mha, shift=UP), run_time=0.45)

            wait_to(0.46)
            play(FadeIn(col_mqa, shift=UP), run_time=0.45)

            wait_to(0.68)
            play(FadeIn(col_gqa, shift=UP), run_time=0.45)

            wait_to(0.88)
            play(FadeIn(printer_note, shift=UP), run_time=0.35)

            set_active(
                printer_title,
                col_mha,
                col_mqa,
                col_gqa,
                printer_note,
            )

        play_segment(
            "p3_02_04_07_printer.mp3",
            fallback_duration=18.0,
            visual_func=visual_printer,
        )

        # =====================================================
        # 8) SERVING IMPACT
        # =====================================================
        def visual_impact(wait_to, play, duration):
            clear_active(play, run_time=0.16)

            impact_title = section_title(
                "Ý nghĩa với LLM Serving",
                subtitle,
                color=GREEN,
            )

            b1 = make_box(
                "KV cache\nnhỏ hơn",
                GREEN,
                width=2.35,
                height=0.82,
                font_size=21,
            )

            b2 = make_box(
                "Giảm memory\nbandwidth",
                BLUE,
                width=2.55,
                height=0.82,
                font_size=21,
            )

            b3 = make_box(
                "Decode phase\nhiệu quả hơn",
                YELLOW,
                width=2.60,
                height=0.82,
                font_size=21,
            )

            chain = VGroup(b1, b2, b3)
            chain.arrange(RIGHT, buff=0.62)
            chain.move_to(UP * 0.35)

            c1 = Arrow(
                b1.get_right(),
                b2.get_left(),
                color=MUTED,
                buff=0.12,
            )

            c2 = Arrow(
                b2.get_right(),
                b3.get_left(),
                color=MUTED,
                buff=0.12,
            )

            final = make_box(
                "Nhiều LLM hiện đại dùng GQA\nhoặc biến thể tương tự",
                PURPLE,
                width=5.70,
                height=0.92,
                font_size=21,
            )
            final.move_to(DOWN * 1.25)

            wait_to(0.02)
            play(FadeIn(impact_title, shift=UP), run_time=0.25)

            wait_to(0.12)
            play(FadeIn(b1, shift=UP), run_time=0.28)

            wait_to(0.28)
            play(
                Create(c1),
                FadeIn(b2, shift=UP),
                run_time=0.30,
            )

            wait_to(0.44)
            play(
                Create(c2),
                FadeIn(b3, shift=UP),
                run_time=0.30,
            )

            wait_to(0.68)
            play(FadeIn(final, shift=UP), run_time=0.35)

            set_active(
                impact_title,
                chain,
                c1,
                c2,
                final,
            )

        play_segment(
            "p3_02_04_08_serving_impact.mp3",
            fallback_duration=14.0,
            visual_func=visual_impact,
        )

        # =====================================================
        # END
        # =====================================================
        final_mobs = [m for m in active_mobs if m is not None]
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            *[FadeOut(m) for m in final_mobs],
            run_time=0.45,
        )
