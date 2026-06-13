# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO TỔNG KẾT ALGORITHMIC INNOVATIONS VÀ CHUYỂN Ý
# Chạy trong thư mục project:
# python make_voice_p3_03_05_algo_summary_transition.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_03_05_01_intro.mp3",
        """
        Đến đây, chúng ta đã đi qua ba nhóm chính
        của an-gô-rít-mic in-nô-vây-sần.
        """
    ),
    (
        "voice/p3_03_05_02_decoding.mp3",
        """
        Thứ nhất là đi-kôu-đing an-gô-rít-m.
        Nhóm này tối ưu cách mô hình sinh to-kần,
        với các kỹ thuật tiêu biểu như non au-tô-ri-gret-sìv đi-kôu-đing,
        spe-kiu-lây-tiv đi-kôu-đing,
        ơ-li éc-zit-ting
        và két-xkây in-fờ-rần.
        """
    ),
    (
        "voice/p3_03_05_03_architecture.mp3",
        """
        Thứ hai là a-ki-téc-chờ đi-dai.
        Nhóm này tối ưu ngay từ kiến trúc mô hình,
        với các hướng như cờn-phi-giu-rây-sần đao-sai-zing,
        a-ten-sần sim-pli-fi-kây-sần,
        em-kiu-ây và gi-kiu-ây,
        em-âu-i,
        cũng như các kiến trúc ri-cờ-rần hoặc s-tây-spây-s.
        """
    ),
    (
        "voice/p3_03_05_04_compression.mp3",
        """
        Thứ ba là mô-đồl com-press-sần.
        Nhóm này làm mô hình nhỏ hơn, nhẹ hơn và rẻ hơn khi in-fờ-rần,
        với hai kỹ thuật chính là nô-lịch đis-ti-lây-sần
        và nét-quớc pru-ning.
        """
    ),
    (
        "voice/p3_03_05_05_common.mp3",
        """
        Điểm chung của các kỹ thuật này là
        chúng can thiệp vào thuật toán hoặc bản thân mô hình
        để giảm chi phí in-fờ-rần.
        """
    ),
    (
        "voice/p3_03_05_06_simple_image.mp3",
        """
        Nói theo một hình ảnh đơn giản:
        đi-kôu-đing an-gô-rít-m thay đổi cách mô-đồl sinh từng to-kần.
        A-ki-téc-chờ đi-dai thay đổi cấu trúc bên trong mô-đồl.
        Mô-đồl com-press-sần làm mô-đồl nhỏ và nhẹ hơn.
        """
    ),
    (
        "voice/p3_03_05_07_need_system.mp3",
        """
        Tuy nhiên, chỉ tối ưu thuật toán là chưa đủ.
        Khi đưa eo-eo-em vào hệ thống thật,
        ta còn phải tối ưu cách mô-đồl chạy trên Gi-Pi-U,
        cách chia mô-đồl lên nhiều thiết bị,
        cách quản lý bộ nhớ,
        cách lập lịch rì-khuétt,
        và cách tối ưu kơ-nồ.
        """
    ),
    (
        "voice/p3_03_05_08_next.mp3",
        """
        Đó là phần tiếp theo là Sít-tờm ÁP-ti-ma-ZÂY-sần
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

    print("Xong! Đã tạo đủ voice cho phần tổng kết Algorithmic Innovations.")


if __name__ == "__main__":
    asyncio.run(main())