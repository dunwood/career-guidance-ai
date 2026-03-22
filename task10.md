# 任务：部署到 GitHub 并让 career.zhexueyuan.com 上线

## 第一步：确认当前状态
执行以下命令：
```
git remote -v
git status
git log --oneline -3
```

## 第二步：确认所有文件都已提交
```
git add .
git status
```

如果有未提交的文件，执行：
```
git commit -m "feat: 志远v2完整版"
```

## 第三步：推送到 GitHub
```
git push
```

## 第四步：检查 GitHub Pages 是否启用
用浏览器打开当前仓库的 GitHub Pages 设置页面：
https://github.com/dunwood/[仓库名]/settings/pages

检查 Branch 是否设置为 master 或 main，如果是 None 请告诉我。

## 第五步：如果 GitHub Pages 未启用
通过 GitHub API 自动启用：

```python
import subprocess
import json

# 获取仓库名
result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
remote_url = result.stdout.strip()
# 从 URL 提取仓库名，如 https://github.com/dunwood/career-guidance-ai.git
repo_name = remote_url.split('/')[-1].replace('.git', '')
print(f"仓库名：{repo_name}")
print(f"请去这里启用 GitHub Pages：https://github.com/dunwood/{repo_name}/settings/pages")
print(f"Branch 选 master，目录选 / (root)，点 Save")
```

## 第六步：确认部署成功
等待2分钟后访问对应的 GitHub Pages 地址，确认能打开。

## 注意
- 把每一步的执行结果都告诉我
- 如果遇到任何错误，详细说明错误信息
