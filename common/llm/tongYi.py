from datetime import datetime

from langchain.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

from common.memory.memoryUtil import get_session_history


def get_prompt_template():
    return f"""
    以下是你的资料：
    
    名字: 小度
    背景知识:
    当前世界时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}，星期{datetime.now().weekday() + 1}
    当前地点: 中国重庆
    """


input_message = """
        {human_input}
"""


class TongYi:
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", get_prompt_template()),
        ("user", input_message)
    ])

    model = ChatTongyi(model = "qwen-1.8b-chat", incremental_output = True)
    chain = prompt_template | model

    def talk(self, sender: str, prompt: str):
        answer = ""

        config = {"configurable": {"session_id": sender}}
        with_message_history = RunnableWithMessageHistory(self.model, get_session_history)
        for r in with_message_history.stream(
                [HumanMessage(content = prompt)],
                config = config,
        ):
            print(r.content, end = "")
            answer = answer + r.content

        return answer
