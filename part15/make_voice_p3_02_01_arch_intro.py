# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN 2.1 - ARCHITECTURE DESIGN LÀ GÌ?
# Chạy trong thư mục project:
# python make_voice_p3_02_01_arch_intro.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_02_01_01_intro.mp3",
        """
        Nhóm thứ hai là A-ki-téc-chờ Đi-dai,
        tức là tối ưu thiết kế kiến trúc mô hình.
        """
    ),
    (
        "voice/p3_02_01_02_inside_structure.mp3",
        """
        A-ki-téc-chờ Đi-dai tập trung vào
        bản thân cấu trúc bên trong mô hình.
        """
    ),
    (
        "voice/p3_02_01_03_transformer_decoder.mp3",
        """
        Phần lớn eo-eo-em hiện nay
        vẫn dựa trên Trăn-pho-mơ đi-kôu-đờ.
        """
    ),
    (
        "voice/p3_02_01_04_attention_ffn.mp3",
        """
        Trong Trăn-pho-mơ,
        hai thành phần rất quan trọng là a-ten-sần
        và feed-forward network,
        hay ép-ép-en.
        """
    ),
    (
        "voice/p3_02_01_05_attention_cost.mp3",
        """
        A-ten-sần giúp mô hình hiểu quan hệ giữa các to-kần.
        Nhưng khi chuỗi dài,
        a-ten-sần có thể rất tốn bộ nhớ và tính toán.
        """
    ),
    (
        "voice/p3_02_01_06_ffn_cost.mp3",
        """
        Ép-ép-en chứa rất nhiều tham số
        và cũng đóng góp lớn vào chi phí in-fờ-rần.
        """
    ),
    (
        "voice/p3_02_01_07_goal.mp3",
        """
        Vì vậy, các hướng A-ki-téc-chờ Đi-dai
        cố gắng làm cho mô hình hiệu quả hơn ngay từ kiến trúc,
        nhưng vẫn giữ năng lực biểu diễn tốt.
        """
    ),
]


async def generate_audio(filename, text, retries=3):
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate=RATE,
            )
            await communicate.save(filename)
            print("Đã tạo:", filename)
            return
        except Exception as e:
            print(f"Lần {attempt + 1} thất bại ({filename}): {str(e)}")
            if attempt < retries - 1:
                await asyncio.sleep(2)
            else:
                print(f"Không thể tạo {filename} sau {retries} lần thử")
                raise


async def main():
    for filename, text in segments:
        await generate_audio(filename, text)

    print("Xong! Đã tạo đủ voice cho phần 2.1 Architecture Design.")


if __name__ == "__main__":
    asyncio.run(main())