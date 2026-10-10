from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


class ChatBot:
    def __init__(self, model: str = "qwen-max", system_prompt: str = ""):
        # 1. 初始化模型，开启流式
        self.llm = ChatTongyi(model=model, streaming=True)

        # 2. 初始化对话历史
        self.chat_history = []
        if system_prompt:
            self.chat_history.append(SystemMessage(content=system_prompt))

    def chat_stream(self, user_input: str) -> str:
        """流式输出，返回完整回复，并写入历史"""
        # 1. 把用户消息加入历史
        self.chat_history.append(HumanMessage(content=user_input))

        # 2. 流式调用模型
        full_response = ""
        for chunk in self.llm.stream(self.chat_history):
            print(chunk.content, end="", flush=True)
            full_response += chunk.content
        print()  # 换行

        # 3. 把 AI 回复加入历史
        self.chat_history.append(AIMessage(content=full_response))
        return full_response

    def clear(self):
        """清空对话历史（保留 SystemMessage）"""
        system_msgs = [m for m in self.chat_history if isinstance(m, SystemMessage)]
        self.chat_history = system_msgs


def main():
    # 初始化 Bot
    bot = ChatBot(
        model="qwen-max",
        system_prompt="背景设定：你现在是一个AI老师，负责上AI课程。回答尽量简洁清晰。"
    )

    print("=" * 50)
    print("🤖 AI 老师已上线！输入内容开始对话。")
    print("💡 输入 'exit' 或 'quit' 退出")
    print("💡 输入 'clear' 清空对话历史")
    print("=" * 50)

    while True:
        # 1. 获取用户输入
        try:
            user_input = input("\n👤 你：").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 再见！")
            break

        # 2. 处理空输入
        if not user_input:
            continue

        # 3. 处理退出指令
        if user_input.lower() in ("exit", "quit"):
            print("👋 再见！")
            break

        # 4. 处理清空指令
        if user_input.lower() == "clear":
            bot.clear()
            print("🧹 对话历史已清空！")
            continue

        # 5. 调用 AI，流式输出
        print("🤖 AI 老师：", end="", flush=True)
        try:
            bot.chat_stream(user_input)
        except Exception as e:
            print(f"\n❌ 出错了：{e}")


if __name__ == "__main__":
    main()