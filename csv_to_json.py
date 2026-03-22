import csv
import json
import os

base = os.path.dirname(__file__)
in_path = os.path.join(base, "data", "majors_v2.csv")
out_path = os.path.join(base, "data", "majors.json")

result = []
with open(in_path, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["专业名称"].strip()
        if not name:
            continue
        # personality: "系统/创造" → ["系统", "创造"]
        personality = [p.strip() for p in row["推荐人格"].split("/") if p.strip()]
        entry = {
            "name": name,
            "alias": row["别名"].strip(),
            "ai_score": int(row["AI生存分"]) if row["AI生存分"] else 0,
            "ai_reason": row["AI生存理由"].strip(),
            "window_score": float(row["window_score"]) if row["window_score"] else 0.0,
            "policy_score": int(row["policy_score"]) if row["policy_score"] else 0,
            "intl_score": int(row["intl_score"]) if row["intl_score"] else 0,
            "employ_score": int(row["employ_score"]) if row["employ_score"] else 0,
            "salary_score": int(row["salary_score"]) if row["salary_score"] else 0,
            "talent_score": int(row["talent_score"]) if row["talent_score"] else 0,
            "window_note": row["window_note"].strip(),
            "personality": personality,
            "rationale": row["推荐理由"].strip(),
            "pitfall": row["避坑点"].strip(),
            "last_updated": row["last_updated"].strip(),
        }
        result.append(entry)

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"已生成：{out_path}，共 {len(result)} 条")
print("\n前3条预览：")
for item in result[:3]:
    print(f"  {item['name']}: window_score={item['window_score']}, personality={item['personality']}")
