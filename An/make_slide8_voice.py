import asyncio
import edge_tts
import os

# ============================================================
# VOICE SLIDE 8 — Latency chi tiết (7 cảnh), TÁCH TỪNG CÂU.
#   python make_slide8_voice.py
# Phiên âm (xem thêm tts-phonetic-rule): TTFT->ti-ti-ép-ti, TPOT->ti-pi-âu-ti,
#   TDS->ti-đi-ét, latency->lây-tân-xi, prompt->pờ-rom, GPU->gi-pi-iu, LLM->eo-eo-em,
#   streaming->sờ-tri-ming, chatbot->chát-bót, server->máy chủ, request->yêu cầu.
#   Dấu . ? -> , để câu liền mạch.
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
os.makedirs("voice", exist_ok=True)

sentences = {
    # ----- C1 HOOK -----
    "s8a_01": "Bây giờ, ta đi sâu vào từng thách thức trong số năm thách thức vừa nêu,",
    "s8a_02": "Và thách thức đầu tiên, cũng là cái người dùng va phải sớm nhất và cảm nhận rõ nhất, chính là độ trễ, hay lây-tân-xi,",
    "s8a_03": "Khi gửi một pờ-rom cho chát-bót, thứ gây khó chịu nhất không hẳn là tổng thời gian chờ, mà là cảm giác không biết hệ thống có đang phản hồi hay không,",
    "s8a_04": "Chỉ vài giây màn hình đứng yên, người dùng đã nghĩ yêu cầu bị lỗi, dù máy chủ vẫn đang chạy,",

    # ----- C2 TTFT -----
    "s8b_01": "Khoảng thời gian từ lúc gửi pờ-rom đến khi token đầu tiên xuất hiện được gọi là ti-ti-ép-ti, tức Time To First Token,",
    "s8b_02": "Ti-ti-ép-ti càng cao thì khoảng im lặng ban đầu càng dài,",
    "s8b_03": "Đây là phần rất nhạy cảm, vì người dùng chưa thấy bất kỳ dấu hiệu nào cho biết hệ thống đang hoạt động,",

    # ----- C3 TPOT -----
    "s8c_01": "Sau token đầu tiên, mô hình tiếp tục sinh các token kế tiếp,",
    "s8c_02": "Thời gian trung bình để sinh mỗi token sau được gọi là ti-pi-âu-ti, tức Time Per Output Token,",
    "s8c_03": "Nếu ti-ti-ép-ti thấp nhưng ti-pi-âu-ti cao, chát-bót bắt đầu trả lời nhanh, nhưng chữ lại nhỏ giọt từng đoạn,",
    "s8c_04": "Khi đó, dù máy vẫn đang chạy, người dùng vẫn cảm thấy trải nghiệm không mượt,",

    # ----- C4 FORMULA -----
    "s8d_01": "Ghép hai phần này lại, ta có công thức trực quan cho độ trễ,",
    "s8d_02": "Tổng độ trễ xấp xỉ bằng ti-ti-ép-ti, cộng với ti-pi-âu-ti nhân số token đầu ra,",
    "s8d_03": "Nghĩa là độ trễ không chỉ phụ thuộc mô hình nhanh hay chậm, mà còn phụ thuộc rất mạnh vào câu trả lời dài bao nhiêu,",

    # ----- C5 BRIDGE + TDS -----
    "s8e_01": "Nhưng trong dịch vụ sờ-tri-ming, biết tổng độ trễ thôi vẫn chưa đủ,",
    "s8e_02": "Người dùng không đợi câu trả lời xong hẳn rồi mới đọc, họ đọc ngay trong lúc token đang chảy ra,",
    "s8e_03": "Vậy câu hỏi quan trọng hơn là, token đi ra có đủ nhanh để người ta đọc một cách tự nhiên không,",
    "s8e_04": "Tốc độ hệ thống đưa token ra cho người dùng được gọi là tốc độ giao token tối thiểu, gọi tắt là ti-đi-ét,",
    "s8e_05": "Nếu token ra quá chậm, người dùng đọc hết phần hiện có rồi phải dừng lại chờ,",
    "s8e_06": "Và dù hệ thống vẫn đang sinh token, trải nghiệm vẫn bị coi là chậm,",

    # ----- C6 HUMAN AXIS (centerpiece) -----
    "s8f_01": "Để thấy ti-đi-ét quan trọng cỡ nào, ta đặt mọi thứ lên cùng một thước, tốc độ con người, tính bằng từ mỗi phút,",
    "s8f_02": "Về đọc, nhóm trẻ đọc khoảng hai trăm ba mươi sáu từ mỗi phút, nhóm lớn tuổi thì chậm hơn,",
    "s8f_03": "Về nói, tiếng Anh khoảng một trăm năm mươi, tiếng Tây Ban Nha tới hai trăm mười tám,",
    "s8f_04": "Token và từ không trùng nhau, nên đây không phải phép quy đổi chính xác,",
    "s8f_05": "Điểm chính là, con người có một dải tốc độ đọc và nghe tự nhiên,",
    "s8f_06": "Giờ đặt tốc độ đưa token của eo-eo-em lên cùng thước này,",
    "s8f_07": "Nếu nó nằm dưới dải con người, người dùng sẽ liên tục phải chờ, chữ khựng lại,",
    "s8f_08": "Còn với trợ lý giọng nói, bộ chuyển văn bản thành giọng nói không đủ nội dung để đọc liền, giọng bị ngắt quãng,",
    "s8f_09": "Chỉ khi tốc độ token vượt dải đó, trải nghiệm mới thật sự mượt,",
    "s8f_10": "Đó chính là ý nghĩa của tốc độ giao token tối thiểu,",

    # ----- C7 SYNTHESIS + TRANSITION -----
    "s8g_01": "Tóm lại, bốn khái niệm này gắn chặt với nhau,",
    "s8g_02": "Ti-ti-ép-ti là thời gian tới token đầu tiên, ti-pi-âu-ti là tốc độ mỗi token sau,",
    "s8g_03": "Tổng độ trễ phụ thuộc cả hai, cùng với số token đầu ra,",
    "s8g_04": "Còn ti-đi-ét nhìn từ phía người dùng, token có ra đủ nhanh để đọc hoặc nghe mượt không,",
    "s8g_05": "Ti-pi-âu-ti càng thấp thì token ra càng nhanh, ti-đi-ét càng cao, ngược lại ti-pi-âu-ti cao kéo cả trải nghiệm đi xuống,",
    "s8g_06": "Vì vậy, tối ưu độ trễ không chỉ là làm mô hình chạy nhanh hơn, mà là làm phản hồi xuất hiện đúng nhịp người dùng thấy mượt,",
    "s8g_07": "Nhưng để giữ được nhịp đó, hệ thống phải nhồi rất nhiều dữ liệu vào bộ nhớ gi-pi-iu, và đó là thách thức tiếp theo,",
}


async def gen(filename, text, retries=6):
    for attempt in range(retries):
        try:
            await edge_tts.Communicate(text=text, voice=VOICE).save(filename)
            print("Đã tạo:", filename)
            return True
        except Exception as e:
            print(f"Lần {attempt + 1} lỗi ({filename}): {e}")
            if attempt < retries - 1:
                await asyncio.sleep(3)
    print("[BỎ QUA]", filename)
    return False


async def main():
    failed = []
    for sid, text in sentences.items():
        if not await gen(f"voice/{sid}.mp3", text):
            failed.append(sid)
    print("LỖI:", failed if failed else "không có")


if __name__ == "__main__":
    asyncio.run(main())
