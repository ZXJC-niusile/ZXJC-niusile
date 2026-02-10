import requests
import time

def download_stats():
    print("🚀 Starting download...")
    
    # 你的 GitHub 用户名
    username = "ZXJC-niusile"
    
    # ==========================
    # 🎨 颜色配置 (TokyoNight 风格)
    # ==========================
    bg_color = "1f2040"      # 背景：深蓝
    title_color = "9194bf"   # 标题：浅蓝
    text_color = "F2E6F1"    # 文字：青色
    icon_color = "DOD1F9"    # 图标：紫色
    ring_color = "9194bf"    # 圆环：紫色
    border_color = "70a5fd"  # 边框：浅蓝 (配合标题颜色)
    
    # 构造 URL
    # ⚠️ 关键修复：已移除 &include_all_commits=true 以解决 503 报错
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
    )

    print(f"🔗 URL: {url}")

    # 重试机制 (尝试 3 次)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 发送请求
            response = requests.get(url, timeout=30)
            
            # 如果遇到 503 (服务器忙)，主动抛出错误进入重试
            if response.status_code == 503:
                raise Exception("Server is busy (503)")
            
            # 检查其他错误 (404等)
            response.raise_for_status()

            # 保存图片
            with open("github_stats.svg", "wb") as f:
                f.write(response.content)
            
            print("✅ Success! Image saved to github_stats.svg")
            return # 成功后直接结束

        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("   Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("❌ All attempts failed.")
                raise # 最后一次如果还失败，让 Action 报错

if __name__ == "__main__":
    download_stats()
