import asyncio
import edge_tts
import os

# ============================================================
# VOICE SLIDE 12 — Accuracy-Efficiency Trade-off + kết Phần 2 (7 cảnh), TÁCH TỪNG CÂU.
#   PYTHONUTF8=1 python make_slide12_voice.py
# Phiên âm: LLM->eo-eo-em, API->a-pi-ai, chatbot->chát-bót. Tên model hiện trên biểu đồ, KHÔNG đọc.
#   speculative decoding->giải mã suy đoán, quantization->lượng tử hóa, lossless->không mất mát.
#   Dấu . ? -> , để câu liền mạch.
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
os.makedirs("voice", exist_ok=True)

sentences = {
    # ----- C1 BRIDGE -----
    "s12a_01": "Thách thức cuối cùng là đánh đổi giữa chất lượng và hiệu quả,",
    "s12a_02": "Trong phục vụ eo-eo-em, ta luôn muốn hệ thống nhanh hơn, rẻ hơn, tốn ít tài nguyên hơn,",
    "s12a_03": "Nhưng gần như mọi cách làm điều đó đều dẫn tới cùng một câu hỏi, ta sẵn sàng đánh đổi bao nhiêu chất lượng để lấy tốc độ hoặc chi phí thấp hơn,",

    # ----- C2 BIỂU ĐỒ -----
    "s12b_01": "Hãy nhìn một biểu đồ thực tế,",
    "s12b_02": "Trục dọc là chất lượng, trục ngang là tốc độ sinh token, còn kích thước mỗi bong bóng thể hiện giá,",
    "s12b_03": "Mỗi chấm là một mô hình,",
    "s12b_04": "Chỉ cần nhìn thoáng qua, ta đã thấy các mô hình trải khắp biểu đồ, chứ không dồn về một góc lý tưởng,",

    # ----- C3 ĐỌC TRADE-OFF -----
    "s12c_01": "Góc trên bên phải, tô xanh, là vùng hấp dẫn nhất, vừa chất lượng cao, vừa tốc độ cao,",
    "s12c_02": "Nhưng ít mô hình nằm trọn ở đó,",
    "s12c_03": "Mô hình mạnh nhất thường nằm phía trên bên trái, chất lượng đỉnh nhưng chậm và đắt,",
    "s12c_04": "Còn nhóm nhanh và rẻ lại nằm thấp hơn về chất lượng,",
    "s12c_05": "Muốn chạy nhanh hơn, ta thường phải chấp nhận giảm chất lượng, hoặc trả thêm chi phí,",

    # ----- C4 KỸ THUẬT & ĐÁNH ĐỔI (DIALS) -----
    "s12d_01": "Vì sao lại có đánh đổi,",
    "s12d_02": "Vì để nhanh và rẻ hơn, ta thường dùng model nhỏ hơn, lượng tử hóa, tỉa bớt tham số, thoát sớm, hay suy luận xếp tầng,",
    "s12d_03": "Nhưng phần lớn các kỹ thuật nén và giảm tính toán này không miễn phí,",
    "s12d_04": "Model nhỏ có thể kém ở câu hỏi khó, lượng tử hóa quá mạnh làm chất lượng giảm, thoát sớm có thể dừng quá sớm, còn xếp tầng thì cần thêm cơ chế kiểm soát,",
    "s12d_05": "Có một ngoại lệ đáng chú ý, giải mã suy đoán cũng giúp tăng tốc, nhưng không hề đánh đổi chất lượng, vì kết quả luôn được mô hình gốc kiểm chứng, nên nó là kỹ thuật không mất mát,",

    # ----- C5 ONE-SIZE-FITS-ALL -----
    "s12e_01": "Và đây là điểm mấu chốt, không có một lựa chọn đúng cho mọi trường hợp,",
    "s12e_02": "Với hỏi đáp đơn giản hay chát-bót giải trí, một mô hình nhỏ nhanh và rẻ có thể đã đủ tốt,",
    "s12e_03": "Nhưng với phân tích pháp lý, y tế, tài chính hay sinh mã phức tạp, giảm chất lượng có thể gây rủi ro lớn,",
    "s12e_04": "Một ứng dụng chạy trên điện thoại có ràng buộc khác hẳn một a-pi-ai phục vụ doanh nghiệp trên cloud,",
    "s12e_05": "Mỗi nhu cầu chọn một điểm khác nhau trên biểu đồ này,",

    # ----- C6 RECAP -> CÂN BẰNG -----
    "s12f_01": "Khép lại phần hai,",
    "s12f_02": "Phục vụ eo-eo-em khó không phải vì chỉ có một nút thắt, mà vì nhiều nút thắt xuất hiện cùng một lúc, độ trễ, bộ nhớ, thông lượng, phần cứng, và đánh đổi chất lượng,",
    "s12f_03": "Tối ưu cái này thường ảnh hưởng cái kia,",
    "s12f_04": "Nói gọn lại, phục vụ eo-eo-em hiệu quả chính là bài toán cân bằng năm yếu tố đó,",

    # ----- C7 CHUYỂN PHẦN 3 -----
    "s12g_01": "Từ đây, các phần tiếp theo sẽ không còn dừng ở việc nêu vấn đề, mà đi vào những kỹ thuật cụ thể để hóa giải từng nút thắt,",
    "s12g_02": "Từ tối ưu thuật toán cho tới tối ưu hệ thống,",
}


async def gen(filename, text, retries=6):
    for attempt in range(retries):
        try:
            await edge_tts.Communicate(text=text, voice=VOICE).save(filename)
            print("Da tao:", filename)
            return True
        except Exception as e:
            print(f"Lan {attempt + 1} loi ({filename}): {e}")
            if attempt < retries - 1:
                await asyncio.sleep(3)
    print("[BO QUA]", filename)
    return False


async def main():
    failed = []
    for sid, text in sentences.items():
        if not await gen(f"voice/{sid}.mp3", text):
            failed.append(sid)
    print("LOI:", failed if failed else "khong co")


if __name__ == "__main__":
    asyncio.run(main())
