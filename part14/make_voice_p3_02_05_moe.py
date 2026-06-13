# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN 2.5 - CONDITIONAL COMPUTING VÀ MOE
# Chạy trong thư mục project:
# python make_voice_p3_02_05_moe.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_02_05_01_intro.mp3",
        """
        Một hướng kiến trúc khác là cờn-đi-sần-nồ com-piu-ting,
        tức là tính toán có điều kiện.
        Ý tưởng chính là không phải mọi to-kần đều cần dùng toàn bộ mô-đồl.
        Thay vào đó, mỗi to-kần chỉ kích hoạt một số phần cần thiết.
        """
    ),
    (
        "voice/p3_02_05_02_router.mp3",
        """
        Ví dụ tiêu biểu là em-âu-i, tức là Mixture of Experts.
        Trong em-âu-i, mô hình có nhiều ép-xpớt.
        Khi một to-kần đi vào, nó sẽ đi qua một rao-tờ.
        Rao-tờ quyết định to-kần này nên được gửi đến ép-xpớt nào.
        Ví dụ, nếu có năm ép-xpớt, một to-kần có thể chỉ kích hoạt ép-xpớt hai và ép-xpớt bốn.
        Các ép-xpớt còn lại không cần chạy cho to-kần đó.
        """
    ),
    (
        "voice/p3_02_05_03_params.mp3",
        """
        Điểm mạnh của em-âu-i là mô hình có thể có tổng số tham số rất lớn,
        nhưng mỗi to-kần chỉ dùng một phần nhỏ trong số đó.
        Nói cách khác, em-âu-i giúp tăng ca-pá-xi-ti của mô hình,
        mà không làm chi phí tính toán cho mỗi to-kần tăng quá nhiều.
        """
    ),
    (
        "voice/p3_02_05_04_analogy.mp3",
        """
        Có thể hình dung đơn giản như một tòa nhà có nhiều phòng chuyên môn.
        To-kần đi vào, rao-tờ chọn vài phòng phù hợp để xử lý,
        thay vì bật toàn bộ tòa nhà.
        Tuy nhiên, các ép-xpớt trong thực tế không nhất thiết có nhãn rõ ràng như ép-xpớt toán hay ép-xpớt code.
        Ép-xpớt là các mạng con được học trong quá trình huấn luyện,
        và rao-tờ cũng được học để phân phối to-kần.
        """
    ),
    (
        "voice/p3_02_05_05_serving.mp3",
        """
        Em-âu-i rất mạnh, nhưng serving em-âu-i phức tạp hơn mô-đồl đen-s thông thường.
        Hệ thống cần rao-tờ chọn ép-xpớt tốt,
        tránh mất cân bằng tải giữa các ép-xpớt,
        và tối ưu cờ-miu-ni-kây-sần khi ép-xpớt nằm trên nhiều Gi-Pi-U.
        """
    ),
    (
        "voice/p3_02_05_06_summary.mp3",
        """
        Tóm lại, em-âu-i giúp tăng ca-pá-xi-ti bằng nhiều ép-xpớt,
        nhưng mỗi to-kần chỉ kích hoạt một phần nhỏ ép-xpớt.
        Đổi lại, hệ thống serving sẽ khó tối ưu hơn.
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
    print("Xong! Đã tạo đủ voice cho phần 2.5 Conditional Computing và MoE.")


if __name__ == "__main__":
    asyncio.run(main())