# adapter.py - ADAPTER PATTERN
from abc import ABC, abstractmethod
import google.generativeai as genai
from config import GEMINI_API_KEY

# ====================== TARGET INTERFACE (chuẩn chung) ======================
class AISummarizer(ABC):
    @abstractmethod
    def summarize(self, title: str, url: str) -> str:
        pass

# ====================== ADAPTEE (Gemini cũ) ======================
class GeminiAdaptee:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, title: str) -> str:
        """Cách cũ của Gemini"""
        for attempt in range(3):
            try:
                prompt = f"Hãy tóm tắt siêu ngắn gọn bằng tiếng Việt: {title}"
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except:
                pass
        return title + " (tóm tắt tạm thời)"

# ====================== ADAPTER ======================
class GeminiAdapter(AISummarizer):
    """Adapter chuyển đổi GeminiAdaptee thành interface chung"""
    def __init__(self):
        self.adaptee = GeminiAdaptee()

    def summarize(self, title: str, url: str) -> str:
        result = self.adaptee.generate(title)
        return f"🔄 [Adapter] {result}"