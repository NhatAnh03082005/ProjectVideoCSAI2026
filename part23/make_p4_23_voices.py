import asyncio
import os

import edge_tts


# ============================================================
# PART 4 - SCENE 23: FUTURE DIRECTIONS AND CONCLUSION
#
# Chay:
#   py make_p4_23_voices.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)


segments = [
    (
        "voice/p4_23_01_full_stack.mp3",
        """
        Nhìn lại toàn bộ phần này, eo-eo-em serving là một bài toán full-stack,
        Ta tối ưu từ thuật toán sinh token, kiến trúc mo-đồ, lượng tử hóa, song song hóa, quản lý bộ nhớ,
        lập lịch rùy-quét, cơ-nồ, com-pai-lờ, cho đến phần cứng.
        Mỗi tầng đều có thể trở thành nút thắt nếu bị bỏ qua.
        """,
    ),
    (
        "voice/p4_23_02_future_directions.mp3",
        """
        Tương lai của lĩnh vực này sẽ tiếp tục mở rộng theo nhiều hướng:
        phần cứng ec-seo-lơ-rây-tờ chuyên dụng hơn, đì-cốt-đinh hiệu quả hơn như sờ-péc-kiu-lơ-tịp in-phơ-rần,
        tối ưu loong con-téc, khám phá kiến trúc thay thế truên-pho-mờ, và triển khai trong môi trường phức tạp như edge, hybrid cloud, hoặc đì-xen-trồ-lai com-piu-tin.
        """,
    ),
    (
        "voice/p4_23_03_no_one_size.mp3",
        """
        Bài học quan trọng nhất là không có giải pháp vạn năng, Một chatbot tiu-tam cần lây-ten-ci thấp,Một hệ thống bát ọp-lai cần thờ-ru-pút cao,
        Một thiết bị biên cần tiết kiệm bộ nhớ và điện năng, Vì mục tiêu khác nhau,cách tối ưu cũng phải khác nhau.
        """,
    ),
    (
        "voice/p4_23_04_final.mp3",
        """
        Kết luận lại, thách thức của kỷ nguyên eo-eo-em
        không chỉ là tạo ra mô hình lớn hơn, mà là phục vụ mô hình đó nhanh hơn, rẻ hơn, ổn định hơn và phù hợp hơn với nhu cầu thực tế,
        Khi hiểu được các tầng tối ưu này, ta không chỉ biết chạy một mo-đồ, mà còn biết xây dựng một hệ thống ây-ai có thể phục vụ người dùng ở quy mô thật.
        """,
    ),
]


async def generate_audio(filename: str, text: str, retries: int = 3):
    for attempt in range(1, retries + 1):
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE)
            await communicate.save(filename)
            print(f"Created: {filename}")
            return
        except Exception as exc:
            print(f"Attempt {attempt}/{retries} failed for {filename}: {exc}")
            if attempt == retries:
                raise
            await asyncio.sleep(2)


async def main():
    for filename, text in segments:
        await generate_audio(filename, text)
    print("Done. Created all Part 23 voice files in ./voice")


if __name__ == "__main__":
    asyncio.run(main())
