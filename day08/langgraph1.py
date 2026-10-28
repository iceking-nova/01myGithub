from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. 定义状态结构：节点通过状态读取和传递数据
class AgentState(TypedDict):
    message: str


# 2. 定义节点函数：读取输入字符串，在末尾追加 "hello world"
def add_hello_world(state: AgentState) -> AgentState:
    return {"message": state["message"] + "，hello world"}


# 3. 创建状态图，指定图使用的状态结构
builder = StateGraph(AgentState)

# 4. 注册节点：将节点名称与处理函数关联
builder.add_node("add_hello_world", add_hello_world)

# 5. 添加边，指定执行顺序：起点 → 处理节点 → 终点
# START 和 END 是内置的虚拟节点，不需要自己定义函数
builder.add_edge(START, "add_hello_world")
builder.add_edge("add_hello_world", END)

# 6. 编译图，生成可执行对象
graph = builder.compile()

# 7. 传入初始状态并执行图
result = graph.invoke({"message": "我是李白"})

# 8. 输出最终状态中的 message
print(result["message"])