# k-LLM：大模型学习项目

这个分支用于记录我的 LLM 学习代码、实验和笔记。

- 学习分支：`llm-learning`
- GitHub 仓库：<https://github.com/rongshunhuang72-droid/01myGithub/tree/llm-learning>
- `master` 保留原有项目；学习代码在 `llm-learning` 上独立更新。

## 当前学习内容

| 文件 | 学习内容 |
| --- | --- |
| `day02/01QianWenKey.py` | 使用 OpenAI 兼容接口调用千问模型 |
| `day02/2.让大模型有记忆.py` | 通过消息历史实现多轮对话 |
| `pyproject.toml` | Python 版本要求与项目依赖 |
| `uv.lock` | 依赖版本锁定文件 |

`index.html` 和 `images/` 是原仓库已有的网站文件，保留在本分支中。

## 本地运行

需要 Python 3.11 或以上版本。在项目目录中使用 PowerShell：

```powershell
# 使用已有虚拟环境安装项目依赖
.\.venv\Scripts\python.exe -m pip install "dashscope>=1.27.7" "openai>=3.28.0"

# API 密钥只放在本机环境变量中
$env:DASHSCOPE_API_KEY = "填写你自己的 API 密钥"

# 运行学习示例
.\.venv\Scripts\python.exe .\day02\01QianWenKey.py
.\.venv\Scripts\python.exe ".\day02\2.让大模型有记忆.py"
```

如果尚未创建虚拟环境，先执行 `python -m venv .venv`。如使用 uv 管理环境，可执行 `uv sync` 安装锁定的依赖。

示例中的接口地址和模型名称沿用当前学习代码；运行时需要 API 密钥拥有对应服务的访问权限。

## 每次学习后保存到 GitHub

```powershell
# 确认当前分支是 llm-learning，并检查改动
git branch --show-current
git status

# 按需选择本次学习修改的文件
git add day02 README.md
git commit -m "学习：记录本次练习"
git push
```

建议按 `day03/`、`day04/` 等目录继续添加练习，并在 README 中记录学习内容。虚拟环境、IDE 配置和 `.env` 密钥文件已通过 `.gitignore` 排除。
