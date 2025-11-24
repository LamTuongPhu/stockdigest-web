# db.py
import sqlite3
import os

# Đường dẫn database (sẽ tự tạo thư mục data nếu chưa có)
DB_PATH = "data/stockdigest.db"


def init_db():
    """Tạo database và các bảng nếu chưa tồn tại"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Bảng người dùng: chat_id + danh sách mã theo dõi
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (chat_id INTEGER PRIMARY KEY, watchlist TEXT)''')

    # Bảng tin đã gửi (tránh gửi trùng)
    c.execute('''CREATE TABLE IF NOT EXISTS sent_news
                 (url TEXT PRIMARY KEY)''')

    conn.commit()
    conn.close()


def get_all_users():
    """Lấy danh sách tất cả user + watchlist của họ"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chat_id, watchlist FROM users")
    data = c.fetchall()
    conn.close()
    return data


def add_user(chat_id):
    """Thêm user mới (khi họ /start lần đầu)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (chat_id, watchlist) VALUES (?, ?)", (chat_id, ""))
    conn.commit()
    conn.close()


def set_watchlist(chat_id, codes):
    """Cập nhật danh sách mã theo dõi – chuẩn hóa IN HOA"""
    codes_str = ",".join([c.strip().upper() for c in codes if c.strip()])
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET watchlist = ? WHERE chat_id = ?", (codes_str, chat_id))
    conn.commit()
    conn.close()


def get_watchlist(chat_id):
    """Lấy danh sách mã mà user đang theo dõi"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT watchlist FROM users WHERE chat_id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0]:
        return [code.strip() for code in row[0].split(",")]
    return []


def was_sent(url):
    """Kiểm tra tin này đã gửi chưa"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM sent_news WHERE url = ?", (url,))
    exists = c.fetchone()
    conn.close()
    return bool(exists)


def mark_as_sent(url):
    """Đánh dấu tin đã được gửi để không gửi lại"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO sent_news (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()