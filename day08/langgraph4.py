from typing import TypedDict
from langgraph.graph import START, END, StateGraph


# 1. 定义状态结构
class CalculatorState(TypedDict):
    num1: float     # 第一个数字
    num2: float     # 第二个数字
    operator: str   # 运算符：+ 或 -
    result: float   # 计算结果


# 2. 定义加法节点：计算加法，并将结果写入状态
def add(state: CalculatorState) -> CalculatorState:
    print("进入加法节点")
    state["result"] = state["num1"] + state["num2"]
    return state


# 3. 定义减法节点：计算减法，并将结果写入状态
def subtract(state: CalculatorState) -> CalculatorState:
    print("进入减法节点")
    state["result"] = state["num1"] - state["num2"]
    return state


# 4. 定义路由函数：根据运算符返回分支标识
# 路由函数由条件边调用，不需要注册成节点
def router(state: CalculatorState) -> str:
    if state["operator"] == "+":
        return "add_operation"
    elif state["operator"] == "-":
        return "sub_operation"
    else:
        raise ValueError(f"不支持的运算符：{state['operator']}")


# 5. 创建状态图
builder = StateGraph(CalculatorState)

# 6. 注册加法和减法两个节点
builder.add_node("add", add)
builder.add_node("subtract", subtract)

# 7. 添加条件边：从起点直接根据初始状态选择计算节点
builder.add_conditional_edges(
    START,   # 从起点出发
    router,  # 调用路由函数，判断走哪个分支
    {
        "add_operation": "add",       # 加法分支 → add 节点
        "sub_operation": "subtract",  # 减法分支 → subtract 节点
    },
)

# 8. 添加普通边：计算完成后进入终点
builder.add_edge("add", END)
builder.add_edge("subtract", END)

# 9. 编译图，生成可执行对象
graph = builder.compile()

# 10. 准备初始状态
initial_state: CalculatorState = {
    "num1": 10.0,
    "num2": 5.0,
    "operator": "+",
    "result": 0.0,  # 初始值，计算节点执行后会覆盖它
}

# 11. 执行图
final_state = graph.invoke(initial_state)

# 12. 输出最终结果
print(
    f"{final_state['num1']} "
    f"{final_state['operator']} "
    f"{final_state['num2']} "
    f"= {final_state['result']}"
)