import requests
import re
import json
import base64

# لیست منابع (می‌توانید منابع بیشتری اضافه کنید)
SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/SoroushApps/Proxy-List/main/MTProto.txt" # منبع خوب برای MTProto
]

def parse_mtproto(link):
    """اطلاعات سرور، پورت و سکرت را از لینک استخراج می‌کند"""
    try:
        server = re.search(r'server=([^&]+)', link).group(1)
        port = re.search(r'port=([^&]+)', link).group(1)
        secret = re.search(r'secret=([^&]+)', link).group(1)
        return {"server": server, "port": port, "secret": secret, "link": link, "type": "mtproto"}
    except:
        return None

def main():
    proxies = []
    
    # 1. دانلود و استخراج لینک‌ها
    for url in SOURCES:
        try:
            print(f"Fetching {url}...")
            resp = requests.get(url, timeout=10)
            # پیدا کردن تمام لینک‌های MTProto
            found_links = re.findall(r'(tg://proxy\?[^\s"]+|https://t\.me/proxy\?[^\s"]+)', resp.text)
            
            for link in found_links:
                data = parse_mtproto(link)
                if data:
                    proxies.append(data)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # 2. حذف تکراری‌ها
    unique_proxies = {v['server']:v for v in proxies}.values()
    final_list = list(unique_proxies)

    # 3. ذخیره در فایل JSON
    with open("proxies.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4)
    
    print(f"✅ Successfully saved {len(final_list)} proxies to proxies.json")

if __name__ == "__main__":
    main()
