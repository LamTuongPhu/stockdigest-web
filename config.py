# config.py
import os

# API Key
GEMINI_API_KEY = "AIzaSyChqfx0S8S4WDhIH2crvQ6iXn9t2ZGmYP8"
TELEGRAM_TOKEN = "8213709616:AAGeVFdODPvtNHmgt81JY9nD2egD8sceNcw"

# Đường dẫn database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # tự tạo thư mục data nếu chưa có
DB_PATH = os.path.join(DATA_DIR, "stockdigest.db")

# Các nguồn tin sẽ crawl
SOURCES = [
    "https://cafef.vn/chung-khoan.chn",
    "https://ndh.vn/chung-khoan",
    "https://vneconomy.vn/chung-khoan.htm",
]