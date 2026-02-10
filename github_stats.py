import requests
import os

# 配置你的 GitHub 用户名
USERNAME = "ZXJC-niusile"
# GitHub Action 环境下会自动获取这个 Token，本地测试时可以手动设置环境变量
TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_stats():
    """从 GitHub API 获取用户的统计数据"""
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    
    # 1. 获取基础资料和公开仓库信息
    # user_url 获取关注者和仓库总数
    user_url = f"https://api.github.com/users/{USERNAME}"
    # repos_url 获取所有公开仓库以统计 Star 总数
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    
    user_response = requests.get(user_url, headers=headers)
    repos_response = requests.get(repos_url, headers=headers)
    
    if user_response.status_code != 200 or repos_response.status_code != 200:
        raise Exception(f"GitHub API 请求失败: {user_response.status_code}")

    user_data = user_response.json()
    repos_data = repos_response.json()
    
    # 统计所有仓库的 Star 总数
    total_stars = sum(repo['stargazers_count'] for repo in repos_data)
    public_repos = user_data.get('public_repos', 0)
    followers = user_data.get('followers', 0)
    
    # 2. 获取总 Commits 数 (利用 Search API 统计该作者在 GitHub 上的所有提交)
    commit_url = f"https://api.github.com/search/commits?q=author:{USERNAME}"
    # Search API 的 Commit 搜索需要特定的 Accept Header
    commit_headers = {**headers, "Accept": "application/vnd.github.cloak-preview"}
    commit_response = requests.get(commit_url, headers=commit_headers)
    
    total_commits = 0
    if commit_response.status_code == 200:
        commit_data = commit_response.json()
        total_commits = commit_data.get('total_count', 0)

    return {
        "stars": total_stars,
        "commits": total_commits,
        "repos": public_repos,
        "followers": followers
    }

def generate_svg(stats):
    """根据统计数据绘制并保存 SVG 矢量图"""
    # 颜色主题：Tokyonight 风格，与主页其他组件保持一致
    bg_color = "#1a1b27"     # 深色背景
    title_color = "#7aa2f7"  # 标题蓝
    label_color = "#bb9af7"  # 标签紫
    value_color = "#9ece6a"  # 数值绿
    line_color = "#444b6a"   # 分割线
    
    svg = f"""<svg width="450" height="180" viewBox="0 0 450 180" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .header {{ font: bold 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {title_color}; }}
        .stat {{ font: bold 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {label_color}; }}
        .value {{ font: normal 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {value_color}; }}
        .rank {{ font: bold 32px 'Segoe UI', Ubuntu, Sans-Serif; fill: {title_color}; }}
    </style>
    
    <!-- 卡片背景 -->
    <rect width="450" height="180" rx="10" fill="{bg_color}" stroke="{line_color}" stroke-width="1"/>
    
    <!-- 标题部分 -->
    <text x="25" y="35" class="header">{USERNAME}'s GitHub Stats</text>
    <line x1="25" y1="45" x2="425" y2="45" stroke="{line_color}" />
    
    <!-- 统计详情 -->
    <g transform="translate(25, 75)">
        <text x="0" y="0" class="stat">⭐ Total Stars:</text>
        <text x="140" y="0" class="value">{stats['stars']}</text>
        
        <text x="0" y="30" class="stat">📝 Total Commits:</text>
        <text x="140" y="30" class="value">{stats['commits']}</text>
        
        <text x="0" y="60" class="stat">📦 Public Repos:</text>
        <text x="140" y="60" class="value">{stats['repos']}</text>
        
        <text x="0" y="90" class="stat">👥 Followers:</text>
        <text x="140" y="90" class="value">{stats['followers']}</text>
    </g>
    
    <!-- 环形 Rank 装饰 (A++) -->
    <circle cx="350" cy="110" r="40" stroke="{line_color}" stroke-width="6" fill="none" />
    <circle cx="350" cy="110" r="40" stroke="{title_color}" stroke-width="6" fill="none" 
            stroke-dasharray="180 251" stroke-linecap="round" transform="rotate(-90 350 110)" />
    <text x="350" y="122" class="rank" text-anchor="middle">A++</text>
</svg>"""

    # 将生成的 SVG 内容写入文件
    with open("github_stats.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    try:
        print(f"正在获取 {USERNAME} 的统计数据...")
        data = fetch_stats()
        generate_svg(data)
        print("成功生成 github_stats.svg！")
    except Exception as e:
        print(f"运行过程中出错: {e}")
