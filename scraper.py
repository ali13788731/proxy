import requests
import re
import json

# منابع معتبر و تازه برای پروکسی‌های مخصوص ایران
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramVipProxy/main/output/proxies.txt",
    "https://raw.githubusercontent.com/vfarid/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/BardiaFA/Proxy-List/main/MTProto.txt",
    "https://raw.githubusercontent.com/Emsadraee/TelegramProxy/main/proxy.txt"
]

def parse_mtproto(text):
    proxies = []
    # پیدا کردن لینک‌های تلگرامی
    links = re.findall(r'(tg://proxy\?[^\s"<>]+|https://t\.me/proxy\?[^\s"<>]+)', text)
    
    for link in links:
        try:
            server = re.search(r'server=([^&]+)', link).group(1)
            port = re.search(r'port=([^&]+)', link).group(1)
            secret = re.search(r'secret=([^&]+)', link).group(1)
            proxies.append({
                "server": server,
                "port": port,
                "secret": secret,
                "link": link.replace("https://t.me/proxy?", "tg://proxy?") # استانداردسازی برای اپلیکیشن
            })
        except:
            continue
    return proxies

def main():
    all_proxies = []
    for url in SOURCES:
        try:
            print(f"در حال دریافت از: {url}")
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                extracted = parse_mtproto(r.text)
                all_proxies.extend(extracted)
        except Exception as e:
            print(f"خطا در منبع {url}: {e}")

    # حذف تکراری‌ها بر اساس سرور
    unique_list = {v['server']:v for v in all_proxies}.values()
    final_data = list(unique_list)[:100] # فقط ۱۰۰ مورد اول برای سرعت بالا

    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)
    print(f"پایان! {len(final_data)} پروکسی ذخیره شد.")

if __name__ == "__main__":
    main()
