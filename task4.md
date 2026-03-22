# 任务：本地测试并推送到 GitHub

## 第一步：本地启动测试服务器

用 Python 启动一个本地服务器，让我可以在浏览器里测试网页：

```
python -m http.server 8080
```

启动后告诉我访问地址（通常是 http://localhost:8080）

## 第二步：确认以下文件都存在

检查这些文件是否存在：
- index.html
- data/majors.json
- data/majors_v2.csv
- data/window_scores.csv

列出 data/ 目录下所有文件。

## 第三步：推送到 GitHub

如果文件都正常，执行以下 git 命令：

```
git add .
git commit -m "feat: 接入五维窗口期数据库，专业数据改为从 majors.json 动态加载"
git push
```

## 注意
- 启动服务器后等我确认测试正常再推送
- 如果 git push 需要输入密码，告诉我
