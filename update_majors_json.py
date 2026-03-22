import json, os

base = os.path.dirname(__file__)
path = os.path.join(base, "data", "majors.json")

with open(path, encoding="utf-8") as f:
    data = json.load(f)

# score_tier mapping
score_tier_map = {
    **{k: 1 for k in ["社会工作","历史学","哲学","学前教育","护理学"]},
    **{k: 2 for k in ["汉语言文学","教育学","翻译","新闻传播学","市场营销",
                       "人力资源管理","物流管理","视觉传达设计","产品设计","数字媒体艺术"]},
    **{k: 3 for k in ["英语","法学","心理学","工商管理","会计学","经济学",
                       "国际经济与贸易","电子商务","中医学","公共卫生与预防医学",
                       "环境科学与工程","化学工程与工艺","生物工程","土木工程","建筑学"]},
    **{k: 4 for k in ["软件工程","数据科学与大数据技术","通信工程","自动化","机械工程",
                       "材料科学与工程","电气工程及其自动化","新能源科学与工程","智能制造工程",
                       "药学","金融学","电子信息工程","数字经济","金融科技"]},
    **{k: 5 for k in ["计算机科学与技术","人工智能","网络安全","临床医学","口腔医学","生物医学工程"]},
}

# holland + social/empathy mapping
holland_map = {
    "计算机科学与技术": (["I","R"], "low", "low"),
    "人工智能":          (["I","R"], "low", "low"),
    "软件工程":          (["I","R"], "low", "low"),
    "数据科学与大数据技术": (["I","C"], "low", "low"),
    "网络安全":          (["I","R"], "low", "low"),
    "电子信息工程":      (["I","R"], "low", "low"),
    "通信工程":          (["I","R"], "low", "low"),
    "自动化":            (["I","R"], "low", "low"),
    "机械工程":          (["R","I"], "low", "low"),
    "土木工程":          (["R","C"], "mid", "low"),
    "建筑学":            (["A","R"], "mid", "mid"),
    "化学工程与工艺":    (["I","R"], "low", "low"),
    "生物工程":          (["I","R"], "low", "low"),
    "环境科学与工程":    (["I","R"], "low", "low"),
    "材料科学与工程":    (["I","R"], "low", "low"),
    "电气工程及其自动化":(["R","I"], "low", "low"),
    "新能源科学与工程":  (["I","R"], "low", "low"),
    "智能制造工程":      (["R","I"], "low", "low"),
    "临床医学":          (["I","S"], "high","high"),
    "口腔医学":          (["R","I"], "high","mid"),
    "药学":              (["I","C"], "low", "low"),
    "护理学":            (["S","R"], "high","high"),
    "中医学":            (["I","S"], "high","high"),
    "生物医学工程":      (["I","R"], "low", "low"),
    "公共卫生与预防医学":(["I","S"], "mid", "mid"),
    "工商管理":          (["E","C"], "high","mid"),
    "金融学":            (["C","I"], "mid", "low"),
    "会计学":            (["C","I"], "low", "low"),
    "经济学":            (["I","C"], "low", "low"),
    "国际经济与贸易":    (["E","C"], "mid", "low"),
    "市场营销":          (["E","A"], "high","mid"),
    "人力资源管理":      (["S","E"], "high","high"),
    "电子商务":          (["E","C"], "mid", "low"),
    "物流管理":          (["C","E"], "mid", "low"),
    "法学":              (["E","I"], "high","mid"),
    "心理学":            (["I","S"], "mid", "high"),
    "社会工作":          (["S","E"], "high","high"),
    "教育学":            (["S","A"], "high","high"),
    "学前教育":          (["S","A"], "high","high"),
    "汉语言文学":        (["A","I"], "low", "mid"),
    "英语":              (["S","A"], "high","mid"),
    "翻译":              (["A","C"], "low", "mid"),
    "新闻传播学":        (["A","E"], "high","mid"),
    "视觉传达设计":      (["A","R"], "low", "mid"),
    "产品设计":          (["A","R"], "mid", "mid"),
    "数字媒体艺术":      (["A","I"], "low", "mid"),
    "历史学":            (["I","A"], "low", "low"),
    "哲学":              (["I","A"], "low", "mid"),
    "数字经济":          (["I","E"], "mid", "low"),
    "金融科技":          (["I","C"], "low", "low"),
}

for item in data:
    name = item["name"]
    item["score_tier"] = score_tier_map.get(name, 3)
    h = holland_map.get(name)
    if h:
        item["holland_primary"] = h[0]
        item["social_demand"]   = h[1]
        item["empathy_demand"]  = h[2]
    else:
        item["holland_primary"] = ["I","R"]
        item["social_demand"]   = "mid"
        item["empathy_demand"]  = "low"

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"更新完成，共 {len(data)} 条")
# 验证几条
for item in data[:3]:
    print(f"  {item['name']}: score_tier={item['score_tier']}, holland={item['holland_primary']}, social={item['social_demand']}")
