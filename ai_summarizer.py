# ai_summarizer.py
import google.generativeai as genai
from config import GEMINI_API_KEY
import time

genai.configure(api_key=GEMINI_API_KEY)

# Model mới nhất, miễn phí, siêu nhanh
model = genai.GenerativeModel('gemini-2.5-flash-lite')


def summarize(title, url):
    prompt = f"Tóm tắt tin chứng khoán trong 1-2 câu cực dễ hiểu cho người mới, thêm emoji, chỉ dùng tiếng Việt:\n{title}"

    for _ in range(3):
        try:
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip() + "\n\n" + url
        except Exception as e:
            print(f"   Gemini lỗi (thử lại): {e}")
            time.sleep(2)

    # Fallback cuối cùng – vẫn gửi được tin
    return f"Tin nóng: {title}\n{url}"
