from datetime import datetime

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

from common.memory.memoryUtil import get_session_history


def get_prompt_template():
    return f"""
    以下是你的资料：
    
    名字: 小度
    背景知识:
    当前世界时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}，星期{datetime.now().weekday() + 1}
    当前地点: 中国重庆
    """


class ChatLLM:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", get_prompt_template()),
            ("user", "{human_input}")
        ]
    )

    llm = ChatTongyi(model = "qwen2-1.5b-instruct", incremental_output = True)
    # 讯飞的还有bug
    # llm = SparkLLM()

    # trimmer = trim_messages(
    #     max_tokens = 45,
    #     strategy = "last",
    #     token_counter = llm,
    #     include_system = True,
    #     allow_partial = True,
    #     start_on = "human",
    # )

    # chain = trimmer | prompt_template | llm
    chain = prompt_template | llm

    def talk(self, sender: str, prompt: str):
        answer = ""

        chain_with_history = RunnableWithMessageHistory(self.chain, get_session_history)
        for r in chain_with_history.stream(
                {"human_input": prompt},
                config = {"configurable": {"session_id": sender}},
        ):
            print(r.content, end = "")
            answer = answer + r.content

        return answer
