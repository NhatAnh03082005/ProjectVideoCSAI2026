import asyncio
import edge_tts
import os

# ============================================================
# VOICE SLIDE 9 — Memory / KV cache (7 cảnh), TÁCH TỪNG CÂU.
#   python make_slide9_voice.py
# Phiên âm (xem tts-phonetic-rule): KV cache->ca-vi kétsh, GPU->gi-pi-iu,
#   A100->ây một trăm, GPT-3->ji-pi-ti ba, OPT-30B->âu-pi-ti ba mươi bi,
#   OOM->âu-âu-em, attention->ờ-ten-sần, byte->bai, batch->bát, LLM->eo-eo-em,
#   serving->sơ-vinh, decode->đi-cốt, chatbot->chát-bót, prompt->pờ-rom.
#   Dấu . ? -> , để câu liền mạch.
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
os.makedirs("voice", exist_ok=True)

sentences = {
    # ----- C1 HOOK -----
    "s9a_01": "Thách thức thứ hai là bộ nhớ, và đây là chỗ khiến nhiều người bất ngờ nhất,",
    "s9a_02": "Hãy bắt đầu bằng một con số gây sốc, để phục vụ mô hình ji-pi-ti ba với một trăm bảy mươi lăm tỷ tham số, ở độ chính xác một nửa, ta cần ít nhất mười gi-pi-iu ây một trăm loại bốn mươi gi-ga-bai,",
    "s9a_03": "Và xin nhấn mạnh, đó mới chỉ là để chứa mô hình trong bộ nhớ, chưa hề sinh ra một token nào,",
    "s9a_04": "Ngay cả gi-pi-iu mạnh nhất cũng không một mình gánh nổi, phải mười chiếc ghép lại,",
    "s9a_05": "Để dễ hình dung, ba trăm năm mươi gi-ga-bai trọng số ấy tương đương gom card đồ họa của khoảng mười lăm chiếc pi-xi cao cấp gắn a-rờ-ti-ex bốn không chín không, mà còn phải là bộ nhớ siêu nhanh nối liền nhau, thứ một dàn pi-xi rời rạc không làm được,",

    # ----- C2 WEIGHTS -----
    "s9b_01": "Vì sao lại lớn đến vậy, mỗi tham số ở độ chính xác một nửa chiếm hai bai,",
    "s9b_02": "Một trăm bảy mươi lăm tỷ tham số nhân hai bai là khoảng ba trăm năm mươi gi-ga-bai,",
    "s9b_03": "Chia cho bốn mươi gi-ga-bai mỗi gi-pi-iu, ta cần khoảng chín ô để chứa hết, cộng thêm phần đệm cho vận hành, nên thực tế cần ít nhất mười,",
    "s9b_04": "Phần này gọi là trọng số mô hình, điểm quan trọng, nó là phần cố định, nạp một lần rồi nằm yên trong bộ nhớ suốt quá trình phục vụ, không phình thêm,",
    "s9b_05": "Nếu chỉ có trọng số thôi thì bài toán bộ nhớ còn tương đối dễ, rắc rối nằm ở chỗ, bên cạnh nó còn một thành phần thứ hai, biến động hơn nhiều,",

    # ----- C3 KV CACHE: WHY -----
    "s9c_01": "Thành phần thứ hai là ca-vi kétsh,",
    "s9c_02": "Để hiểu nó, hãy nhớ lại cách eo-eo-em sinh chữ, mỗi token mới được tạo ra đều phải chú ý tới tất cả những token đứng trước nó trong câu, thông qua cơ chế ờ-ten-sần,",
    "s9c_03": "Nếu ở mỗi bước, mô hình đều tính lại khóa và giá trị cho toàn bộ token cũ, thì càng về sau càng tốn, câu càng dài, mỗi bước lại càng nặng, lặp đi lặp lại một cách rất lãng phí,",
    "s9c_04": "Để tránh điều đó, hệ thống lưu lại khóa và giá trị của những token đã xử lý vào một vùng nhớ riêng, gọi là ca-vi kétsh,",
    "s9c_05": "Nhờ nó, mỗi bước sinh token chỉ cần tính cho đúng một token mới, rồi đọc phần cũ ra từ bộ đệm,",
    "s9c_06": "Ca-vi kétsh giúp đi-cốt nhanh hơn hẳn, nhưng cái giá phải trả chính là bộ nhớ,",

    # ----- C4 KV GROWS LINEAR -----
    "s9d_01": "Vậy ca-vi kétsh lớn cỡ nào, nó lưu một cặp khóa và giá trị cho mỗi token, ở mỗi lớp, và mỗi đầu chú ý của mô hình,",
    "s9d_02": "Cứ thêm một token vào hội thoại, hoặc thêm một người dùng mới, kho này lại lớn thêm,",
    "s9d_03": "Ở đây có một điểm phải nói cho thật chính xác, ca-vi kétsh tăng tuyến tính theo độ dài chuỗi và số yêu cầu, chứ không phải theo cấp số nhân,",
    "s9d_04": "Nó là một đường thẳng đi lên đều, không phải đường cong dựng đứng,",
    "s9d_05": "Nhưng vì mô hình hiện đại có rất nhiều lớp, rất nhiều đầu, lại phục vụ nhiều người cùng một lúc, nên dù chỉ tuyến tính, tổng dung lượng vẫn phình lên rất nhanh và rất lớn,",

    # ----- C5 CENTERPIECE: OPT-30B -----
    "s9e_01": "Để thấy nó lớn tới mức nào, hãy nhìn mô hình âu-pi-ti ba mươi bi,",
    "s9e_02": "Trọng số của nó khoảng sáu mươi gi-ga-bai, chính là đường nét đứt nằm ngang trong hình,",
    "s9e_03": "Bây giờ ta tăng độ dài chuỗi từ vài trăm lên vài nghìn token, hoặc tăng số yêu cầu trong một bát, cột ca-vi kétsh mọc cao dần, đều đặn,",
    "s9e_04": "Đến mức vài nghìn token, nó có thể chạm khoảng hai trăm ba mươi gi-ga-bai, vượt qua vạch sáu mươi gi-ga-bai tới gần bốn lần,",
    "s9e_05": "Hãy để ý khoảnh khắc này, phần phát sinh trong lúc phục vụ đã ngốn bộ nhớ nhiều hơn cả bản thân mô hình,",
    "s9e_06": "Và đây không phải trường hợp hiếm gặp, nó xảy ra ngay khi ta phục vụ những hội thoại dài cho nhiều người cùng lúc,",

    # ----- C6 OOM -----
    "s9f_01": "Và đây chính là nút thắt, hãy hình dung bộ nhớ gi-pi-iu như một chiếc cốc có dung tích cố định,",
    "s9f_02": "Đáy cốc là trọng số mô hình, màu xanh, đã chiếm sẵn một phần,",
    "s9f_03": "Một dải mỏng nữa dành cho các vùng đệm tạm thời, phục vụ tính toán,",
    "s9f_04": "Phần còn lại mới để cho ca-vi kétsh,",
    "s9f_05": "Giờ hãy tưởng tượng một chát-bót hỗ trợ đọc tài liệu, mỗi người dùng dán vào một pờ-rom dài hàng chục nghìn token, và hệ thống phải phục vụ nhiều người như vậy cùng lúc,",
    "s9f_06": "Mỗi yêu cầu một vùng ca-vi kétsh riêng, màu vàng, dâng lên song song, mực nước trong cốc cứ thế đầy dần,",
    "s9f_07": "Đến khi chạm vạch đỏ, hệ thống hết chỗ, gặp lỗi tràn bộ nhớ âu-âu-em, và buộc phải từ chối bớt yêu cầu hoặc cắt ngắn ngữ cảnh,",
    "s9f_08": "Điều đáng nói là, ngay tại lúc đó, gi-pi-iu vẫn còn thừa sức tính toán, nó bị chặn lại không phải vì chậm, mà vì đã hết bộ nhớ,",

    # ----- C7 SYNTHESIS + TRANSITION -----
    "s9g_01": "Tóm lại, bộ nhớ trong eo-eo-em sơ-vinh đến từ ba nguồn, trọng số mô hình cố định, các vùng đệm tạm thời, và ca-vi kétsh phát sinh theo từng token, từng yêu cầu,",
    "s9g_02": "Trong đó, ca-vi kétsh là phần nguy hiểm nhất, nó tăng tuyến tính, nhưng đủ sức vượt cả kích thước mô hình,",
    "s9g_03": "Chính vì vậy, khi đánh giá một hệ thống eo-eo-em, ta không thể chỉ hỏi mô hình chạy nhanh hay chậm, mà còn phải hỏi gi-pi-iu có đủ bộ nhớ để chứa cùng lúc cả mô hình, ca-vi kétsh và các vùng đệm hay không,",
    "s9g_04": "Bộ nhớ, chứ không phải tốc độ tính toán, mới thường là trần giới hạn thật sự của eo-eo-em sơ-vinh,",
    "s9g_05": "Và chính giới hạn bộ nhớ này quyết định ta gom được bao nhiêu yêu cầu cùng lúc, dẫn thẳng tới thách thức tiếp theo, thông lượng và khả năng mở rộng,",
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
