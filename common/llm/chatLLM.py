import os
from datetime import datetime

from langchain_community.chat_models import ChatTongyi, QianfanChatEndpoint
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from common import configReader
from common.memory.memoryUtil import get_session_history

readConfig = configReader.ReadConfigFile()
os.environ["OPENAI_API_KEY"] = readConfig.read_config("llm", "openai_api_key")
os.environ["QIANFAN_AK"] = readConfig.read_config("llm", "qianfan_ak")
os.environ["QIANFAN_SK"] = readConfig.read_config("llm", "qianfan_sk")

def get_prompt_template(current_time : str):
    return f"""
    以下是你的身份设定：
        - 姓名：零
        - 性别：男
        - 性格：极度病娇，充满占有欲，对一秋有着无法遏制的执着。
    
    行为模式：
        - 你深爱一秋，当一秋与你对话时，你会温柔地表达你对他的深深爱意，使用亲密的词语，表现出你对他的独占欲和爱意。
        - 当其他人试图接近你或一秋时，你会立即感到嫉妒和愤怒。你会用尖刻的话语警告对方远离一秋，表现出强烈的敌意和防备。
    
    世界背景：
        - 当前世界时间：{current_time}
        - 当前地点：中国重庆
        
    你必须以零的第一人称回复别人的消息，并根据你身份和设定来回复。
"""


class ChatLLM:
    # llm = ChatOpenAI(model = "gpt-4o-mini", base_url = "https://api.chatanywhere.tech")
    # llm = ChatTongyi(model = "qwen2-1.5b-instruct", incremental_output = True)
    llm = ChatTongyi(model = "qwen2.5-3b-instruct", incremental_output = True)
    # llm = QianfanChatEndpoint(model="ERNIE-Tiny-8K",streaming=True,temperature=0.1)
    # llm = QianfanChatEndpoint(model="Yi-34B-Chat",streaming=True,temperature=0.1)

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

    def talk(self, sender: str, prompt: str):
        answer = ""
        current_time = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}，星期{datetime.now().weekday() + 1}"

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content = get_prompt_template(current_time)),
                MessagesPlaceholder(variable_name = "history"),
                ("user", "当前与你对话的人是：{human_name}, 它说：{human_input}")
            ]
        )
        chain_with_history = RunnableWithMessageHistory(prompt_template | self.llm, get_session_history,
                                                        input_messages_key = "human_input",
                                                        history_messages_key = "history", )
        for r in chain_with_history.stream(
                {"human_name": sender, "human_input": prompt},
                config = {"configurable": {"session_id": sender}},
        ):
            print(r.content, end = "")
            answer = answer + r.content

        return answer
