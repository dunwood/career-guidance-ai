# 任务：把 majors_v2.csv 接入网页

## 背景
- `index.html` 是现有网页，专业数据目前硬编码在 JS 的 `MAJORS` 对象里
- `data/majors_v2.csv` 是新的专业数据，包含五维窗口期评分
- 目标：网页启动时从 CSV 文件读取专业数据，不再依赖硬编码

## 要求

### 第一步：把 CSV 转成 JSON
用 Python 把 `data/majors_v2.csv` 转换成 `data/majors.json`，格式如下：

```json
[
  {
    "name": "计算机科学与技术",
    "alias": "计算机/CS/软件工程/码农",
    "ai_score": 6,
    "ai_reason": "核心工作正在分层...",
    "window_score": 8.7,
    "policy_score": 9,
    "intl_score": 8,
    "employ_score": 9,
    "salary_score": 9,
    "talent_score": 8,
    "window_note": "需求量仍大但供给严重过剩...",
    "personality": ["系统", "创造"],
    "rationale": "逻辑思维强...",
    "pitfall": "警惕框架思维...",
    "last_updated": "2026-01"
  }
]
```

保存为 `data/majors.json`，编码 UTF-8。

### 第二步：修改 index.html
在 index.html 的 JS 部分：

1. 删除或注释掉原来硬编码的 `const MAJORS = {...}` 对象
2. 在页面加载时用 fetch 读取 `data/majors.json`
3. 把读取到的数据存入 `state.majorsDB`
4. 原来所有引用 `MAJORS` 的地方改为引用 `state.majorsDB`
5. 在 fetch 失败时显示错误提示「数据加载失败，请刷新重试」

### 注意
- 保持原有的四维评分计算逻辑不变
- window_score 直接用 JSON 里的值，不需要重新计算
- 备份原来的 index.html 为 index.backup.html
