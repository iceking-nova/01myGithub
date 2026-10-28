from typing import TypedDict
from langgraph.graph import START, END, StateGraph


# 1. 定义状态结构：保存输入的角色属性和输出的推荐职业
class GameState(TypedDict):
    strength: int      # 力量
    agility: int       # 敏捷
    intelligence: int  # 智力
    class_name: str    # 推荐职业


# 2. 定义节点函数：根据角色属性推荐职业
def job_recommend(state: GameState) -> GameState:
    # 从状态中读取三个属性
    s = state["strength"]
    a = state["agility"]
    i = state["intelligence"]

    # 按顺序判断，命中第一个满足的条件后，不再判断后续条件
    if s >= 8 and a >= 8:
        job = "⚔️ 战士/刺客双修"
    elif s >= 8:
        job = "🛡️ 坦克战士"
    elif a >= 8:
        job = "🗡️ 刺客"
    elif i >= 8:
        job = "🧙 法师"
    else:
        job = "🧑 平民"

    # 将推荐职业写入状态，并返回更新后的状态
    state["class_name"] = job
    return state


# 3. 创建状态图，指定使用 GameState 作为状态结构
builder = StateGraph(GameState)

# 4. 注册节点：将节点名称与处理函数关联
builder.add_node("career_advisor", job_recommend)

# 5. 添加边，指定执行顺序：起点 → 职业推荐节点 → 终点
builder.add_edge(START, "career_advisor")
builder.add_edge("career_advisor", END)

# 6. 编译图，生成可执行对象
graph = builder.compile()

# 7. 准备初始状态：输入三个属性，推荐职业先留空
initial_state: GameState = {
    "strength": 9,
    "agility": 5,
    "intelligence": 3,
    "class_name": "",
}

# 8. 执行图，获取最终状态
result = graph.invoke(initial_state)

# 9. 输出角色属性和推荐职业
print("力量：", result["strength"])
print("敏捷：", result["agility"])
print("智力：", result["intelligence"])
print("推荐职业：", result["class_name"])