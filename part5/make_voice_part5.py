import asyncio
import edge_tts
import os

# ============================================================
# PART 5 — AUTOREGRESSIVE DECODING: 15:00 - 19:00
# Tạo 4 file audio, mỗi file tương ứng một video con khoảng 1 phút
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(script_dir, "voice_part5"), exist_ok=True)

segments = [
    (
        "voice_part5/p5_01.mp3",
        """
        Bây giờ chúng ta đến một cơ chế cực kỳ quan trọng trong eo, eo, em in phờ rần: ao tô ri gờ rét xíp đì cốt đình.

        Ý tưởng chính rất đơn giản nhưng lại ảnh hưởng rất lớn đến hiệu năng hệ thống.

        Eo, eo, em không sinh toàn bộ câu trả lời trong một lần.

        Thay vào đó, mô hình sinh từng tóc cần một.

        Tóc cần có thể là một từ, một phần của từ, một dấu câu, hoặc một ký hiệu đặc biệt.

        Ví dụ, nếu pờ rom là: Thủ đô của Việt Nam là, mô hình có thể sinh tóc cần đầu tiên là Hà.

        Sau đó, dựa trên pờ rom ban đầu cộng với tóc cần Hà vừa sinh ra, mô hình tiếp tục sinh tóc cần tiếp theo là Nội.

        Sau đó nó lại sinh dấu chấm.

        Từ góc nhìn người dùng, ta thấy câu trả lời xuất hiện dần dần trên màn hình.

        Nhưng từ góc nhìn hệ thống, mỗi tóc cần mới là một bước in phờ rần riêng.

        Vì vậy, một câu trả lời dài không phải là một lần chạy mô hình, mà là rất nhiều lần chạy nối tiếp nhau.

        Đây là điểm nền tảng để hiểu vì sao eo, eo, em sơ ving khó tăng tốc.
        """
    ),
    (
        "voice_part5/p5_02.mp3",
        """
        Điểm quan trọng nhất của ao tô ri gờ rét xíp đì cốt đình là tóc cần sau phụ thuộc vào tóc cần trước.

        Mô hình không thể sinh tóc cần thứ hai nếu tóc cần thứ nhất chưa được tạo ra.

        Ví dụ, với pờ rom: Thủ đô của Việt Nam là.

        Bước đầu tiên, mô hình dự đoán tóc cần Hà.

        Sau đó tóc cần Hà được nối vào chuỗi ngữ cảnh.

        Bây giờ ngữ cảnh mới trở thành: Thủ đô của Việt Nam là Hà.

        Dựa trên ngữ cảnh mới này, mô hình tiếp tục dự đoán tóc cần Nội.

        Sau đó tóc cần Nội lại được nối vào chuỗi.

        Ngữ cảnh tiếp tục thay đổi thành: Thủ đô của Việt Nam là Hà Nội.

        Cuối cùng, mô hình có thể sinh dấu chấm để kết thúc câu.

        Như vậy, ao pút không được tạo độc lập.

        Mỗi tóc cần mới đều phụ thuộc vào pờ rom ban đầu và toàn bộ các tóc cần đã sinh trước đó.

        Đây là lý do quá trình đi cốt có tính tuần tự rất mạnh.

        Nếu bước trước chưa xong, bước sau chưa thể bắt đầu.
        """
    ),
    (
        "voice_part5/p5_03.mp3",
        """
        Ta có thể hình dung ao tô ri gờ rét xíp đì cốt đình như một vòng lặp.

        Ban đầu, hệ thống có pờ rom của người dùng.

        Pờ rom này được đưa vào mô hình để sinh tóc cần tiếp theo.

        Khi tóc cần mới được sinh ra, hệ thống không dừng lại.

        Tóc cần đó được thêm vào cuối chuỗi hiện tại.

        Sau đó toàn bộ chuỗi mới lại được dùng làm ngữ cảnh cho bước tiếp theo.

        Quá trình này lặp đi lặp lại cho đến khi mô hình sinh đủ số tóc cần, hoặc gặp tóc cần kết thúc.

        Trong cốt mô phỏng, ta có thể thấy vòng lặp rất rõ.

        Mỗi vòng, mô hình gọi hàm đi cốt để lấy nét tóc cần.

        Sau đó nét tóc cần được ờ pen vào danh sách tóc cần hiện tại.

        Chính thao tác ờ pen này làm cho tóc cần mới trở thành một phần của ngữ cảnh cho vòng lặp sau.

        Đây là lý do eo, eo, em in phờ rần khác với việc tính toán toàn bộ ao pút song song.

        Với mỗi ri quét, đì cốt phây phải đi từng bước theo thời gian.

        Điều này tạo ra áp lực lớn cho lây tần xì và khả năng phục vụ nhiều ri quét đồng thời.
        """
    ),
    (
        "voice_part5/p5_04.mp3",
        """
        Chính vì sinh tuần tự từng tóc cần, ao tô ri gờ rét xíp đì cốt đình tạo ra một nút thắt lớn cho eo, eo, em sơ ving.

        Nếu một câu trả lời cần 100 tóc cần, mô hình phải trải qua khoảng 100 bước đì cốt.

        Mỗi bước cần đọc ngữ cảnh, chạy ét ten sần, dùng ca vê két, tính lô gít và chọn tóc cần tiếp theo.

        Với một người dùng, điều này ảnh hưởng trực tiếp đến lây tần xì.

        Người dùng phải chờ tóc cần đầu tiên, rồi đợi từng tóc cần tiếp theo được sờ trim ra.

        Với nhiều người dùng cùng lúc, vấn đề còn lớn hơn nhiều.

        Hệ thống phải phục vụ nhiều chuỗi đì cốt song song có độ dài khác nhau.

        Ri quét ngắn kết thúc nhanh, còn ri quét dài giữ G P U lâu hơn.

        Vì vậy, sơ ving cần các kỹ thuật như bát ching, sờ ke du linh, ca vê két và tối ưu cơ nồ để tận dụng G P U.

        Tóm lại, đì cốt tuần tự giải thích cách eo, eo, em sinh ngôn ngữ từng bước.

        Nhưng đây cũng là lý do khiến lây tần xì và thờ ru pút trở thành thách thức trung tâm.
        """
    ),
]


async def generate_audio(filename, text, rate="+6%", retries=3):
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
        rate = "-5%"
        await generate_audio(filename, text, rate=rate)

    print("Done! Generated part 5 audio files.")


if __name__ == "__main__":
    asyncio.run(main())