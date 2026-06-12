import sys
import os
import asyncio
import edge_tts

# Fix Unicode output on Windows console
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============================================================
# TẠO FILE AUDIO BẰNG EDGE-TTS (GIỌNG NAM TIẾNG VIỆT)
# Giọng dùng: vi-VN-NamMinhNeural
#
# Chạy trong thư mục project:
#   uv run python make_quantization_voice.py
# hoặc:
#   python make_quantization_voice.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"  # Giọng nam tiếng Việt

script_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(script_dir, "voice_part1"), exist_ok=True)

# ---- Text segments (p1_01–p1_13) --------------------

segments = [
    (
        "voice_part1/p1_01.mp3",
        """
        Xin chào thầy và các bạn,
        Chủ đề mà chúng ta tìm hiểu ngày hôm nay là:
        Tu guát E phít sừn Dê nờ rây tịp eo, eo em Sơ ving,
        Hay: làm thế nào để phục vụ các mô hình ngôn ngữ lớn một cách hiệu quả hơn trong thực tế.
        """
    ),
    (
        "voice_part1/p1_02.mp3",
        """
        Ngày nay, chúng ta đã rất quen thuộc với các công cụ như Chát G P T, Clót, Gem mi nai hay Cô pai lợt.
        Nhìn từ phía người dùng, mọi thứ có vẻ rất đơn giản,
        Chúng ta nhập một câu hỏi,
        Đợi vài giây,
        Và câu trả lời bắt đầu xuất hiện trên màn hình,
        Nhưng thực tế, để phục vụ hàng triệu người dùng mỗi ngày, phía sau các chatbot này là cả một hệ thống rất lớn.
        """
    ),
    (
        "voice_part1/p1_03.mp3",
        """
        Ví dụ, người dùng nhập prom:
        Rai mi ờ chóp áp li cây sừn i meo,
        Tức là: hãy viết giúp tôi một email xin việc,
        Từ góc nhìn bên ngoài, đây chỉ là một thao tác nhập câu hỏi bình thường.
        """
    ),
    (
        "voice_part1/p1_04.mp3",
        """
        Nhưng phía sau mỗi câu trả lời AI không chỉ là một mô hình thông minh,
        Đằng sau nó là một hệ thống phục vụ mô hình,
        Hệ thống đó được gọi là eo, eo, em, Sơ ving Sít tầm.
        """
    ),
    (
        "voice_part1/p1_05.mp3",
        """
        Một ri quét từ người dùng sẽ đi qua nhiều bước,
        Đầu tiên là người dùng gửi prom,
        Sau đó ri quét được chuyển đến sơ vờ,
        Sơ vờ xử lý đầu vào, chuẩn bị dữ liệu, rồi đưa ri quét vào hệ thống phục vụ mô hình.
        """
    ),
    (
        "voice_part1/p1_06.mp3",
        """
        Tiếp theo, dữ liệu được gửi đến G P U,
        G P U là phần cứng chính dùng để chạy các mô hình ngôn ngữ lớn,
        Ở đây, mô hình sẽ bắt đầu tính toán để tạo ra câu trả lời.
        """
    ),
    (
        "voice_part1/p1_07.mp3",
        """
        Sau khi mô hình chạy in phơ rần, kết quả không được tạo ra một lần toàn bộ,
        Eo, eo, em thường sinh câu trả lời theo từng tô cần,
        Vì vậy, người dùng nhìn thấy câu trả lời xuất hiện dần dần, giống như đang được gõ từng chữ.
        """
    ),
    (
        "voice_part1/p1_08.mp3",
        """
        Như vậy, một câu trả lời tưởng chừng rất đơn giản lại cần cả một pai lai phía sau,
        Từ diu dờ, đến sơ vờ, đến G P U, đến mô hình, rồi cuối cùng là tô cần strim trả về người dùng.
        """
    ),
    (
        "voice_part1/p1_09.mp3",
        """
        Nếu chỉ chạy thử trong môi trường phát triển, mọi thứ khá đơn giản,
        Ta có thể chạy một mô hình cục bộ,
        Gửi một ri quét,
        Kiểm tra kết quả,
        Nhưng trong môi trường prờ đắc sừn, bài toán hoàn toàn khác.
        """
    ),
    (
        "voice_part1/p1_10.mp3",
        """
        Trong thực tế, hệ thống có thể phải phục vụ hàng nghìn hoặc hàng triệu người dùng cùng lúc,
        Mỗi người gửi một prom khác nhau,
        Độ dài đầu vào khác nhau,
        Và độ dài câu trả lời cũng khác nhau,
        Điều này làm cho việc phục vụ eo, eo, em trở nên khó hơn rất nhiều.
        """
    ),
    (
        "voice_part1/p1_11.mp3",
        """
        Khi số lượng ri quét tăng lên, hệ thống bắt đầu gặp nhiều nút thắt,
        Ví dụ:
        độ trễ phản hồi,
        số ri quét xử lý đồng thời,
        giới hạn bộ nhớ G P U,
        và chi phí vận hành rất cao.
        """
    ),
    (
        "voice_part1/p1_12.mp3",
        """
        Vì vậy, vấn đề không còn chỉ là mô hình có thông minh hay không,
        Mà còn là:
        hệ thống có phản hồi đủ nhanh không,
        có chịu tải được không,
        có tiết kiệm G P U không,
        và có ổn định khi triển khai ở quy mô lớn không.
        """
    ),
    (
        "voice_part1/p1_13.mp3",
        """
        Đây chính là câu hỏi trung tâm của eo, eo, em Sơ ving:
        Làm sao phục vụ các mô hình ngôn ngữ lớn nhanh hơn, rẻ hơn và đáng tin cậy hơn?
        Và đó cũng là nội dung chính mà video này sẽ phân tích.
        """
    ),
]


def clean_text(text):
    """Làm sạch text trước khi gửi vào edge-tts."""
    return text.strip()


async def generate_audio(mp3_path, text, retries=5):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resolved_path = os.path.join(script_dir, mp3_path)
    """Tạo file audio bằng edge-tts với retry."""
    text = clean_text(text)

    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate="+0%",
                volume="+0%"
            )

            await communicate.save(resolved_path)
            print(f"[OK] Created: {resolved_path}")
            return

        except Exception as e:
            print(f"[FAIL] Attempt {attempt + 1} ({resolved_path}): {e}")

            if attempt < retries - 1:
                wait_time = 2 * (attempt + 1)
                print(f"[INFO] Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"[ERROR] Failed to generate: {resolved_path}")
                raise


async def main():
    print(f"[INFO] Sử dụng giọng: {VOICE}")

    for mp3_path, text in segments:
        await generate_audio(mp3_path, text)
        await asyncio.sleep(1)

    print("\nDone! Đã tạo xong tất cả các file audio trong thư mục voice/")


if __name__ == "__main__":
    asyncio.run(main())