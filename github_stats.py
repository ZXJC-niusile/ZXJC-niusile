import requests
import time
import random

def download_stats():
    print("🚀 Starting download...")
    
    username = "ZXJC-niusile"
    
    # 🎨 颜色配置 (你的午夜紫罗兰风格)
    bg_color = "1f2040"
    title_color = "9194bf"
    text_color = "F2E6F1"
    icon_color = "D0D1F9"
    ring_color = "9194bf"
    border_color = "70a5fd"
    
    url = (
        f"https://github-readme-stats.vercel.app/api"
        f"?username={username}"
        f"&show_icons=true"
        f"&hide_border=false"
        f"&bg_color={bg_color}"
        f"&title_color={title_color}"
        f"&text_color={text_color}"
        f"&icon_color={icon_color}"
        f"&ring_color={ring_color}"
        f"&border_color={border_color}"
        # 强制不使用缓存，尝试获取最新数据
        f"&cache_seconds=0" 
    )

    print(f"🔗 URL: {url}")

    # 伪装成浏览器的请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache"
    }

    # 重试机制：最多试 5 次，每次等待时间延长
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # 发送带 Header 的请求
            response = requests.get(url, headers=headers, timeout=45)
            
            if response.status_code == 503:
                raise Exception("Server is busy (503)")
            
            response.raise_for_status()

            with open("github_stats.svg", "wb") as f:
                f.write(response.content)
            
            print("✅ Success! Image saved to github_stats.svg")
            return 

        except Exception as e:
            wait_time = (attempt + 1) * 5 + random.randint(1, 5) # 等待 6~30 秒不等
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"   Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("❌ All attempts failed. Vercel is likely down.")
                raise 

if __name__ == "__main__":
    download_stats()
