from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://maas.qianwenaiapi.com/compatible-mode/v1",
)

# 维护一个消息列表，每一个元素是一个键值对 存储用户级雄消息和非用户级消息
chat_history = []

messages = {"role": "user", "content": "我是一个大模型开发工程师，你好"}
chat_history.append(messages)

# 第一次问ai
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=chat_history,
    extra_body={"enable_thinking": True}
)

chat_history.append({"role":"assistant","content":completion.choices[0].message.content})

messages2 = {"role": "user", "content": "我是谁？"}
chat_history.append(messages2)


# 第二次问ai
completion2 = client.chat.completions.create(
    model="qwen3.8-max",
    messages=chat_history,
    extra_body={"enable_thinking": True}
)

print(completion2.choices[0].message.content)
