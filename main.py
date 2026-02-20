import requests
import re
import json
import html
import jdatetime
from datetime import datetime, timedelta

# لیست کانال‌های پروکسی
CHANNELS = [
    "Myporoxy", "TelMTProto", "ProxyMTProto", "mt_p_roxy", 
    "ProxyHagh", "MTProtoProxies", "PinkProxy", "v2rayng_vpn"
]

def process_proxy(link):
    try:
        if "https://t.me/proxy" in link:
            link = link.replace("https://t.me/proxy", "tg://proxy")
            
        server_match = re.search(r'server=([\w\.\-\[\]:]+)', link)
        port_match = re.search(r'port=(\d+)', link)
        secret_match = re.search(r'secret=([\w\.\-\%]+)', link)
        
        # بررسی می‌کنیم که حتماً دیتا پیدا شده باشه تا ارور نده
        if server_match and port_match and secret_match:
            return {
                "server": server_match.group(1),
                "port": port_match.group(1),
                "secret": secret_match.group(1),
                "link": link
            }
    except Exception as e:
        pass
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

    print(f"⚡ در حال پردازش {len(unique_links)} پروکسی...")
    for link in unique_links:
        proxy_data = process_proxy(link)
        if proxy_data:
            valid_proxies.append(proxy_data)

    # --- زمان‌بندی ---
    utc_now = datetime.utcnow()
    tehran_time = utc_now + timedelta(hours=3, minutes=30)
    now_shamsi = jdatetime.datetime.fromgregorian(datetime=tehran_time).strftime("%Y/%m/%d - %H:%M")

    # --- خروجی JSON برای اپلیکیشن اندروید ---
    final_output = {
        "last_updated": now_shamsi,
        "proxies": valid_proxies
    }
    
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)
        
    print(f"🏁 تمام شد. {len(valid_proxies)} پروکسی در proxies.json ذخیره شد.")

if __name__ == "__main__":
    main()
