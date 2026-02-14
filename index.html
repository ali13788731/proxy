import requests
import re
import json
import html
import socket
import time
import jdatetime
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# لیست کانال‌های پروکسی
CHANNELS = [
    "Myporoxy", "TelMTProto", "ProxyMTProto", "mt_p_roxy", 
    "ProxyHagh", "MTProtoProxies", "PinkProxy", "v2rayng_vpn"
]

# تنظیمات زمان‌بندی
CHECK_INTERVAL = 30  # هر چند ثانیه اینترنت را چک کند (در زمان قطعی)
RUN_INTERVAL = 600   # هر چند ثانیه (۱۰ دقیقه) اسکریپت اجرا شود (در زمان وصلی)

def check_internet():
    """بررسی اتصال به اینترنت با پینگ کردن DNS گوگل"""
    try:
        # اتصال به 8.8.8.8 پورت 53 (DNS) با تایم‌اوت 3 ثانیه
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def get_ping(server, port):
    """تست پینگ واقعی (اتصال TCP)"""
    try:
        start = time.time()
        sock = socket.create_connection((server, int(port)), timeout=1.5)
        sock.close()
        return int((time.time() - start) * 1000)
    except:
        return 9999

def process_proxy(link):
    """استخراج و تست پینگ هر لینک"""
    try:
        if "https://t.me/proxy" in link:
            link = link.replace("https://t.me/proxy", "tg://proxy")
            
        server_match = re.search(r'server=([\w\.\-\[\]:]+)', link)
        port_match = re.search(r'port=(\d+)', link)
        secret_match = re.search(r'secret=([\w\.\-\%]+)', link)

        if not (server_match and port_match and secret_match):
            return None

        server = server_match.group(1)
        port = port_match.group(1)
        secret = secret_match.group(1)
        
        ping = get_ping(server, port)
        
        if ping < 3000: 
            return {
                "server": server,
                "port": port,
                "secret": secret,
                "link": link,
                "ping": ping
            }
    except Exception as e:
        return None
    return None

def run_scraper():
    """بدنه اصلی برنامه که اجرا می‌شود"""
    print(f"\n🚀 شروع عملیات در ساعت: {datetime.now().strftime('%H:%M:%S')}")
    print("📥 در حال دریافت لیست پروکسی‌ها...")
    
    raw_links = []
    for chan in CHANNELS:
        try:
            url = f"https://t.me/s/{chan}"
            # تایم‌اوت را کمی بیشتر کردیم تا در اینترنت ضعیف هم کار کند
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            clean_text = html.unescape(res.text)
            links = re.findall(r'(?:https://t\.me/|tg://)proxy\?(?:[^"\s>]+)', clean_text)
            raw_links.extend(links)
            print(f"✅ {chan}: {len(links)} یافت شد.")
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت {chan}: {e}")
            continue
        except Exception as e:
            print(f"⚠️ خطای ناشناس در {chan}")
            continue

    unique_links = list(set(raw_links))
    valid_proxies = []

    if not unique_links:
        print("⚠️ هیچ لینکی یافت نشد. اینترنت چک شود.")
        return

    print(f"⚡ در حال تست پینگ {len(unique_links)} پروکسی...")
    
    # استفاده از ThreadPoolExecutor برای سرعت بالا
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(process_proxy, unique_links)
        for r in results:
            if r: valid_proxies.append(r)

    valid_proxies.sort(key=lambda x: x['ping'])

    # --- تنظیم زمان ---
    utc_now = datetime.utcnow()
    tehran_time = utc_now + timedelta(hours=3, minutes=30)
    now_shamsi = jdatetime.datetime.fromgregorian(datetime=tehran_time).strftime("%Y/%m/%d - %H:%M")
    
    final_output = {
        "last_updated": now_shamsi,
        "proxies": valid_proxies
    }

    try:
        with open("proxies.json", "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=4, ensure_ascii=False)
        print(f"💾 فایل ذخیره شد. تعداد پروکسی: {len(valid_proxies)}")
    except Exception as e:
        print(f"❌ خطا در ذخیره فایل: {e}")

    print(f"🏁 پایان عملیات. زمان: {now_shamsi}")

if __name__ == "__main__":
    print("✅ اسکریپت ضد قطعی اینترنت فعال شد.")
    print("--------------------------------------")
    
    while True:
        try:
            if check_internet():
                # اگر اینترنت وصل بود، برنامه اجرا شود
                run_scraper()
                
                print(f"💤 استراحت برای {RUN_INTERVAL} ثانیه...")
                time.sleep(RUN_INTERVAL)
            else:
                # اگر اینترنت قطع بود
                print(f"⛔ اینترنت قطع است! تلاش مجدد در {CHECK_INTERVAL} ثانیه دیگر...")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n🛑 برنامه توسط کاربر متوقف شد.")
            break
        except Exception as e:
            # اگر خطای خیلی بدی رخ داد که کل برنامه خواست کرش کند
            print(f"🔥 خطای بحرانی (Critical Error): {e}")
            print("🔄 راه‌اندازی مجدد خودکار...")
            time.sleep(10)
