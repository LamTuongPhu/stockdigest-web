# force_send.py – GỬI TIN THỦ CÔNG ĐỂ TEST
from telegram import Bot
from config import TELEGRAM_TOKEN
import asyncio


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    chat_id = 878601042  # ← SỬA DÒNG NÀY

    await bot.send_message(chat_id=chat_id,
                           text="TEST THÀNH CÔNG! StockDigest đã chạy 100%!!!\nTin sẽ về ào ào từ bây giờ!")
    print("Đã gửi tin test thành công!")


if __name__ == "__main__":
    asyncio.run(main())