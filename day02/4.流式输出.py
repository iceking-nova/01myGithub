from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://maas.qianwenaiapi.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你的知识截止到哪？具体到月"}]

print("模型回复：")

# 1. 【修改点】：加上 stream=True
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True  # 开启流式
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)

# 最后打个换行，让终端提示符回到下一行
print()