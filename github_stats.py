import os
import requests
import datetime

# 配置部分
USERNAME = "ZXJC-niusile"  # 你的 GitHub 用户名
TOKEN = os.environ.get("GH_TOKEN") # 从环境变量获取 Token
OUTPUT_FILE = "github_stats.svg" # 输出文件名

def get_data():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    # 使用 GraphQL 查询获取更精准的数据（包括总贡献、Star 数等）
    query = """
    query($login: String!) {
      user(login: $login) {
        name
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          nodes {
            stargazers {
              totalCount
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    response = requests.post("https://api.github.com/graphql", json={'query': query, 'variables': {'login': USERNAME}}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code}")
    return response.json()

def calculate_stats(data):
    user = data['data']['user']
    
    # 计算总 Star 数
    total_stars = sum(repo['stargazers']['totalCount'] for repo in user['repositories']['nodes'])
    
    # 贡献数据
    contrib = user['contributionsCollection']
    total_commits = contrib['totalCommitContributions']
    total_prs = contrib['totalPullRequestContributions']
    total_issues = contrib['totalIssueContributions']
    total_contributions = contrib['contributionCalendar']['totalContributions']
    
    # 计算当前连胜 (Current Streak)
    # 倒序遍历日历
    streak = 0
    calendar = contrib['contributionCalendar']['weeks']
    today = datetime.date.today()
    found_start = False
    
    # 扁平化所有天数并倒序
    all_days = []
    for week in calendar:
        for day in week['contributionDays']:
            all_days.append(day)
    
    # 从最后一天（今天或昨天）开始往前数
    for day in reversed(all_days):
        date_obj = datetime.datetime.strptime(day['date'], "%Y-%m-%d").date()
        if date_obj > today: continue # 排除未来（时区差异）
        
        count = day['contributionCount']
        
        # 如果还没开始计数，且今天没提交，允许从昨天算起
        if not found_start:
            if count > 0:
                found_start = True
                streak += 1
            elif (today - date_obj).days > 1:
                # 超过一天没提交，Streak 断了
                break
        else:
            if count > 0:
                streak += 1
            else:
                break
                
    return {
        "stars": total_stars,
        "commits": total_commits,
        "prs": total_prs,
        "issues": total_issues,
        "contribs": total_contributions,
        "streak": streak
    }

def create_svg(stats):
    # 这里是一个简单的 SVG 模板，仿照了常见的 Dark Mode 风格
    svg_content = f"""
    <svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg">
        <style>
            .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #2f80ed; }}
            .stat {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #fff; }}
            .label {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #9f9f9f; }}
            .bg {{ fill: #1a1b27; stroke: #e4e2e2; stroke-opacity: 0.5; }}
        </style>
        <rect x="0.5" y="0.5" width="494" height="194" rx="4.5" class="bg" stroke-width="1"/>
        <text x="25" y="35" class="header">{USERNAME}'s GitHub Stats</text>
        
        <g transform="translate(25, 80)">
             <text x="0" y="0" class="label">Total Stars:</text>
             <text x="100" y="0" class="stat">{stats['stars']}</text>
        </g>
        <g transform="translate(25, 110)">
             <text x="0" y="0" class="label">Total Commits:</text>
             <text x="100" y="0" class="stat">{stats['commits']}</text>
        </g>
        <g transform="translate(25, 140)">
             <text x="0" y="0" class="label">Total PRs:</text>
             <text x="100" y="0" class="stat">{stats['prs']}</text>
        </g>
        
        <g transform="translate(250, 80)">
             <text x="0" y="0" class="label">Total Contribs:</text>
             <text x="110" y="0" class="stat">{stats['contribs']}</text>
        </g>
        <g transform="translate(250, 110)">
             <text x="0" y="0" class="label">Current Streak:</text>
             <text x="110" y="0" class="stat">{stats['streak']} Days</text>
        </g>
        <g transform="translate(250, 140)">
             <text x="0" y="0" class="label">Total Issues:</text>
             <text x="110" y="0" class="stat">{stats['issues']}</text>
        </g>
    </svg>
    """
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    data = get_data()
    stats = calculate_stats(data)
    create_svg(stats)
    print("Stats SVG generated successfully.")
