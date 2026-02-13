import requests
import re
import json

# منابعی که پروکسی‌های سالم و تازه دارند
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramVipProxy/main/output/proxies.txt",
    "https://raw.githubusercontent.com/vfarid/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/LalatinaHub/Telegram-Proxie/master/Proxy-List.txt"
]

def main():
    proxies = []
    print("شروع استخراج...")
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            # جستجوی تمام لینک‌های مربوط به پروکسی تلگرام
            found = re.findall(r'tg://proxy\?[^\s"<>]+', r.text)
            print(f"پیدا شد در {url}: {len(found)} مورد")
            
            for link in found:
                try:
                    # استخراج اطلاعات از لینک
                    server = re.search(r'server=([^&]+)', link).group(1)
                    port = re.search(r'port=([^&]+)', link).group(1)
                    secret = re.search(r'secret=([^&]+)', link).group(1)
                    proxies.append({
                        "server": server,
                        "port": port,
                        "secret": secret,
                        "link": link
                    })
                except:
                    continue
        except Exception as e:
            print(f"خطا در {url}: {e}")

    # حذف تکراری‌ها
    final_data = {v['server']:v for v in proxies}.values()
    final_list = list(final_data)[:50] # گرفتن ۵۰ تای اول برای سرعت

    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4)
    
    print(f"مجموعاً {len(final_list)} پروکسی ذخیره شد.")

if __name__ == "__main__":
    main()
