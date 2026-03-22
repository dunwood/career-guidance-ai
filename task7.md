# 任务：两项合并——可折叠子维度 + 长报告功能

---

## 第一部分：四个主维度点击展开子维度

结果卡片里四个评分格（AI生存、窗口期、家庭适配、人格匹配）
每个都可以点击展开子维度明细，默认折叠，点击展开/收起。

### 窗口期子维度（已有数据）
展示5条进度条：政策信号、国际趋势、就业信号、薪资信号、人才缺口

### AI生存子维度
- 核心工作性质：识别模式 or 处理例外
- AI替代风险：高/中/低（ai_score <4高，4-7中，>7低）
- 人类护城河：显示 ai_reason 字段内容

### 家庭适配子维度
从用户填写的家庭问卷结果展示：
- 经济支持：充足/一般/有压力
- 行业资源：有匹配/无匹配
- 风险偏好：保守/中性/进取
- 城市匹配：匹配/不匹配
- 时间规划：适合/需权衡

### 人格匹配子维度
- 主导型：如「研究型(I)」
- 次导型：如「实用型(R)」
- 社交能量：内向/外向（根据ei值）
- 决策风格：逻辑思维/情感导向（根据tf值）
- 匹配说明：一句话

### 交互
- 点击评分格展开/收起
- 右上角显示 ▼/▲
- 展开动画 max-height transition 0.3s
- 删除之前窗口期格外面单独显示的5条进度条

### CSS
```css
.score-item { cursor:pointer; position:relative; }
.score-expand-icon { position:absolute; top:8px; right:8px; font-size:10px; color:var(--muted); }
.score-sub { max-height:0; overflow:hidden; transition:max-height 0.3s ease; }
.score-sub.open { max-height:300px; }
.sub-row { display:flex; align-items:center; justify-content:space-between; font-size:12px; color:var(--muted); padding:4px 0; border-bottom:1px solid var(--border); }
.sub-row:last-child { border-bottom:none; }
.sub-label { min-width:60px; }
.sub-bar { flex:1; height:3px; background:var(--border); border-radius:2px; margin:0 8px; position:relative; }
.sub-bar-fill { position:absolute; left:0; top:0; height:100%; background:var(--accent3); border-radius:2px; }
.sub-val { min-width:20px; text-align:right; }
```

---

## 第二部分：长报告功能

### 2.1 每个专业卡片底部加按钮
```html
<button class="btn-report" onclick="generateReport('${major_name}')">
  📄 生成完整职业规划报告
</button>
```

```css
.btn-report {
  width:100%; padding:12px; margin-top:12px;
  background:transparent; border:1.5px solid var(--accent3);
  border-radius:12px; color:var(--accent3);
  font-size:14px; font-family:'Noto Serif SC',serif;
  cursor:pointer; transition:all .2s;
}
.btn-report:hover { background:rgba(0,229,255,0.08); }
```

### 2.2 调用 DeepSeek API 生成报告

```javascript
async function generateReport(majorName) {
  const major = Object.values(state.majorsDB).find(m => m.name === majorName);
  if (!major) return;

  showReportModal('loading');

  const profile = state.personalityProfile || {};
  const hollandName = { R:'实用型', I:'研究型', A:'艺术型', S:'社会型', E:'企业型', C:'常规型' };
  const primaryName = hollandName[profile.primary] || '未知';

  const prompt = `你是一位专业的职业规划顾问，请为以下学生生成一份详细的职业规划报告。

## 学生基本信息
- 分数段：${state.scoreRange}
- 科目：${state.subject}
- 人格主导型：${primaryName}
- 社交能量：${(profile.ei||0) > 0 ? '偏外向' : '偏内向'}
- 决策风格：${(profile.tf||0) > 0 ? '逻辑思维型' : '情感导向型'}

## 目标专业：${majorName}

## 专业评分数据
- AI生存分：${major.ai_score}/10（${major.ai_reason}）
- 窗口期综合分：${major.window_score}/10
  - 政策信号：${major.policy_score}/10
  - 国际趋势：${major.intl_score}/10
  - 就业信号：${major.employ_score}/10
  - 薪资信号：${major.salary_score}/10
  - 人才缺口：${major.talent_score}/10
- 窗口期说明：${major.window_note}
- 避坑提示：${major.pitfall}

## 报告要求
请生成一份约1500字的职业规划报告，包含以下六个部分：

1. **专业概览**（200字）：这个专业学什么，毕业后做什么
2. **AI时代生存分析**（250字）：结合AI生存分，分析这个专业在AI时代的价值和风险
3. **行业窗口期判断**（250字）：结合五维数据，分析国内外趋势，判断现在入场是否合适
4. **个人匹配度分析**（250字）：结合学生人格特质，分析适合度和潜在挑战
5. **职业发展路径**（300字）：毕业后1年、3年、5年、10年的典型发展路径
6. **行动建议**（250字）：在校期间重点培养哪些能力，避开哪些坑

语言要求：直接有判断，用数据支撑，对学生说话，结尾给明确总结建议`;

  try {
    const apiKey = state.apiKey || localStorage.getItem('deepseek_api_key');
    if (!apiKey) { showReportModal('no-key'); return; }

    const res = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 3000
      })
    });

    const data = await res.json();
    const report = data.choices[0].message.content;
    showReportModal('content', majorName, report);

  } catch(e) {
    showReportModal('error');
  }
}
```

### 2.3 Modal JS

```javascript
function showReportModal(status, majorName='', content='') {
  let modal = document.getElementById('reportModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'reportModal';
    document.body.appendChild(modal);
  }

  if (status === 'loading') {
    modal.innerHTML = `
      <div class="modal-overlay" onclick="closeReportModal()">
        <div class="modal-box" onclick="event.stopPropagation()">
          <div class="modal-loading">
            <div class="modal-spinner"></div>
            <p>正在生成报告，约需15秒…</p>
          </div>
        </div>
      </div>`;
  } else if (status === 'content') {
    modal.innerHTML = `
      <div class="modal-overlay" onclick="closeReportModal()">
        <div class="modal-box" onclick="event.stopPropagation()">
          <div class="modal-header">
            <div class="modal-title">📄 ${majorName} 职业规划报告</div>
            <div class="modal-actions">
              <button class="modal-btn" onclick="copyReport()">复制全文</button>
              <button class="modal-btn modal-close" onclick="closeReportModal()">✕ 关闭</button>
            </div>
          </div>
          <div class="modal-content" id="reportContent">${content.replace(/\n/g,'<br>').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')}</div>
        </div>
      </div>`;
  } else if (status === 'no-key') {
    modal.innerHTML = `
      <div class="modal-overlay" onclick="closeReportModal()">
        <div class="modal-box" onclick="event.stopPropagation()">
          <div class="modal-loading">
            <p>请先填写 DeepSeek API Key</p>
            <button class="btn" style="margin-top:16px" onclick="closeReportModal()">关闭</button>
          </div>
        </div>
      </div>`;
  } else {
    modal.innerHTML = `
      <div class="modal-overlay" onclick="closeReportModal()">
        <div class="modal-box" onclick="event.stopPropagation()">
          <div class="modal-loading">
            <p>生成失败，请检查网络或 API Key</p>
            <button class="btn" style="margin-top:16px" onclick="closeReportModal()">关闭</button>
          </div>
        </div>
      </div>`;
  }

  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';
}

function closeReportModal() {
  const modal = document.getElementById('reportModal');
  if (modal) modal.style.display = 'none';
  document.body.style.overflow = '';
}

function copyReport() {
  const content = document.getElementById('reportContent');
  if (!content) return;
  navigator.clipboard.writeText(content.innerText).then(() => {
    const btn = document.querySelector('.modal-btn');
    if (btn) { btn.textContent = '✓ 已复制'; setTimeout(() => btn.textContent = '复制全文', 2000); }
  });
}
```

### 2.4 Modal CSS

```css
#reportModal { display:none; position:fixed; inset:0; z-index:1000; }
.modal-overlay {
  position:fixed; inset:0; background:rgba(0,0,0,0.85);
  display:flex; align-items:flex-end; justify-content:center;
}
@media (min-width:600px) { .modal-overlay { align-items:center; } }
.modal-box {
  background:var(--surface); border-radius:20px 20px 0 0;
  width:100%; max-width:600px; max-height:90vh;
  display:flex; flex-direction:column; overflow:hidden;
}
@media (min-width:600px) { .modal-box { border-radius:20px; max-height:85vh; } }
.modal-header {
  display:flex; justify-content:space-between; align-items:center;
  padding:16px 20px; border-bottom:1px solid var(--border);
  position:sticky; top:0; background:var(--surface); z-index:1; flex-shrink:0;
}
.modal-title { font-size:15px; font-weight:700; }
.modal-actions { display:flex; gap:8px; }
.modal-btn {
  padding:7px 14px; border-radius:8px;
  border:1px solid var(--border); background:transparent;
  color:var(--muted); font-size:13px;
  font-family:'Noto Serif SC',serif; cursor:pointer;
}
.modal-close { border-color:var(--accent); color:var(--accent); }
.modal-content {
  padding:20px; overflow-y:auto;
  font-size:15px; line-height:1.9; color:var(--text); flex:1;
}
.modal-content strong { color:var(--accent2); }
.modal-loading { padding:60px 20px; text-align:center; color:var(--muted); font-size:15px; }
.modal-spinner {
  width:32px; height:32px; border-radius:50%;
  border:3px solid var(--border); border-top-color:var(--accent3);
  animation:spin 0.8s linear infinite; margin:0 auto 16px;
}
@keyframes spin { to { transform:rotate(360deg); } }
```

---

## 最后：测试清单
1. 点击四个评分格，确认都能展开/收起
2. 点击「生成完整报告」，Modal 弹出显示加载动画
3. 手机端（窄屏）Modal 从底部弹出，Web端居中显示
4. 复制全文按钮正常工作
5. 确认正常后执行 git push
