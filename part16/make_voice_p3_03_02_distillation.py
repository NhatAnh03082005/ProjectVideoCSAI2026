# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN 3.2 - KNOWLEDGE DISTILLATION
# Chạy trong thư mục project:
# python make_voice_p3_03_02_distillation.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_03_02_01_intro.mp3",
        """
        Kỹ thuật đầu tiên là nô-lịch đis-ti-lây-sần,
        hay chưng cất tri thức.
        """
    ),
    (
        "voice/p3_03_02_02_teacher_student.mp3",
        """
        Ý tưởng là dùng một mô-đồl lớn làm ti-chờ,
        rồi huấn luyện một mô-đồl nhỏ hơn làm sờ-tu-đần.
        """
    ),
    (
        "voice/p3_03_02_03_learn_from_teacher.mp3",
        """
        Sờ-tu-đần không chỉ học từ nhãn dữ liệu gốc,
        mà còn học từ đầu ra của ti-chờ.
        Đặc biệt, ti-chờ không chỉ cho biết đáp án đúng,
        mà còn cho biết mức độ tin cậy đối với các lựa chọn khác.
        """
    ),
    (
        "voice/p3_03_02_04_soft_label_example.mp3",
        """
        Ví dụ, ti-chờ không chỉ nói đáp án đúng là A.
        Ti-chờ còn cho biết A có xác suất rất cao,
        B cũng khá hợp lý,
        C thấp hơn,
        và D gần như sai.
        """
    ),
    (
        "voice/p3_03_02_05_soft_label_benefit.mp3",
        """
        Những sóp lây-bồ như vậy giúp sờ-tu-đần
        học được cách ra quyết định của ti-chờ tốt hơn,
        so với việc chỉ học đúng hoặc sai.
        """
    ),
    (
        "voice/p3_03_02_06_goal.mp3",
        """
        Mục tiêu của nô-lịch đis-ti-lây-sần là tạo ra
        một mô-đồl nhỏ hơn, chạy nhanh hơn, tốn ít bộ nhớ hơn,
        nhưng vẫn giữ lại được một phần năng lực của mô-đồl lớn.
        """
    ),
    (
        "voice/p3_03_02_07_analogy.mp3",
        """
        Có thể hình dung ti-chờ như một giáo sư rất giỏi
        nhưng chậm và tốn kém.
        Còn sờ-tu-đần là một trợ giảng nhỏ hơn, rẻ hơn,
        được huấn luyện để bắt chước cách trả lời của giáo sư.
        """
    ),
    (
        "voice/p3_03_02_08_tradeoff.mp3",
        """
        Tuy nhiên, sờ-tu-đần thường không thể mạnh hoàn toàn như ti-chờ.
        Đây vẫn là một trây-đóp giữa chất lượng, tốc độ và chi phí.
        Vì vậy, nô-lịch đis-ti-lây-sần phù hợp khi ta muốn triển khai
        một mô-đồl nhẹ hơn trong môi trường tài nguyên hạn chế,
        nhưng vẫn muốn giữ chất lượng ở mức chấp nhận được.
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
    print("Xong! Đã tạo đủ voice cho phần 3.2 Knowledge Distillation.")


if __name__ == "__main__":
    asyncio.run(main())