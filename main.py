import requests
import re
import json
import html
import socket
import time
import base64  # اضافه شده برای خروجی Base64
import jdatetime
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# لیست کانال‌های پروکسی
CHANNELS = [
    "Myporoxy", "TelMTProto", "ProxyMTProto", "mt_p_roxy", 
    "ProxyHagh", "MTProtoProxies", "PinkProxy", "v2rayng_vpn"
]

def get_ping(server, port):
    try:
        start = time.time()
        sock = socket.create_connection((server, int(port)), timeout=1.5)
        sock.close()
        return int((time.time() - start) * 1000)
    except:
        return 9999

def process_proxy(link):
    try:
        if "https://t.me/proxy" in link:
            link = link.replace("https://t.me/proxy", "tg://proxy")
            
        server = re.search(r'server=([\w\.\-\[\]:]+)', link).group(1)
        port = re.search(r'port=(\d+)', link).group(1)
        secret = re.search(r'secret=([\w\.\-\%]+)', link).group(1)
        
        ping = get_ping(server, port)
        
        if ping < 3000: 
            return {
                "server": server,
                "port": port,
                "secret": secret,
                "link": link,
                "ping": ping
            }
    except:
        return None

def main():
    print("🚀 در حال دریافت لیست پروکسی‌ها...")
    raw_links = []
    for chan in CHANNELS:
        try:
            url = f"https://t.me/s/{chan}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            clean_text = html.unescape(res.text)
            links = re.findall(r'(?:https://t\.me/|tg://)proxy\?(?:[^"\s>]+)', clean_text)
            raw_links.extend(links)
            print(f"✅ {chan}: {len(links)} یافت شد.")
        except:
            continue

    unique_links = list(set(raw_links))
    valid_proxies = []

    print(f"⚡ در حال تست پینگ {len(unique_links)} پروکسی...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(process_proxy, unique_links)
        for r in results:
            if r: valid_proxies.append(r)

    # مرتب‌سازی بر اساس پینگ
    valid_proxies.sort(key=lambda x: x['ping'])

    # --- زمان‌بندی ---
    utc_now = datetime.utcnow()
    tehran_time = utc_now + timedelta(hours=3, minutes=30)
    now_shamsi = jdatetime.datetime.fromgregorian(datetime=tehran_time).strftime("%Y/%m/%d - %H:%M")

    # --- خروجی 1: JSON برای اپلیکیشن اندروید ---
    final_output = {
        "last_updated": now_shamsi,
        "proxies": valid_proxies
    }
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    # --- خروجی 2: Base64 Subscription ---
    # ساخت لیست متنی لینک‌ها
    plain_text_links = ""
    for p in valid_proxies:
        plain_text_links += p['link'] + "\n"
    
    # کدگذاری به Base64
    base64_bytes = base64.b64encode(plain_text_links.encode('utf-8'))
    base64_string = base64_bytes.decode('utf-8')

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(base64_string)
    
    # ذخیره نسخه متنی ساده (اختیاری)
    with open("proxies.txt", "w", encoding="utf-8") as f:
        f.write(plain_text_links)
        
    print(f"🏁 تمام شد. {len(valid_proxies)} پروکسی ذخیره شد. خروجی Base64 در sub.txt قرار گرفت.")

if __name__ == "__main__":
    main()
