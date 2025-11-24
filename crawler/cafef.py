# crawler/cafef.py
import requests
from bs4 import BeautifulSoup
import re

def crawl_news():
    print("   → Đang quét CafeF, NDH, VnEconomy...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36"
    }
    urls = [
        "https://cafef.vn/chung-khoan.chn",
        "https://ndh.vn/chung-khoan",
        "https://vneconomy.vn/chung-khoan.htm",
    ]

    articles = []
    seen_urls = set()

    # Danh sách mã CK lớn + mã đang HOT hôm nay (cập nhật 24/11/2025)
    BIG_STOCKS = {
        'VCB', 'HPG', 'FPT', 'MWG', 'VIC', 'SSI', 'VND', 'HCM', 'AAA', 'BSI',
        'USD', 'FTSE', 'NIM', 'SJC', 'VFS', 'VHM', 'MSN', 'GAS', 'PLX', 'BID',
        'CTG', 'MBB', 'ACB', 'TCB', 'VPB', 'SHB', 'STB', 'EIB', 'LPB', 'HDB'
    }

    for base_url in urls:
        try:
            r = requests.get(base_url, headers=headers, timeout=20)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')

            for a in soup.find_all('a', href=True):
                title = (a.get('title') or a.get_text(strip=True))
                link = a['href']

                if not title or len(title) < 15:
                    continue

                # Chuẩn hóa link
                if link.startswith('/'):
                    link = "https://" + base_url.split("/")[2] + link
                elif not link.startswith('http'):
                    link = base_url.rstrip('/') + '/' + link.lstrip('/')

                if link in seen_urls:
                    continue
                seen_urls.add(link)

                # Bắt mã bằng regex + bắt buộc thêm mã lớn/hot
                codes = set(re.findall(r'\b[A-Z]{3,6}\b', title))  # mở rộng lên 6 ký tự
                title_upper = title.upper()
                extra_codes = {code for code in BIG_STOCKS if code in title_upper}
                codes.update(extra_codes)

                # Từ khóa quan trọng (thêm nhiều hơn)
                keywords = [
                    'cổ tức', 'lợi nhuận', 'chia cổ tức', 'kết quả kinh doanh',
                    'niêm yết', 'thoái vốn', 'tăng vốn', 'chia tách', 'phát hành',
                    'đại hội', 'bầu', 'cổ đông', 'quỹ', 'ETF', 'bán giải chấp'
                ]

                if codes or any(kw in title.lower() for kw in keywords):
                    articles.append({
                        'title': title,
                        'url': link,
                        'codes': sorted(list(codes)),  # sắp xếp cho đẹp
                        'source': base_url.split('.')[0].upper()
                    })

                    # DEBUG: in ra để bạn thấy mã nào được bắt
                    if codes:
                        print(f"   Tin có mã: {sorted(codes)} → {title[:70]}...")

        except Exception as e:
            print(f"   Lỗi crawl {base_url}: {e}")
            continue

    print(f"   → Tìm được {len(articles)} tin nóng có mã CK! (tối đa 60)")
    return articles[:60]  # 60 tin