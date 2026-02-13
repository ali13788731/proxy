import requests
import re
import json
import html
import socket
import time
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
        sock = socket.create_connection((server, int(port)), timeout=2.5)
        sock.close()
        return int((time.time() - start) * 1000)
    except:
        return 9999

def process_proxy(link):
    """استخراج و تست پینگ هر لینک"""
    try:
        server = re.search(r'server=([\w\.\-\[\]:]+)', link).group(1)
        port = re.search(r'port=(\d+)', link).group(1)
        secret = re.search(r'secret=([\w\.\-\%]+)', link).group(1)
        
        ping = get_ping(server, port)
        if ping < 4000: # فقط پروکسی‌های زنده
            return {
                "server": server, "port": port, "secret": secret,
                "link": link, "ping": ping, "time": time.strftime("%H:%M")
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
    final_data = []

    # پینگ موازی برای سرعت بالا
    with ThreadPoolExecutor(max_workers=40) as executor:
        results = executor.map(process_proxy, unique_links)
        for r in results:
            if r: final_data.append(r)

    # مرتب‌سازی: سریع‌ترین‌ها در اول لیست
    final_data.sort(key=lambda x: x['ping'])

    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
    
    print(f"🏁 به روزرسانی تمام شد. {len(final_data)} پروکسی آماده است.")

if __name__ == "__main__":
    main()
