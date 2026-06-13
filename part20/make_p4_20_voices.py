import asyncio
import os

import edge_tts


# ============================================================
# PART 4 - SCENE 20: REQUEST SCHEDULING
#
# Chay:
#   py make_p4_20_voices.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)


segments = [
    (
        "voice/p4_20_01_intro.mp3",
        """
        Sau khi đã biết bộ nhớ được quản lý thế nào,
        ta cần trả lời câu hỏi tiếp theo:
        khi hàng ngàn người cùng gửi rì-quét,
        hệ thống xếp họ vào gi-pi-iu ra sao?

        Vấn đề là mỗi rì-quét rất khác nhau.
        Có người hỏi một câu ngắn,
        có người gửi cả tài liệu dài.

        Có câu trả lời chỉ vài token,
        có câu trả lời kéo dài hàng trăm token.
        """,
    ),
    (
        "voice/p4_20_02_static_batching.mp3",
        """
        Cách đơn giản là sờ-tây-tíc bát-chinh:
        gom một nhóm rì-quét lại,
        cho chạy cùng nhau,
        rồi đợi cả nhóm hoàn tất mới nhận nhóm mới.

        Cách này giống một chiếc xe buýt:
        dù vài hành khách đã đến nơi,
        xe vẫn không cho người mới lên
        cho đến khi cả nhóm cũ kết thúc.

        Với e lờ em,
        rì-quét ngắn sẽ phải chờ rì-quét dài.
        """,
    ),
    (
        "voice/p4_20_03_partial_idle.mp3",
        """
        Điều nguy hiểm là gi-pi-iu nhìn bên ngoài có vẻ vẫn đang chạy,
        nhưng bên trong batch đã rỗng từng phần.

        Những slot của rì-quét đã hoàn tất
        không được dùng để phục vụ rì-quét mới.

        Khi số rì-quét trong batch giảm dần,
        gi-pi-iu utilization cũng giảm.

        Đây là lý do eo-eo-em serving
        cần lập lịch mịn hơn cấp rì-quét.
        """,
    ),
    (
        "voice/p4_20_04_iteration.mp3",
        """
        cờn-ti-niu-ợt bát-chinh giải quyết bằng cách lập lịch ở cấp i-tơ-rây-sần.
        Mỗi vòng đì-cốt, bát sinh thêm một token cho các rì-quét đang hoạt động.
        Nếu một rì-quét kết thúc ở vòng này, rì-quét mới trong hàng đợi có thể được đưa vào ở vòng tiếp theo.
        Bát không còn là một đoàn cố định từ đầu đến cuối, mà là một dòng chảy liên tục.
        """,
    ),
    (
        "voice/p4_20_05_conveyor.mp3",
        """
        Một ẩn dụ dễ hình dung hơn là băng chuyền,
        Thay vì đợi cả xe buýt đầy rồi chạy một chuyến, hệ thống giống một băng chuyền đang quay,
        Ai xử lý xong thì bước xuống, người mới lập tức được đặt vào vị trí trống ở nhịp kế tiếp.
        Nhờ vậy gi-pi-iu được giữ bận hơn, đặc biệt khi có nhiều rì-quét ngắn dài xen kẽ.
        """,
    ),
    (
        "voice/p4_20_06_prefill_decode.mp3",
        """
        Nhưng rùy-quét sờ-ke-chu-linh không chỉ là thêm hay bớt rì-quét,
        eo-eo-em in-phơ-rần có hai pha rất khác nhau.
        Pri-fill là lúc hệ thống xử lý toàn bộ prompt ban đầu và tạo cây vi cát.
        Đì-cốt là lúc hệ thống sinh từng token tiếp theo bằng cách đọc lại cây vi cát.
        Pri-fill thường nặng về còm-piu, còn đì-cốt thường bị giới hạn bởi việc đọc bộ nhớ.
        """,
    ),
    (
        "voice/p4_20_07_long_prefill_blocks.mp3",
        """
        Hãy tưởng tượng đang có nhiều rì-quét nhỏ cần sinh token đều đặn,
        Đột nhiên một người gửi vào prompt dài hàng chục nghìn token,
        Nếu hệ thống xử lý pri-fill của prompt dài đó một mạch, gi-pi-iu có thể bị chiếm lâu, làm các rì-quét đang đì-cốt bị khựng,
        Người dùng cảm giác chữ đang stream bỗng đứng lại.
        """,
    ),
    (
        "voice/p4_20_08_chunked_prefill.mp3",
        """
        chân pri-fill xử lý vấn đề này bằng cách cắt prompt dài thành nhiều chân nhỏ.
        Thay vì nuốt cả prompt dài trong một lần, sờ-ke-chu-lơ đưa từng chân vào gi-pi-iu,
        xen kẽ với các bước đì-cốt của rì-quét khác, Như vậy prompt dài vẫn được xử lý,
        nhưng không làm dòng token của những rì-quét đang stream bị nghẽn quá lâu.
        """,
    ),
    (
        "voice/p4_20_09_priority_slo.mp3",
        """
        Trong pờ-rồ-đấc-sần, sờ-ke-chu-lơ còn phải quan tâm đến mục tiêu dịch vụ.
        Có rì-quét tương tác cần phản hồi ngay, có job óp-lai có thể chờ lâu hơn.
        Có hệ thống ưu tiên rì-quét ngắn để giảm thời gian hoàn tất, có hệ thống đảm bảo công bằng giữa người dùng.
        Vì vậy sờ-ke-chu-linh là bài toán cân bằng giữa thờ-ru-pút, lây-ten-ci, phe-nẹt, và ét eo ô.
        """,
    ),
    (
        "voice/p4_20_10_disaggregation.mp3",
        """
        Một hướng nâng cao là tách pri-fill và đì-cốt ra các nhóm tài nguyên khác nhau.
        Vì pri-fill và đì-cốt dùng tài nguyên khác nhau, ta có thể để một cụm gi-pi-iu chuyên xử lý prompt ban đầu.
        Sau đó chuyển cây vi cát hoặc sờ-tây sang cụm khác chuyên đì-cốt, Cách này có thể tối ưu gút-pút trong một số quấc-loát, nhưng hệ thống phức tạp hơn nhiều.
        """,
    ),
    (
        "voice/p4_20_11_full_timeline.mp3",
        """
        Bây giờ ghép lại toàn bộ bức tranh,
        Rì-quét đi vào kiu, Sờ-ke-chu-lơ quyết định đưa prompt vào pri-fill, có thể chia chân nếu prompt dài,
        Sau đó rì-quét bước vào đì-cốt pun, mỗi i-tơ-rây-sần sinh thêm token, Khi rì-quét kết thúc, slot được trả lại ngay cho rì-quét mới, Đây là dòng chảy cơ bản của một eo-eo-em serving en-chần hiện đại.
        """,
    ),
    (
        "voice/p4_20_12_summary_transition.mp3",
        """
        Tóm lại, rùy-quét sờ-ke-chu-linh quyết định gi-pi-iu phục vụ ai, vào lúc nào, và theo nhịp nào.
        con-ti-niu-ợt bát-chinh giúp bát sống liên tục theo từng i-tơ-rây-sần, chân pri-fill tránh để prompt dài chặn dòng đì-cốt,
        Nhưng ngay cả khi scheduler đã tốt, mỗi phép toán bên trong gi-pi-iu
        vẫn cần được viết thật hiệu quả, Đó là lý do ta đi xuống tầng cơ-nồ óp-ti-mai-zây-sần.
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
    print("Done. Created all Part 20 voice files in ./voice")


if __name__ == "__main__":
    asyncio.run(main())
