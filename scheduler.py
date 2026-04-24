# scheduler.py - SINGLETON PATTERN

import threading
from apscheduler.schedulers.background import BackgroundScheduler
from email_service import send_daily_email
import time
from template_method import daily_processor

class NewsScheduler:
    """=== SINGLETON PATTERN ==="""
    _instance = None          # Lưu instance duy nhất
    _lock = threading.Lock()  # Đảm bảo thread-safe
    _is_running = False

    def __new__(cls):
        """Phương thức tạo instance - chỉ cho phép tạo 1 lần"""
        if cls._instance is None:
            with cls._lock:                    # Khóa để tránh race condition
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.scheduler = BackgroundScheduler()
        return cls._instance                   # Luôn trả về cùng 1 instance

    def start(self):
        """Khởi động scheduler (chỉ chạy 1 lần)"""
        if self._is_running:
            print("✅ Scheduler đã chạy rồi, bỏ qua...")
            return

        self.scheduler.add_job(daily_job, 'cron', hour=7, minute=30)
        self.scheduler.add_job(daily_job, 'cron', hour=19, minute=30)
        self.scheduler.start()
        self._is_running = True
        print("✅ Singleton Scheduler đã khởi động thành công!")

# Hàm daily_job (giữ để app.py import được)
def daily_job():
    print("Bắt đầu crawl và gửi tin nóng...")
    daily_processor.process()          # ← Dùng Template Method
    print("Hoàn thành gửi tin hôm nay!")

# Tạo instance Singleton (chỉ tạo 1 lần duy nhất)
scheduler = NewsScheduler()