# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

# ============================================================
# TẠO VOICE CHO PHẦN 2.6 - RECURRENT UNIT VÀ ALTERNATIVE ARCHITECTURES
# Chạy trong thư mục project:
# python make_voice_p3_02_06_recurrent.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_02_06_01_intro.mp3",
        """
        Ngoài việc tối ưu Trăn-pho-mơ, còn có các hướng kiến trúc thay thế.
        Một vài ví dụ là A rờ đắp-liu kê-vi, Rét-nét, hoặc các s-tây-spây-s mô-đồl.
        Mục tiêu của các hướng này là giảm sự phụ thuộc vào a-ten-sần toàn cục,
        đặc biệt khi xử lý xi-quần dài.
        """
    ),
    (
        "voice/p3_02_06_02_transformer_attention.mp3",
        """
        Trăn-pho-mơ rất mạnh vì a-ten-sần cho phép một to-kần mới
        kết nối với nhiều to-kần trước đó trong ngữ cảnh.
        Trên hình, các đường màu xanh thể hiện to-kần mới đang nhìn lại nhiều to-kần cũ.
        Nhưng khi chuỗi dài hơn, attention map sẽ lớn hơn.
        Attention chuẩn vì vậy có thể tốn nhiều bộ nhớ và tính toán.
        """
    ),
    (
        "voice/p3_02_06_03_recurrent_state.mp3",
        """
        Các kiến trúc dạng ri-cờ-rần hoặc s-tây-spây-s cố gắng xử lý chuỗi theo cách khác.
        Thay vì lưu và nhìn lại toàn bộ quan hệ giữa các to-kần,
        mô hình duy trì một trạng thái nén.
        Ở mỗi bước, state cũ và to-kần mới đi vào ri-cờ-rần unit.
        Sau đó mô hình tạo ra state mới.
        Chuỗi h không, h một, h hai, h ba ở phía trên minh họa state được cập nhật tuần tự theo thời gian.
        """
    ),
    (
        "voice/p3_02_06_04_cost_caveat.mp3",
        """
        Nhờ cách cập nhật state như vậy, trong một số trường hợp,
        chi phí có thể tuyến tính hơn theo độ dài chuỗi.
        Bên trái là full a-ten-sần, chi phí tăng nhanh khi context dài.
        Bên phải là state update, chi phí tăng đều hơn.
        Tuy nhiên, cần nói cẩn thận:
        đây không phải là giải pháp thay thế Trăn-pho-mơ trong mọi trường hợp.
        """
    ),
    (
        "voice/p3_02_06_05_summary.mp3",
        """
        Trăn-pho-mơ vẫn là nền tảng chính của rất nhiều eo-eo-em hiện đại.
        Các kiến trúc rì - CỜ - rần và s-tây-spây-s là hướng nghiên cứu quan trọng.
        Nhưng hiệu quả còn phụ thuộc vào bài toán, dữ liệu huấn luyện,
        phần cứng, và cách triển khai in-fờ-rần.
        Vì vậy, ý chính là:
        rì-CỜ-rần và s-tây-spây-s Á-khờ-kà-tếch-chờ-zờ có thể giúp xử lý xi-quần dài hiệu quả hơn,
        nhưng hiện tại chưa phải lời giải thay thế hoàn toàn Trăn-pho-mơ trong mọi tình huống.
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
    print("Xong! Đã tạo đủ voice cho phần 2.6 Recurrent Unit.")


if __name__ == "__main__":
    asyncio.run(main())