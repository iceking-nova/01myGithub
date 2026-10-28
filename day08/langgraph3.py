from typing import TypedDict
from langgraph.graph import START, END, StateGraph


# 1. 定义状态结构：在两个节点之间传递包裹信息和处理结果
class PackageState(TypedDict):
    package_id: str       # 包裹单号
    is_damaged: bool      # 是否损坏：True 表示损坏，False 表示完好
    inspection_note: str  # 验货备注
    final_action: str     # 最终处理结果：签收或拒收


# 2. 定义节点1：验货
def inspect(state: PackageState) -> PackageState:
    # 读取包裹单号
    pkg_id = state["package_id"]

    # 模拟验货规则：单号中包含 "9"，就认为包裹损坏
    # 这里只是教学示例，实际业务需要使用真实的验货结果
    damaged = "9" in pkg_id

    # 将验货结果和备注写入状态
    if damaged:
        state["is_damaged"] = True
        state["inspection_note"] = f"⚠️ 包裹 {pkg_id} 外包装破损"
    else:
        state["is_damaged"] = False
        state["inspection_note"] = f"✅ 包裹 {pkg_id} 完好无损"

    return state


# 3. 定义节点2：根据验货结果决定签收或拒收
def sign(state: PackageState) -> PackageState:
    # 读取上一个节点写入的验货结果
    if state["is_damaged"]:
        state["final_action"] = f"❌ 拒收！{state['inspection_note']}"
    else:
        state["final_action"] = f"✅ 签收成功！{state['inspection_note']}"

    return state


# 4. 创建状态图
builder = StateGraph(PackageState)

# 5. 注册两个节点：将节点名称与对应函数关联
builder.add_node("inspect", inspect)
builder.add_node("sign", sign)

# 6. 添加边，指定执行顺序：起点 → 验货 → 签收处理 → 终点
builder.add_edge(START, "inspect")
builder.add_edge("inspect", "sign")
builder.add_edge("sign", END)

# 7. 编译图，生成可执行对象
graph = builder.compile()

# 8. 准备初始状态
# 验货结果和最终操作由后续节点填写，这里先设置初始值
initial_state: PackageState = {
    "package_id": "PKG1239",
    "is_damaged": False,
    "inspection_note": "",
    "final_action": "",
}

# 9. 执行图，获取两个节点处理后的最终状态
result = graph.invoke(initial_state)

# 10. 输出处理结果
print("包裹单号：", result["package_id"])
print("是否损坏：", result["is_damaged"])
print("验货备注：", result["inspection_note"])
print("最终操作：", result["final_action"])