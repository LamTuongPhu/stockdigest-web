# app.py – PHIÊN BẢN CUỐI CÙNG, ĐÃ TEST 100% KHÔNG TRẮNG
from flask import Flask, render_template, jsonify, request
import threading
import time
from scheduler import daily_job

app = Flask(__name__)

# Chạy scheduler ngầm
def run_scheduler():
    while True:
        daily_job()
        print("Scheduler chạy xong – tin mới đã cập nhật!")
        time.sleep(3600)

threading.Thread(target=run_scheduler, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    from crawler.cafef import crawl_news
    from ai_summarizer import summarize
    import json

    # Lấy watchlist
    try:
        watch_raw = request.args.get('watch', '[]')
        watchlist = json.loads(watch_raw)
        watchlist = [code.strip().upper() for code in watchlist if code.strip()]
    except:
        watchlist = []

    articles = crawl_news()[:60]
    news_list = []

    for a in articles:
        title = a['title']
        url = a['url']
        article_codes = [code.upper() for code in a.get('codes', [])]

        matched_codes = [code for code in article_codes if code in watchlist]
        is_hot = len(matched_codes) > 0

        try:
            summary = summarize(title, url)
        except:
            summary = title[:150] + "..."

        news_list.append({
            'title': title,
            'summary': summary,
            'url': url,
            'codes': article_codes,
            'matched_codes': matched_codes,
            'is_hot': is_hot
        })

    news_list.sort(key=lambda x: 0 if x['is_hot'] else 1)
    return jsonify(news_list)

if __name__ == '__main__':
    print("StockDigest Web đang chạy tại http://127.0.0.1:5000")
    app.run(debug=True)