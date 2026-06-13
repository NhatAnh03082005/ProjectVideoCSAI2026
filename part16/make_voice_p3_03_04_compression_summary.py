# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN CHỐT MODEL COMPRESSION
# Chạy trong thư mục project:
# python make_voice_p3_03_04_compression_summary.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_03_04_01_intro.mp3",
        """
        Tóm lại, mô-đồl com-press-sần giúp giảm kích thước
        và chi phí in-fờ-rần của mô hình.
        """
    ),
    (
        "voice/p3_03_04_02_distillation.mp3",
        """
        Nô-lịch đis-ti-lây-sần tạo mô-đồl nhỏ
        học theo mô-đồl lớn.
        """
    ),
    (
        "voice/p3_03_04_03_pruning.mp3",
        """
        Nét-quớc pru-ning loại bỏ
        những phần ít quan trọng trong mạng.
        """
    ),
    (
        "voice/p3_03_04_04_tradeoff.mp3",
        """
        Nhưng giống các hướng tối ưu khác,
        mô-đồl com-press-sần cũng có trade-off giữa tốc độ, bộ nhớ và chất lượng.
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

    print("Xong! Đã tạo đủ voice cho phần chốt Model Compression.")


if __name__ == "__main__":
    asyncio.run(main())