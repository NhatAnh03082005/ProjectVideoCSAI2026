# -*- coding: utf-8 -*-

import asyncio
from dataclasses import replace
import time
from pathlib import Path

import edge_tts


VOICE = "vi-VN-NamMinhNeural"
CONCURRENCY = 2
SAVE_TIMEOUT = 120

Path("voice").mkdir(exist_ok=True)

segments = [ 
    # (
    #     "voice/p3_01_01_bottleneck.mp3",
    #     """
    #     Đầu tiên là đi-câu-đình a-gờ-rít-đờm, tức là các thuật toán giải mã,

    #     Trong mô hình ngôn ngữ lớn, đi-câu-đình là quá trình mô hình tạo ra câu trả lời bằng cách dự đoán to-kần tiếp theo, rồi tiếp tục dùng các to-kần đã sinh để dự đoán to-kần kế tiếp,

    #     Phần lớn mô hình ngôn ngữ lớn hiện nay dùng cơ chế O-tô-ri-g're-sív đi-câu-đình,
    #     nghĩa là mô hình sinh từng to-kần một,

    #     Ví dụ prompt là, Thủ đô của Việt Nam là, Mô hình có thể sinh to-kần tiếp theo là chữ Hà,
    #     sau đó dùng toàn bộ chuỗi mới để sinh tiếp là chữ Nội, rồi sinh dấu chấm, rồi tiếp tục sinh các to-kần phía sau,

    #     Điểm mạnh của cách này là mỗi to-kần được sinh ra dựa trên toàn bộ ngữ cảnh trước đó,
    #     Nhờ vậy câu trả lời thường mạch lạc và đúng ngữ cảnh,

    #     Nhưng vấn đề là quá trình này có tính tuần tự rất mạnh, Muốn sinh to-kần thứ mười thì phải có to-kần thứ chín,
    #     Muốn có to-kần thứ chín thì phải sinh xong to-kần thứ tám,

    #     Điều này làm quá trình sinh văn bản bị chậm, đặc biệt khi câu trả lời dài
    #     Vì vậy, các thuật toán giải mã mới cố gắng trả lời câu hỏi:
    #     có cách nào sinh to-kần nhanh hơn tận dụng song song tốt hơn nhưng vẫn giữ chất lượng gần như mô hình gốc không?
    #     """,
    # ),
# (
#     "voice/p3_01_02_non_ar.mp3",
#     """
#     Hướng đầu tiên là non O-tô-ri-g're-sív đi-câu-đình,
#     hay có thể hiểu là giải mã không tự hồi quy.

#     Ý tưởng rất trực tiếp:
#     thay vì sinh từng to-kần một,
#     mô hình cố gắng sinh nhiều to-kần song song trong cùng một lần.

#     Trên hình, bên trái là O-tô-ri-g're-sív.
#     Các to-kần được sinh theo thứ tự:
#     một, rồi hai, rồi ba, rồi bốn.
#     Nó giống như viết từng chữ từ trái sang phải.

#     Bên phải là non O-tô-ri-g're-sív.
#     Các to-kần một, hai, ba, bốn được tạo gần như cùng lúc.
#     Nhờ vậy tốc độ có thể nhanh hơn,
#     vì mô hình phá bớt sự phụ thuộc tuần tự
#     và tận dụng song song tốt hơn.

#     Nhưng nhược điểm là chất lượng thường khó bằng cách sinh tuần tự.

#     Lý do là ngôn ngữ tự nhiên có tính phụ thuộc rất mạnh.
#     To-kần phía sau thường phụ thuộc vào to-kần phía trước.

#     Ví dụ, nếu ta đổi từ ăn thành uống,
#     thì từ phía sau cũng phải đổi theo.
#     Ta không còn nói ăn cơm nữa,
#     mà phải nói uống nước.

#     Vì vậy, nếu mô hình sinh nhiều to-kần cùng lúc
#     khi chưa chắc to-kần trước là gì,
#     câu trả lời có thể bị mất mạch,
#     lặp ý,
#     hoặc sai ngữ cảnh.

#     Tóm lại,
#     non O-tô-ri-g're-sív đi-câu-đình có tiềm năng tăng tốc bằng sinh song song,
#     nhưng phải đánh đổi với độ tin cậy
#     và tính mạch lạc của văn bản.
#     """
# ),
# (
#     "voice/p3_01_03_speculative.mp3",
#     """
#     Một kỹ thuật quan trọng hơn và thực tế hơn là spéc-kyu-lơ-típ đi-câu-đình hay giải mã suy đoán,
#     Đây là một ý tưởng rất hay để tăng tốc mô hình ngôn ngữ lớn mà vẫn kiểm soát được chất lượng,
#     Ta tưởng tượng có hai mô hình Một mô hình lớn gọi là ta-gịt mô-đồl Đây là mô hình chính,chất lượng cao,nhưng chạy chậm và tốn tài nguyên,

#     Một mô hình nhỏ hơn gọi là draft mô-đồl Mô hình này yếu hơn nhưng chạy nhanh hơn nhiều,

#     Thay vì để mô-đồl lớn tự sinh từng to-kần một hệ thống cho draft mô-đồl đoán trước vài to-kần,

#     Ví dụ draft mô-đồl đoán trước Hà Nội là thủ đô Sau đó ta-gịt mô-đồl sẽ kiểm tra các to-kần này,

#     Nếu mô-đồl lớn thấy cả cụm to-kần đều phù hợp ví dụ như câu Hà Nội là thủ đô, hệ thống có thể chấp nhận nhiều to-kần cùng lúc,

#     Lúc này thay vì phải sinh Hà, rồi sinh Nội, rồi sinh là, rồi sinh thủ, rồi sinh đô, mô-đồl lớn có thể duyệt cả nhóm to-kần nhanh hơn,

#     Nhưng không phải bản nháp nào cũng đúng Ví dụ nếu draft mô-đồl đoán thành Hà Nội là thủ thức Các to-kần đầu như Hà, Nội, là, thủ có thể vẫn phù hợp,
#     Nhưng đến to-kần thức thì sai ngữ cảnh, Khi đó hệ thống sẽ dừng ở to-kần sai, bỏ phần sai phía sau, rồi để ta-gịt mô-đồl sinh tiếp từ vị trí đó.

#     Có thể hiểu đơn giản như sau, draft mô-đồl giống như một trợ lý viết nháp thật nhanh,Ta-gịt mô-đồl giống như một chuyên gia kiểm tra bản nháp,

#     Nếu bản nháp đúng chuyên gia duyệt luôn nhiều to-kần,
#     Nếu bản nháp sai chuyên gia sửa từ chỗ sai,
#     Điểm quan trọng là spéc-kyu-lơ-típ đi-câu-đình không phải là để mô-đồl nhỏ trả lời thay mô-đồl lớn,

#     Mô-đồl nhỏ chỉ đề xuất trước, Quyết định cuối cùng vẫn thuộc về mô-đồl lớn,

#     Vì vậy nếu cơ chế kiểm tra và quay lại khi sai được thiết kế đúng, đầu ra vẫn tuân theo mô-đồl lớn,

#     Ta chỉ thay đổi cách sinh nhanh hơn chứ không thay đổi mô-đồl quyết định cuối cùng,

#     Vậy vì sao cách này có thể nhanh hơn?

#     Điểm hay của kỹ thuật này là nó tận dụng khả năng xử lý song song của Tren-pho-mờ.

#     Trong cách sinh thông thường mô-đồl lớn phải sinh to-kần một rồi to-kần hai rồi to-kần ba một cách tuần tự.
#     Còn với spéc-kyu-lơ-típ đi-câu-đình draft mô-đồl đoán trước một nhóm to-kần và ta-gịt mô-đồl kiểm tra cả nhóm đó trong một lần chạy.

#     Nếu draft mô-đồl đoán tốt, ta-gịt mô-đồl có thể chấp nhận nhiều to-kần cùng lúc Khi đó số lần gọi mô-đồl lớn giảm xuống,
#     và quá trình đi-kôu-đình nhanh hơn,
#     Tuy nhiên spéc-kyu-lơ-típ đi-câu-đình không phải lúc nào cũng tăng tốc mạnh,
#     Nó hiệu quả nhất khi draft mô-đồl vừa nhanh vừa đoán đủ gần với ta-gịt mô-đồl,

#     Nếu draft mô-đồl đoán sai quá nhiều ta-gịt mô-đồl phải sửa liên tục nên lợi ích tăng tốc sẽ giảm,

#     Tóm lại spéc-kyu-lơ-típ đi-câu-đình dùng mô-đồl nhỏ để đoán nhanh, dùng mô-đồl lớn để kiểm tra từ đó sinh được nhiều to-kần hơn trong mỗi bước suy luận.
#     """
# ),
    # (
    #     "voice/p3_01_04_early_exit.mp3",
    #     """
    #     Kỹ thuật tiếp theo là ơ-li éc-sịt tức là thoát sớm, Các mô hình ngôn ngữ lớn thường có rất nhiều layer,
    #     Bình thường khi sinh một to-kần dữ liệu phải đi qua toàn bộ các layer từ đầu đến cuối, Nếu mô-đồl có tám mươi layer,
    #     thì mọi to-kần đều phải đi qua đủ tám mươi layer Nhưng không phải mọi bước sinh to-kần đều khó như nhau,
    #     Có những bước mà mô hình đã rất tự tin ngay từ các layer giữa,
    #     Ví dụ sau một đoạn ngữ cảnh rất rõ ràng, phân phối xác suất cho to-kần tiếp theo có thể đã nghiêng mạnh về một to-kần nhất định,
    #     Khi đó ơ-li éc-sịt đặt ra một câu hỏi, Nếu ở layer trung gian mô hình đã đủ tự tin,có cần chạy tiếp đến layer cuối không?

    #     Ý tưởng là tại một số layer giữa ta gắn thêm các cửa thoát hoặc bộ dự đoán trung gian,

    #     Nếu mô hình đủ tự tin nó có thể dừng sớm và xuất to-kần luôn,
    #     Nhờ vậy những trường hợp dễ dùng ít tính toán hơn Còn những trường hợp khó vẫn đi qua toàn bộ mô hình,

    #     Có thể hình dung mô-đồl như một tòa nhà tám mươi tầng to-kần khó phải đi lên đến tầng tám mươi mới đủ thông tin để quyết định,
    #     to-kần dễ có thể dừng ở tầng hai mươi hoặc tầng ba mươi,
    #     Tuy nhiên khó khăn nằm ở câu hỏi, khi nào thì đủ tự tin,
    #     Nếu dừng quá sớm, biểu diễn trung gian có thể chưa đủ thông tin làm chất lượng giảm hoặc mô hình sinh sai,

    #     Vì vậy ơ-li éc-sịt luôn cần một tiêu chí Kón-phơ-đình hoặc một cơ chế kiểm tra đủ tốt,

    #     Tóm lại, ơ-li éc-sịt không bắt mọi to-kần đi hết toàn bộ mạng mà cho những bước dễ thoát sớm để tiết kiệm tính toán
    #     """,
    # ),
# (
#     "voice/p3_01_05_cascade.mp3",
#     """
#     Một hướng khác là kát-kây in-phơ-rình tức là suy luận theo tầng,
#     Ý tưởng chính là không phải rì-khuét nào cũng cần dùng mô-đồl lớn,
#     Thay vì dùng một mô-đồl lớn cho mọi câu hỏi hệ thống dùng một router để đánh giá độ khó của rì-khuét rồi chọn mô-đồl phù hợp,
#     Nếu rì-khuét dễ, router đưa tới smol mô-đồl, tức là mô-đồl nhỏ, nhanh và rẻ,
#     Nếu rì-khuét trung bình, router đưa tới mi-đi-ùm mô-đồl, để cân bằng giữa tốc độ và chất lượng,
#     Nếu rì-khuét khó, router mới đưa tới Large mô-đồl, để giữ chất lượng câu trả lời,
#     Ví dụ câu chào bạn có thể dùng mô-đồl nhỏ, viết email ngắn có thể dùng mô-đồl vừa, còn phân tích tài liệu kỹ thuật dài thì cần mô-đồl lớn,
#     Cách này giúp tiết kiệm chi phí suy luận vì Large mô-đồl chỉ được dùng khi thật sự cần,
#     Nhưng kát-kây in-phơ-rình cần router đủ tốt, Nếu router chọn đúng, hệ thống vừa nhanh vừa rẻ, Nếu router chọn sai, ví dụ câu khó lại đưa cho mô-đồl nhỏ, chất lượng câu trả lời sẽ giảm,
#     Tóm lại, kát-kây in-phơ-rình tối ưu ở cấp độ rì-khuét câu dễ dùng smol mô-đồl, câu vừa dùng mi-đi-ùm mô-đồl, câu khó dùng Large mô-đồl.
# """
# ),


    (
        "voice/p3_01_06_summary.mp3",
        """
        Tóm lại, nhóm đi-kôu-đình a-gờ-rít-đờm là cố gắng xử lý một nút thắt lớn của eo-eo-em generation là sinh to-kần tuần tự quá chậm,
        Có thể tóm tắt nhóm này thành bốn hướng chính,
        Hướng thứ nhất là non O-tô-ri-g're-sív đi-câu-đình cố gắng sinh song song nhiều to-kần,
        Hướng thứ hai là spéc-kyu-lơ-típ đi-câu-đình dùng mô-đồl nhỏ để đoán trước một nhóm to-kần rồi dùng mô-đồl lớn để kiểm tra và quyết định to-kần nào được chấp nhận, 
        Hướng thứ ba là ơ-li éc-sịt cho phép dừng sớm ở layer giữa nếu mô hình đã đủ tự tin,
        Hướng thứ tư là kát-kây in-phơ-rình chọn mô-đồl phù hợp theo độ khó của rì-khuét,
        Điểm chung là các phương pháp này đều muốn giảm thời gian suy luận hoặc giảm chi phí phục vụ mô hình,
        nhưng luôn phải cân bằng giữa tốc độ, chi phí, và chất lượng đầu ra,
        """,
    ),
]


async def generate_audio(filename, text, semaphore, retries=3):
    output_path = Path(filename)
    if output_path.exists() and output_path.stat().st_size > 0:
        print("Bỏ qua file đã có:", filename)
        return

    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")

    for attempt in range(retries):
        try:
            async with semaphore:
                start = time.perf_counter()
                communicate = edge_tts.Communicate(text=text.strip(), voice=VOICE)
                await asyncio.wait_for(
                    communicate.save(str(temp_path)),
                    timeout=SAVE_TIMEOUT,
                )
                temp_path.replace(output_path)
                elapsed = time.perf_counter() - start
                print(f"Đã tạo: {filename} ({elapsed:.1f}s)")
            return
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            error_message = str(e) or type(e).__name__
            print(f"Lần {attempt + 1} thất bại ({filename}): {error_message}")
            if attempt < retries - 1:
                await asyncio.sleep(2)
            else:
                raise


async def main():
    semaphore = asyncio.Semaphore(CONCURRENCY)
    await asyncio.gather(
        *(generate_audio(filename, text, semaphore) for filename, text in segments)
    )
    print("Xong voice phần đi-kôu-đình Algorithms!")


if __name__ == "__main__":
    asyncio.run(main())
