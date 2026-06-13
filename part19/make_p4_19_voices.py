import asyncio
import os

import edge_tts


# ============================================================
# PART 4 - SCENE 19: MEMORY MANAGEMENT
#
# Chay:
#   py make_p4_19_voices.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)


segments = [
    (
        "voice/p4_19_01_memory_intro.mp3",
        """
        Bây giờ ta đến phần rất quan trọng trong eo-eo-em serving: quản lý bộ nhớ.
        Khi mới nghe, ta thường nghĩ gi-pi-iu chỉ cần đủ chỗ để chứa mo-đồ quây, Nhưng trong in-phơ-rần thật, vi ram còn phải chứa quởc-space tạm thời, bát đang chạy, và đặc biệt là cây vi cát.
        Nhiều khi hệ thống không nghẽn vì thiếu phép tính, mà nghẽn vì không còn chỗ để lưu trạng thái sinh token.
        """,
    ),
    (
        "voice/p4_19_02_autoregressive.mp3",
        """
        Lý do cây vi cát xuất hiện nằm ở cách eo-eo-em sinh văn bản, Mô hình không viết cả câu trong một lần,
        Nó sinh token thứ nhất, rồi dùng toàn bộ pri-phít đã có để sinh token thứ hai,
        rồi tiếp tục như vậy, Nghĩa là token mới luôn phụ thuộc vào các token trước đó, 
        Nếu mỗi bước đều tính lại mọi thứ từ đầu chi phí sẽ tăng rất nhanh,
        """,
    ),
    (
        "voice/p4_19_03_kv_memory.mp3",
        """
        Trong mỗi layer tren-pho-mờ, ờ-ten-sần tạo ra query, ki , và va-liu.
        Khi sinh token mới, query của token mới cần so với ki và va-liu của các token cũ, Vì key và value cũ đã tính rồi, ta lưu lại chúng trong cây vi cát.
        Có thể hiểu cây vi cát giống như cuốn sổ ghi chú: thay vì đọc lại toàn bộ sách từ đầu, mô hình mở sổ ra xem những thông tin đã ghi.
        """,
    ),
    (
        "voice/p4_19_04_growth.mp3",
        """
        Vấn đề là cây vi cát không cố định, Mỗi khi mo-đồ sinh thêm một token, mỗi layer lại có thêm key và value mới để lưu.
        Nếu batch có nhiều rùy-quét, mỗi rùy-quét lại có một đoạn cát riêng, Vì vậy, khi si-quần dài hơn, hoặc số người dùng đồng thời nhiều hơn, cây vi cát có thể trở thành phần chiếm vi ram rất lớn.
        """,
    ),
    (
        "voice/p4_19_05_naive_allocation.mp3",
        """
        Một cách đơn giản là cấp phát trước cho mỗi rùy-quét
        một vùng đủ lớn theo độ dài tối đa, Ví dụ rùy-quét có thể sinh tối đa hai nghìn không trăm bốn mươi tám token, ta giữ chỗ cho hai nghìn không trăm bốn mươi tám token ngay từ đầu,
        Nhưng nếu người dùng chỉ sinh hai trăm token, thì phần còn lại bị bỏ trống,
        Cách này dễ cốt, nhưng cực kỳ lãng phí khi rùy-quét dài ngắn khác nhau.
        """,
    ),
    (
        "voice/p4_19_06_hotel_old.mp3",
        """
        Hãy tưởng tượng bộ nhớ gi-pi-iu như một khách sạn.
        Cách cũ giống như yêu cầu cả đoàn khách phải ở các phòng liền kề, Khách sạn vẫn còn nhiều phòng trống rải rác,
        nhưng không có một dãy phòng liên tục đủ dài,
        Kết quả là lễ tân phải từ chối đoàn khách, tương tự hệ thống báo hết bộ nhớ, dù tổng chỗ trống rải rác vẫn còn.
        """,
    ),
    (
        "voice/p4_19_07_paged_intro.mp3",
        """
        pây đờ-ten-sần đổi cách nghĩ.
        Thay vì bắt cây vi cát của một rùy-quét nằm trong một vùng liên tục,
        nó chia cache thành các bờ-lóoc cố định, giống như chia khách sạn thành từng phòng độc lập,
        Rùy-quét có thể dùng các bờ-lóoc rải rácở nhiều vị trí khác nhau.
        Miễn là hệ thống có một bảng ghi lại bờ-lóoc nào thuộc về rùy-quét nào.
        """,
    ),
    (
        "voice/p4_19_08_block_table.mp3",
        """
        Điểm cốt lõi là block tây-bồ, Với rùy-quét A,
        token từ không đến mười lăm có thể nằm ở bờ-lóoc vật lý số ba, Token từ mười sáu đến ba mươi mốt nằm ở bờ-lóoc số chín.
        Token tiếp theo nằm ở bờ-lóoc số một, Khi ờ-ten-sần cần đọc cây vi cát, nó không cần cát nằm liền nhau.
        Nó chỉ cần tra bảng để biết phải đọc bờ-lóoc vật lý nào.
        """,
    ),
    (
        "voice/p4_19_09_benefit.mp3",
        """
        Khi cấp phát theo bờ-lóoc nhỏ, các khoảng trống rải rác có thể được tái sử dụng linh hoạt,
        Rùy-quét kết thúc thì bờ-lóoc của nó được trả lại cho pool, Rùy-quét mới có thể lấy các bờ-lóoc trống này ngay.
        Nhờ vậy, cùng một gi-pi-iu có thể chứa nhiều rùy-quét hơn, bát-ch sai lớn hơn, và thờ-râu-pút thường tăng đáng kể, tùy quấc-loát.
        """,
    ),
    (
        "voice/p4_19_10_not_quality.mp3",
        """
        Một điều cần phân biệt rõ: Pây dờ-ten-sần không làm mô hình giỏi hơn, cũng không thay đổi xác suất token đầu ra.
        Nó là tối ưu hệ thống.
        Tức là cùng một mo-đồ, cùng một thuật toán đì-cốt, nhưng hệ thống quản lý cây vi cát thông minh hơn để phục vụ được nhiều rùy-quét hơn.
        """,
    ),
    (
        "voice/p4_19_11_offloading_intro.mp3",
        """
        Nếu sau khi quản lý tốt hơn mà gi-pi-iu vẫn không đủ chỗ, một hướng khác là óp-loát-đinh,
        Ý tưởng rất đơn giản: thứ gì chưa cần dùng ngay có thể tạm đặt ở nơi rẻ hơn nhưng chậm hơn,
        như ci-pi-diu ram hoặc disk, Khi cần, hệ thống kéo dữ liệu đó quay lại gi-pi-iu để tính,
        """,
    ),
    (
        "voice/p4_19_12_offload_types.mp3",
        """
        Có thể óp-loát nhiều loại dữ liệu.
        Một số hệ thống óp-loát mo-đồ quây, nghĩa là không giữ toàn bộ trọng số trên gi-pi-iu cùng lúc,
        Một số hệ thống óp-loát cây vi cát, đặc biệt khi con-téc dài hoặc có nhiều phiên hội thoại,
        Hai cách này đều giúp tiết kiệm vi ram,nhưng cách lập lịch truyền dữ liệu sẽ khác nhau.
        """,
    ),
    (
        "voice/p4_19_13_offload_tradeoff.mp3",
        """
        Cái giá của óp-loát-đinh là đường đi dữ liệu dài hơn,
        Gi-pi-iu đọc ếch-bi-em rất nhanh,nhưng kéo dữ liệu từ ci-pi-diu ram hoặc disk qua bus sẽ chậm hơn.
        Nếu kéo dữ liệu không đúng lúc, gi-pi-iu phải đứng chờ,
        Vì vậy óp-loát-đinh thường phù hợp khi mục tiêu là chạy được mô hình lớn trên phần cứng hạn chế,
        không phải khi cần lây-tần-ci thấp nhất,
        """,
    ),
    (
        "voice/p4_19_14_integration.mp3",
        """
        Trong hệ thống thật, me-mơ-ri ma-nịt-mần không đứng một mình,
        Nếu batch lớn hơn nhờ Pây dờ-ten-sần, sờ-ke-chồ-l cũng phải quyết định rùy-quét nào được thêm vào bát-ch,
        Nếu óp-loát-đinh dữ liệu, sờ-ke-chồ-l cũng phải biết khi nào cần pờ-rùy-phét để gi-pi-iu không chờ,
        Nói cách khác, quản lý bộ nhớ và lập lịch rùy-quét luôn liên quan chặt chẽ với nhau.
        """,
    ),
    (
        "voice/p4_19_15_summary.mp3",
        """
        Tóm lại,
        cây vi cát là trí nhớ tạm giúp đì-cốt nhanh hơn, nhưng cũng là nguồn tiêu thụ vi ram rất lớn.
        Pây dờ-ten-sần làm cho cây vi cát linh hoạt hơn bằng block table và các block không liên tục.
        óp-loát-đinh mở rộng không gian bộ nhớ bằng CPU ram hoặc disk, nhưng phải trả giá bằng lây-tần-ci.
        Sau khi đã biết bộ nhớ được quản lý thế nào, câu hỏi tiếp theo là: các rùy-quét sẽ được xếp hàng và đưa vào gi-pi-iu ra sao?
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
    print("Done. Created all Part 19 voice files in ./voice")


if __name__ == "__main__":
    asyncio.run(main())
