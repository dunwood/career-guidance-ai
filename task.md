# 任务：生成窗口期五维评分数据

## 执行步骤

用 Python 调用 DeepSeek API，为50个中国大学专业生成窗口期五维评分数据，保存为 window_scores.csv。

## API 信息

- URL: https://api.deepseek.com/chat/completions
- Model: deepseek-chat
- Key: 见项目根目录 .env 文件的 DEEPSEEK_API_KEY

## Prompt

```
你是一个职业规划数据分析师。请为以下50个中国大学专业，对「窗口期」维度打分。

评分标准：
- policy_score（政策信号1-10）：中国政府政策对该行业的支持力度
- intl_score（国际趋势1-10）：10=国外刚爆发中国刚起步（黄金窗口），8=国外成熟中国上升，6=国外中国同步，4=国外饱和中国跟着饱和，2=双双衰退
- employ_score（就业信号1-10）：近3年毕业生就业率和对口率
- salary_score（薪资信号1-10）：近3年起薪增长趋势
- talent_score（人才缺口1-10）：招聘需求增长 vs 毕业生供给比

输出格式（纯CSV，无表头，无其他文字）：
专业名称,policy_score,intl_score,employ_score,salary_score,talent_score,window_note

专业列表：
计算机科学与技术,人工智能,软件工程,数据科学与大数据技术,网络安全,电子信息工程,通信工程,自动化,机械工程,土木工程,建筑学,化学工程与工艺,生物工程,环境科学与工程,材料科学与工程,电气工程及其自动化,新能源科学与工程,智能制造工程,临床医学,口腔医学,药学,护理学,中医学,生物医学工程,公共卫生与预防医学,工商管理,金融学,会计学,经济学,国际经济与贸易,市场营销,人力资源管理,电子商务,物流管理,法学,心理学,社会工作,教育学,学前教育,汉语言文学,英语,翻译,新闻传播学,视觉传达设计,产品设计,数字媒体艺术,历史学,哲学,数字经济,金融科技
```

## Python 脚本要求

1. 从 .env 文件读取 DEEPSEEK_API_KEY
2. 调用 DeepSeek API 发送上面的 prompt
3. 把返回结果保存为 data/window_scores.csv
4. 同时打印到终端确认

## 执行

请直接写出 Python 脚本并运行。
