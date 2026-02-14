import datetime
import os

def generate_progress_svg():
    print("🚀 Generating Progress Bar...")
    
    # 1. 获取当前时间 (🚨 强制转换为北京时间 UTC+8，解决 GitHub 时差问题)
    utc_now = datetime.datetime.utcnow()
    now = utc_now + datetime.timedelta(hours=8)
    current_year = now.year
    
    # 2. 定义今年开始和明年开始的时间
    start_of_year = datetime.datetime(current_year, 1, 1)
    start_of_next_year = datetime.datetime(current_year + 1, 1, 1)
    
    # 3. 计算时间差
    total_seconds = (start_of_next_year - start_of_year).total_seconds()
    passed_seconds = (now - start_of_year).total_seconds()
    
    # 计算剩余天数 (倒计时)
    remaining_delta = start_of_next_year - now
    days_left = remaining_delta.days
    
    # 计算百分比
    percentage = (passed_seconds / total_seconds) * 100
    # 限制在 0-100 之间
    percentage = max(0, min(100, percentage))
    
    # 4. SVG配置
    width = 300          # 图片总宽度
    height = 20          # 图片高度
    border_radius = 4    # 圆角大小
    
    # 计算进度条的宽度
    progress_width = (percentage / 100) * width
    
    # 🎨 从 YML 环境变量读取配置 (如果没有配置，则默认使用你写在下面的颜色)
    def get_color(env_var, default):
        color = os.environ.get(env_var, default)
        return f"#{color}" if not color.startswith("#") else color

    bg_color = get_color("PROG_BG_COLOR", "1a1b27")      # 背景颜色
    bar_color = get_color("PROG_BAR_COLOR", "70a5fd")     # 进度条颜色
    text_color = get_color("PROG_TEXT_COLOR", "bf91f3")   # 文字颜色
    
    # 5. 生成 SVG 内容 (增加了 clip-path 保证进度条随圆角完美切割)
    svg_content = f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
      <defs>
          <clipPath id="round-corner">
              <rect width="{width}" height="{height}" rx="{border_radius}" ry="{border_radius}"/>
          </clipPath>
      </defs>
      
      <rect width="{width}" height="{height}" fill="{bg_color}" rx="{border_radius}" ry="{border_radius}" />
      
      <rect width="{progress_width}" height="{height}" fill="{bar_color}" clip-path="url(#round-corner)" />
      
      <text x="{width/2}" y="14" fill="{text_color}" font-family="Arial, Helvetica, sans-serif" font-size="11" text-anchor="middle" font-weight="bold">
        {current_year} Progress: {percentage:.1f}% ({days_left} Days Left)
      </text>
    </svg>"""
    
# 6. 保存文件到 image 文件夹
    # 👇 新增：确保 image 文件夹存在，如果不存在就自动创建一个
    os.makedirs("image", exist_ok=True)
    
    # 👇 修改：路径改为 "image/progress.svg"
    with open("image/progress.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"✅ Generated image/progress.svg: {percentage:.1f}% with {days_left} days left.")

if __name__ == "__main__":
    generate_progress_svg()
