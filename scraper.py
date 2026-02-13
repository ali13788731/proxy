import requests
import re
import json

# لیست کانال‌های قوی پروکسی (نام کاربری بدون @)
CHANNELS = [
    "Myporoxy",
    "TelMTProto",
    "ProxyMTProto",
    "mt_p_roxy",
    "ProxyHagh",
    "MTProtoProxies"
]

def scrape_channel(channel_name):
    url = f"https://t.me/s/{channel_name}"
    print(f"در حال بررسی کانال: {channel_name}...")
    
    try:
        # دریافت محتوای HTML کانال
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # الگوی پیدا کردن لینک‌های پروکسی
        # دنبال لینک‌هایی می‌گردیم که server= و port= و secret= داشته باشند
        pattern = r'https://t\.me/proxy\?server=[\w\.\-]+&port=\d+&secret=[\w\.\-%]+'
        links = re.findall(pattern, response.text)
        
        return list(set(links)) # حذف تکراری‌ها در هر کانال
    except Exception as e:
        print(f"خطا در {channel_name}: {e}")
        return []

def main():
    all_proxies = []
    
    for channel in CHANNELS:
        links = scrape_channel(channel)
        print(f"یافت شد: {len(links)} عدد")
        
        for link in links:
            try:
                # استخراج دقیق پارامترها برای فایل جیسون
                server = re.search(r'server=([\w\.\-]+)', link).group(1)
                port = re.search(r'port=(\d+)', link).group(1)
                secret = re.search(r'secret=([\w\.\-%]+)', link).group(1)
                
                all_proxies.append({
                    "server": server,
                    "port": port,
                    "secret": secret,
                    "link": link
                })
            except:
                continue

    # حذف تکراری‌های کلی بر اساس سرور
    unique_proxies = {p['server']: p for p in all_proxies}.values()
    final_list = list(unique_proxies)

    # ذخیره در فایل
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4)
        
    print(f"\n✅ تمام شد! مجموعاً {len(final_list)} پروکسی منحصر‌به‌فرد ذخیره شد.")

if __name__ == "__main__":
    main()
