# 观察 Codex 与 MCP 服务之间的真实消息

连接结构：`Codex ↔ mcp_proxy.py ↔ mcp.py`。

代理转发原始 stdio 消息，同时在 `day07/mcp_logs/` 下为每次启动创建一个独立日志文件。
日志中的 JSON 为便于阅读进行了缩进，管道中传输的原始字节保持不变。

## 使用

Codex 的 `database` 服务应启动 `mcp_proxy.py`，代理会自动启动同目录的 `mcp.py`。
不要在 PyCharm 中另行启动服务来代替 Codex 的连接。

配置完成后重新加载 Codex（如未加载新配置，退出并重新打开应用），在聊天中输入：

```
请调用 database MCP 服务的 list_tables 工具，列出所有表。
请调用 database MCP 服务的 describe_table 工具，查看 users 表的字段。
```

用 PyCharm 打开 `day07/mcp_logs/` 中最新的 `.log` 文件即可查看。
也可以在 PowerShell 中实时观察最新日志：

```powershell
$capture = Get-ChildItem 'D:\Develop-project3\k-LLM\day07\mcp_logs\*.log' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
Get-Content -LiteralPath $capture.FullName -Encoding UTF8 -Tail 100 -Wait
```

`Ctrl+C` 只停止实时查看。每个代理进程有自己的日志文件；如果存在多个聊天连接，
可以搜索所有日志中的 `tools/call`，找到实际调用所在的文件。

## 日志怎么看

- `Codex -> MCP Server`：客户端请求或通知，例如 `initialize`、`notifications/initialized`、`tools/list`、`tools/call`。
- `MCP Server -> Codex`：服务端的响应或请求。可用相同的 `id` 对应某次请求和响应。
- `MCP Server stderr`：服务端调试日志，不是 JSON-RPC 协议消息。

消息是否出现、顺序如何，以真实客户端和服务端的协商结果为准。
日志只记录 Codex 与本地 MCP 服务之间的通信，不包含 Codex 与模型之间的全部对话。

## 恢复直接连接

在 `C:\Users\24130\.codex\config.toml` 中，把 `[mcp_servers.database]` 的 `args` 从
`mcp_proxy.py` 改回 `mcp.py`，重新加载 Codex 即可。服务代码不需要改动。
