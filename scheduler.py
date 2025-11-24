

import asyncio
import sqlite3
from config import TELEGRAM_TOKEN, DB_PATH
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot
from db import init_db, was_sent, mark_as_sent
from crawler.cafef import crawl_news
from ai_summarizer import summarize

bot = Bot(token=TELEGRAM_TOKEN)


def get_active_chat_ids():
    """Lấy tất cả chat_id có watchlist (tức là đã /watch hoặc /start)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT DISTINCT chat_id FROM users WHERE watchlist IS NOT NULL AND trim(watchlist) != ''")
        rows = c.fetchall()
        conn.close()
        return [row[0] for row in rows] if rows else []
    except:
        return []


async def send_message(chat_id, text):
    try:
        await bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)
        print(f"   Đã gửi thành công đến {chat_id}")
    except Exception as e:
        print(f"   Lỗi gửi cho {chat_id}: {e}")


def daily_job():
    print("Bắt đầu crawl tin mới...")
    init_db()
    articles = crawl_news()
    print(f"→ Tìm được {len(articles)} tin nóng có mã ")

    active_chat_ids = get_active_chat_ids()
    if not active_chat_ids:
        print("   Chưa có người dùng nào /watch → không gửi tin")
        return

    for article in articles:
        if was_sent(article['url']):
            continue

        summary = summarize(article['title'], article['url'])
        print(f"Đang gửi tin: {summary.splitlines()[0][:80]}...")

        # Lấy watchlist của từng người dùng
        for chat_id in active_chat_ids:
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("SELECT watchlist FROM users WHERE chat_id = ?", (chat_id,))
                row = c.fetchone()
                conn.close()

                if not row or not row[0]:
                    continue
                watchlist = [code.strip() for code in row[0].split(",") if code.strip()]

                if any(code in article['codes'] for code in watchlist):
                    asyncio.run(send_message(chat_id, summary))
                    asyncio.run(asyncio.sleep(10))  # chống flood
            except Exception as e:
                print(f"   Lỗi xử lý user {chat_id}: {e}")

        mark_as_sent(article['url'])
    print("Hoàn thành gửi tin hôm nay!\n")


if __name__ == "__main__":
    init_db()

    scheduler = BlockingScheduler()
    scheduler.add_job(daily_job, 'cron', hour=8,  minute=0,  timezone="Asia/Ho_Chi_Minh")
    scheduler.add_job(daily_job, 'cron', hour=20, minute=0,  timezone="Asia/Ho_Chi_Minh")

    print("StockDigest Scheduler đang chạy – sẽ gửi tin lúc 8h sáng & 8h tối")
    print("Người dùng hiện tại sẽ nhận tin:", get_active_chat_ids() or "Chưa có ai")

    daily_job()  # chạy luôn lần đầu để test
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler đã dừng.")