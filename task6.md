# 任务：三项合并修复

## 修复一：高分学生不推荐低门槛专业

在 index.html 的 runCalculation 函数里找到 scorePenalty 计算部分，改为双向惩罚：

```javascript
const SCORE_MAP = {'700+':5,'650-700':4,'600-650':3,'550-600':2,'500-550':1,'<500':1};
const studentScore = SCORE_MAP[state.scoreRange] || 2;
const scoreTier = m.score_tier || 3;
// 双向惩罚：分数不够扣分，分数远超门槛也扣分
const scorePenalty = Math.max(0, (scoreTier - studentScore)) * 2   // 分数不够
                   + Math.max(0, (studentScore - scoreTier) - 1) * 1.5; // 分数远超（允许1档误差）
```

同时确认 majors.json 里每个专业有 score_tier 字段，参考值如下：

score_tier=1：社会工作, 历史学, 哲学, 学前教育, 护理学
score_tier=2：汉语言文学, 教育学, 翻译, 新闻传播学, 市场营销, 人力资源管理, 物流管理, 视觉传达设计, 产品设计, 数字媒体艺术
score_tier=3：英语, 法学, 心理学, 工商管理, 会计学, 经济学, 国际经济与贸易, 电子商务, 中医学, 公共卫生与预防医学, 环境科学与工程, 化学工程与工艺, 生物工程, 土木工程, 建筑学
score_tier=4：软件工程, 数据科学与大数据技术, 通信工程, 自动化, 机械工程, 材料科学与工程, 电气工程及其自动化, 新能源科学与工程, 智能制造工程, 药学, 金融学, 电子信息工程, 数字经济, 金融科技
score_tier=5：计算机科学与技术, 人工智能, 网络安全, 临床医学, 口腔医学, 生物医学工程

---

## 修复二：升级人格测评系统

### 2.1 替换人格问卷题目

删除原来的 PERSONALITY_QS 数组，替换为以下15题（霍兰德主框架 + MBTI E/I 和 T/F 辅助）：

```javascript
const PERSONALITY_QS = [
  // 霍兰德 R 实用型
  {
    q: "周末你更享受哪种活动？",
    opts: ["动手组装或修理东西", "读书研究一个感兴趣的问题", "参加聚会认识新朋友", "构思一个创意项目"]
  },
  // 霍兰德 I 研究型
  {
    q: "遇到一个复杂问题，你的第一反应是？",
    opts: ["拆解成步骤逐一解决", "查资料搞清楚底层原理", "找人讨论集思广益", "凭直觉找到突破口"]
  },
  // 霍兰德 S 社会型
  {
    q: "在团队里你最享受哪个角色？",
    opts: ["执行具体任务的人", "分析数据提供方案的人", "协调沟通连接大家的人", "提出新方向的人"]
  },
  // 霍兰德 E 企业型
  {
    q: "以下哪种成就感对你最重要？",
    opts: ["把一件事做到极致完美", "搞清楚一个没人懂的问题", "帮助别人解决了难题", "说服别人接受了你的想法"]
  },
  // 霍兰德 A 艺术型
  {
    q: "做一个项目时你更在意？",
    opts: ["流程规范结果可靠", "逻辑严密数据准确", "过程中人与人的配合", "最终呈现是否有创意"]
  },
  // 霍兰德 C 常规型
  {
    q: "哪种工作方式让你最有安全感？",
    opts: ["有明确规则和流程可以遵循", "有大量资料可以深入研究", "有团队一起面对挑战", "有足够自由发挥空间"]
  },
  // MBTI E/I 外向内向
  {
    q: "一天高强度社交后，你通常感觉？",
    opts: ["有点累但很充实", "很疲惫需要独处恢复", "还好，无所谓", "取决于跟谁在一起"]
  },
  // MBTI E/I
  {
    q: "你更擅长哪种沟通方式？",
    opts: ["当面交流，反应快", "深思熟虑后书面表达", "两种都可以", "看场合"]
  },
  // MBTI T/F 思维情感
  {
    q: "朋友向你倾诉烦恼，你的第一反应是？",
    opts: ["帮他分析问题找解决方案", "先共情听他说完再说", "两者结合", "给他讲道理"]
  },
  // MBTI T/F
  {
    q: "做决定时你更依赖？",
    opts: ["数据和逻辑分析", "直觉和个人感受", "他人的意见和建议", "规则和先例"]
  },
  // 压力耐受
  {
    q: "面对紧急截止日期，你通常？",
    opts: ["压力下反而效率更高", "提前规划避免这种情况", "有些焦虑但能完成", "很难受，影响发挥"]
  },
  // 工作节奏
  {
    q: "你理想的工作节奏是？",
    opts: ["快节奏、多变化、充满挑战", "有规律、可预期、稳步推进", "项目制，忙完有长假", "弹性自由，自己安排"]
  },
  // 成就动机
  {
    q: "什么最能驱动你持续投入一件事？",
    opts: ["看到成果带来的实际影响", "不断突破认知边界的快感", "被人需要和认可的满足感", "创造出前所未有的东西"]
  },
  // 独立vs协作
  {
    q: "你更喜欢哪种工作状态？",
    opts: ["独立深度工作，自己做决定", "小团队紧密协作", "大团队各司其职", "灵活切换都行"]
  },
  // 长期规划
  {
    q: "对于职业发展，你更倾向？",
    opts: ["在一个领域深耕成为专家", "跨领域积累成为多面手", "管理团队做领导者", "创业或做独立的事"]
  }
];
```

### 2.2 升级人格计算逻辑

删除原来的 calcPersonalityScore 函数，替换为：

```javascript
function calcPersonalityProfile(answers) {
  // 霍兰德六型得分
  const holland = { R:0, I:0, A:0, S:0, E:0, C:0 };
  // MBTI 辅助维度
  let ei = 0; // 正=外向, 负=内向
  let tf = 0; // 正=思维, 负=情感

  // Q1-Q6: 霍兰德（选项顺序对应 R/I/S/E/A/C 不同题不同）
  const hollandMap = [
    ['R','I','S','A'],  // Q1
    ['R','I','S','A'],  // Q2
    ['R','I','S','A'],  // Q3
    ['R','I','S','E'],  // Q4
    ['C','I','S','A'],  // Q5
    ['C','I','S','A'],  // Q6
  ];
  for (let i=0; i<6; i++) {
    if (answers[i] !== undefined) {
      const type = hollandMap[i][answers[i]];
      if (type) holland[type]++;
    }
  }

  // Q7-Q8: E/I
  if (answers[6] === 0) ei += 2;
  if (answers[6] === 1) ei -= 2;
  if (answers[7] === 0) ei += 1;
  if (answers[7] === 1) ei -= 1;

  // Q9-Q10: T/F
  if (answers[8] === 0) tf += 2;
  if (answers[8] === 1) tf -= 2;
  if (answers[9] === 0) tf += 1;
  if (answers[9] === 1) tf -= 1;

  // 排序找主导型和次导型
  const sorted = Object.entries(holland).sort((a,b) => b[1]-a[1]);
  const primary = sorted[0][0];
  const secondary = sorted[1][0];

  return { holland, primary, secondary, ei, tf };
}

function calcPersonalityScore(m, profile) {
  const { primary, secondary, ei, tf } = profile;

  // 霍兰德匹配（主框架）
  let score = 5;
  if (m.holland_primary && m.holland_primary.includes(primary)) score += 3;
  else if (m.holland_primary && m.holland_primary.includes(secondary)) score += 1.5;

  // E/I 修正
  if (m.social_demand === 'high' && ei < 0) score -= 1.5;  // 内向不适合高社交
  if (m.social_demand === 'low' && ei > 0) score -= 0.5;   // 轻微扣分

  // T/F 修正
  if (m.empathy_demand === 'high' && tf > 0) score -= 1;   // 强思维不适合高共情
  if (m.empathy_demand === 'high' && tf < 0) score += 0.5; // 情感型加分

  return Math.max(1, Math.min(10, Math.round(score * 10) / 10));
}
```

### 2.3 更新 majors.json

在每个专业记录里加入以下字段：
- `holland_primary`: 霍兰德主型数组，如 ["I","R"] 表示研究型+实用型
- `social_demand`: "high"（大量人际互动）或 "low"（独立工作）或 "mid"
- `empathy_demand`: "high"（需要高共情）或 "low" 或 "mid"

各专业参考值：

计算机科学与技术: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
人工智能: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
软件工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
数据科学与大数据技术: holland_primary=["I","C"], social_demand="low", empathy_demand="low"
网络安全: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
电子信息工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
通信工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
自动化: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
机械工程: holland_primary=["R","I"], social_demand="low", empathy_demand="low"
土木工程: holland_primary=["R","C"], social_demand="mid", empathy_demand="low"
建筑学: holland_primary=["A","R"], social_demand="mid", empathy_demand="mid"
化学工程与工艺: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
生物工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
环境科学与工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
材料科学与工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
电气工程及其自动化: holland_primary=["R","I"], social_demand="low", empathy_demand="low"
新能源科学与工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
智能制造工程: holland_primary=["R","I"], social_demand="low", empathy_demand="low"
临床医学: holland_primary=["I","S"], social_demand="high", empathy_demand="high"
口腔医学: holland_primary=["R","I"], social_demand="high", empathy_demand="mid"
药学: holland_primary=["I","C"], social_demand="low", empathy_demand="low"
护理学: holland_primary=["S","R"], social_demand="high", empathy_demand="high"
中医学: holland_primary=["I","S"], social_demand="high", empathy_demand="high"
生物医学工程: holland_primary=["I","R"], social_demand="low", empathy_demand="low"
公共卫生与预防医学: holland_primary=["I","S"], social_demand="mid", empathy_demand="mid"
工商管理: holland_primary=["E","C"], social_demand="high", empathy_demand="mid"
金融学: holland_primary=["C","I"], social_demand="mid", empathy_demand="low"
会计学: holland_primary=["C","I"], social_demand="low", empathy_demand="low"
经济学: holland_primary=["I","C"], social_demand="low", empathy_demand="low"
国际经济与贸易: holland_primary=["E","C"], social_demand="mid", empathy_demand="low"
市场营销: holland_primary=["E","A"], social_demand="high", empathy_demand="mid"
人力资源管理: holland_primary=["S","E"], social_demand="high", empathy_demand="high"
电子商务: holland_primary=["E","C"], social_demand="mid", empathy_demand="low"
物流管理: holland_primary=["C","E"], social_demand="mid", empathy_demand="low"
法学: holland_primary=["E","I"], social_demand="high", empathy_demand="mid"
心理学: holland_primary=["I","S"], social_demand="mid", empathy_demand="high"
社会工作: holland_primary=["S","E"], social_demand="high", empathy_demand="high"
教育学: holland_primary=["S","A"], social_demand="high", empathy_demand="high"
学前教育: holland_primary=["S","A"], social_demand="high", empathy_demand="high"
汉语言文学: holland_primary=["A","I"], social_demand="low", empathy_demand="mid"
英语: holland_primary=["S","A"], social_demand="high", empathy_demand="mid"
翻译: holland_primary=["A","C"], social_demand="low", empathy_demand="mid"
新闻传播学: holland_primary=["A","E"], social_demand="high", empathy_demand="mid"
视觉传达设计: holland_primary=["A","R"], social_demand="low", empathy_demand="mid"
产品设计: holland_primary=["A","R"], social_demand="mid", empathy_demand="mid"
数字媒体艺术: holland_primary=["A","I"], social_demand="low", empathy_demand="mid"
历史学: holland_primary=["I","A"], social_demand="low", empathy_demand="low"
哲学: holland_primary=["I","A"], social_demand="low", empathy_demand="mid"
数字经济: holland_primary=["I","E"], social_demand="mid", empathy_demand="low"
金融科技: holland_primary=["I","C"], social_demand="low", empathy_demand="low"

---

## 修复三：结果卡片展示五维窗口期明细

在每个专业卡片的「窗口期」评分下面，加入可折叠的五维明细：

```html
<div class="window-detail">
  <div class="dim-bar"><span>政策信号</span><div class="bar" style="width:${policy}0%"></div><span>${policy}</span></div>
  <div class="dim-bar"><span>国际趋势</span><div class="bar" style="width:${intl}0%"></div><span>${intl}</span></div>
  <div class="dim-bar"><span>就业信号</span><div class="bar" style="width:${employ}0%"></div><span>${employ}</span></div>
  <div class="dim-bar"><span>薪资信号</span><div class="bar" style="width:${salary}0%"></div><span>${salary}</span></div>
  <div class="dim-bar"><span>人才缺口</span><div class="bar" style="width:${talent}0%"></div><span>${talent}</span></div>
</div>
```

CSS 样式：
```css
.window-detail { margin-top:10px; padding-top:10px; border-top:1px solid var(--border); }
.dim-bar { display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:12px; color:var(--muted); }
.dim-bar .bar { flex:1; height:4px; background:var(--border); border-radius:2px; position:relative; }
.dim-bar .bar::after { content:''; position:absolute; left:0; top:0; height:100%; background:var(--accent3); border-radius:2px; width:var(--w); }
```

---

## 最后：测试

修改完后用700分重新测试：
1. 护理学不应出现在强烈推荐
2. 人格问卷显示15道题
3. 结果卡片窗口期下显示五维明细

截图确认后执行 git push。
