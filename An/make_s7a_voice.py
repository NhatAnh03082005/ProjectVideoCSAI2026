import asyncio
import edge_tts
import os

# ============================================================
# VOICE 7A — TÁCH TỪNG CÂU để đồng bộ "nói tới đâu, hiện tới đó".
# Mỗi câu = 1 file mp3 -> scene phát lần lượt, hiệu ứng khớp từng câu.
#   python make_s7a_voice.py
# Quy tắc phiên âm + đổi . ? thành , : xem make_slide7_voice.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
os.makedirs("voice", exist_ok=True)

# (id, câu). id dùng làm tên file: voice/s7a_<id>.mp3
sentences = [
    ("01", "Hãy tưởng tượng bạn hỏi chát-bót, và màn hình cứ im lặng suốt mấy giây mới hiện chữ,"),
    ("02", "Khoảng lặng đó chính là độ trễ, thứ người dùng cảm nhận đầu tiên,"),
    ("03", "Nhưng độ trễ không phải một con số duy nhất, mà gồm hai phần tách biệt,"),
    ("04", "Thứ nhất là ti-ti-ép-ti, thời gian để có được token đầu tiên,"),
    ("05", "Nó phụ thuộc độ dài pờ-rom và bước tính toán ban đầu, trước khi máy kịp trả lời,"),
    ("06", "Thứ hai là ti-pi-âu-ti, thời gian sinh ra mỗi token tiếp theo,"),
    ("07", "Chính phần này quyết định cảm giác máy gõ chữ nhanh hay chậm,"),
    ("08", "Ví dụ bạn chờ tám giây mới thấy chữ đầu, rồi mỗi chữ sau chỉ mất khoảng năm mươi mi-li-giây,"),
    ("09", "Vậy tổng độ trễ bằng ti-ti-ép-ti, cộng với ti-pi-âu-ti nhân số token,"),
    ("10", "Nhưng độ trễ mới chỉ là thách thức đầu tiên, thứ quyết định ta có phục vụ nổi nhiều người hay không, lại nằm ở bộ nhớ,"),
]


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
    for sid, text in sentences:
        if not await gen(f"voice/s7a_{sid}.mp3", text):
            failed.append(sid)
    print("LỖI:", failed if failed else "không có")


if __name__ == "__main__":
    asyncio.run(main())
