import os
import requests
import csv

# Read API key from env file
env_path = os.path.join(os.path.dirname(__file__), "env")
api_key = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
            break

if not api_key:
    raise ValueError("DEEPSEEK_API_KEY not found in env file")

prompt = """你是一个职业规划数据分析师。请为以下50个中国大学专业，对「窗口期」维度打分。

评分标准：
- policy_score（政策信号1-10）：中国政府政策对该行业的支持力度
- intl_score（国际趋势1-10）：10=国外刚爆发中国刚起步（黄金窗口），8=国外成熟中国上升，6=国外中国同步，4=国外饱和中国跟着饱和，2=双双衰退
- employ_score（就业信号1-10）：近3年毕业生就业率和对口率
- salary_score（薪资信号1-10）：近3年起薪增长趋势
- talent_score（人才缺口1-10）：招聘需求增长 vs 毕业生供给比

输出格式（纯CSV，无表头，无其他文字）：
专业名称,policy_score,intl_score,employ_score,salary_score,talent_score,window_note

专业列表：
计算机科学与技术,人工智能,软件工程,数据科学与大数据技术,网络安全,电子信息工程,通信工程,自动化,机械工程,土木工程,建筑学,化学工程与工艺,生物工程,环境科学与工程,材料科学与工程,电气工程及其自动化,新能源科学与工程,智能制造工程,临床医学,口腔医学,药学,护理学,中医学,生物医学工程,公共卫生与预防医学,工商管理,金融学,会计学,经济学,国际经济与贸易,市场营销,人力资源管理,电子商务,物流管理,法学,心理学,社会工作,教育学,学前教育,汉语言文学,英语,翻译,新闻传播学,视觉传达设计,产品设计,数字媒体艺术,历史学,哲学,数字经济,金融科技"""

response = requests.post(
    "https://api.deepseek.com/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    },
    timeout=120,
)

response.raise_for_status()
content = response.json()["choices"][0]["message"]["content"].strip()

# Print to terminal
print("=== API 返回内容 ===")
print(content)
print("===================")

# Save to data/window_scores.csv with header
output_path = os.path.join(os.path.dirname(__file__), "data", "window_scores.csv")
with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
    f.write("专业名称,policy_score,intl_score,employ_score,salary_score,talent_score,window_note\n")
    f.write(content + "\n")

print(f"\n已保存到: {output_path}")
