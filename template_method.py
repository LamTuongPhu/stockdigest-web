# template_method.py - TEMPLATE METHOD PATTERN
from abc import ABC, abstractmethod

# Import các module đã có sẵn trong dự án
from crawler.cafef import crawl_news
from ai_summarizer import summarize
from email_service import send_daily_email


class NewsProcessor(ABC):
    """=== TEMPLATE METHOD PATTERN ===
    Định nghĩa khung quy trình xử lý tin (skeleton algorithm)
    Subclass chỉ cần override các bước cụ thể (_crawl_news, _notify)"""

    def process(self, watchlist: list = None):
        """Template Method - KHÔNG được override (giống Run() trong Bài 3 PDF)"""
        print("🚀 [Template Method] Bắt đầu quy trình xử lý tin chứng khoán...")

        articles = self._crawl_news()                    # Bước 1
        processed = self._summarize_and_filter(articles, watchlist or [])  # Bước 2 (hook)
        self._notify(processed)                          # Bước 3

        return processed                                 # Trả về cho web API dùng

    @abstractmethod
    def _crawl_news(self):
        """Primitive Operation 1 - Phải override"""
        pass

    def _summarize_and_filter(self, articles, watchlist):
        """Hook method - Có thể override nếu cần thay đổi logic tóm tắt"""
        result = []
        for article in articles[:30]:
            summary = summarize(article['title'], article['url'])
            codes = article.get('codes', [])
            matched = [c for c in codes if c in watchlist]
            is_hot = len(matched) > 0

            result.append({
                'title': article['title'],
                'summary': summary,
                'url': article['url'],
                'codes': codes,
                'is_hot': is_hot,
                'matched_codes': matched
            })
        return result

    @abstractmethod
    def _notify(self, processed):
        """Primitive Operation 2 - Phải override"""
        pass


# ==================== CONCRETE CLASS ====================

class DailyEmailProcessor(NewsProcessor):
    """Chế độ gửi email sáng/tối (dùng trong scheduler)"""
    def _crawl_news(self):
        return crawl_news()

    def _notify(self, processed):
        print("📧 [Template Method] Gửi email tin nóng hàng ngày")
        send_daily_email()          # Gọi hàm cũ của bạn


class WebNewsProcessor(NewsProcessor):
    """Chế độ web realtime (dùng trong /api/news)"""
    def _crawl_news(self):
        return crawl_news()

    def _notify(self, processed):
        print("🌐 [Template Method] Cập nhật tin cho giao diện web")
        # Observer vẫn chạy trong Facade (không gọi lại để tránh circular import)


# ==================== INSTANCE SẴN ĐỂ DÙNG ====================
daily_processor = DailyEmailProcessor()
web_processor = WebNewsProcessor()