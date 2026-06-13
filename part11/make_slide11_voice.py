import asyncio
import edge_tts
import os

# ============================================================
# VOICE SLIDE 11 — Hardware Compatibility & Acceleration (5 cảnh), TÁCH TỪNG CÂU.
#   PYTHONUTF8=1 python make_slide11_voice.py
# Phiên âm: NVIDIA->en-vi-đi-a, AMD->ây-em-đi, TPU->ti-pi-iu, GPU->gi-pi-iu, CPU->xi-pi-iu,
#   CUDA->ku-đa, ROCm->rốc-em, Vulkan->vun-can, OpenCL->âu-pừn-xi-eo, DirectX->đai-rếch-ích,
#   SYCL->sai-cồ, kernel->ke-nồ, backend->béc-en, edge->ét, LLM->eo-eo-em, runtime->ran-tham,
#   batch->bát. Dấu . ? -> , để câu liền mạch.
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
os.makedirs("voice", exist_ok=True)

sentences = {
    # ----- C1 BRIDGE -----
    "s11a_01": "Thách thức thứ tư là khả năng tương thích và tăng tốc phần cứng,",
    "s11a_02": "Trong môi trường nghiên cứu, ta thường mặc định mô hình chạy trên một gi-pi-iu en-vi-đi-a thật mạnh trong trung tâm dữ liệu,",
    "s11a_03": "Nhưng khi đưa vào thực tế, một câu hỏi lập tức xuất hiện, liệu cùng một cách tối ưu có chạy tốt trên mọi loại thiết bị không,",

    # ----- C2 BẢN ĐỒ PHẦN CỨNG -----
    "s11b_01": "Trên thực tế eo-eo-em có thể được triển khai ở rất nhiều nơi,",
    "s11b_02": "Ở cloud hay trung tâm dữ liệu, hệ thống có thể dùng gi-pi-iu en-vi-đi-a, gi-pi-iu ây-em-đi, hoặc ti-pi-iu,",
    "s11b_03": "Ở máy cá nhân, mô hình có thể chạy trên xi-pi-iu hoặc card đồ họa phổ thông,",
    "s11b_04": "Còn trên điện thoại và thiết bị ét, nó phải chạy trong điều kiện bộ nhớ, năng lượng và sức tính toán hạn chế hơn nhiều,",

    # ----- C3 HỆ SINH THÁI / RUNTIME -----
    "s11c_01": "Và mỗi loại phần cứng lại đi kèm một hệ sinh thái riêng,",
    "s11c_02": "En-vi-đi-a thường gắn với ku-đa, ây-em-đi có rốc-em,",
    "s11c_03": "Một số môi trường lại dùng vun-can, âu-pừn-xi-eo, đai-rếch-ích hay sai-cồ,",
    "s11c_04": "Các bộ tăng tốc chuyên dụng thì có ran-tham và trình biên dịch riêng,",
    "s11c_05": "Nói cách khác, không có một mẫu số chung duy nhất,",

    # ----- C4 CENTERPIECE -----
    "s11d_01": "Và đây là điểm mấu chốt, một kỹ thuật tối ưu không nhất thiết hoạt động tốt trên mọi phần cứng,",
    "s11d_02": "Một ke-nồ được tối ưu rất khéo cho gi-pi-iu en-vi-đi-a có thể không chạy được, hoặc chạy rất kém, trên gi-pi-iu ây-em-đi,",
    "s11d_03": "Một phương pháp hợp với trung tâm dữ liệu có thể hoàn toàn không hợp với điện thoại,",
    "s11d_04": "Và một chiến lược tăng bát để tận dụng gi-pi-iu có thể bất khả thi trên thiết bị ét, đơn giản vì không đủ bộ nhớ,",
    "s11d_05": "Cùng một ý tưởng, nơi thì chạy mượt, nơi cần chỉnh sửa, nơi thì chịu thua,",

    # ----- C5 OUTRO -> TRADE-OFF -----
    "s11e_01": "Vì vậy, phục vụ eo-eo-em không chỉ là bài toán thuật toán, mà là bài toán hệ thống, dùng đúng phần cứng, đúng béc-en cho từng môi trường,",
    "s11e_02": "Cốt lõi của cả thách thức này là sự không đồng nhất, từ máy chủ mạnh đến thiết bị người dùng cuối,",
    "s11e_03": "Nhưng giả sử ta đã lo xong cả độ trễ, bộ nhớ, thông lượng và phần cứng, vẫn còn một câu hỏi cuối,",
    "s11e_04": "Làm nhanh hơn hoặc rẻ hơn, liệu chất lượng có còn giữ được không,",
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
