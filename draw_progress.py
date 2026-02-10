import datetime
import os

def generate_progress_svg():
    # 1. 获取当前时间
    now = datetime.datetime.now()
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
    
    # 颜色配置 (可以修改这里)
    bg_color = "#e1e4e8"      # 灰色背景
    bar_color = "#3776AB"     # 进度条颜色 (Python蓝)
    text_color = "#586069"    # 文字颜色 (深灰)
    
    # 5. 生成 SVG 内容
    svg_content = f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
      <!-- 背景灰色条 -->
      <rect rx="{border_radius}" ry="{border_radius}" width="{width}" height="{height}" fill="{bg_color}" />
      
      <!-- 前景蓝色进度条 -->
      <rect rx="{border_radius}" ry="{border_radius}" width="{progress_width}" height="{height}" fill="{bar_color}" />
      
      <!-- 中间文字: 显示百分比和剩余天数 -->
      <text x="{width/2}" y="14" fill="{text_color}" font-family="Arial, Helvetica, sans-serif" font-size="11" text-anchor="middle" font-weight="bold">
        {current_year} Progress: {percentage:.1f}% ({days_left} Days Left)
      </text>
    </svg>"""
    
    # 6. 保存文件到仓库根目录
    with open("progress.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"Generated progress.svg: {percentage:.1f}% with {days_left} days left.")

if __name__ == "__main__":
    generate_progress_svg()
