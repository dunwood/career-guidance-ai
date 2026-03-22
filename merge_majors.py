import csv
import os

base = os.path.dirname(__file__)

# Read majors.csv
majors = []
with open(os.path.join(base, "data", "majors.csv"), encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        majors.append(row)

# Read window_scores.csv into a dict keyed by 专业名称
scores = {}
with open(os.path.join(base, "data", "window_scores.csv"), encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["专业名称"].strip()
        if name:
            scores[name] = row

# Merge
output_fields = [
    "专业名称", "别名", "AI生存分", "AI生存理由",
    "window_score", "policy_score", "intl_score", "employ_score",
    "salary_score", "talent_score", "window_note",
    "推荐人格", "推荐理由", "避坑点", "last_updated"
]

merged = []
for row in majors:
    name = row["专业名称"].strip()
    s = scores.get(name, {})

    if s:
        p = float(s["policy_score"])
        i = float(s["intl_score"])
        e = float(s["employ_score"])
        sa = float(s["salary_score"])
        t = float(s["talent_score"])
        window_score = round(p * 0.35 + i * 0.25 + e * 0.20 + sa * 0.10 + t * 0.10, 1)
        new_row = {
            "专业名称": name,
            "别名": row["别名"],
            "AI生存分": row["AI生存分"],
            "AI生存理由": row["AI生存理由"],
            "window_score": window_score,
            "policy_score": s["policy_score"],
            "intl_score": s["intl_score"],
            "employ_score": s["employ_score"],
            "salary_score": s["salary_score"],
            "talent_score": s["talent_score"],
            "window_note": s["window_note"],
            "推荐人格": row["推荐人格"],
            "推荐理由": row["推荐理由"],
            "避坑点": row["避坑点"],
            "last_updated": row["last_updated"],
        }
    else:
        new_row = {
            "专业名称": name,
            "别名": row["别名"],
            "AI生存分": row["AI生存分"],
            "AI生存理由": row["AI生存理由"],
            "window_score": 0,
            "policy_score": "",
            "intl_score": "",
            "employ_score": "",
            "salary_score": "",
            "talent_score": "",
            "window_note": "",
            "推荐人格": row["推荐人格"],
            "推荐理由": row["推荐理由"],
            "避坑点": row["避坑点"],
            "last_updated": row["last_updated"],
        }
    merged.append(new_row)

# Save
out_path = os.path.join(base, "data", "majors_v2.csv")
with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output_fields)
    writer.writeheader()
    writer.writerows(merged)

print(f"已保存：{out_path}，共 {len(merged)} 条记录\n")
print("前5行预览：")
print(",".join(output_fields))
for row in merged[:5]:
    print(",".join(str(row[k]) for k in output_fields))
