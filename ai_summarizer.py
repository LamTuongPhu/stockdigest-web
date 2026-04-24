# ai_summarizer.py - STRATEGY + PROXY + DECORATOR + ADAPTER
from abc import ABC, abstractmethod
import time
from adapter import GeminiAdapter   # ← Adapter mới

# ====================== STRATEGY INTERFACE ======================
class SummarizerStrategy(ABC):
    @abstractmethod
    def summarize(self, title: str, url: str) -> str:
        pass

# ====================== CONCRETE STRATEGY (dùng Adapter) ======================
class GeminiStrategy(SummarizerStrategy):
    def __init__(self):
        self.adapter = GeminiAdapter()   # Sử dụng Adapter

    def summarize(self, title: str, url: str) -> str:
        return self.adapter.summarize(title, url)

# ====================== PROXY + DECORATOR (giữ nguyên) ======================
class SummarizerProxy(SummarizerStrategy):
    def __init__(self, strategy: SummarizerStrategy):
        self._strategy = strategy
        self._cache = {}

    def summarize(self, title: str, url: str) -> str:
        key = title + url
        if key in self._cache:
            print(f"✅ Proxy: Cache hit")
            return self._cache[key]
        result = self._strategy.summarize(title, url)
        self._cache[key] = result
        return result

class SummarizerDecorator(SummarizerStrategy):
    def __init__(self, wrapped: SummarizerStrategy):
        self._wrapped = wrapped

    def summarize(self, title: str, url: str) -> str:
        start = time.time()
        result = self._wrapped.summarize(title, url)
        duration = round(time.time() - start, 2)
        return f"⏱️ [{duration}s] 🔥 {result}"

# ====================== CONTEXT ======================
class SummarizerContext:
    def __init__(self, strategy: SummarizerStrategy):
        self._strategy = strategy

    def summarize(self, title: str, url: str) -> str:
        return self._strategy.summarize(title, url)

# ====================== SỬ DỤNG ======================
base = GeminiStrategy()
proxy = SummarizerProxy(base)
decorated = SummarizerDecorator(proxy)
summarizer = SummarizerContext(decorated)

def summarize(title: str, url: str) -> str:
    return summarizer.summarize(title, url)