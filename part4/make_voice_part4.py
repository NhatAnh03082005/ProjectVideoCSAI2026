import asyncio
import edge_tts
import os

# ============================================================
# PART 4 — TRAINING VS INFERENCE VS SERVING: 11:00 - 15:00
# Tạo 4 file audio, mỗi file tương ứng một video con khoảng 1 phút
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(script_dir, "voice_part4"), exist_ok=True)

segments = [
    (
        "voice_part4/p4_01.mp3",
        """
        Sau khi đã hiểu bối cảnh kiến trúc eo, eo, em hiện đại, chúng ta cần phân biệt ba khái niệm rất dễ bị nhầm lẫn.

        Đó là trên ninh, in phờ rần và sơ ving.

        Đầu tiên là trên ninh.

        Trên ninh là giai đoạn huấn luyện mô hình từ dữ liệu.

        Trong giai đoạn này, mô hình được đưa vào một lượng dữ liệu rất lớn, ví dụ như văn bản, mã nguồn, tài liệu, hội thoại hoặc các tập dữ liệu chuyên biệt.

        Mục tiêu của trên ninh là điều chỉnh các trọng số bên trong mô hình.

        Có thể hiểu đơn giản là mô hình học cách dự đoán tóc cần tiếp theo dựa trên ngữ cảnh trước đó.

        Nếu mô hình dự đoán sai, thuật toán huấn luyện sẽ tính lỗi và cập nhật trọng số để lần sau dự đoán tốt hơn.

        Quá trình này lặp lại rất nhiều lần trên khối lượng dữ liệu khổng lồ.

        Trên ninh thường tốn rất nhiều tài nguyên, nhiều G P U, nhiều thời gian và chi phí rất cao.

        Tuy nhiên, trên ninh thường không phải là trọng tâm chính của video này.

        Vì trong eo, eo, em sơ ving, chúng ta giả sử mô hình đã được huấn luyện xong.

        Vấn đề quan trọng hơn là: sau khi có mô đồ rồi, làm thế nào để sử dụng nó hiệu quả trong thực tế.
        """
    ),
    (
        "voice_part4/p4_02.mp3",
        """
        Khái niệm thứ hai là in phờ rần.

        In phờ rần là giai đoạn sử dụng mô hình đã huấn luyện để tạo ra kết quả.

        Ví dụ, người dùng nhập câu hỏi: hãy giải thích trăng pho mờ là gì.

        Hệ thống đưa pờ rom đó vào mô hình, mô hình xử lý ngữ cảnh và sinh ra câu trả lời.

        Nếu trên ninh giống như dạy học sinh, thì in phờ rần giống như lúc hỏi học sinh một câu và nhận câu trả lời.

        Trong eo, eo, em, in phờ rần không chỉ là phép tính một lần.

        Pờ rom được chuyển thành tóc cần rồi đưa qua mô hình để dự đoán tóc cần tiếp theo.

        Tóc cần mới sinh lại được thêm vào ngữ cảnh để mô hình dự đoán tóc cần kế tiếp.

        Vì vậy, in phờ rần của eo, eo, em diễn ra theo dạng sinh tóc cần từng bước.

        Điều này đòi hỏi mô hình không chỉ phản hồi đúng, mà còn phải đủ nhanh để người dùng cảm nhận được câu trả lời mượt mà.

        Nhưng nếu chỉ một người dùng hỏi một mô hình, ta mới chỉ đang nói đến in phờ rần đơn lẻ.

        Để đưa mô hình thành dịch vụ thật, chúng ta cần một tầng lớn hơn: sơ ving.
        """
    ),
    (
        "voice_part4/p4_03.mp3",
        """
        Khái niệm thứ ba là sơ ving.

        Sơ ving là tổ chức in phờ rần thành dịch vụ thực tế, cho phép nhiều người dùng truy cập mô hình cùng lúc.

        Nếu trên ninh là dạy học, in phờ rần là hỏi bài, thì sơ ving là xây dựng trường học để phục vụ hàng ngàn học sinh cùng lúc.

        Trong hệ thống eo, eo, em sơ ving, ri quét từ người dùng đi qua nhiều thành phần.

        Hệ thống phải nhận ri quét, tóc cần nai dờ pờ rom, đưa vào in phờ rần en gin, điều phối G P U, sinh tóc cần và sờ trim đầu ra về cho người dùng.

        Mọi thứ phức tạp hơn khi nhiều người dùng gửi các yêu cầu có độ dài ngắn khác nhau cùng lúc.

        Nếu lập lịch không tốt, ri quét ngắn sẽ bị nghẽn sau ri quét dài.

        Vì vậy, sơ ving cần các kỹ thuật như bát ching, sờ ke du linh, quản lý ca vê két và tối ưu lay tơn si, thờ ru pút.

        Đây chính là bài toán hệ thống thực sự của eo, eo, em. Hãy cùng khám phá cơ chế vận hành chi tiết ngay sau đây.
        """
    ),
    (
        "voice_part4/p4_04.mp3",
        """
        Bây giờ ta có thể nhìn lại toàn bộ pai lai của eo, eo, em sơ ving.

        Mọi thứ bắt đầu bằng diu sơ pờ rom gửi đến sơ vờ.

        Tóc cần nai dờ sẽ chuyển văn bản thành các tóc cần số.

        Các tóc cần đi vào eo, eo, em en gin để quản lý bộ nhớ, bát ching và điều phối tính toán qua G P U.

        Sau đó, mô hình sinh tóc cần đầu ra từng bước, đi cốt lại thành văn bản và sờ trim dần về phía người dùng.

        Như vậy, in phờ rần chỉ là việc mô hình sinh kết quả.

        Còn sơ ving bao gồm cả hệ thống xung quanh: từ tóc cần hóa, lập lịch, me mo ri me ních mần cho đến sờ tri minh đầu ra và quản lý lay tơn si.

        Đây chính là sự khác biệt cốt lõi.

        Trên ninh tạo ra mô đồ, in phờ rần dùng mô đồ, và sơ ving biến in phờ rần thành dịch vụ thực tế có thể mở rộng.

        Phần tiếp theo của video sẽ tập trung sâu vào cơ chế sinh tóc cần và quản lý ca vê két.
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

    print("Done! Generated part 4 audio files.")


if __name__ == "__main__":
    asyncio.run(main())