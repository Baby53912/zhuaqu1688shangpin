import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# 创建数据存储目录
os.makedirs("data", exist_ok=True)

output_file = f"data/今日热卖_{datetime.now().strftime('%Y%m%d')}.csv"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 多源尝试
urls = [
    ("5118抖音热搜", "https://www.5118.com/douyin/hot/"),
    ("百度-抖音爆款", "https://www.baidu.com/s?wd=抖音爆款商品+2026年6月"),
    ("百度-今日热卖", "https://www.baidu.com/s?wd=今日抖音热销商品"),
]

all_items = []
success_source = ""

for name, url in urls:
    try:
        print(f"尝试抓取：{name}...")
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 提取任何长度超过20的文本块
        items = []
        for tag in soup.find_all(['p', 'div', 'span', 'a', 'li', 'h3']):
            text = tag.get_text(strip=True)
            if 20 < len(text) < 500:
                items.append(text)
        
        if items:
            all_items = items
            success_source = name
            break
    except Exception as e:
        print(f"失败：{e}")

# 保存到CSV
with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['序号', '原始文本', '数据来源'])
    for i, item in enumerate(all_items[:50], 1):
        writer.writerow([i, item, success_source])

print(f"成功从 {success_source} 抓取 {len(all_items)} 条数据，保存到 {output_file}")
