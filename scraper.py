import requests
import re
import json
import html  # برای حل مشکل کاراکترهای HTML اضافه شد

# لیست کانال‌های پروکسی (می‌توانید کانال‌های بیشتری اضافه کنید)
CHANNELS = [
    "Myporoxy",
    "TelMTProto",
    "ProxyMTProto",
    "mt_p_roxy",
    "ProxyHagh",
    "MTProtoProxies",
    "PinkProxy",
    "v2rayng_vpn" 
]

def scrape_channel(channel_name):
    url = f"https://t.me/s/{channel_name}"
    print(f"🔎 در حال بررسی کانال: {channel_name}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        # مهم: تبدیل کدهای HTML مثل &amp; به کاراکتر اصلی &
        clean_content = html.unescape(response.text)
        
        # الگوی منعطف‌تر برای پیدا کردن لینک‌ها
        # این الگو هم لینک‌های https و هم tg:// را پیدا می‌کند
        pattern = r'(?:https://t\.me/|tg://)proxy\?(?:[^"\s>]+)'
        
        candidates = re.findall(pattern, clean_content)
        
        valid_proxies = []
        for link in candidates:
            # فیلتر کردن لینک‌هایی که پارامترهای اصلی را ندارند
            if "server=" in link and "port=" in link and "secret=" in link:
                # اگر لینک با tg شروع شد، برای نمایش در وب بهتر است https شود (اختیاری)
                if link.startswith("tg://"):
                    link = link.replace("tg://", "https://t.me/")
                valid_proxies.append(link)
                
        return list(set(valid_proxies))
        
    except Exception as e:
        print(f"❌ خطا در {channel_name}: {e}")
        return []

def main():
    all_proxies = []
    
    for channel in CHANNELS:
        links = scrape_channel(channel)
        print(f"   یافت شد: {len(links)} عدد")
        
        for link in links:
            try:
                # استخراج پارامترها با Regex دقیق‌تر
                server_match = re.search(r'server=([\w\.\-\[\]:]+)', link)
                port_match = re.search(r'port=(\d+)', link)
                secret_match = re.search(r'secret=([\w\.\-\%]+)', link)
                
                if server_match and port_match and secret_match:
                    all_proxies.append({
                        "server": server_match.group(1),
                        "port": port_match.group(1),
                        "secret": secret_match.group(1),
                        "link": link
                    })
            except Exception as e:
                continue

    # حذف تکراری‌ها بر اساس ترکیب سرور و پورت
    unique_proxies = {}
    for p in all_proxies:
        key = f"{p['server']}:{p['port']}"
        unique_proxies[key] = p
    
    final_list = list(unique_proxies.values())

    # ذخیره در فایل
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ تمام شد! مجموعاً {len(final_list)} پروکسی منحصر‌به‌فرد ذخیره شد.")

if __name__ == "__main__":
    main()
