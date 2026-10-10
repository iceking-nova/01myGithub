from openai import OpenAI
import os

class MultiTurnChat:
    """
    多轮对话管理类
    用于封装大模型对话历史维护与调用逻辑
    """

    # 1. 在初始化方法里，新增 api_key 参数
    def __init__(self, api_key: str, base_url: str, model: str, system_prompt: str = None):
        """
        初始化客户端与对话历史
        参数说明：
            api_key: 你的 API 密钥
            base_url: API 服务地址
            model: 模型名称
            system_prompt: 系统提示词（可选），用于设定模型角色与行为规范
        """
        # 2. 把 api_key 传给 OpenAI 客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.chat_history = []

        # 若提供了系统提示词，则将其添加至对话历史起始位置
        if system_prompt:
            self.chat_history.append({"role": "system", "content": system_prompt})

    def add_user_message(self, content: str) -> None:
        """添加用户消息至对话历史"""
        self.chat_history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        """添加助手（模型）消息至对话历史"""
        self.chat_history.append({"role": "assistant", "content": content})

    def send(self, user_message: str) -> str:
        """
        发送用户消息，调用模型，返回回复内容，并自动更新对话历史
        """
        # 将用户消息加入历史
        self.add_user_message(user_message)

        # 调用模型
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            # 3. 把你代码里的 extra_body 参数搬过来，开启思考模式
            extra_body={"enable_thinking": True}
        )

        # 提取模型回复内容
        model_reply = completion.choices[0].message.content

        # 将模型回复加入历史
        self.add_assistant_message(model_reply)

        return model_reply

    def get_history(self) -> list:
        """获取完整的对话历史"""
        return self.chat_history


# ========== 使用示例（支持用户动态输入） ==========
if __name__ == "__main__":
    # 1. 配置参数（完全按照你的环境来）
    # 从环境变量获取 Key，和你的代码一致
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    BASE_URL = "https://maas.qianwenaiapi.com/compatible-mode/v1"
    MODEL = "qwen3.8-max"
    SYSTEM_PROMPT = "背景设定：你现在是一个AI老师，负责上AI课程。"

    # 简单检查一下环境变量有没有配置好
    if not API_KEY:
        print("❌ 错误：未找到 DASHSCOPE_API_KEY 环境变量，请先配置！")
        exit()

    # 2. 创建多轮对话实例（记得把 API_KEY 传进去）
    chat = MultiTurnChat(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=MODEL,
        system_prompt=SYSTEM_PROMPT
    )

    print("多轮对话已启动，输入内容后按回车发送。输入 'exit' 或 'quit' 退出程序。\n")

    # 3. 循环接收用户输入
    while True:
        # 获取用户输入
        user_input = input("用户: ")

        # 退出条件判断
        if user_input.lower() in ["exit", "quit"]:
            print("对话结束。")
            break

        # 跳过空输入
        if not user_input.strip():
            print("请勿输入空白内容。\n")
            continue

        # 调用模型并获取回复
        try:
            reply = chat.send(user_input)
            # 输出模型回复
            print(f"AI老师: {reply}\n")
        except Exception as e:
            print(f"请求出错了: {e}\n")