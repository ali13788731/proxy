import requests
import re
import json
import html
import socket
import time
import jdatetime
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# --- تنظیمات ---
CHANNELS = [
    "Myporoxy", "TelMTProto", "ProxyMTProto", "mt_p_roxy", 
    "ProxyHagh", "MTProtoProxies", "PinkProxy", "v2rayng_vpn"
]
CHECK_INTERVAL = 20  # زمان چک مجدد در صورت قطع اینترنت (ثانیه)
RUN_INTERVAL = 300   # فاصله زمانی بین هر آپدیت کلی (ثانیه - ۵ دقیقه)

def check_internet():
    """بررسی اتصال به اینترنت"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def get_ping(server, port):
    """تست پینگ TCP"""
    try:
        start = time.time()
        sock = socket.create_connection((server, int(port)), timeout=1.5)
        sock.close()
        return int((time.time() - start) * 1000)
    except:
        return 9999

def process_proxy(link):
    """پردازش و استخراج مشخصات پروکسی"""
    try:
        if "https://t.me/proxy" in link:
            link = link.replace("https://t.me/proxy", "tg://proxy")
        
        server = re.search(r'server=([\w\.\-\[\]:]+)', link).group(1)
        port = re.search(r'port=(\d+)', link).group(1)
        secret = re.search(r'secret=([\w\.\-\%]+)', link).group(1)
        
        ping = get_ping(server, port)
        if ping < 3000:
            return {"server": server, "port": port, "secret": secret, "link": link, "ping": ping}
    except:
        return None

def fetch_channel_links(chan, session):
    """دریافت لینک‌ها از کانال به صورت موازی"""
    try:
        url = f"https://t.me/s/{chan}"
        res = session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if res.status_code == 200:
            clean_text = html.unescape(res.text)
            links = re.findall(r'(?:https://t\.me/|tg://)proxy\?(?:[^"\s>]+)', clean_text)
            return links
    except:
        pass
    return []

def run_scraper():
    """اجرای عملیات استخراج و تست"""
    print(f"\n✨ شروع پردازش: {datetime.now().strftime('%H:%M:%S')}")
    all_links = []
    
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=len(CHANNELS)) as executor:
            futures = [executor.submit(fetch_channel_links, chan, session) for chan in CHANNELS]
            for future in futures:
                all_links.extend(future.result())

    unique_links = list(set(all_links))
    print(f"📥 تعداد لینک‌های یافت شده: {len(unique_links)}")
    
    valid_proxies = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(process_proxy, unique_links)
        for r in results:
            if r: valid_proxies.append(r)

    valid_proxies.sort(key=lambda x: x['ping'])

    # زمان شمسی
    tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
    now_shamsi = jdatetime.datetime.fromgregorian(datetime=tehran_time).strftime("%Y/%m/%d - %H:%M")

    output = {"last_updated": now_shamsi, "proxies": valid_proxies}
    
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"✅ پایان. {len(valid_proxies)} پروکسی ذخیره شد.")

if __name__ == "__main__":
    print("🚀 اسکریپت فعال شد. منتظر اتصال...")
    while True:
        try:
            if check_internet():
                run_scraper()
                time.sleep(RUN_INTERVAL)
            else:
                print("⚠️ اینترنت قطع است. صبر برای اتصال مجدد...")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"🔥 خطا: {e}")
            time.sleep(10)
