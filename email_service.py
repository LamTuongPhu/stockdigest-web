# email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from crawler.cafef import crawl_news
from ai_summarizer import summarize


GMAIL_USER = "lamtuongphu@gmail.com"
GMAIL_APP_PASSWORD = "uors htec fpjf bois"


def send_daily_email():
    # Đọc danh sách người đăng ký
    if not os.path.exists('subscribers.json'):
        print("Chưa có ai đăng ký email")
        return

    with open('subscribers.json', 'r', encoding='utf-8') as f:
        subscribers = json.load(f)

    # Crawl tin mới
    articles = crawl_news()[:60]
    all_hot_news = []

    for article in articles:
        title = article['title']
        url = article['url']
        codes = [c.upper() for c in article.get('codes', [])]
        try:
            summary = summarize(title, url)
        except:
            summary = title[:200] + "..."

        # Kiểm tra xem có mã nào trùng với người dùng không
        for sub in subscribers:
            user_codes = [c.upper() for c in sub.get('codes', [])]
            matched = [c for c in codes if c in user_codes]
            if matched and article not in all_hot_news:
                all_hot_news.append({
                    'title': title,
                    'summary': summary.replace('\n', '<br>'),
                    'url': url,
                    'matched': matched
                })

    if not all_hot_news:
        print("Hôm nay không có tin nóng nào")
        return

    # Tạo nội dung email đẹp
    html_body = """
    <h2 style="color:#d32f2f">StockDigest – Tin nóng chứng khoán hôm nay</h2>
    <p>Xin chào! Dưới đây là những tin quan trọng có mã bạn đang theo dõi:</p>
    <hr>
    """
    for item in all_hot_news[:10]:
        html_body += f"""
        <div style="margin:20px 0; padding:15px; border-left:5px solid #d32f2f; background:#fafafa;">
            <h3 style="color:#d32f2f; margin:0">{item['title']}</h3>
            <p><strong>Mã liên quan:</strong> {', '.join(item['matched'])}</p>
            <p>{item['summary']}</p>
            <p><a href="{item['url']}" style="color:#1976d2; font-weight:bold">Đọc chi tiết →</a></p>
        </div>
        <hr>
        """

    html_body += "<p><small>StockDigest – Tin chứng khoán AI tự động • Mỗi ngày 7h30 & 19h30</small></p>"

    # Gửi cho từng người
    for sub in subscribers:
        email = sub['email']
        msg = MIMEMultipart()
        msg['From'] = f"StockDigest <{GMAIL_USER}>"
        msg['To'] = email
        msg['Subject'] = f" Tin nóng hôm nay – {len(all_hot_news)} tin có mã bạn theo dõi"

        msg.attach(MIMEText(html_body, 'html'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"Đã gửi email thành công tới {email}")
        except Exception as e:
            print(f"Lỗi gửi tới {email}: {e}")

# Test ngay lập tức (gọi 1 lần để kiểm tra)
if __name__ == "__main__":
    send_daily_email()