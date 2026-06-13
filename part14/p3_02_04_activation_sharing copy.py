# -*- coding: utf-8 -*-

import asyncio
import edge_tts
import os

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

os.makedirs("voice", exist_ok=True)

segments = [
    # (
    #     "voice/p3_02_04_01_intro.mp3",
    #     """
    #     Một hướng rất quan trọng trong A-ki-téc-chờ Đi-dai là ác-ti-vây-sần se-rinh,
    #     Trong tắc-xô-nô-mi, ác-ti-vây-sần se-rinh có nhiều biến thể,
    #     Ở đây mình tập trung vào em-kiu-ây và gi-kiu-ây vì hai kỹ thuật này liên quan trực tiếp đến kê-vi cát khi mô-đồl đang phục vụ,
    #     """
    # ),
    # (
    #     "voice/p3_02_04_02_kv_cache.mp3",
    #     """
    #     Trước hết ta cần hiểu kê-vi cát là gì,
    #     Trong a-ten-sần, mô hình dùng ba thành phần, quy-ri, ki và va-liu,
    #     Khi đi-kôu các to-kần trước đó đã được xử lý rồi,
    #     Nếu mỗi lần sinh to-kần mới mà tính lại toàn bộ ki và va-liu của tất cả to-kần cũ thì rất tốn kém,
    #     Vì vậy hệ thống lưu ki và va-liu của các to-kần trước đó vào một vùng nhớ gọi là kê-vi cát,
    #     Khi sinh to-kần mới mô-đồl chỉ cần tạo quy-ri mới rồi đọc ki và va-liu đã lưu trong kê-vi cát để sinh to-kần tiếp theo,
    #     """
    # ),
    (
        "voice/p3_02_04_03_kv_problem.mp3",
        """
        Kê-vi cát giúp tránh tính lại từ đầu nhưng nó cũng tạo ra một vấn đề lớn,
        Càng nhiều to-kần, kê-vi cát càng phình to,
        Càng nhiều rì-khuétt chạy cùng lúc,
        kê-vi cát càng chiếm nhiều bộ nhớ Gi-Pi-U,
        Vì vậy trong serving giảm kích thước kê-vi cát là một hướng tối ưu rất quan trọng,
        """
    ),
    # (
    #     "voice/p3_02_04_04_mha.mp3",
    #     """
    #     Trong măn-ti head a-ten-sần truyền thống,
    #     mỗi a-ten-sần head có bộ ki và va-liu riêng,
    #     Ví dụ quy-ri head một dùng ki một và va-liu một,
    #     Quy-ri head hai dùng ki hai và va-liu hai,
    #     Cứ như vậy mỗi head có một cặp ki va-liu riêng,
    #     Cách này giúp biểu diễn phong phú,
    #     nhưng làm kê-vi cát rất lớn.
    #     """
    # ),
    # (
    #     "voice/p3_02_04_05_mqa.mp3",
    #     """
    #     Măn-ti quy-ri a-ten-sần, viết tắt là em-kiu-ây,
    #     giải quyết bằng cách cho nhiều quy-ri head dùng chung một bộ ki và va-liu,
    #     Tức là quy-ri một, quy-ri hai, quy-ri ba và quy-ri bốn
    #     đều đọc cùng một cặp ki va-liu,
    #     Nhờ vậy, số lượng ki và va-liu cần lưu giảm mạnh,
    #     nên kê-vi cát nhỏ hơn nhiều,
    #     """
    # ),
    # (
    #     "voice/p3_02_04_06_gqa.mp3",
    #     """
    #     Grúp quy-ri a-ten-sần, viết tắt là gi-kiu-ây là cách trung gian,
    #     Thay vì tất cả quy-ri head dùng chung một cặp ki va-liu như em-kiu-ây,
    #     gi-kiu-ây chia các quy-ri head thành nhiều nhóm,
    #     Mỗi nhóm dùng chung một bộ ki và va-liu,
    #     Ví dụ, quy-ri một và hai dùng chung nhóm một,
    #     còn quy-ri ba và bốn dùng chung nhóm hai,
    #     """
    # ),
    # (
    #     "voice/p3_02_04_07_printer.mp3",
    #     """
    #     Có thể hiểu bằng ví dụ máy in, Măn-ti head a-ten-sần giống như mỗi nhân viên có một máy in riêng Rất linh hoạt, nhưng tốn chỗ,
    #     Em-kiu-ây giống như cả công ty dùng chung một máy in Rất tiết kiệm, nhưng có thể hạn chế hơn,
    #     Gi-kiu-ây giống như mỗi phòng ban dùng chung một máy in Vừa tiết kiệm hơn măn-ti head a-ten-sần,
    #     vừa giữ được độ linh hoạt tốt hơn em-kiu-ây,
    #     """
    # ),
    # (
    #     "voice/p3_02_04_08_serving_impact.mp3",
    #     """
    #     Ý nghĩa với eo-eo-em serving là rất lớn,
    #     Em-kiu-ây và gi-kiu-ây giúp giảm kích thước kê-vi cát, giảm áp lực memory bandwidth và làm đi-kôu phase hiệu quả hơn,
    #     Đây là lý do nhiều mô hình ngôn ngữ lớn hiện đại sử dụng gi-kiu-ây hoặc các biến thể tương tự để phục vụ in-phơ-rần tốt hơn.
    #     """
    # ),
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
                raise


async def main():
    for filename, text in segments:
        await generate_audio(filename, text)
    print("Xong! Đã tạo đủ audio cho phần Activation Sharing.")


if __name__ == "__main__":
    asyncio.run(main())