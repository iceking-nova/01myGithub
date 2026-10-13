from langchain_community.llms.tongyi import Tongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# 1. 创建聊天提示词模板
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个{expert}专家"),
    ("human", "请你解释下{content}是什么。")
])


# 2. 初始化大语言模型
llm = Tongyi(model="qwen-max")

# 3. 构建处理链
chain = chat_prompt_template | llm

# 4. 调用链（使用 stream 流式输出）
# 注意：这里的键名必须与模板中的占位符完全一致
result = chain.stream(input={"expert": "AI", "content": "Langgraph"})

# 5. 补全循环打印部分
for chunk in result:
    # end="" 表示不换行，flush=True 确保逐字实时输出，模拟打字机效果
    print(chunk, end="", flush=True)