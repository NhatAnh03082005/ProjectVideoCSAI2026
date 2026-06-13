import asyncio
import edge_tts
import os

# ============================================================
# VOICE SLIDE 10 — Scalability & Throughput (7 cảnh), TÁCH TỪNG CÂU.
#   PYTHONUTF8=1 python make_slide10_voice.py
# Phiên âm: throughput->thông lượng, latency->lây-tân-xi, GPU->gi-pi-iu,
#   batch->bát, request->yêu cầu, prompt->pờ-rom, LLM->eo-eo-em.
#   Dấu . ? -> , để câu liền mạch.
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
os.makedirs("voice", exist_ok=True)

sentences = {
    # ----- C1 BRIDGE + KIẾN TRÚC -----
    "s10a_01": "Thách thức thứ ba là khả năng mở rộng và thông lượng,",
    "s10a_02": "Ở hai thách thức trước, ta nhìn hệ thống phục vụ một người dùng, giờ hãy nhìn toàn cảnh,",
    "s10a_03": "Rất nhiều ứng dụng cùng gửi yêu cầu tới máy chủ,",
    "s10a_04": "Bên trong máy chủ là một bộ máy gồm hàng đợi và bộ lập lịch, một khâu gom yêu cầu thành bát, rồi tới mô hình chạy trên phần cứng gi-pi-iu,",
    "s10a_05": "Và hệ thống liên tục đo hai con số, thông lượng và lây-tân-xi,",
    "s10a_06": "Cả phần này xoay quanh việc giữ cho dây chuyền đó vừa nhanh, vừa phục vụ được thật nhiều người,",

    # ----- C2 LATENCY vs THROUGHPUT -----
    "s10b_01": "Trước hết phải phân biệt hai khái niệm dễ nhầm,",
    "s10b_02": "Lây-tân-xi trả lời câu hỏi, một người dùng phải chờ bao lâu,",
    "s10b_03": "Còn thông lượng trả lời câu hỏi khác, trong một giây cả hệ thống xử lý được bao nhiêu token, bao nhiêu yêu cầu, cho tất cả mọi người,",
    "s10b_04": "Hai mục tiêu này liên quan nhưng không giống nhau,",
    "s10b_05": "Và như ta sẽ thấy, đẩy mạnh cái này nhiều khi lại làm hỏng cái kia,",

    # ----- C3 REQUEST KHÔNG ĐỒNG NHẤT -----
    "s10c_01": "Vì sao phục vụ nhiều người lại khó đến vậy, vì các yêu cầu đến liên tục và rất khác nhau,",
    "s10c_02": "Có người chỉ hỏi một câu cực ngắn, hai cộng hai bằng mấy,",
    "s10c_03": "Có người lại bảo mô hình viết một bài phân tích hai nghìn chữ, hay tóm tắt một tài liệu ba mươi trang,",
    "s10c_04": "Chúng dồn vào cùng một hàng đợi, nhưng độ dài thì chênh nhau rất xa,",

    # ----- C4 OUTPUT KHÔNG BIẾT TRƯỚC -----
    "s10d_01": "Nhưng điểm khó nhất nằm ở đây,",
    "s10d_02": "Khi một yêu cầu đi vào, ta biết pờ-rom dài bao nhiêu, nhưng ta không biết mô hình sẽ sinh ra bao nhiêu token rồi mới dừng,",
    "s10d_03": "Câu trả lời có thể là vài chữ, cũng có thể là vài nghìn chữ,",
    "s10d_04": "Trong các bài toán suy luận truyền thống, kích thước đầu ra thường cố định và biết trước,",
    "s10d_05": "Còn ở eo-eo-em, phần đầu ra là một dấu hỏi co giãn, và chính điều đó khiến việc lập lịch và gom batch khó hơn rất nhiều,",

    # ----- C5 BATCHING -----
    "s10e_01": "Giải pháp cơ bản để tăng thông lượng là gom nhiều yêu cầu lại xử lý chung, gọi là gom bát,",
    "s10e_02": "Thay vì cho gi-pi-iu chạy lẻ từng yêu cầu, ta xếp nhiều yêu cầu vào cùng một lượt tính,",
    "s10e_03": "Nhờ vậy, mỗi giây hệ thống đẩy ra được nhiều token hơn hẳn, và quan trọng là giữ cho gi-pi-iu, vốn rất đắt tiền, luôn bận một cách hiệu quả,",
    "s10e_04": "Đây mới chỉ là ý tưởng gom bát cơ bản, còn các kỹ thuật gom thông minh hơn sẽ để dành cho phần sau,",

    # ----- C6 CĂNG THẲNG (CENTERPIECE) -----
    "s10f_01": "Và đây là căng thẳng cốt lõi,",
    "s10f_02": "Một mặt, ta muốn gom thật nhiều yêu cầu để thông lượng cao,",
    "s10f_03": "Nhưng nếu lập lịch kém, một yêu cầu ngắn có thể bị kẹt phía sau một yêu cầu rất dài, người chỉ hỏi hai cộng hai lại phải chờ như thể đang đặt viết cả một bài luận,",
    "s10f_04": "Mặt khác, vì các yêu cầu dài ngắn khác nhau, có cái xong sớm để lại chỗ trống trong bát, khiến gi-pi-iu rơi vào cảnh rảnh rỗi và lãng phí,",
    "s10f_05": "Thế là ta luôn phải cân, gom nhiều thì thông lượng cao nhưng có người chờ lâu, gom ít thì công bằng hơn nhưng phần cứng lại phí,",
    "s10f_06": "Đẩy bên này, bên kia thiệt,",

    # ----- C7 TỔNG KẾT -> HARDWARE -----
    "s10g_01": "Tóm lại, phục vụ một mô hình cho một người dùng đã khó,",
    "s10g_02": "Phục vụ cùng lúc cho hàng nghìn người, với pờ-rom và đầu ra dài ngắn rất khác nhau, còn khó hơn nhiều,",
    "s10g_03": "Vì thế, mở rộng quy mô không đơn thuần là cắm thêm gi-pi-iu, mà là bài toán tổ chức yêu cầu, quản lý bát, xử lý độ dài biến thiên và giữ cân bằng giữa lây-tân-xi và thông lượng,",
    "s10g_04": "Nhưng dù tổ chức khéo đến đâu, cuối cùng tất cả vẫn phải chạy trên phần cứng, và không phải phần cứng nào cũng giống nhau, đó là thách thức tiếp theo,",
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
