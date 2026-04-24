# observer.py - OBSERVER PATTERN
from abc import ABC, abstractmethod

class Observer(ABC):
    """Interface của Observer Pattern"""
    @abstractmethod
    def update(self, news_list):
        pass

class ConsoleObserver(Observer):
    """Observer cụ thể: In ra console khi có tin nóng"""
    def update(self, news_list):
        hot_count = sum(1 for item in news_list if item.get('is_hot', False))
        if hot_count > 0:
            print(f"🛎️ Observer: Có {hot_count} tin nóng mới! Đang thông báo cho người dùng...")

class WebObserver(Observer):
    """Observer cụ thể: Có thể mở rộng để push realtime lên web (sau này)"""
    def update(self, news_list):
        hot_count = sum(1 for item in news_list if item.get('is_hot', False))
        if hot_count > 0:
            print(f"🌐 WebObserver: Đã cập nhật {hot_count} tin nóng lên giao diện web!")