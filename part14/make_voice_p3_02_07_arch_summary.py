# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN CHỐT ARCHITECTURE DESIGN
# Chạy trong thư mục project:
# python make_voice_p3_02_07_arch_summary.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_02_07_01_intro.mp3",
        """
        Tóm lại, Architecture Design tập trung vào việc
        làm cho bản thân mô hình hiệu quả hơn ngay từ thiết kế kiến trúc.
        """
    ),
    (
        "voice/p3_02_07_02_config.mp3",
        """
        Cờn-phi-giu-rây-sần đao-sai-zing
        giảm kích thước cấu hình mô-đồl.
        """
    ),
    (
        "voice/p3_02_07_03_attention.mp3",
        """
        A-ten-sần sim-pli-fi-kây-sần giảm chi phí attention khi sequence dài.
        """
    ),
    (
        "voice/p3_02_07_04_mqa_gqa.mp3",
        """
        Em-kiu-ây và gi-kiu-ây giảm kích thước kê-vi cache và giảm áp lực memory bandwidth trong decode phase.
        """
    ),
    (
        "voice/p3_02_07_05_moe.mp3",
        """
        Em-âu-i chỉ kích hoạt một phần expert cần thiết Nhờ vậy mô hình có thể tăng capacity
        mà không làm compute cho mỗi to-kần tăng tương ứng như mô-đồl dense.
        """
    ),
    (
        "voice/p3_02_07_06_recurrent.mp3",
        """
        Recurrent hoặc state-space architectures
        là hướng nghiên cứu để xử lý sequence dài hiệu quả hơn
        """
    ),
    (
        "voice/p3_02_07_07_tradeoff.mp3",
        """
        Điểm chung là:
        thay đổi kiến trúc có thể đem lại hiệu quả lớn cho serving.
        Nhưng thường đi kèm trade-off về chất lượng,
        độ phức tạp huấn luyện hoặc độ khó khi triển khai hệ thống.
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
    print("Xong! Đã tạo đủ voice cho phần chốt Architecture Design.")


if __name__ == "__main__":
    asyncio.run(main())