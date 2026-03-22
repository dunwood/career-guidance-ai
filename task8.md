# 任务：两项——报告摘要 + 家庭问卷升级

---

## 第一部分：报告摘要

### 目标
每个专业卡片里，在「生成完整报告」按钮上方，先显示一句话AI摘要。
摘要在结果计算完成后自动生成（不需要用户点击），显示为灰色小字。
点击「生成完整报告」才弹出完整1500字报告。

### 摘要生成逻辑

在 renderResults() 完成后，对排名前5的专业自动调用 DeepSeek 生成摘要。

```javascript
async function generateSummary(major, profile) {
  const hollandName = { R:'实用型', I:'研究型', A:'艺术型', S:'社会型', E:'企业型', C:'常规型' };
  const primaryName = hollandName[profile.primary] || '';

  const prompt = `用一句话（30字以内）总结这个专业对该学生的适合度。
专业：${major.name}
AI生存分：${major.aiScore}/10
窗口期分：${major.window_score}/10
人格匹配：${major.personalityScore}/10
学生类型：${primaryName}
只输出这一句话，不要任何其他内容。`;

  try {
    const apiKey = state.apiKey || localStorage.getItem('deepseek_api_key');
    if (!apiKey) return null;

    const res = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 100
      })
    });
    const data = await res.json();
    return data.choices[0].message.content.trim();
  } catch(e) { return null; }
}
```

### 摘要展示位置

在每个专业卡片的 major-detail 文字下方、btn-report 按钮上方，加入：

```html
<div class="major-summary" id="summary-${major_name}">
  <span class="summary-dot">···</span>
</div>
```

摘要生成后更新内容：
```javascript
const el = document.getElementById(`summary-${major.name}`);
if (el && summary) el.innerHTML = `💬 ${summary}`;
```

CSS：
```css
.major-summary {
  font-size:13px; color:var(--muted); line-height:1.7;
  padding:8px 0; min-height:28px;
  border-top:1px solid var(--border); margin-top:10px;
}
.summary-dot { letter-spacing:3px; animation: pulse 1.2s infinite; }
@keyframes pulse { 0%,100%{opacity:.3} 50%{opacity:1} }
```

---

## 第二部分：家庭问卷升级

### 现有5题（保留，只微调文字）

题目1（经济能力）— 保持不变
题目2（父母行业）— 增加一个选项：「政府/公务员/事业单位」value="gov"
题目3（风险偏好）— 保持不变
题目4（城市）— 保持不变
题目5（时间偏好）— 保持不变

### 新增3题（加在现有5题后面）

题目6：
```javascript
{
  text: "孩子未来是否考虑出国发展或留学深造？",
  options: [
    { text: "不考虑，希望留在国内", value: 1 },
    { text: "可能考虑，看情况", value: 2 },
    { text: "明确希望出国留学或工作", value: 3 }
  ], key: "abroad"
}
```

题目7：
```javascript
{
  text: "家里对孩子选专业最看重什么？",
  options: [
    { text: "就业稳定，饿不死", value: "stable" },
    { text: "收入高，有钱途", value: "income" },
    { text: "有意义，孩子喜欢", value: "interest" },
    { text: "有社会地位，体面", value: "status" }
  ], key: "priority"
}
```

题目8：
```javascript
{
  text: "孩子有没有明确说过「绝对不想做」的工作类型？",
  options: [
    { text: "没有，比较开放", value: "open" },
    { text: "不想坐办公室，喜欢动手或户外", value: "no_office" },
    { text: "不想做销售或需要大量社交的工作", value: "no_social" },
    { text: "不想做重复性的工作，想有创造空间", value: "no_routine" }
  ], key: "avoid"
}
```

### 把新增字段接入 calcFamilyScore

在 calcFamilyScore 函数里加入新字段的权重逻辑：

```javascript
// 出国意愿
const abroadVal = f.abroad || 1;
if (abroadVal === 3 && m.city === 't3') score -= 1; // 想出国但专业国际化程度低
if (abroadVal === 3 && m.intl_score >= 8) score += 1; // 想出国且国际趋势好

// 家庭优先级
if (f.priority === 'stable' && m.stability === 'H') score += 1.5;
if (f.priority === 'stable' && m.stability === 'L') score -= 1.5;
if (f.priority === 'income' && major.window_score >= 8) score += 1;
if (f.priority === 'interest') score += 0; // 中性，由人格匹配决定

// 排除厌恶
if (f.avoid === 'no_social' && m.social_demand === 'high') score -= 2;
if (f.avoid === 'no_office' && m.social_demand === 'low') score -= 1;
if (f.avoid === 'no_routine' && m.holland_primary && m.holland_primary.includes('C')) score -= 1.5;
```

### 更新进度条
家庭问卷从5题变8题，进度条百分比从 (i+1)/5 改为 (i+1)/8

---

## 最后：测试
1. 结果出来后，前5个专业卡片自动出现摘要文字
2. 家庭问卷显示8题
3. 新增字段影响家庭适配分（可用不同答案测试对比）
4. 确认正常后 git push
