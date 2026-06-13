import asyncio
import os

import edge_tts


# ============================================================
# PART 4 - SCENE 21: KERNEL OPTIMIZATION
#
# Chay:
#   py make_p4_21_voices.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)


segments = [
    (
        "voice/p4_21_01_intro.mp3",
        """
        Sau sờ-ke-chu-linh, ta đi xuống tầng thấp hơn nữa: cơ-nồ óp-ti-mai-zây-sần, cơ-nồ là đoạn chương trình thật sự chạy trên gi-pi-diu
        cho một phép toán như mát-mun, lây-ơ nom hay ơd-ten-sần.

        Ở tầng này, câu hỏi không còn là mo-đồ sinh token nào, mà là dữ liệu đi qua chip ra sao, đọc từ đâu, ghi vào đâu, và có bị di chuyển quá nhiều hay không.
        """,
    ),
    (
        "voice/p4_21_02_hbm_sram.mp3",
        """
        Hãy tưởng tượng ếch-bi-em trên gi-pi-diu là một kho hàng rất lớn, còn ét ram hoặc re-chét-tơ là bàn làm việc rất nhỏ nhưng cực nhanh,
        Nếu mỗi phép toán đều phải chạy ra kho lấy dữ liệu, rồi đem về bàn, rồi lại cất kết quả ra kho, thời gian sẽ bị tiêu tốn vào di chuyển dữ liệu.
        Vì vậy nhiều tối ưu kernel tập trung vào việc giữ dữ liệu gần nơi tính toán càng lâu càng tốt.
        """,
    ),
    (
        "voice/p4_21_03_fusion.mp3",
        """
        Cơ-nồ phiu-sần là một ý tưởng rất tự nhiên, Thay vì chạy phép cộng bias,
        ghi kết quả ra ếch-bi-em, rồi đọc lại để chạy ắc-ti-vây-sần, rồi lại ghi ra, ta gộp các phép toán nhỏ thành một cơ-nồ,
        Dữ liệu được giữ trên bàn làm việc nhanh, đi qua nhiều bước liên tiếp, rồi mới ghi kết quả cuối cùng ra bộ nhớ lớn.
        """,
    ),
    (
        "voice/p4_21_04_prefill_attention.mp3",
        """
        ờ-ten-sần là phép toán đặc biệt quan trọng,
        Ở pha pờ-rì-phiu, mô hình xử lý toàn bộ prompt cùng lúc.
        Nếu prompt dài, ma trận ờ-ten-sần có kích thước theo số token nhân số token,
        Việc tạo và lưu trực tiếp ma trận khổng lồ này trong ếch-bi-em sẽ rất tốn bộ nhớ và băng thông.
        """,
    ),
    (
        "voice/p4_21_05_flashattention.mp3",
        """
        phờ-lát ờ-ten-sần xử lý ờ-ten-sần theo các block nhỏ vừa với ét ram,
        Thay vì tạo toàn bộ ma trận ờ-ten-sần rồi ghi ra ếch-bi-em, nó đưa từng tile vào bộ nhớ nhanh,
        tính toán từng phần, cập nhật kết quả bằng kỹ thuật online softmax, rồi chỉ ghi kết quả cần thiết,
        đừng trải cả tấm bản đồ khổng lồ ra bàn, hãy xử lý từng mảnh vừa bàn.
        """,
    ),
    (
        "voice/p4_21_06_decode_attention.mp3",
        """
        Ở pha đì-cốt, bài toán lại khác,
        Mỗi i-đơ-rây-sần chỉ có một que-ry mới, nhưng que-ri đó phải đọc key và va-liu của toàn bộ pờ-ri-phít trong kây vi cát,
        Vì vậy đì-cốt ờ-ten-sần thường không giống pờ-rùy-phiu ờ-ten-sần,
        Các cơ-nồ như pây ờ-ten-sần, phờ-lát đì-cốt-đinh hoặc phờ-lát in-phơ tập trung tối ưu cách đọc kây vi cát dài, chọn chiều song song phù hợp và tận dụng gi-pi-diu tốt hơn.
        """,
    ),
    (
        "voice/p4_21_07_variable_length.mp3",
        """
        Một thách thức khác là si-quần len biến thiên, Nếu một bát có prompt dài một nghìn token
        và prompt ngắn năm mươi token, cách đơn giản là padding tất cả lên một nghìn,
        Nhưng phần pát-đing không mang thông tin vẫn tiêu tốn còm-piu và me-mơ-ruy,
        Vì vậy các hệ thống dùng pách-king, ra-gịt ten-sờ hoặc bất-kít-tinh để giảm phần rỗng này.
        """,
    ),
    (
        "voice/p4_21_08_compilation.mp3",
        """
        Cuối cùng là au-tô-ma-tic com-pi-lây-sần, Thay vì viết tay mọi cơ-nồ cho mọi phần cứng,
        các còm-pai-lờ như ti-vi-em, chai-tần, toóc-in-đắc-tờ hoặc em-eo-ai-a, có thể sinh và tối ưu code cho cấu hình cụ thể.
        Một cơ-nồ tối ưu cho en-vi-đi-a gi-pi-diu chưa chắc tối ưu cho ây-em-đi gi-pi-diu, ci-pi-diu hay edge đì-vai.
        còm-pai-lờ giúp hệ thống thích nghi tốt hơn với phần cứng đa dạng.
        """,
    ),
    (
        "voice/p4_21_09_summary.mp3",
        """
        Tóm lại, cơ-nồ óp-ti-mai-zây-sần là nghệ thuật làm cho dữ liệu di chuyển ít hơn và tính toán hiệu quả hơn.
        cơ-nồ phiu-sần giảm đọc ghi trung gian, 
        phờ-lát ờ-ten-sần tối ưu ờ-ten-sần ở pờ-rùy-phiu bằng tai-linh, đì-cốt ờ-ten-sần cần tối ưu cho việc đọc kây-vi cát,
        va-ri-ơ-bồ len cần giảm pát-đinh, và còm-pai-lờ giúp thích nghi với nhiều phần cứng, Tầng này nhỏ nhưng quyết định rất lớn đến hiệu năng thật.
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
    print("Done. Created all Part 21 voice files in ./voice")


if __name__ == "__main__":
    asyncio.run(main())
