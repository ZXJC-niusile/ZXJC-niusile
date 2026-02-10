import requests

def download_stats():
    # ==========================================
    # 🎨 自定义颜色配置
    # ==========================================
    
    # 背景颜色 (TokyoNight 深蓝背景)
    bg_color = "1a1b27" 
    
    # 标题颜色
    title_color = "70a5fd" 
    
    # 文字颜色
    text_color = "38bdae" 
    
    # 图标颜色
    icon_color = "bf91f3" 
    
    # 圆环颜色 (Rank 圆环)
    ring_color = "bf91f3" 
    
    # ✅ 边框颜色 (新功能！)
    # 我预设了一个和背景协调的淡紫色，你可以改成 'ffffff' (白) 或 'e4e2e2' (灰) 看看默认效果
    border_color = "70a5fd" 

    # ==========================================
    # 生成逻辑
    # ==========================================
    
    base_url = "https://github-readme-stats.vercel.app/api"
    
    params = (
        f"?username=ZXJC-niusile"
        f"&show_icons=true"
        f"&include_all_commits=true"
        f"&hide_border=false"         # 👈 这里改成了 false，显示边框！
        f"&bg_color={bg_color}"
        f"&title_color={title_color}"
        f"&text_color={text_color}"
        f"&icon_color={icon_color}"
        f"&ring_color={ring_color}"
        f"&border_color={border_color}" # 👈 加上了边框颜色参数
    )
    
    url = base_url + params

    print(f"Downloading stats with BORDER...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status() 

        with open("github_stats.svg", "wb") as f:
            f.write(response.content)
        
        print("✅ Success! Stats card with border saved.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise 

if __name__ == "__main__":
    download_stats()
