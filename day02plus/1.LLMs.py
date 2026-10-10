from langchain_community.llms.tongyi import Tongyi

# 创建调用通义千问的客户端
tongyi = Tongyi(model="qwen-max")

invoke = tongyi.invoke("hello，你是谁？")

print(invoke)