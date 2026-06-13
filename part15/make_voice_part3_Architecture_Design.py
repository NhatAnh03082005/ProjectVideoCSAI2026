# -*- coding: utf-8 -*-

from pathlib import Path
import asyncio
import edge_tts

VOICE = "vi-VN-NamMinhNeural"
RATE = "+0%"

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "voice"
OUT_DIR.mkdir(exist_ok=True)

SEGMENTS = [
    # (
    #     "p3_02_01_arch_intro.mp3",
    #     """
    #     Nhóm thứ hai là A-ki-téc-chờ Đi-dai, tức là tối ưu thiết kế kiến trúc mô hình,
    #     A-ki-téc-chờ Đi-dai tập trung vào bản thân cấu trúc bên trong mô hình,
    #     Phần lớn mô hình Ngôn ngữ lớn hiện nay vẫn dựa trên Trăn-pho-mơ đi-câu-đờ.

    #     Trong Trăn-pho-mơ, hai thành phần rất quan trọng là a-ten-sần và phít-pho-quợt nét-quợc hay ép-ép-en,
    #     A-ten-sần giúp mô hình hiểu quan hệ giữa các to-kần, Nhưng khi chuỗi dài, a-ten-sần có thể rất tốn bộ nhớ và tính toán,
    #     Ép-ép-en chứa rất nhiều tham số và cũng đóng góp lớn vào chi phí in-phơ-rần.
    #     Vì vậy các hướng A-ki-téc-chờ Đi-dai cố gắng làm cho mô hình hiệu quả hơn ngay từ kiến trúc nhưng vẫn giữ năng lực biểu diễn tốt,
    #     """
    # ),
    
# (
#     "p3_02_02_config_downsizing.mp3",
#     """
#     Hướng đầu tiên là cờn-phi-giu-rây-sần đao-sai-zing tức là giảm cấu hình mô hình,
#     Đây là cách trực tiếp nhất làm cho mô-đồl nhỏ hơn ngay từ cấu hình ban đầu,
#     Một Large mô-đồl nặng và tốn tài nguyên được thu nhỏ thành một mô-đồl nhẹ hơn,
#     Nếu mô-đồl quá lớn, ta có thể giảm một số thành phần cấu hình,
#     Ví dụ số layer có thể giảm từ tám mươi xuống bốn mươi,
#     Hi-đần đi-men-sần có thể giảm từ tám một chín hai xuống bốn không chín sáu,
#     Số a-ten-sần head có thể giảm từ sáu mươi bốn xuống ba mươi hai,
#     Kích thước ép-ép-en và vô-cáp-biu-lơ-ri cũng có thể được rút gọn nếu phù hợp,
#     Khi giảm các cấu hình này,mô-đồl sẽ nhỏ hơn,cần ít bộ nhớ hơn và in-phơ-rần nhanh hơn,
#     Nhưng đây cũng là cách dễ làm giảm chất lượng nhất,
#     Lý do là layer, hi-đần size, a-ten-sần head và ép-ép-en size đều ảnh hưởng trực tiếp đến năng lực biểu diễn của mô hình,
#     Nếu giảm quá mạnh mô-đồl có thể khó hiểu ngữ cảnh phức tạp hoặc suy luận kém hơn,
#     Vì vậy cờn-phi-giu-rây-sần đao-sai-zing là giảm kích thước mô-đồl để chạy nhanh hơn,
#     nhưng phải chấp nhận rủi ro giảm năng lực của mô-đồl,
#     Trong thực tế hướng này thường cần kết hợp với phai-tiu-ning hoặc đít-ti-lây-sần
#     để giữ chất lượng tốt hơn,
#     """,
# ),
# (
#     "p3_02_03_attention_simplification.mp3",
#     """
#     Hướng tiếp theo là a-ten-sần sim-pli-fi-kây-sần tức là đơn giản hóa a-ten-sần,
#     Trong Trăn-pho-mơ truyền thống, self a-ten-sần cho phép mỗi to-kần nhìn vào các to-kần khác trong chuỗi,
#     Điều này rất mạnh vì mô hình có thể kết nối thông tin ở xa nhau,
#     Nhưng khi xi-quần dài, chi phí a-ten-sần tăng rất nhanh,
#     Với full a-ten-sần độ phức tạp thường là bậc hai theo độ dài chuỗi,
#     Nói trực quan, nếu chuỗi dài gấp đôi, số quan hệ giữa các to-kần có thể tăng khoảng bốn lần,
#     Với prompt ngắn thì vấn đề chưa quá lớn Nhưng với lon con-téc,
#     ví dụ vài chục nghìn to-kần, a-ten-sần trở thành bottleneck rất nặng,
#     Trong eo-eo-em serving, ta thường nhìn theo hai giai đoạn,
#     Ở pri-phiu phase, mô-đồl xử lý toàn bộ prompt ban đầu nên full a-ten-sần tạo ra một ma trận quan hệ lớn giữa các to-kần,
#     Ở đi-kôu phase, mô-đồl sinh từng to-kần mới,Mỗi to-kần mới cần đọc các to-kần trước đó thông qua kê-vi kát-xơ,
#     Khi ngữ cảnh càng dài,việc đọc kê-vi kát-xơ càng tốn memory bandwidth.
#     Vì vậy, ý tưởng chung của a-ten-sần sim-pli-fi-kây-sần là không phải to-kần nào cũng cần nhìn toàn bộ mọi to-kần khác, Thay vào đó ta chỉ giữ lại phần ngữ cảnh quan trọng,
#     Một số cách thường gặp là lôu-cồl a-ten-sần, cho to-kần chỉ nhìn các to-kần gần nó,
#     Sliding window a-ten-sần, cho to-kần chỉ nhìn một cửa sổ ngữ cảnh gần nhất,
#     Sparse a-ten-sần,chỉ giữ một số kết nối quan trọng,
#     Và context compression, nén hoặc rút gọn ngữ cảnh để giảm số to-kần cần xử lý,
#     Mục tiêu là giảm com-pu-TÂY-shần, giảm memory và hỗ trợ lon context tốt hơn,
#     Nhưng trade-off là nếu bỏ bớt ngữ cảnh không khéo mô-đồl có thể mất thông tin quan trọng,
#     Vì vậy a-ten-sần sim-pli-fi-kây-sần không chỉ là cắt bớt a-ten-sần,
#     mà là cắt sao cho vẫn giữ lại phần ngữ cảnh quan trọng nhất.
#     """,
# ),

    (
        "p3_02_04_activation_sharing.mp3",
        """
        Một hướng rất quan trọng trong A-ki-téc-chờ Đi-dai là ác-ti-vây-sần se-rinh,
        Trong thắc-so-nơ-mi, ác-ti-vây-sần se-rinh có nhiều biến thể,
        Ở đây mình tập trung vào em-kiu-ây và gi-kiu-ây vì hai kỹ thuật này liên quan trực tiếp đến kê-vi cache khi serving,
        Trước hết ta cần hiểu kê-vi kát-xơ là gì,
        Trong a-ten-sần, mô hình dùng ba thành phần:quy-ri, ki và va-liu,
        Khi đi-kôu, các to-kần trước đó đã được xử lý rồi,
        Nếu mỗi lần sinh to-kần mới mà tính lại toàn bộ ki và va-liu
        của tất cả to-kần cũ sẽ rất tốn kém,
        Vì vậy hệ thống lưu ki và va-liu của các to-kần trước đó vào một vùng nhớ gọi là kê-vi cache,
        Khi sinh to-kần mới, mô-đồl chỉ cần tạo quy-ri mới rồi so sánh quy-ri này với ki và va-liu đã lưu trong kê-vi kát-xơ,
        Kê-vi kát-xơ giúp tránh tính lại từ đầu nhưng nó cũng tạo ra một vấn đề lớn càng nhiều to-kần, kê-vi kát-xơ càng phình to,
        Càng nhiều rì-khuét, kê-vi kát-xơ càng chiếm nhiều bộ nhớ Gi-Pi-U.
        Trong mân-ti head a-ten-sần truyền thống, mỗi a-ten-sần head có bộ ki và va-liu riêng,
        Điều này giúp mô hình biểu diễn phong phú nhưng cũng làm kê-vi kát-xơ rất lớn,
        Multi Quy-ri A-ten-sần, viết tắt là em-kiu-ây, giải quyết bằng cách cho nhiều quy-ri head dùng chung một bộ ki và va-liu head,
        Nhờ vậy số lượng ki và va-liu cần lưu giảm mạnh,
        Grouped Quy-ri A-ten-sần, viết tắt là gi-kiu-ây là cách trung gian,
        Thay vì tất cả quy-ri head dùng chung một ki và va-liu như em-kiu-ây, gi-kiu-ây chia quy-ri head thành nhiều nhóm,
        Mỗi nhóm dùng chung một bộ ki và va-liu,
        Có thể hiểu bằng ví dụ đơn giản em-hát-ây giống như mỗi nhân viên có một máy in riêng.
        Rất linh hoạt, nhưng tốn chỗ,
        Em-kiu-ây giống như cả công ty dùng chung một máy in,
        Rất tiết kiệm nhưng có thể hạn chế hơn,
        Gi-kiu-ây giống như mỗi phòng ban dùng chung một máy in, Vừa tiết kiệm hơn em-hát-ây,
        vừa giữ được độ linh hoạt tốt hơn em-kiu-ây,
        Ý nghĩa với eo-eo-em serving là rất lớn em-kiu-ây và gi-kiu-ây giúp giảm kích thước kê-vi cache,
        giảm áp lực memory bandwidth và làm đi-kôu phase hiệu quả hơn.
        Đây là lý do nhiều eo-eo-em hiện đại sử dụng gi-kiu-ây hoặc các biến thể tương tự để phục vụ in-phơ-rần tốt hơn.
        """,
    ),
    # (
    #     "p3_02_05_moe.mp3",
    #     """
    #     Một hướng kiến trúc khác là cờn-đi-sần-nồ com-piu-ting,
    #     tiêu biểu là em-âu-i,
    #     tức Mixture of Experts.

    #     Ý tưởng của em-âu-i là mô hình có nhiều expert,
    #     nhưng mỗi to-kần chỉ kích hoạt một vài expert cần thiết.

    #     Thay vì mọi to-kần đều đi qua toàn bộ mạng,
    #     to-kần sẽ đi qua một router.

    #     Router quyết định to-kần này nên được gửi đến expert nào.

    #     Ta có thể hình dung mô-đồl như một tòa nhà có nhiều phòng chuyên môn.

    #     Một to-kần đi vào,
    #     router sẽ chọn một vài phòng phù hợp để xử lý to-kần đó,
    #     thay vì bật toàn bộ tòa nhà.

    #     Điểm mạnh của em-âu-i là:
    #     mô-đồl có thể có tổng số tham số rất lớn,
    #     nhưng mỗi to-kần chỉ dùng một phần nhỏ trong số đó.

    #     Nói cách khác,
    #     em-âu-i cho phép tăng capacity của mô-đồl
    #     mà không làm chi phí tính toán tăng tương ứng ở mỗi to-kần.

    #     Tuy nhiên,
    #     cần nói cẩn thận.

    #     Trong thực tế,
    #     các expert không nhất thiết được gắn nhãn rõ ràng
    #     như expert toán,
    #     expert code,
    #     hay expert văn bản.

    #     Đó chỉ là cách hình dung trực quan.

    #     Thật ra,
    #     expert là các mạng con được học trong quá trình huấn luyện.
    #     Router cũng được học
    #     để phân phối to-kần đến các expert phù hợp.

    #     Em-âu-i rất mạnh,
    #     nhưng serving em-âu-i cũng khó hơn mô-đồl dense thông thường.

    #     Có ba vấn đề lớn.

    #     Thứ nhất,
    #     cần router chọn expert phù hợp.

    #     Thứ hai,
    #     khi triển khai trên nhiều Gi-Pi-U,
    #     có thể xảy ra mất cân bằng tải.

    #     Nếu quá nhiều to-kần cùng đổ vào một expert,
    #     expert đó sẽ trở thành bottleneck.

    #     Thứ ba,
    #     em-âu-i cần tối ưu tốt về communication và kernel,
    #     vì to-kần có thể phải được gửi qua các Gi-Pi-U khác nhau.

    #     Vì vậy,
    #     em-âu-i có thể tóm tắt như sau:
    #     em-âu-i tăng dung lượng mô hình bằng nhiều expert,
    #     nhưng mỗi to-kần chỉ kích hoạt một phần expert.

    #     Đổi lại,
    #     hệ thống serving trở nên phức tạp hơn.
    #     """,
    # ),
    # (
    #     "p3_02_06_alternative_arch.mp3",
    #     """
    #     Ngoài việc tối ưu Trăn-pho-mơ,
    #     còn có các hướng kiến trúc thay thế hoặc hybrid,
    #     ví dụ như a-rờ-đắp-liu-kây-vi,
    #     RetNet,
    #     Mamba,
    #     hoặc các state space model.

    #     Mục tiêu của các hướng này là giảm sự phụ thuộc vào a-ten-sần toàn cục,
    #     đặc biệt khi xử lý xi-quần dài.

    #     Trăn-pho-mơ rất mạnh,
    #     vì a-ten-sần cho phép to-kần kết nối với nhiều to-kần khác.

    #     Nhưng a-ten-sần chuẩn có thể tốn nhiều bộ nhớ và tính toán khi chuỗi dài.

    #     Các kiến trúc dạng ri-cơ-rần hoặc state space
    #     cố gắng xử lý chuỗi theo cách khác.

    #     Thay vì lưu và nhìn lại toàn bộ quan hệ giữa các to-kần,
    #     mô hình duy trì một trạng thái nén
    #     và cập nhật trạng thái đó theo thời gian.

    #     Nhờ vậy,
    #     trong một số trường hợp,
    #     chi phí có thể tuyến tính hơn theo độ dài chuỗi.

    #     Tuy nhiên,
    #     cần nói cẩn thận:
    #     đây không phải là giải pháp thay thế Trăn-pho-mơ trong mọi trường hợp.

    #     Trăn-pho-mơ vẫn là nền tảng chính
    #     của rất nhiều eo-eo-em hiện đại.

    #     Các kiến trúc mới là hướng nghiên cứu quan trọng,
    #     nhưng hiệu quả còn phụ thuộc vào bài toán,
    #     dữ liệu huấn luyện,
    #     phần cứng,
    #     và cách triển khai in-phơ-rần.

    #     Vì vậy,
    #     ý chính ở đây là:
    #     ri-cơ-rần và state space architectures
    #     là hướng nghiên cứu nhằm xử lý xi-quần dài hiệu quả hơn,
    #     nhưng chưa phải lời giải thay thế hoàn toàn Trăn-pho-mơ
    #     trong mọi tình huống.
    #     """,
    # ),
    # (
    #     "p3_02_07_arch_summary.mp3",
    #     """
    #     Tóm lại,
    #     A-ki-téc-chờ Đi-dai-zần
    #     cố gắng làm cho bản thân mô hình hiệu quả hơn.

    #     Cờn-phi-giu-rây-sần đao-sai-zing
    #     giảm kích thước cấu hình mô-đồl.

    #     A-ten-sần sim-pli-fi-kây-sần
    #     giảm chi phí a-ten-sần khi xi-quần dài.

    #     Em-kiu-ây và gi-kiu-ây
    #     giảm kích thước kê-vi cache
    #     và giảm áp lực memory bandwidth trong đi-kôu phase.

    #     Em-âu-i chỉ kích hoạt một phần expert cần thiết,
    #     giúp tăng capacity
    #     mà không tăng compute tương ứng cho mỗi to-kần.

    #     Ri-cơ-rần hoặc state space architectures
    #     là hướng nghiên cứu để xử lý xi-quần dài hiệu quả hơn.

    #     Điểm chung là:
    #     thay đổi kiến trúc có thể đem lại hiệu quả lớn.

    #     Nhưng thường đi kèm trade-off
    #     về chất lượng,
    #     độ phức tạp huấn luyện,
    #     hoặc độ khó khi triển khai hệ thống.
    #     """,
    # ),
    # )
]


async def make_one(filename: str, text: str):
    out_path = OUT_DIR / filename
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
    )
    await communicate.save(str(out_path))
    print(f"Saved: {out_path}")


async def main():
    for filename, text in SEGMENTS:
        await make_one(filename, text)


if __name__ == "__main__":
    asyncio.run(main())
