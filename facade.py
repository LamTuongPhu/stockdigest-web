# facade.py - FACADE PATTERN + OBSERVER PATTERN + TEMPLATE METHOD
from observer import ConsoleObserver, WebObserver
from template_method import web_processor   # ← Template Method cho web


class StockDigestFacade:
    """Facade + Subject của Observer Pattern"""

    def __init__(self):
        self._observers = []
        self.attach(ConsoleObserver())  # Mặc định attach console
        self.attach(WebObserver())      # Attach web observer

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, news_list):
        """Kích hoạt tất cả Observer"""
        for observer in self._observers:
            observer.update(news_list)

    def get_news(self, watchlist: list = None):
        """Lấy tin tức cho web (sử dụng Template Method)"""
        if watchlist is None:
            watchlist = []

        # 🔥 Sử dụng Template Method Pattern (WebNewsProcessor)
        result = web_processor.process(watchlist)

        # Observer
        self.notify(result)
        return result

    def send_daily_email(self):
        """ (daily email dùng DailyEmailProcessor trong scheduler)"""
        from email_service import send_daily_email
        send_daily_email()


# Instance duy nhất
facade = StockDigestFacade()