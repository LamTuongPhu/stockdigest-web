# bot.py – CHẠY NGON LÀNH TRÊN PYTHON 3.13 + WINDOWS + python-telegram-bot 22.x
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from db import init_db, add_user, set_watchlist, get_watchlist

# DÒNG QUAN TRỌNG NHẤT: Fix lỗi "event loop is already running" trên Windows + IDE
nest_asyncio.apply()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_user(chat_id)
    await update.message.reply_text(
        "Chào mừng đến StockDigest!\n\n"
        "Tin chứng khoán tóm tắt siêu dễ hiểu cho F0\n\n"
        "Dùng lệnh:\n"
        "/watch VCB HPG AAA → theo dõi mã\n"
        "/list → xem danh sách\n"
        "Tin sẽ tự động gửi 8h sáng & 8h tối"
    )


async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Ví dụ: /watch VCB HPG AAA")
        return
    chat_id = update.effective_chat.id
    set_watchlist(chat_id, context.args)
    await update.message.reply_text(f"Đã thêm: {', '.join([c.upper() for c in context.args])}")


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    codes = get_watchlist(chat_id)
    if codes:
        await update.message.reply_text("Bạn đang theo dõi: " + ", ".join(codes))
    else:
        await update.message.reply_text("Chưa theo dõi mã nào. Gõ /watch ...")


async def main():
    init_db()
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("list", list_cmd))

    print("Bot đang chạy... Nhấn Ctrl+C để dừng")
    await app.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    from config import TELEGRAM_TOKEN

    # Fix event loop cho Windows + Jupyter/PyCharm
    print("Bot đang khởi động...")
    asyncio.run(main())