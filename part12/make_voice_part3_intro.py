import asyncio
import edge_tts
import os

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p3_00_01_hook.mp3",
        """
        Ở phần trước, chúng ta đã thấy rằng eo-eo-em Serving không đơn giản chỉ là chạy một mô hình lớn,
        Khi phục vụ mô hình ngôn ngữ lớn trong thực tế, hệ thống phải đối mặt với nhiều thách thức
        """
    ),

    (
        "voice/p3_00_02_question.mp3",
        """
        Vậy câu hỏi tiếp theo là:
        làm sao để tối ưu quá trình phục vụ mô hình ngôn ngữ lớn,
        """
    ),

    (
        "voice/p3_00_03_two_groups.mp3",
        """
        Nhìn tổng quát, các hướng tối ưu quá trình phục vụ mô hình ngôn ngữ lớn có thể chia thành hai nhóm lớn,

        Nhóm thứ nhất là An-gờ-rít-thờ-mịch In-nơ-vây-sầnz,
        tức là cải tiến ở mức thuật toán hoặc thiết kế mô hình,

        Nhóm thứ hai là Sít-tờm ÁP-ti-ma-ZÂY-sần,
        tức là tối ưu cách hệ thống chạy mô hình trên phần cứng thật,
        """
    ),

    (
        "voice/p3_00_04_algorithmic_focus.mp3",
        """
        Trong phần này, mình sẽ tập trung vào An-gờ-rít-thờ-mịch In-nơ-vây-sầnz,

        Thay vì chỉ hỏi: làm sao chạy mô-đồl nhanh hơn trên Gi-Pi-U,
        nhóm này đặt ra một câu hỏi sâu hơn:

        Có thể thay đổi cách mô hình suy luận để ngay từ đầu nó đã nhẹ hơn,
        nhanh hơn, hoặc ít tốn tài nguyên hơn không?
        """
    ),

    (
        "voice/p3_00_05_three_groups.mp3",
        """
        Để trả lời câu hỏi đó,
        phần An-gờ-rít-thờ-mịch In-nơ-vây-sầnz sẽ đi qua ba nhóm chính,

        Thứ nhất là đi-kôu-đình a-gờ-rít-đờm,
        tức là tối ưu cách mô hình sinh tâu-kần,

        Thứ hai là A-ki-tếch-chờ Đi-dai,
        tức là thay đổi kiến trúc bên trong mô hình để suy luận hiệu quả hơn,

        Thứ ba là mô-đồl cầm-prét-sần,
        tức là nén mô hình để nó nhỏ hơn, nhanh hơn và rẻ hơn khi triển khai,
        """
    ),

    (
        "voice/p3_00_06_goal.mp3",
        """
        Mục tiêu chung của các kỹ thuật này là giảm độ trễ,
        giảm lượng tính toán, giảm bộ nhớ và giảm chi phí suy luận,
        nhưng vẫn cố gắng giữ chất lượng đầu ra tốt nhất có thể,
        """
    ),
]


async def generate_audio(filename, text, retries=3):
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE)
            await communicate.save(filename)
            print("Đã tạo:", filename)
            return
        except Exception as e:
            print(f"Lần {attempt + 1} thất bại ({filename}): {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2)
            else:
                raise


async def main():
    for filename, text in segments:
        await generate_audio(filename, text)

    print("Xong voice phần 3!")


if __name__ == "__main__":
    asyncio.run(main())