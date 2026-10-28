from typing import List, TypedDict

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import START, END, StateGraph



# ==================================================
# 1. 定义模型和工具
# ==================================================

# 从环境变量 DASHSCOPE_API_KEY 读取 API Key
model = ChatTongyi(
    model="qwen-plus",
    max_retries=1,
    model_kwargs={"timeout": 30},
)


@tool
def get_weather(location: str) -> str:
    """
    查询指定位置的天气信息。

    Args:
        location: 地理位置，例如北京、上海。

    Returns:
        天气情况。
    """
    # 按截图保留固定假数据，并非真实天气查询
    return f"今天{location}的温度是 200°C"


@tool
def multiply(a: int, b: int) -> int:
    """
    将两个整数相乘。

    Args:
        a: 第一个整数。
        b: 第二个整数。

    Returns:
        相乘的结果。
    """
    return a * b


# 工具列表
tools = [get_weather, multiply]

# 将工具信息提供给模型，让模型能够生成工具调用请求
# 注意：bind_tools 不会直接执行这些工具
model_with_tools = model.bind_tools(tools)

# 建立“工具名称 → 工具对象”的映射，方便后面查找并执行
tools_by_name = {
    tool_item.name: tool_item
    for tool_item in tools
}


# ==================================================
# 2. 定义状态
# ==================================================

class ReActAgentState(TypedDict):
    messages: List[BaseMessage]  # 完整消息历史
    llm_calls: int              # 模型调用次数


# ==================================================
# 3. 定义模型节点
# ==================================================

def llm_call(state: ReActAgentState) -> ReActAgentState:
    """调用模型，让模型决定调用工具还是直接回答。"""


    # 系统提示词 + 当前消息历史
    msgs = [
        SystemMessage(content="你是一个有用的助手。")
    ] + state["messages"]

    # 模型可能返回：
    # 1. 带 tool_calls 的 AIMessage：请求调用工具
    # 2. 不带 tool_calls 的 AIMessage：直接回答
    # model_with_tools就是基于langchain定义的model
    ai_message = model_with_tools.invoke(msgs)

    # 将模型回复追加到消息历史
    state["messages"] = state["messages"] + [ai_message]

    # 只有真正调用模型时，才增加模型调用次数
    state["llm_calls"] += 1

    return state


# ==================================================
# 4. 定义工具节点
# ==================================================

def tool_call(state: ReActAgentState) -> ReActAgentState:
    """执行模型请求的工具调用，并将结果写入消息历史。"""

    # 最后一条消息是模型刚刚返回的 AIMessage
    last_message = state["messages"][-1]

    # 模型一次可能请求调用多个工具
    tool_calls = last_message.tool_calls

    for tool_request in tool_calls:
        # 取出工具名称和参数
        tool_name = tool_request["name"]
        tool_args = tool_request["args"]

        # 查找工具并执行
        tool_result = tools_by_name[tool_name].invoke(tool_args)

        # 把工具结果追加到消息历史
        # tool_call_id 用于将结果与模型发出的工具请求对应起来
        state["messages"].append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_request["id"],
            )
        )

    return state


# ==================================================
# 5. 定义路由函数
# ==================================================

def router(state: ReActAgentState) -> str:
    """根据模型最后一条回复，决定执行工具还是结束。"""

    last_message = state["messages"][-1]

    # 模型请求调用工具 → 进入工具节点
    if (
        hasattr(last_message, "tool_calls")
        and last_message.tool_calls
    ):
        return "tool_call"

    # 模型没有请求调用工具 → 结束流程
    return END


# ==================================================
# 6. 构建图
# ==================================================

builder = StateGraph(ReActAgentState)

# 注册两个节点
builder.add_node("llm_call", llm_call)
builder.add_node("tool_call", tool_call)

# 起点 → 模型节点
builder.add_edge(START, "llm_call")

# 模型节点 → 根据模型回复，选择执行工具或结束
builder.add_conditional_edges(
    "llm_call",
    router,
    {
        "tool_call": "tool_call",
        END: END,
    },
)

# 工具节点 → 回到模型节点
# 让模型读取工具结果，决定下一步操作
builder.add_edge("tool_call", "llm_call")

# 编译图
graph = builder.compile()


# from pathlib import Path
#
# # 将图片保存在当前 Python 文件所在目录
# image_path = Path(__file__).resolve().with_name("react_agent_graph.png")
#
# graph.get_graph(xray=True).draw_mermaid_png(
#     output_file_path=str(image_path)
# )
#
# print("流程图已保存到：", image_path)


# ==================================================
# 7. 测试运行（截图中的测试部分未完整显示，这里补全）
# ==================================================

if __name__ == "__main__":
    initial_state: ReActAgentState = {
        "messages": [
            HumanMessage(content="请调用乘法工具，计算3乘以4等于多少？")
        ],
        "llm_calls": 0,
    }

    final_state = graph.invoke(initial_state)

    print(final_state)