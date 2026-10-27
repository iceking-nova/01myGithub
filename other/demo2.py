import os
import requests
import json

url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 运行前设置环境变量 BIGMODEL_API_KEY
api_key = os.environ["BIGMODEL_API_KEY"]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "glm-4.5-air",  # 根据你的资源包修改模型名称
    "messages": [{"role": "user", "content": "你是什么模型？"}]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    if "choices" in result:
        print(result["choices"][0]["message"]["content"])
    else:
        print("请求成功，但返回格式异常：", result)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print("错误详情:", response.text)