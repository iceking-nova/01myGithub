"""MySQL MCP Server - Mock 版本，不连接真实数据库。"""

import sys
from pathlib import Path

# 避免直接运行 mcp.py 时，当前文件遮蔽同名的 MCP SDK。
if __name__ == "__main__" and __package__ is None:
    script_dir = Path(__file__).resolve().parent
    sys.path[:] = [p for p in sys.path if Path(p or ".").resolve() != script_dir]

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MySQL")

# Mock 数据
TABLES = {
    "users": "id, username, email, created_at",
    "orders": "id, user_id, product, amount, status",
    "products": "id, name, price, stock",
}


@mcp.tool()
def list_tables() -> str:
    """列出所有表，返回所有表名。"""
    return f"📋 数据库表: {', '.join(TABLES.keys())}"


@mcp.tool()
def describe_table(table_name: str) -> str:
    """查看表结构，table_name 为要查询的表名。"""
    if table_name in TABLES:
        return f"📊 表 {table_name} 的字段: {TABLES[table_name]}"
    return f"❌ 表 {table_name} 不存在"


if __name__ == "__main__":
    # stdout 用于 MCP 协议，因此启动提示输出到 stderr。
    print("MCP Server Started", file=sys.stderr)
    mcp.run(transport="stdio")
