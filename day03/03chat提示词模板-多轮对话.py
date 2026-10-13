from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 构建带有历史记录占位符的提示词模板
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个AI专家"),
    MessagesPlaceholder("history"),  # 关键：留出位置给历史消息
    ("human", "我刚才问了什么内容？"), # 关键：测试模型是否记得刚才的对话
])

# 2. 模拟历史对话记录
chat_history = [
    ("human", "什么是Langgraph"),
    ("ai", "LangGraph是一种将自然语言处理（NLP）与图神经网络（GNN, Graph Neural Networks）相结合的技术或方法。")
]


# 3. 初始化对话模型 (注意这里用的是 ChatTongyi，和之前的不同)
llm = ChatTongyi(model="qwen-max")

# 4. 构建 Chain 并调用
chain = chat_prompt_template | llm
result = chain.invoke(input={"history": chat_history})

# 5. 打印结果和类型
print(type(result)) # 应该输出 <class 'langchain_core.messages.ai.AIMessage'>
print(result)
print(result.content) # 输出纯文本内容："你刚才问的是：'什么是Langgraph'。"