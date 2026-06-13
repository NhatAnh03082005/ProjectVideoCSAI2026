import asyncio
import os

import edge_tts


# ============================================================
# Tao 12 file audio cho Part 4 - Scene 17: Low-bit Quantization
#
# Chay trong thu muc project:
#   py make_p4_17_voice_resume.py
# ============================================================


VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "voice/p4_17_01_hook.mp3",
        """
        Chúng ta bắt đầu Phần 4: Xi-x-từm Óp-ti-mai-dây-sần. Nếu các phần trước giống như tìm cách để mô hình suy nghĩ thông minh hơn, thì phần này giống như hỏi: làm sao để đưa mô hình đó lên máy thật, phục vụ thật nhiều người, mà không cháy Di-Pi-Yu, không hết Vi-Ram, và không làm người dùng chờ quá lâu? Kỹ thuật đầu tiên là Lâu-bít Quăn-ti-dây-sần.
        """,
    ),
    (
        "voice/p4_17_02_numbers_inside_model.mp3",
        """
        Hãy tưởng tượng bên trong một eo-eo-Em không phải là một bộ não bí ẩn, mà là một thành phố khổng lồ làm từ các con số. Mỗi quây là một viên gạch nhỏ. Một mô hình có hàng tỷ viên gạch như vậy. Nếu mỗi viên gạch được ghi bằng quá nhiều chữ số, cả thành phố sẽ rất nặng, và Di-Pi-Yu phải tốn rất nhiều bộ nhớ chỉ để cất nó.
        """,
    ),
    (
        "voice/p4_17_03_precision_as_ruler.mp3",
        """
        Pre-si-dần có thể hiểu như độ mịn của một cây thước. Ép-Pi ba mươi hai giống như một cây thước có rất nhiều vạch chia nhỏ, ghi được số rất chi tiết. Ép-Pi mười sáu hay Bi-Ép mười sáu ít vạch hơn, nhưng vẫn đủ dùng trong nhiều phép tính học sâu. Còn In-ti tám hay In-ti bốn thì giống như dùng thước thô hơn: ít vạch chia hơn, tiết kiệm hơn, nhưng không còn biểu diễn được mọi giá trị thật mượt như ban đầu.
        """,
    ),
    (
        "voice/p4_17_04_bucket_mapping.mp3",
        """
        Ý tưởng của quăn-ti-dây-sần là:
        thay vì giữ mọi số thực với độ chi tiết cao,
        ta chia trục số thành các ô rời rạc,
        giống như đặt nhiều chiếc xô trên một đường thẳng.
        Một quây ban đầu rơi vào đâu,
        ta thay nó bằng nhãn của chiếc xô gần nhất.
        Khi cần tính,
        hệ thống dùng nhãn đó cùng với hệ số sờ-keo
        để xấp xỉ lại giá trị ban đầu.
        """,
    ),
    (
        "voice/p4_17_05_tiny_example.mp3",
        """
        Ví dụ, một quây có giá trị khoảng 0 phẩy 73.
        Nếu ta dùng sờ-keo là 0 phẩy 1,
        thì giá trị này có thể được làm tròn thành nhãn q bằng 7.
        Khi khôi phục để tính toán,
        ta lấy 7 nhân 0 phẩy 1, được 0 phẩy 7.
        Ta đã mất một chút thông tin,
        nhưng đổi lại, thay vì lưu một số thực dài,
        ta chỉ lưu một số nguyên nhỏ.
        """,
    ),
    (
        "voice/p4_17_06_not_pruning.mp3",
        """
        Điểm rất dễ nhầm là:
        quăn-ti-dây-sần không phải là cắt bỏ mô hình.
        Nếu pruning giống như lấy kéo cắt bớt một số nhánh cây,
        thì quăn-ti-dây-sần giống như viết lại nhãn trên từng chiếc lá
        bằng chữ ngắn hơn.
        Số lượng quây về cơ bản vẫn còn đó,
        cấu trúc mạng vẫn còn đó,
        chỉ là mỗi quây được lưu bằng ít bit hơn.
        """,
    ),
    (
        "voice/p4_17_07_precision_levels.mp3",
        """
        Bây giờ ta xếp các định dạng theo kích thước.
        ép-pi ba mươi hai dùng 32 bit cho một số,
        thường rất chính xác nhưng tốn bộ nhớ.
        ép-pi mười sáu và bi-ép mười sáu dùng 16 bit,
        phổ biến trong đíp lân-ning.
        in-ti tám và ép-pi tám đều là 8 bit,
        nhưng một bên là số nguyên,
        một bên là số thực 8 bit.
        in-ti bốn chỉ dùng 4 bit, nhỏ hơn nữa,
        nhưng biểu diễn thô hơn và nhạy với lỗi hơn.
        """,
    ),
    (
        "voice/p4_17_08_memory_example.mp3",
        """
        Lợi ích đầu tiên là giảm me-mơ-ri phút-pờ-rin.
        Ví dụ rất gần đúng:
        một mô hình 7 tỷ tham số,
        nếu mỗi tham số dùng ép-pi mười sáu,
        chỉ riêng weight đã khoảng 14 GB.
        Nếu chuyển sang in-ti tám, con số này có thể gần 7 GB.
        Nếu dùng in-ti bốn, về lý tưởng có thể gần 3 phẩy 5 GB,
        chưa tính mê-ta đa-ta và âu-vờ-hét.
        Nhờ vậy, vi-ram còn chỗ cho bát-chờ lớn hơn
        hoặc kây-vi cát-chờ dài hơn.
        """,
    ),
    (
        "voice/p4_17_09_bandwidth.mp3",
        """
        Lợi ích thứ hai là giảm băng thông.
        chi-pi-diu không chỉ cần tính nhanh,
        nó còn phải liên tục kéo dữ liệu từ bộ nhớ.
        Hãy tưởng tượng ết-bi-em là một đường cao tốc,
        còn quây là các xe tải chở hàng.
        Nếu mỗi quây nhỏ đi một nửa,
        số bai phải vận chuyển cũng giảm.
        Với eo-eo-em in-phơ-rần,
        nhiều lúc nút thắt nằm ở đường vận chuyển dữ liệu này,
        nên giảm bai có thể quan trọng không kém giảm phép tính.
        """,
    ),
    (
        "voice/p4_17_10_speed_hardware_kernel.mp3",
        """
        Lợi ích thứ ba là tốc độ,
        nhưng đây là chỗ phải nói cẩn thận.
        quăn-ti-dây-sần không tự động làm mọi thứ nhanh hơn.
        Nó chỉ thật sự tăng tốc khi phần cứng và cơ-nồ
        biết tính trực tiếp hoặc gần trực tiếp với định dạng thấp bit.
        Nếu chi-pi-diu không hỗ trợ tốt,
        hệ thống có thể phải giải lượng tử hóa ngược về ép-pi mười sáunrồi mới nhân ma trận,
        Khi đó ta tiết kiệm bộ nhớ nhưng chưa chắc tiết kiệm thời gian.
        """,
    ),
    (
        "voice/p4_17_11_ptq_qat.mp3",
        """
        Có hai hướng phổ biến.
        pi-ti-kiu, hay pốt truên-ning quăn-ti-dây-sần,
        nghĩa là mô hình đã train xong rồi mới lượng tử hóa,Ta dùng một tập ca-lơ-bờ-rây-sần nhỏ để tìm sờ-keo phù hợp,
        giống như chỉnh lại thước đo trước khi đo thật,
        kiu-ây-ti, hay quăn-ti-dây-sần ờ-que truên-ning,
        đưa hiệu ứng lượng tử hóa vào trong lúc truên,
        để mô hình học cách chịu đựng sai số.
        pi-ti-kiu nhanh và tiện hơn, kiu-ây-ti thường tốn công hơn nhưng có thể giữ chất lượng tốt hơn.
        """,
    ),
    (
        "voice/p4_17_12_summary_transition.mp3",
        """
        Tóm lại,
        lâu-bít quăn-ti-dây-sần giống như viết lại toàn bộ cuốn sách mô hình
        bằng ký hiệu ngắn hơn.
        Nó giúp mô hình nhẹ hơn,
        giảm áp lực bộ nhớ và băng thông,
        đôi khi tăng tốc rất mạnh
        nếu đi cùng phần cứng phù hợp.
        Nhưng nếu giảm bit quá sâu, chất lượng có thể giảm;
        nếu cơ-nồ không tốt, tốc độ có thể không tăng.
        Và khi một chi-pi-diu vẫn không đủ,
        ta cần kỹ thuật tiếp theo: pa-ra-leo com-piu-tây-sần.
        """,
    ),
]


async def generate_audio(filename, text, retries=3):
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE)
            await communicate.save(filename)
            print("Da tao:", filename)
            return
        except Exception as exc:
            print(f"Lan {attempt + 1} that bai ({filename}): {exc}")
            if attempt < retries - 1:
                await asyncio.sleep(2)
            else:
                raise


async def main():
    for filename, text in segments:
        await generate_audio(filename, text)
    print("Xong! Da tao du 12 file audio trong thu muc voice.")


if __name__ == "__main__":
    asyncio.run(main())
