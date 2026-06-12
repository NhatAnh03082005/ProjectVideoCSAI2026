import asyncio
import edge_tts
import os

VOICE = "vi-VN-NamMinhNeural"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(script_dir, "voice_part2"), exist_ok=True)

segments = [
    (
        "voice_part2/p2_01.mp3",
        """
        Sau phần mở đầu, chúng ta có thể thấy rằng eo, eo, em không còn chỉ là một mô hình trong phòng thí nghiệm,
        Ngày nay, các mô hình ngôn ngữ lớn đã được triển khai rộng rãi trong rất nhiều ứng dụng thực tế,
        Ứng dụng quen thuộc nhất là chát bót,
        Ví dụ như Chát G P T, Clót, Gem mi nai, hoặc Cô pai lót,
        Người dùng có thể đặt câu hỏi, nhờ giải thích bài học, viết i meo, tóm tắt tài liệu, hoặc hỗ trợ ra quyết định,
        Từ phía người dùng, chát bót có vẻ đơn giản,
        Nhưng phía sau mỗi câu trả lời là một hệ thống phải xử lý pờ rom, chạy mô hình, sinh token, và phản hồi gần như theo thời gian thực.
        """
    ),
    (
        "voice_part2/p2_02.mp3",
        """
        Nhưng eo, eo, em không chỉ dừng lại ở chát bót,
        Một ứng dụng rất phổ biến khác là code den nờ rây sần,
        Các công cụ như git hub, Cô pai lót có thể gợi ý code, hoàn thành hàm, giải thích lỗi, hoặc hỗ trợ lập trình viên viết chương trình nhanh hơn.
        Bên cạnh đó, eo, eo, em còn được dùng cho tát au tu ma sần,
        Ví dụ như phân loại i meo, trích xuất thông tin từ văn bản, tạo báo cáo, hoặc tự động điều phối nhiều bước trong một quy trình làm việc,
        Khi những tác vụ này được đưa vào sản phẩm thật, hệ thống không chỉ cần trả lời đúng, mà còn phải trả lời nhanh và ổn định.
        """
    ),
    (
        "voice_part2/p2_03.mp3",
        """
        Ngoài chát bót và sinh code, eo, eo, em còn được dùng như một pơ sần nồ cô pai lót,
        Nó có thể hỗ trợ người dùng trong công việc hằng ngày, như lên lịch, soạn nội dung, tóm tắt cuộc họp, tìm kiếm thông tin, hoặc hỗ trợ ra quyết định,
        Trong lĩnh vực sáng tạo, eo, eo, em cũng hỗ trợ át cờ ri ây sần.
        Nó có thể viết pờ rom, tạo ý tưởng hình ảnh, xây dựng kịch bản, hoặc kết hợp với mô hình tạo ảnh và video để tạo nội dung đa phương tiện,
        Một hướng nâng cao hơn là rô bô tích cần trôn,
        Ở đây, eo, eo, em giúp rô bốt hiểu lệnh tự nhiên của con người và phân rã nhiệm vụ thành nhiều bước nhỏ.
        """
    ),
    (
        "voice_part2/p2_04.mp3",
        """
        Điểm quan trọng là:
        khi eo, eo, em chỉ là một bản demo nhỏ, một rì quét chậm vài giây vẫn có thể chấp nhận được,
        Nhưng khi eo, eo, em trở thành sản phẩm thật, hệ thống phải phục vụ rất nhiều người dùng cùng lúc,
        Mỗi người có pờ rom khác nhau,
        Độ dài đầu vào khác nhau,
        Và độ dài câu trả lời cũng khác nhau,
        Lúc này, bài toán không còn chỉ là mô hình có thông minh hay không,
        Mà là hệ thống có phục vụ mô hình đó hiệu quả hay không,
        Nói cách khác, trọng tâm chuyển từ mô đồ in theo li dần sang sơ ving e phi xần cì,
        Đây chính là lý do eo, eo, em sơ ving trở thành một bài toán kỹ thuật quan trọng trong các hệ thống A I hiện đại.
        """
    ),
]


async def generate_audio(filename, text, rate="-5%", retries=3):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resolved_path = os.path.join(script_dir, filename)
    for attempt in range(retries):
        try:
            if os.path.exists(resolved_path):
                os.remove(resolved_path)

            communicate = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate=rate,
                volume="+0%"
            )
            await communicate.save(resolved_path)
            print("Generated:", resolved_path)
            return

        except Exception as e:
            print(f"Attempt {attempt + 1} failed ({resolved_path}): {str(e)}")
            if attempt < retries - 1:
                await asyncio.sleep(2)
            else:
                raise


async def main():
    for filename, text in segments:
        rate = "-12%" if "p2_04" in filename else "-5%"
        await generate_audio(filename, text, rate=rate)

    print("Done! Generated part 2 audio files.")


if __name__ == "__main__":
    asyncio.run(main())