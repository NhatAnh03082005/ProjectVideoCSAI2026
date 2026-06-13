import asyncio
import edge_tts
import os

# ============================================================
# TẠO FILE AUDIO CHO SLIDE 7 — VIGNETTE 5 YẾU TỐ (trừ Intro)
# Giọng nam tiếng Việt, dùng edge-tts.
#   python make_slide7_voice.py
#
# QUY TẮC VIẾT SCRIPT CHO TEXT-TO-SPEECH (giúp đọc mượt):
#   - Từ tiếng Anh -> phiên âm kiểu Việt có dấu gạch nối
#       LLM        -> eo-eo-em
#       serving    -> sơ-ving
#       model      -> mô-đồ
#       server     -> sơ-vờ
#       API        -> ây-pi-ai
#       prompt     -> pờ-rom
#       latency    -> lây-tân-xi
#       throughput -> thư-ru-pút
#       TTFT       -> ti-ti-ép-ti
#       TPOT       -> ti-pi-âu-ti
#       KV cache   -> ca-vi kétsh
#       GPU        -> gi-pi-iu
#       NVIDIA     -> en-vi-đia
#       AMD        -> ây-em-đi
#       TPU        -> ti-pi-iu
#       CPU        -> xi-pi-iu
#       runtime    -> răn-tham
#       output     -> ao-pút
#       accuracy   -> ác-kiu-ra-xi
#       efficiency -> i-phi-sần-xi
#       bottleneck -> bót-ờ-nếch
#       chatbot    -> chát-bót
#       CUDA       -> cu-đa
#       ROCm       -> rốc-em
#       millisecond-> mi-li-giây
#   - Dấu chấm (.) và dấu hỏi (?) -> dấu phẩy (,) để câu liền mạch, không ngắt cứng.
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        # 7A — LATENCY
        "voice/s7a_latency.mp3",
        """
        Hãy tưởng tượng bạn hỏi chát-bót và màn hình im lặng suốt mấy giây mới hiện chữ,
        Khoảng lặng đó chính là độ trễ — thứ người dùng cảm nhận đầu tiên,
        Nhưng độ trễ không phải một con số duy nhất, mà gồm hai phần tách biệt,
        Thứ nhất là ti-ti-ép-ti, thời gian tới token đầu tiên,
        nó phụ thuộc độ dài pờ-rom và bước tính toán ban đầu trước khi máy bắt đầu trả lời,
        Thứ hai là ti-pi-âu-ti, thời gian sinh ra mỗi token tiếp theo,
        chính phần này quyết định cảm giác máy gõ chữ nhanh hay chậm,
        Ví dụ bạn chờ tám giây mới thấy chữ đầu, rồi mỗi chữ sau mất khoảng năm mươi mi-li-giây,
        Vậy tổng độ trễ sẽ bằng ti-ti-ép-ti cộng với ti-pi-âu-ti nhân số token sinh ra,
        Đây là lý do lây-tân-xi sẽ được mổ xẻ kỹ ngay ở phần tiếp theo,
        """
    ),
    (
        # 7B — MEMORY / KV CACHE
        "voice/s7b_memory.mp3",
        """
        Mỗi mô hình lớn đã chiếm gần hết bộ nhớ gi-pi-iu chỉ để chứa trọng số,
        Nhưng đó mới chỉ là phần cố định, nằm yên một chỗ,
        Phần đáng lo hơn nằm ở ca-vi kétsh, bộ nhớ đệm lưu lại key và value của từng token đã sinh ra,
        Cứ thêm một người dùng mới, hoặc một cuộc hội thoại dài hơn,
        phần ca-vi kétsh lại phình lên gần như tuyến tính theo số token,
        Ví dụ chỉ riêng ca-vi kétsh, mỗi yêu cầu có thể ngốn thêm vài gi-ga-bai bộ nhớ,
        Đến lúc tổng bộ nhớ chạm ngưỡng tràn, hệ thống không còn chỗ trống,
        và buộc phải từ chối bớt yêu cầu, hoặc cắt ngắn ngữ cảnh đang xử lý,
        Chính vì vậy, bộ nhớ và kích thước mô hình là một nút thắt rất lớn của eo-eo-em sơ-ving,
        """
    ),
    (
        # 7C — THROUGHPUT
        "voice/s7c_throughput.mp3",
        """
        Một hệ thống thật phải phục vụ hàng trăm, hàng nghìn yêu cầu cùng một lúc,
        Để tận dụng tối đa gi-pi-iu, người ta gom nhiều yêu cầu lại thành một loạt rồi xử lý song song, gọi là bát,
        Nhưng vấn đề là các yêu cầu dài ngắn rất khác nhau và kết thúc lệch nhau,
        Yêu cầu ngắn đã xong từ lâu vẫn phải nằm chờ yêu cầu dài nhất trong loạt,
        tạo ra những ô trống bị bỏ phí ngay trong lưới xử lý,
        Khi xếp loạt khéo hơn và lấp đầy các ô trống đó,
        số token mỗi giây có thể nhảy từ khoảng một nghìn hai lên hơn ba nghìn,
        Gom yêu cầu sao cho gi-pi-iu gần như không nghỉ phút nào,
        chính là bài toán thư-ru-pút, hay khả năng mở rộng của cả hệ thống,
        """
    ),
    (
        # 7D — HARDWARE
        "voice/s7d_hardware.mp3",
        """
        Cùng một mô hình có thể chạy trên gi-pi-iu en-vi-đia, ây-em-đi, ti-pi-iu, xi-pi-iu hay cả điện thoại,
        Nghe thì rất linh hoạt, nhưng thực tế mỗi nền tảng lại là một ổ cắm riêng,
        Gi-pi-iu en-vi-đia dùng cu-đa, còn ây-em-đi lại dùng rốc-em,
        và ti-pi-iu thì cần một trình biên dịch hoàn toàn khác,
        Muốn mô hình chạy được, ta phải gắn thêm một lớp răn-tham phù hợp,
        đôi khi phải biên dịch và tối ưu lại gần như từ đầu cho từng nền tảng,
        Hơn nữa, hiệu năng trên mỗi nơi cũng chênh nhau rõ rệt,
        có chỗ chạy rất nhanh, có chỗ thì chỉ chạy được cho có,
        Vì vậy tương thích phần cứng không hề là viết một lần rồi chạy được mọi nơi,
        """
    ),
    (
        # 7E — ACCURACY–EFFICIENCY TRADE-OFF
        "voice/s7e_tradeoff.mp3",
        """
        Có rất nhiều kỹ thuật giúp mô hình chạy nhanh hơn và rẻ hơn,
        như lượng tử hóa, cắt tỉa tham số, hay chưng cất mô hình,
        Nhưng gần như không có bữa trưa miễn phí ở đây,
        Mỗi lần ta nén mô hình hoặc hạ độ chính xác của các con số,
        tốc độ và chi phí được cải thiện, nhưng chất lượng đầu ra lại nhích xuống,
        Ví dụ độ chính xác có thể tụt từ chín mươi hai phần trăm xuống còn tám mươi tám phần trăm,
        chỉ sau một bước nén để chạy nhanh hơn,
        Với một chát-bót giải trí thì mức đó có thể chấp nhận được,
        nhưng với y tế hay tài chính thì lại không,
        Vì vậy chọn điểm cân bằng giữa ác-kiu-ra-xi và i-phi-sần-xi luôn tùy vào từng bài toán cụ thể,
        """
    ),
    (
        # 7F — OUTRO
        "voice/s7f_outro.mp3",
        """
        Năm thách thức này chính là bản đồ bót-ờ-nếch của chúng ta,
        Hiểu rõ chúng, các kỹ thuật tối ưu ở phần sau sẽ trở nên có động cơ rõ ràng,
        Bắt đầu với cái người dùng cảm nhận đầu tiên — độ trễ,
        """
    ),
]


async def generate_audio(filename, text, retries=6):
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE)
            await communicate.save(filename)
            print("Đã tạo:", filename)
            return True
        except Exception as e:
            print(f"Lần {attempt + 1} thất bại ({filename}): {str(e)}")
            if attempt < retries - 1:
                await asyncio.sleep(3)  # backoff dài hơn để né throttle của edge-tts
    print(f"[BỎ QUA] Không thể tạo {filename} sau {retries} lần thử")
    return False


async def main():
    failed = []
    for filename, text in segments:
        ok = await generate_audio(filename, text)
        if not ok:
            failed.append(filename)
    if failed:
        print("Các file LỖI (chạy lại script để thử tiếp):", ", ".join(failed))
    else:
        print(f"Xong! Đã tạo {len(segments)} file audio trong thư mục voice.")


if __name__ == "__main__":
    asyncio.run(main())
