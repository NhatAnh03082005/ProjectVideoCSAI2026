import asyncio
import edge_tts
import os

VOICE = "vi-VN-NamMinhNeural"

os.makedirs("voice", exist_ok=True)

segments = [
    (
        "p3_03_01_01_intro.mp3",
        """
        Nhóm cuối cùng trong an-gô-rít-mic in-nô-vây-sần là mô-đồl com-press-sần,
        tức là nén mô hình.
        """,
    ),
    (
        "p3_03_01_02_goal.mp3",
        """
        Mục tiêu rất rõ ràng:
        làm mô hình nhỏ hơn, nhẹ hơn, rẻ hơn,
        để in-fờ-rần nhanh hơn và dễ triển khai hơn.
        """,
    ),
    (
        "p3_03_01_04_focus.mp3",
        """
        Trong phần an-gô-rít-mic in-nô-vây-sần,
        mình sẽ tập trung vào hai kỹ thuật chính:
        nô-lịch đis-ti-lây-sần,
        và nét-quớc pru-ning.
        """,
    ),
]

async def generate_audio(filename, text, retries=3):
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text=text, voice=VOICE)
            await communicate.save(filename)
            print("Đã tạo:", filename)
            return
        except Exception as e:
            print(f"Lần {attempt + 1} thất bại ({filename}): {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2)
            else:
                raise


async def main():
    for filename, text in segments:
        await generate_audio(filename, text)

    print("Xong voice phần 3!")


if __name__ == "__main__":
    asyncio.run(main())