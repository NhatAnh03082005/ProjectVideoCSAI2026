import asyncio
import os

import edge_tts


# ============================================================
# PART 4 - SCENE 18: PARALLEL COMPUTATION
#
# Chạy:
#   py make_p4_18_voices.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)


segments = [
    (
        "voice/p4_18_01_problem.mp3",
        """
        Sau quăn-ti-dây-sần, mô hình đã nhẹ hơn, nhưng vẫn có nhiều trường hợp một chi-pi-diu là không đủ.
        Có hai lý do.
        Một là mô hình quá lớn, không nhét vừa vào vi ram của một chi-pi-diu.
        Hai là số ri-quét quá nhiều, một chi-pi-diu xử lý không kịp.
        Pa ra lel com piu tây sần xuất hiện để chia gánh nặng này ra nhiều thiết bị.
        Trong ta xô nô mi của bài báo, nhóm này gồm mô đờ pa-ra-lel-li-zừm, si-quần pa-ra-lel-li-zừm, clao sờ-cây-ling, và đì-sen-trờ-lai in-phơ-rần.
        """,
    ),
    (
        "voice/p4_18_02_model_parallelism.mp3",
        """
        Đầu tiên là mô đờ pa ra-leo-li-zừm: ta chia chính mô hình ra nhiều gi-pi-iu,
        Hãy tưởng tượng mô hình là một cuốn sách khổng lồ mà một cái bàn không chứa nổi,
        Cách tự nhiên là xé cuốn sách thành nhiều tập, đặt mỗi tập lên một bàn khác nhau,
        Với eo-eo-em , các tập sách đó có thể là một phần bên trong lây ờ, hoặc là một nhóm lây ờ liên tiếp.
        """,
    ),
    (
        "voice/p4_18_03_tensor_parallel.mp3",
        """
        Ten xơ pa ra lel li zừm là cách chia ở bên trong một lây ờ, 
        Ví dụ một phép nhân ma trận rất lớn: thay vì một gi pi iu nhân toàn bộ ma trận,
        ta cắt ma trận uây theo cột, hoặc cắt các ờ-ten-sần hed, rồi giao từng phần cho từng gi pi iu.
        Mỗi chi-pi-diu tính một mảnh kết quả. Sau đó, các mảnh này phải được ghép hoặc cộng lại
        bằng giao tiếp giữa chi-pi-diu, thường là ol-ghe-đờ hoặc các bước tương tự.
        """,
    ),
    (
        "voice/p4_18_04_tensor_tradeoff.mp3",
        """
        Trực quan hơn, ten-xơ pa-ra-lel giống như hai người cùng giải một phép tính lớn trên cùng một bảng.
        Mỗi người làm một nửa, nên phần tính có thể nhanh hơn.
        Nhưng sau mỗi bước, họ phải nhìn sang bài của nhau để ghép đáp án.
        Nếu hai người ngồi cạnh nhau, giao tiếp nhanh, cách này rất hiệu quả.
        Nếu họ ở xa,thời gian trao đổi có thể ăn mất lợi ích song song.
        """,
    ),
    (
        "voice/p4_18_05_pipeline_parallel.mp3",
        """
        Pai-lai pa-ra-lel-li-zừm thì khác.
        Thay vì chia một lây ờ, ta chia mô hình theo chiều sâu.
        Chi-pi-diu một giữ các lây ờ đầu, chi-pi-diu hai giữ các lây ờ giữa, chi-pi-diu ba giữ các lây ờ cuối.
        Dữ liệu đi qua mô hình giống như một sản phẩm đi qua dây chuyền nhà máy, Trạm đầu làm xong thì chuyển ắc-ti-vây-sần sang trạm sau.
        Cách này giúp chạy được mô hình lớn hơn, vì mỗi chi-pi-diu chỉ giữ một phần lây ờ.
        """,
    ),
    (
        "voice/p4_18_06_pipeline_bubble.mp3",
        """
        Nhưng pai-lai có một vấn đề gọi là pai-ai bắp-bồ.
        Ở đầu dây chuyền, chi-pi-diu sau phải chờ chi-pi-diu trước tạo ra ắc-ti-vây-sần.
        Ở cuối dây chuyền, chi-pi-diu trước có thể đã hết việc, trong khi chi-pi-diu sau còn xử lý.
        Vì vậy, pai-lai pa-ra-leo thường giúp tăng thru-pút, khi có nhiều rùy-quét hoặc mai-crô bát chảy liên tục.
        Nhưng nó không tự động làm một rùy-quét đơn chạy nhanh hơn từ đầu đến cuối.
        """,
    ),
    (
        "voice/p4_18_07_sequence_parallel.mp3",
        """
        Khi bài toán là loong con-text, nút thắt không chỉ nằm ở mô hình lớn, mà còn ở chuỗi token quá dài.
        Si-quần pa-ra-lel-li-zừm chia theo chiều token.
        Ví dụ một tài liệu dài được cắt thành nhiều đoạn,mỗi chi-pi-diu giữ một đoạn.
        Cách này giúp phân tán com-piu và sờ-to-rịt theo chiều si-quần,
        đặc biệt hữu ích khi ờ-ten-sần và cây vi cát tăng mạnh theo độ dài ngữ cảnh.
        """,
    ),
    (
        "voice/p4_18_08_sequence_communication.mp3",
        """
        Điểm quan trọng là:
        các đoạn token không được xử lý như những hòn đảo riêng biệt.
        Trong Truên-pho-mờ, ờ-ten-sần cần biết quan hệ giữa token hiện tại và các token khác trong ngữ cảnh.
        Vì vậy, các chi-pi-diu phải trao đổi kết quả trung gian, ví dụ bằng ring-stai com-miu-ni-cây-sần, hoặc ol-ghe-đờ.
        Nếu bỏ giao tiếp này, mô hình sẽ mất bức tranh toàn cục của văn bản.
        """,
    ),
    (
        "voice/p4_18_09_cloud_scaling.mp3",
        """
        Tiếp theo là clao sờ-cây-ling.
        Nếu ten xơ và pai lai giúp chia một mô hình lên nhiều gi pi iu, thì clao sờ-cây-ling nhìn bài toán ở quy mô dịch vụ.
        Câu hỏi là: làm sao mở rộng nhiều máy, nhiều vùng clao, hoặc dùng tài nguyên rẻ hơn như spot in sờ tần để phục vụ lượng ri quest thay đổi theo thời gian.
        Ví dụ ban ngày ri quest ít thì dùng ít gi pi iu, tối cao điểm thì mở rộng thêm cụm gi pi iu.
        """,
    ),
    (
        "voice/p4_18_10_decentralized.mp3",
        """
        Một hướng thú vị hơn là đi sen trờ lai zd in-phơ-rần: tận dụng nhiều chi-pi-diu rải rác, có thể nằm ở các máy khác nhau,
        vị trí khác nhau, thậm chí qua in-tơ-nét.
        Trực quan giống như thay vì xây một siêu nhà máy duy nhất, ta nhờ rất nhiều xưởng nhỏ cùng làm việc.
        Ý tưởng này giúp khai thác tài nguyên dư thừa, nhưng đổi lại phải đối mặt với băng thông thấp,
        độ trễ mạng,thiết bị không đồng nhất, lỗi kết nối, và cả vấn đề riêng tư.
        """,
    ),
    (
        "voice/p4_18_11_which_parallelism.mp3",
        """
        Vậy chọn kiểu nào? Nếu một lây ờ quá lớn
        và bạn có nhiều chi-pi-diu nối nhanh trong cùng máy, ten-xơ  pa-ra-lel là ứng viên mạnh.
        Nếu mô hình quá sâu, hoặc quá lớn để chứa trên một chi-pi-diu, pai-lai pa-ra-lel giúp chia lây ờ.
        Nếu con text quá dài, si-quần pa-ra-lel xử lý theo chiều token.
        Nếu bài toán là tra-phích tăng giảm theo thời gian, clao sờ-cây-ling quan trọng hơn.
        Còn đi sen trờ lai zd in phơ rần phù hợp khi muốn tận dụng tài nguyên rải rác, nhưng phải chấp nhận hệ thống phức tạp hơn.
        """,
    ),
    (
        "voice/p4_18_12_summary_transition.mp3",
        """
        Tóm lại, pa-ra-lel com-piu-tây-sần là cách biến một bài toán quá nặng cho một chi-pi-diu thành nhiều phần nhỏ hơn cho nhiều thiết bị cùng xử lý.
        Nhưng song song hóa không miễn phí, Càng chia nhiều ta càng phải trả chi phí giao tiếp,
        đồng bộ lập lịch và quản lý trạng thái.
        Và ngay cả khi đã có nhiều chi-pi-diu, một nút thắt khác vẫn luôn xuất hiện trong eo-eo-em serving: bộ nhớ, đặc biệt là cây vi cát-ch.
        Đó là phần tiếp theo.
        """,
    ),
]



async def generate_audio(filename: str, text: str, retries: int = 3):
    for attempt in range(1, retries + 1):
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE)
            await communicate.save(filename)
            print(f"Created: {filename}")
            return
        except Exception as exc:
            print(f"Attempt {attempt}/{retries} failed for {filename}: {exc}")
            if attempt == retries:
                raise
            await asyncio.sleep(2)


async def main():
    for filename, text in segments:
        await generate_audio(filename, text)
    print("Done. Created all Part 18 voice files in ./voice")


if __name__ == "__main__":
    asyncio.run(main())
