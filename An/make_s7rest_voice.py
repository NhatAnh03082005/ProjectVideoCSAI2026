import asyncio
import edge_tts
import os

# ============================================================
# VOICE 7B–7E — TÁCH TỪNG CÂU (đồng bộ "nói tới đâu hiện tới đó").
#   python make_s7rest_voice.py
# Phiên âm: OOM -> âu-âu-em, batch -> bát. Còn lại xem make_slide7_voice.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"
os.makedirs("voice", exist_ok=True)

sentences = {
    # ----- 7B MEMORY (làm kĩ) -----
    "s7b_01": "Một mô hình ngôn ngữ lớn chiếm gần hết bộ nhớ gi-pi-iu chỉ để chứa trọng số,",
    "s7b_02": "Phần trọng số này là cố định, nằm yên ở đáy bộ nhớ,",
    "s7b_03": "Nhưng khi phục vụ, mỗi người dùng lại sinh thêm một phần gọi là ca-vi kétsh,",
    "s7b_04": "Ca-vi kétsh lưu lại key và value của từng token đã xử lý,",
    "s7b_05": "Cứ thêm một người dùng, hoặc hội thoại càng dài, phần này càng dâng cao,",
    "s7b_06": "Nó phình lên gần như tuyến tính theo tổng số token,",
    "s7b_07": "Đến một lúc, bộ nhớ chạm ngưỡng tràn, gọi là âu-âu-em,",
    "s7b_08": "Khi đó hệ thống hết chỗ, và buộc phải từ chối bớt yêu cầu,",
    "s7b_09": "Giải quyết xong bài toán bộ nhớ, thách thức tiếp theo là phải phục vụ thật nhiều người cùng một lúc, mà không ai phải chờ quá lâu,",

    # ----- 7C THROUGHPUT (vừa-kĩ) -----
    "s7c_01": "Một hệ thống thật phải phục vụ hàng nghìn yêu cầu cùng lúc,",
    "s7c_02": "Để tận dụng gi-pi-iu, ta gom nhiều yêu cầu thành một loạt, gọi là bát,",
    "s7c_03": "Nhưng các yêu cầu dài ngắn khác nhau, và kết thúc lệch nhau,",
    "s7c_04": "Yêu cầu ngắn xong sớm vẫn phải chờ yêu cầu dài nhất trong loạt,",
    "s7c_05": "Chỗ chờ đó tạo ra những ô trống bị bỏ phí trong gi-pi-iu,",
    "s7c_06": "Xếp loạt khéo hơn để lấp đầy ô trống, số token mỗi giây tăng vọt,",
    "s7c_07": "Đó là bài toán thư-ru-pút, và dù tối ưu khéo đến đâu, tất cả vẫn phải chạy được trên phần cứng thực tế,",

    # ----- 7D HARDWARE (ngắn) -----
    "s7d_01": "Cùng một mô hình có thể chạy trên nhiều loại phần cứng khác nhau,",
    "s7d_02": "Gi-pi-iu en-vi-đia, ây-em-đi, ti-pi-iu, xi-pi-iu, hay cả điện thoại,",
    "s7d_03": "Nhưng mỗi nền tảng là một ổ cắm riêng, với răn-tham riêng,",
    "s7d_04": "Muốn chạy được, thường phải biên dịch và tối ưu lại cho từng nơi,",
    "s7d_05": "Và để vừa chạy nhanh trên mọi phần cứng vừa tiết kiệm, ta thường phải nén mô hình, dẫn tới một sự đánh đổi,",

    # ----- 7E TRADEOFF (vừa) -----
    "s7e_01": "Có nhiều kỹ thuật giúp mô hình chạy nhanh hơn và rẻ hơn,",
    "s7e_02": "Như lượng tử hóa, cắt tỉa, hay chưng cất mô hình,",
    "s7e_03": "Nhưng gần như không có bữa trưa miễn phí ở đây,",
    "s7e_04": "Mỗi lần nén để nhanh và rẻ, chất lượng đầu ra lại giảm đi,",
    "s7e_05": "Ví dụ độ chính xác có thể tụt từ chín mươi hai, xuống tám mươi tám phần trăm,",
    "s7e_06": "Năm thách thức đó, độ trễ, bộ nhớ, thư-ru-pút, phần cứng, và đánh đổi, hợp lại thành bức tranh đầy đủ của eo-eo-em sơ-ving,",
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
