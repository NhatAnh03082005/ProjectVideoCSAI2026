import asyncio
import edge_tts
import os

# ============================================================
# PART 6 — pờ rì phiu VS đì cốt & KV két: 19:00 - 23:00
# Tạo 4 file audio, mỗi file tương ứng một video con khoảng 1 phút
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(script_dir, "voice_part6"), exist_ok=True)

segments = [
    (
        "voice_part6/p6_01.mp3",
        """
        Sau khi hiểu ao tô ri gờ rét xíp đì cốt đình, chúng ta có thể chia một rì quét eo, eo, em thành hai pha chính.

        Hai pha đó là pờ rì phiu và đì cốt.

        pờ rì phiu còn được gọi là con tét phây.

        Đây là pha mô hình đọc toàn bộ pờ rom ban đầu của người dùng.

        Ví dụ, nếu người dùng nhập một pờ rom dài gồm nhiều câu, thì ở pha pờ rì phiu, hệ thống sẽ xử lý tất cả các tóc cần trong pờ rom đó.

        Mục tiêu của pờ rì phiu là xây dựng biểu diễn ngữ cảnh ban đầu để mô hình hiểu người dùng đang hỏi gì.

        Sau pờ rì phiu, hệ thống bước sang pha đì cốt.

        đì cốt là pha sinh từng tóc cần đầu ra.

        Mỗi lần đì cốt, mô hình dự đoán một tóc cần mới, nối tóc cần đó vào chuỗi hiện tại, rồi tiếp tục sinh tóc cần kế tiếp.

        Vì vậy, nếu pờ rì phiu giống như đọc đề bài, thì đì cốt giống như viết câu trả lời từng chữ một.

        Sự khác biệt này rất quan trọng trong eo, eo, em sơ ving.

        Vì pờ rì phiu và đì cốt có đặc điểm tính toán khác nhau, bo đồ néc khác nhau, và cách tối ưu cũng khác nhau.
        """
    ),
    (
        "voice_part6/p6_02.mp3",
        """
        Bây giờ ta nhìn kỹ hơn vào pha pờ rì phiu.

        Trong pờ rì phiu, hệ thống nhận pờ rom ban đầu từ người dùng.

        pờ rom này được tóc cần nai dờ chuyển thành một chuỗi tóc cần.

        Sau đó, toàn bộ chuỗi tóc cần của pờ rom được đưa qua mô hình.

        Điểm quan trọng là các tóc cần trong pờ rom đã có sẵn ngay từ đầu.

        Vì vậy, trong nhiều trường hợp, mô hình có thể xử lý nhiều tóc cần của pờ rom song song hơn so với pha đì cốt.

        Đây là lý do pờ rì phiu thường có đặc điểm com piu in ten sịp.

        Nghĩa là nó cần nhiều phép tính, đặc biệt khi pờ rom dài.

        Ví dụ, nếu người dùng đưa vào một tài liệu dài, hoặc một đoạn code dài, thì pờ rì phiu phải đọc toàn bộ phần đó trước khi sinh câu trả lời.

        Pha pờ rì phiu cũng là lúc hệ thống tạo ra K V két ban đầu.

        K V két lưu lại thông tin ki và va liu của các tóc cần trong pờ rom.

        Những thông tin này sẽ được tái sử dụng ở các bước đì cốt sau.

        Nhờ vậy, khi sinh tóc cần mới, mô hình không cần tính lại toàn bộ pờ rom từ đầu.

        Đây là nền tảng quan trọng giúp in phờ rần của eo, eo, em khả thi hơn trong thực tế.
        """
    ),
    (
        "voice_part6/p6_03.mp3",
        """
        Sau pờ rì phiu, hệ thống chuyển sang pha đì cốt, hay còn gọi là gen nờ rây sần phây.

        Đây là pha mô hình bắt đầu sinh câu trả lời từng tóc cần một.

        Ở mỗi bước đì cốt, mô hình cần nhìn lại pờ rom ban đầu và toàn bộ các tóc cần đã sinh trước đó.

        Nếu không có K V két, mô hình sẽ phải tính lại ki và va liu cho toàn bộ ngữ cảnh ở mỗi bước.

        Điều này cực kỳ tốn kém, đặc biệt khi pờ rom dài hoặc ao pút dài.

        K V két giải quyết vấn đề này bằng cách lưu lại ki và va liu của các tóc cần trước đó trong ét ten sần.

        Khi tóc cần mới được sinh ra, mô hình chỉ cần tính ki và va liu cho tóc cần mới.

        Các ki và va liu cũ được lấy lại từ két.

        Có thể hiểu trực quan K V két giống như một cuốn sổ ghi nhớ.

        Khi đọc một tài liệu dài, nếu mỗi lần viết thêm một từ mà phải đọc lại toàn bộ tài liệu từ đầu thì rất chậm.

        Nhưng nếu ta đã ghi chú những thông tin quan trọng, ta có thể tra lại ghi chú đó thay vì xử lý lại mọi thứ.

        Nhờ K V két, đì cốt nhanh hơn rất nhiều so với việc tính lại toàn bộ ngữ cảnh ở mỗi tóc cần.
        """
    ),
    (
        "voice_part6/p6_04.mp3",
        """
        Tuy K V két giúp tăng tốc đì cốt, nó cũng tạo ra một thách thức rất lớn cho eo, eo, em sơ ving.

        Đó là bộ nhớ.

        K V két phải lưu ki và va liu cho các tóc cần đã xuất hiện trong ngữ cảnh.

        Khi pờ rom càng dài, két càng lớn.

        Khi câu trả lời càng dài, két cũng tiếp tục tăng.

        Khi bát sai lớn, tức là hệ thống xử lý nhiều rì quét cùng lúc, tổng lượng két cần lưu càng nhiều hơn.

        Và khi có nhiều người dùng đồng thời, bộ nhớ G P U có thể nhanh chóng trở thành nút thắt.

        Đây là lý do đì cốt thường dễ bị mem mo ri bao.

        Nghĩa là tốc độ không chỉ bị giới hạn bởi số phép tính, mà còn bị giới hạn bởi việc đọc ghi dữ liệu trong bộ nhớ.

        Trong thực tế, một hệ thống sơ ving tốt phải vừa tận dụng K V két để tránh tính toán lại, vừa quản lý két thật hiệu quả để không lãng phí Vi RAM.

        Những vấn đề như pờ rom dài, ao pút dài, bát lớn và nhiều rì quét đồng thời chính là nền cho các thách thức mà phần tiếp theo sẽ phân tích.

        Vì vậy, hiểu pờ rì phiu, đì cốt và K V két là bước chuẩn bị quan trọng trước khi đi vào lây tần xì, thờ ru pút và mem mo ri bo đồ néc.
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

    print("Done! Generated part 6 audio files.")


if __name__ == "__main__":
    asyncio.run(main())
