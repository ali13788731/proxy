import requests
import re
import json
import html
import socket
import time
import jdatetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs

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
        # استانداردسازی لینک
        clean_link = link.replace("tg://proxy", "https://t.me/proxy")
        parsed_url = urlparse(clean_link)
        params = parse_qs(parsed_url.query)
        
        server = params.get('server', [None])[0]
        port = params.get('port', [None])[0]
        secret = params.get('secret', [None])[0]
        
        if not all([server, port, secret]):
            return None
            
        ping = get_ping(server, port)
        
        if ping < 3000: 
            return {
                "server": server,
                "port": port,
                "secret": secret,
                "link": f"tg://proxy?server={server}&port={port}&secret={secret}",
                "ping": ping
            }
    except Exception as e:
        return None
    return None

def main():
    print("🚀 در حال دریافت لیست پروکسی‌ها...")
    raw_links = []
    
    # استفاده از Session برای سرعت بیشتر و شبیه‌سازی مرورگر
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    for chan in CHANNELS:
        try:
            url = f"https://t.me/s/{chan}"
            res = session.get(url, timeout=15)
            # رنک‌گیری دقیق‌تر لینک‌ها
            links = re.findall(r'tg://proxy\?[^"\'\s<>]+|https://t\.me/proxy\?[^"\'\s<>]+', res.text)
            raw_links.extend(links)
            print(f"✅ {chan}: {len(links)} یافت شد.")
        except Exception as e:
            print(f"❌ خطا در کانال {chan}: {e}")
            continue

    unique_links = list(set(raw_links))
    valid_proxies = []

    print(f"⚡ در حال تست پینگ {len(unique_links)} پروکسی...")
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(process_proxy, unique_links)
        for r in results:
            if r: valid_proxies.append(r)

    valid_proxies.sort(key=lambda x: x['ping'])
    
    # فقط ۳۰ تای برتر رو نگه دار (برای شلوغ نشدن صفحه)
    valid_proxies = valid_proxies[:30]

    now_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d - %H:%M")
    
    final_output = {
        "last_updated": now_shamsi,
        "proxies": valid_proxies
    }

    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)
    
    print(f"🏁 تمام شد. {len(valid_proxies)} پروکسی ذخیره شد.")

if __name__ == "__main__":
    main()
