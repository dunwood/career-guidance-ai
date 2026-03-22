# 任务：合并窗口期数据到 majors.csv

## 背景
- `data/majors.csv` 是现有专业数据，有字段：专业名称,别名,AI生存分,AI生存理由,窗口期状态,窗口期说明,推荐人格,推荐理由,避坑点,last_updated
- `data/window_scores.csv` 是新生成的窗口期五维评分数据，有字段：专业名称,policy_score,intl_score,employ_score,salary_score,talent_score,window_note

## 要求

用 Python 完成以下操作：

1. 读取两个 CSV 文件
2. 按「专业名称」字段合并
3. 删除旧的「窗口期状态」和「窗口期说明」两个字段
4. 加入新的五个字段：policy_score, intl_score, employ_score, salary_score, talent_score, window_note
5. 新增一个计算字段 window_score，公式为：
   window_score = policy_score×0.35 + intl_score×0.25 + employ_score×0.20 + salary_score×0.10 + talent_score×0.10
   结果保留一位小数
6. 最终字段顺序：
   专业名称, 别名, AI生存分, AI生存理由, window_score, policy_score, intl_score, employ_score, salary_score, talent_score, window_note, 推荐人格, 推荐理由, 避坑点, last_updated
7. 保存为 data/majors_v2.csv（不要覆盖原文件）
8. 打印合并结果前5行确认

## 注意
- 文件编码用 UTF-8-BOM
- 如果某个专业在 window_scores.csv 里找不到，window_score 填 0，其余字段填空
