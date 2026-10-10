from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage

# 1. 创建调用通义千问的客户端
# 建议先用 qwen-max 确保能跑通，跑通后再尝试 qwen3-max
llm = ChatTongyi(model="qwen-max")

# 2. 准备上下文
chat_history = [
    SystemMessage(content="背景设定：你现在是一个AI老师，负责上AI课程。"),
    HumanMessage(content="你是谁?")
]

# 3. 携带上下文去调用模型
result = llm.invoke(input=chat_history)

# 4. 打印结果
print(result)
#print(result.content)