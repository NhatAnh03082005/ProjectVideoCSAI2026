# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN 3.3 - NETWORK PRUNING
# Chạy trong thư mục project:
# python make_voice_p3_03_03_pruning.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_03_03_01_intro.mp3",
        """
        Kỹ thuật thứ hai là nét-quớc pru-ning,
        tức là cắt tỉa mô hình.
        """
    ),
    (
        "voice/p3_03_03_02_big_network.mp3",
        """
        Ý tưởng là trong một mạng niu-rồ lớn,
        không phải mọi phần đều quan trọng như nhau.
        Một số wây, niu-rôn, a-ten-sần head,
        lây-ờ hoặc blóc có thể đóng góp ít hơn cho kết quả cuối cùng.
        """
    ),
    (
        "voice/p3_03_03_03_remove_parts.mp3",
        """
        Pru-ning cố gắng xác định
        và loại bỏ những phần ít quan trọng đó.
        Trên hình, các phần mờ màu đỏ là những phần sẽ bị cắt bỏ.
        """
    ),
    (
        "voice/p3_03_03_04_levels.mp3",
        """
        Có thể pru-ning ở nhiều mức:
        cắt wây riêng lẻ,
        cắt niu-rôn,
        cắt a-ten-sần head,
        cắt lây-ờ,
        hoặc cắt cả blóc.
        """
    ),
    (
        "voice/p3_03_03_05_goal.mp3",
        """
        Mục tiêu là giảm kích thước mô-đồl
        và giảm số phép tính.
        Nói cách khác, mô hình sau khi cắt tỉa
        có thể nhỏ hơn và nhẹ hơn khi phục vụ.
        """
    ),
    (
        "voice/p3_03_03_06_warning.mp3",
        """
        Nhưng có một điểm rất quan trọng:
        Pru-ning không tự động làm mô-đồl chạy nhanh hơn.
        """
    ),
    (
        "voice/p3_03_03_07_unstructured.mp3",
        """
        Nếu ta chỉ cắt wây rời rạc,
        nhưng Gi-Pi-U và kơ-nồ vẫn không tận dụng được sự thưa đó,
        tốc độ thực tế có thể không tăng nhiều.
        Đây là vấn đề của ân-strắc-chờd pru-ning.
        """
    ),
    (
        "voice/p3_03_03_08_structured.mp3",
        """
        Vì vậy, pru-ning hiệu quả nhất thường là strắc-chờd pru-ning,
        tức là cắt theo cấu trúc rõ ràng.
        Ví dụ, cắt cả head, cả niu-rôn, cả blóc,
        hoặc theo dạng sờ-pa-sì-ti mà phần cứng hỗ trợ.
        """
    ),
    (
        "voice/p3_03_03_09_summary.mp3",
        """
        Nói ngắn gọn:
        Pru-ning không chỉ là cắt bớt tham số,
        mà phải cắt theo cách hệ thống in-fờ-rần có thể tận dụng được.
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
    print("Xong! Đã tạo đủ voice cho phần 3.3 Network Pruning.")


if __name__ == "__main__":
    asyncio.run(main())