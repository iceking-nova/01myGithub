from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate

# 1. 声明提示词模板
prompt_template = PromptTemplate.from_template(
    "假设你是一个{expert}专家，请你解释一下{content}是什么。"
)

# 2. 创建模型客户端
llm = ChatTongyi(model="qwen-max", streaming=True)

# 3. 组装 Chain（LCEL 表达式） |
chain = prompt_template | llm

# 4. 调用模型
result = chain.stream(input={"expert": "AI", "content": "Langgraph"})

# 打印输出的结果
for chunk in result:
    print(chunk.content, end="", flush=True)