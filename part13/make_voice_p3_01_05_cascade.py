# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN 1.5 - CASCADE INFERENCE
# Chạy trong thư mục project:
# python make_voice_p3_01_05_cascade.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_01_05_01_intro.mp3",
        """
        Một hướng khác là két-xkây in-fờ-rần,
        tức là suy luận theo tầng.
        """
    ),
    (
        "voice/p3_01_05_02_multi_model.mp3",
        """
        Thay vì dùng một mô-đồl lớn cho mọi câu hỏi,
        hệ thống có thể tổ chức nhiều mô-đồl từ nhỏ đến lớn.
        """
    ),
    (
        "voice/p3_01_05_03_easy_medium_hard.mp3",
        """
        Câu dễ thì giao cho mô-đồl nhỏ.
        Câu trung bình thì dùng mô-đồl vừa.
        Câu khó mới chuyển sang mô-đồl lớn.
        """
    ),
    (
        "voice/p3_01_05_04_examples.mp3",
        """
        Ví dụ:
        một câu chào hỏi đơn giản có thể dùng mô-đồl nhỏ.
        Một email ngắn có thể dùng mô-đồl vừa.
        Một yêu cầu phân tích tài liệu kỹ thuật dài thì cần mô-đồl lớn.
        """
    ),
    (
        "voice/p3_01_05_05_cost.mp3",
        """
        Cách này giúp tiết kiệm chi phí,
        vì mô-đồl lớn chỉ được dùng khi thật sự cần.
        """
    ),
    (
        "voice/p3_01_05_06_router.mp3",
        """
        Nhưng két-xkây in-fờ-rần cần một bộ định tuyến,
        gọi là rau-tờ,
        để đánh giá rì-khuétt nào dễ,
        rì-khuétt nào khó.
        """
    ),
    (
        "voice/p3_01_05_07_router_risk.mp3",
        """
        Nếu rau-tờ chọn đúng,
        hệ thống vừa nhanh, vừa rẻ.
        Nhưng nếu rau-tờ chọn sai,
        ví dụ câu khó lại đưa cho mô-đồl nhỏ,
        chất lượng câu trả lời sẽ giảm.
        """
    ),
    (
        "voice/p3_01_05_08_summary.mp3",
        """
        Vậy nên két-xkây in-fờ-rần tối ưu ở cấp độ rì-khuétt:
        câu dễ dùng mô-đồl nhỏ để nhanh và rẻ,
        câu khó dùng mô-đồl lớn để giữ chất lượng.
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

    print("Xong! Đã tạo đủ voice cho phần 1.5 Cascade Inference.")


if __name__ == "__main__":
    asyncio.run(main())