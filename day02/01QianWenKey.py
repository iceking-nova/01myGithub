from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://maas.qianwenaiapi.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你的知识截止到哪？具体到月"}]

# 1. 去掉 stream=True，或者显式写成 stream=False
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={"enable_thinking": True} # 依然保持后台思考，获取更准确的答案
)

# 2. 直接从返回结果中提取最终的回复内容并打印
# completion.choices[0].message.content 就是我们要的最终文本
print("模型回复：")
print(completion)
#print(completion.choices[0].message.content)