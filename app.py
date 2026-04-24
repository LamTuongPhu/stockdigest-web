from flask import Flask, render_template, request, jsonify
from scheduler import scheduler
from facade import facade

app = Flask(__name__)

scheduler.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/news')
def get_news():
    # Lấy danh sách mã người dùng đang theo dõi từ URL
    watch_str = request.args.get('watchlist', '')
    watchlist = [c.strip().upper() for c in watch_str.split(',') if c.strip()]

    news = facade.get_news(watchlist)  # Truyền vào Facade
    return jsonify(news)


if __name__ == '__main__':
    print("🚀 StockDigest Web Server đang chạy...")
    print("🌐 Truy cập: http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)