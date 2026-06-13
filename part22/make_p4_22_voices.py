import asyncio
import os

import edge_tts


# ============================================================
# PART 4 - SCENE 22: FRAMEWORKS AND CASE STUDY
#
# Chay:
#   py make_p4_22_voices.py
# ============================================================

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)


segments = [
    (
        "voice/p4_22_01_intro.mp3",
        """
        Sau khi đi qua quăn-ti-dây-sần, pa-ra-leo còm-piu-tây-sần, me-mơ-ti ma-nịch-mần, sờ-ke-chu-linh và cơ-nồ óp-tơ-mi-zây-sần, ta thấy, eo-eo-em ,serving không thể chỉ dựa vào một mẹo đơn lẻ,
        Các kỹ thuật này được đóng gói vào những phờ-rêm-quấc serving,
        phờ-rêm-quấc giống như một dàn nhạc: me-mơ-ri ma-nan-chờ, sờ-ke-chu-lờ, cơ-nồ bách-èn, và đì-chi-biu-tịt rân-tam
        phải chơi cùng nhịp.
        """,
    ),
    (
        "voice/p4_22_02_vllm.mp3",
        """
        vi e lờ em ,nổi bật vì giải trực diện bài toán kây-vi cát bằng pây ờ-ten-sần, kết hợp với cần-ti-niu-ợt bát-chinh để phục vụ nhiều rùy-quét đồng thời.
        Nếu quấc-loát có nhiều người dùng và mục tiêu là thờ-ru-pút cao, vi e lờ em thường là lựa chọn rất mạnh,
        Điểm cần nhớ không phải là tên vi e lờ em,
        mà là bài học: quản lý kây-vi cát tốt có thể thay đổi hiệu năng serving.
        """,

    ),
    (
        "voice/p4_22_03_tensorrt_deepspeed.mp3",
        """
        Ten-sờ a-ti, e lờ em, phù hợp khi hệ thống chạy sâu trong hệ sinh thái en-bi-đi-a
        và muốn tận dụng cơ-nồ, ten-sờ co, troai-tần In-ti-grây-shần, và các tối ưu phục vụ pờ-rờ-đấc-sần,
        Đíp-sờ-pít in-phơ-rần lại quen thuộc trong các bài toán multi gi-pi-diu hoặc mul-ti nốt,nơi pe-ra-leo-li-zầm và óp-loát-đinh đóng vai trò quan trọng,
        Hai phờ-rêm-quậc này nhắc ta rằng phần cứng và hạ tầng quyết định rất nhiều đến lựa chọn serving.
        """,
    ),
    (
        "voice/p4_22_04_other_frameworks.mp3",
        """
        Nếu gi-pi-diu me-mơ-ri hạn chế, các hướng như phléch-gen hoặc ze-rô in-phơ-rần nhấn mạnh óp-loát-đinh sang xi-pi-diu ram hoặc disk để chạy mô hình lớn hơn,
        Ti-gi-ai của Hấc-ginh Phây nổi bật ở khả năng tích hợp và triển khai thuận tiện trong hệ sinh thái Hấc-ginh Phây,
        lai e lờ em, tập trung vào quản lý Kây-vi cát ở mức token, còn em eo xi, e lờ em, hướng đến triển khai linh hoạt trên nhiều loại phần cứng.
        """,
    ),
    (
        "voice/p4_22_05_workload_choice.mp3",
        """
        Cách chọn phờ-rêm-quấc nên bắt đầu từ quấc-loát,
        Nếu nhiều rùy-quét đồng thời, hãy nhìn vào bát-chinh và Kây-vi cát.
        Nếu mo-đồ quá lớn so với gi-pi-diu, hãy nhìn vào pa-ra-leo-li-zầm hoặc óp-loát-đinh.
        Nếu lây-tần-xi từng rùy-quét là mục tiêu chính, hãy nhìn vào spéc-kiu-lây-tive đì-cốt-đinh và cơ-nồ tối ưu.
        Nếu cần chạy đa nền tảng, hãy nhìn vào cờm-pai-lờ và bách-èn sụp-pót.
        """,
    ),
    (
        "voice/p4_22_06_summary.mp3",
        """
        Tóm lại,
        phờ-rêm-quấc không phải chiếc đũa thần, Nó là một tập hợp các đánh đổi.
        vi e lờ em, mạnh về kây-vi cát và thờ-ru-pút, Ten-sờ a-ti, e lờ em mạnh khi bám sát en-vi-đi-a,
        phléch-gen hữu ích khi thiếu gi-pi-diu me-mơ-ri, Ti-gi-ai thuận tiện triển khai, em eo xi, e lờ em linh hoạt đa nền tảng.
        Không có lựa chọn tốt nhất cho mọi bài toán, chỉ có lựa chọn phù hợp nhất với quấc-loát của bạn.
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
    print("Done. Created all Part 22 voice files in ./voice")


if __name__ == "__main__":
    asyncio.run(main())
