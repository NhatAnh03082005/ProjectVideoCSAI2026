import asyncio
import edge_tts
import os

# ============================================================
# PART 3 — LLM BACKGROUND: 7:00 - 11:00
# Tạo 4 file audio, mỗi file tương ứng một video con khoảng 1 phút
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(script_dir, "voice_part3"), exist_ok=True)

segments = [
    (
        "voice_part3/p3_01.mp3",
        """
        Trước khi đi sâu vào eo, eo, em Sơ ving, chúng ta cần hiểu ngắn gọn: bên trong một mô hình ngôn ngữ lớn hiện đại có gì.

        Phần lớn các eo, eo, em hiện nay như G P T, La ma, mít trồ, dê mi nai hay díp sít đều dựa trên kiến trúc tren phom mơ đì cốt đờ

        Ở mức trực quan, đì cốt đờ là phần của mô hình chịu trách nhiệm đọc chuỗi tóc cần đã có, xử lý ngữ cảnh, rồi dự đoán tóc cần tiếp theo.

        Ví dụ, nếu pờ rom là: Thủ đô của Việt Nam là, thì mô hình sẽ dự đoán tóc cần tiếp theo có khả năng cao là Hà, rồi sau đó là Nội.

        Điểm quan trọng là mô hình không sinh toàn bộ câu trả lời trong một lần.

        Nó phải lặp lại quá trình dự đoán tóc cần rất nhiều lần.

        Mỗi lần sinh tóc cần mới, tóc cần đó lại được đưa ngược trở lại làm ngữ cảnh cho bước kế tiếp.

        Vì vậy, khi nói về eo, eo, em sơ ving, chúng ta không chỉ nói về việc chạy một mô đồ duy nhất một lần.

        Thực tế, hệ thống đang phải phục vụ một quá trình sinh tóc cần lặp đi lặp lại, diễn ra liên tục trong tren phom mơ đì cốt đờ.

        Đây là lý do vì sao kiến trúc đì cốt đờ ảnh hưởng trực tiếp đến lây tần xì, thờ ru pút, mem mo ri và chi phí in phờ rần.

        Nói cách khác, tren phom mơ đì cốt đờ chính là nền tảng kiến trúc mà hầu hết các kỹ thuật tối ưu sơ ving phía sau phải dựa vào.
        """
    ),
    (
        "voice_part3/p3_02.mp3",
        """
        Bên trong tren phom mơ đì cốt đờ, phần lõi thường được tạo thành từ nhiều tren phom mơ bờ lóc lặp lại.

        Mỗi bờ lóc có hai thành phần quan trọng nhất.

        Thành phần thứ nhất là seo phờ ten sần.

        seo phờ ten sần giúp mô hình quyết định tóc cần nào trong ngữ cảnh hiện tại là quan trọng đối với tóc cần đang được xử lý.

        Ví dụ, trong câu: Hà Nội là thủ đô của Việt Nam, khi mô hình xử lý cụm từ thủ đô, nó cần chú ý đến Hà Nội và Việt Nam.

        Có thể hiểu đơn giản, ờ ten sần giống như cách con người đọc tài liệu.

        Khi đọc một đoạn văn, chúng ta không chú ý đều tất cả các từ.

        Thay vào đó, não sẽ tập trung vào những từ có liên quan nhất đến ý đang hiểu.

        Thành phần thứ hai là phít pho guất nét guộc, hay F F N.

        Nếu ờ ten sần giúp mô hình lấy thông tin quan trọng từ ngữ cảnh, thì F F N tiếp tục biến đổi thông tin đó thành biểu diễn mạnh hơn.

        Nói dễ hiểu hơn, ờ ten sần giúp mô hình biết nên nhìn vào đâu, còn F F N giúp mô hình xử lý sâu hơn những gì đã nhìn thấy.

        Một eo, eo, em hiện đại không chỉ có một bờ lóc như vậy.

        Nó có thể có hàng chục, thậm chí hàng trăm tren phom mơ bờ lóc xếp chồng lên nhau.

        Khi dữ liệu đi qua nhiều bờ lóc, mô hình dần xây dựng được biểu diễn ngữ cảnh phức tạp hơn.

        Đây là lý do các mô hình lớn có khả năng hiểu câu dài, suy luận theo ngữ cảnh và sinh câu trả lời tự nhiên hơn.
        """
    ),
    (
        "voice_part3/p3_03.mp3",
        """
        Mặc dù cùng dựa trên tren phom mơ đì cốt đờ, các eo, eo, em hiện đại vẫn có nhiều điểm khác nhau trong thiết kế.

        Điểm khác đầu tiên là số lây ờ.

        mô đồ càng lớn thường có càng nhiều lây ờ, nghĩa là dữ liệu phải đi qua nhiều tầng xử lý hơn.

        Điều này có thể giúp mô hình mạnh hơn, nhưng cũng làm in phờ rần chậm hơn và tốn tài nguyên hơn.

        Điểm khác thứ hai là hít đần đì men sần.

        Đây là kích thước véc tờ biểu diễn bên trong mô hình.

        hít đần đì men sần càng lớn thì mô hình càng có khả năng biểu diễn thông tin phong phú hơn, nhưng đồng thời cũng làm tăng mem mo ri và cầm piu.

        Ngoài ra, các mô hình còn khác nhau ở số lượng ờ ten sần head.

        ờ ten sần head giúp mô hình nhìn ngữ cảnh từ nhiều góc độ khác nhau.

        Một số mô hình dùng mâu tai Head ờ ten sần truyền thống.

        Một số khác dùng M Q A hoặc G Q A, tức là cho nhiều que ri head chia sẻ ít ki va liu head hơn.

        Thiết kế này đặc biệt quan trọng trong sơ ving, vì nó có thể giảm kích thước K V cát trong giai đoạn đì cốt.

        Một số mô hình hiện đại còn dùng M, O, E, hay mích tờ of éc pợt.

        Với M, O, E, mỗi tóc cần không cần kích hoạt toàn bộ mô hình, mà chỉ đi qua một số éc pợt được chọn.

        Nhờ đó, mô hình có thể có rất nhiều tham số, nhưng chi phí tính toán trên mỗi tóc cần không tăng tương ứng.

        Những khác biệt như lây ờ, hít đần sai, ờ ten sần head, M Q A, G Q A hay M, O, E đều ảnh hưởng trực tiếp đến tốc độ in phờ rần, lượng bộ nhớ cần dùng và khả năng phục vụ nhiều rì quét cùng lúc.
        """
    ),
    (
        "voice_part3/p3_04.mp3",
        """
        Tuy có nhiều khác biệt về chi tiết thiết kế, các mô hình ngôn ngữ lớn hiện đại vẫn có một lõi kiến trúc tương đối giống nhau.

        Phần lớn đều bắt đầu bằng tóc cần em bét đình.

        Đây là bước chuyển các tóc cần đầu vào thành véc tờ số để mô hình có thể xử lý.

        Sau đó, dữ liệu đi qua nhiều tren phom mơ bờ lóc lặp lại.

        Trong mỗi bờ lóc thường có seo phờ ten sần, phít pho guất nét guộc, no mờ lờ dây sần và rì si dù ồ co néc sần.

        Cuối cùng, mô hình tạo ra phân phối xác suất cho tóc cần tiếp theo.

        tóc cần có xác suất phù hợp sẽ được chọn, rồi đưa trở lại chuỗi đầu vào để tiếp tục sinh tóc cần mới.

        Chính cấu trúc lõi tương đối giống nhau này giúp các hệ thống eo, eo, em sơ ving có thể xây dựng những kỹ thuật tối ưu dùng chung cho nhiều mô hình.

        Ví dụ, vì nhiều mô hình đều dùng ờ ten sần, nên ta có thể tối ưu ờ ten sần bằng cơ nồ tốt hơn.

        Vì quá trình đì cốt cần dùng lại thông tin của các tóc cần trước, nên ta có thể dùng K V cát để tránh tính toán lại toàn bộ ngữ cảnh.

        Vì nhiều rì quét có thể được xử lý cùng lúc, hệ thống có thể dùng bát chìng và sờ ke dồ lìng để tận dụng G P U tốt hơn.

        Vì mô đồ guây rất lớn, ta có thể dùng quan ti dây sần để giảm dung lượng bộ nhớ.

        Và nếu một mô hình quá lớn cho một G P U, ta có thể chia mô hình lên nhiều G P U bằng các kỹ thuật peo rờ leo i dầm.

        Vì vậy, hiểu kiến trúc lõi của eo, eo, em không chỉ giúp ta hiểu mô đồ hoạt động như thế nào.

        Nó còn giúp ta hiểu vì sao các phần tiếp theo của video lại tập trung vào pờ rì phiu, đì cốt, K V cát, mem mo ri phút pờ rin, thờ ru pút và lây tần xì.

        Đây là nền tảng để chuyển sang phần tiếp theo: phân biệt trên ning, in phờ rần và sơ ving.
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

    print("Done! Generated part 3 audio files.")


if __name__ == "__main__":
    asyncio.run(main())