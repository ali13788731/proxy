import requests
import re
import json
import html
import socket
import time
import jdatetime  # برای تاریخ شمسی
from concurrent.futures import ThreadPoolExecutor

# لیست کانال‌های پروکسی
CHANNELS = [
    "Myporoxy", "TelMTProto", "ProxyMTProto", "mt_p_roxy", 
    "ProxyHagh", "MTProtoProxies", "PinkProxy", "v2rayng_vpn"
]

def get_ping(server, port):
    """تست پینگ واقعی (اتصال TCP)"""
    try:
        start = time.time()
        # کاهش تایم‌اوت به 1.5 ثانیه برای سرعت بیشتر
        sock = socket.create_connection((server, int(port)), timeout=1.5)
        sock.close()
        return int((time.time() - start) * 1000)
    except:
        return 9999

def process_proxy(link):
    """استخراج و تست پینگ هر لینک"""
    try:
        # تبدیل لینک وب به لینک مستقیم تلگرام
        if "https://t.me/proxy" in link:
            link = link.replace("https://t.me/proxy", "tg://proxy")
            
        server = re.search(r'server=([\w\.\-\[\]:]+)', link).group(1)
        port = re.search(r'port=(\d+)', link).group(1)
        secret = re.search(r'secret=([\w\.\-\%]+)', link).group(1)
        
        ping = get_ping(server, port)
        
        # فقط پروکسی‌های با پینگ زیر 3000 میلی‌ثانیه
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
            # استخراج لینک‌ها
            links = re.findall(r'(?:https://t\.me/|tg://)proxy\?(?:[^"\s>]+)', clean_text)
            raw_links.extend(links)
            print(f"✅ {chan}: {len(links)} یافت شد.")
        except:
            continue

    unique_links = list(set(raw_links))
    valid_proxies = []

    # پینگ موازی
    print(f"⚡ در حال تست پینگ {len(unique_links)} پروکسی...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(process_proxy, unique_links)
        for r in results:
            if r: valid_proxies.append(r)

    # مرتب‌سازی: کمترین پینگ اول لیست
    valid_proxies.sort(key=lambda x: x['ping'])

    # دریافت زمان فعلی به وقت ایران (شمسی)
    # با فرض اینکه سرور گیت‌هاب UTC است، ۳:۳۰ ساعت اضافه می‌کنیم یا از کتابخانه برای تایم‌زون استفاده می‌کنیم
    # اینجا مستقیماً زمان را تبدیل می‌کنیم
    now_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d - %H:%M")

    # ساختار نهایی جیسون
    final_output = {
        "last_updated": now_shamsi,
        "proxies": valid_proxies
    }

    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)
    
    print(f"🏁 تمام شد. {len(valid_proxies)} پروکسی فعال ذخیره شد. زمان: {now_shamsi}")

if __name__ == "__main__":
    main()
