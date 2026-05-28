import requests
import re
import base64
import os

# لیست منابع (لینک‌های Raw که حاوی کانفیگ هستند)
# می‌توانید لینک‌های بیشتری به این لیست اضافه کنید
SOURCES = [
    "https://raw.githubusercontent.com/mzz2017/gg/main/v2ray/sub",
    "https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription_num",
    # لینک‌های خود را اینجا اضافه کنید
]

# پترن Regex برای پیدا کردن لینک‌های V2Ray (Vless, Vmess, Trojan, SS)
CONFIG_PATTERN = re.compile(r'(vless|vmess|trojan|ss)://[^\s]+')
MAX_CONFIGS_PER_FILE = 200

def fetch_configs():
    all_configs = set() # استفاده از set برای حذف خودکار تکراری‌ها
    
    for url in SOURCES:
        try:
            print(f"Fetching from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            text = response.text
            
            # بررسی اینکه آیا سورس خودش Base64 است یا متن ساده
            try:
                decoded_text = base64.b64decode(text).decode('utf-8')
                text = decoded_text
            except Exception:
                pass # اگر Base64 نبود، همان متن ساده را پردازش می‌کنیم
            
            # استخراج کانفیگ‌ها
            matches = CONFIG_PATTERN.findall(text)
            for match in re.finditer(CONFIG_PATTERN, text):
                all_configs.add(match.group(0))
                
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            
    return list(all_configs)

def save_sublinks(configs):
    # تقسیم لیست به بخش‌های ۲۰۰ تایی
    chunks = [configs[i:i + MAX_CONFIGS_PER_FILE] for i in range(0, len(configs), MAX_CONFIGS_PER_FILE)]
    
    # ساخت پوشه برای ذخیره فایل‌ها در صورت نیاز (اینجا در همون روت ذخیره میکنیم)
    for i, chunk in enumerate(chunks):
        filename = f"sub{i+1}.txt" # نام فایل‌ها: sub1.txt, sub2.txt و...
        
        # چسباندن کانفیگ‌ها با اینتر
        raw_text = '\n'.join(chunk)
        
        # انکد به Base64
        encoded_bytes = base64.b64encode(raw_text.encode('utf-8'))
        encoded_str = encoded_bytes.decode('utf-8')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(encoded_str)
            
        print(f"Saved {len(chunk)} configs to {filename}")

if __name__ == "__main__":
    print("Starting config extraction...")
    configs = fetch_configs()
    print(f"Total unique configs found: {len(configs)}")
    
    if configs:
        save_sublinks(configs)
        print("All sublinks generated successfully.")
    else:
        print("No configs found!")
