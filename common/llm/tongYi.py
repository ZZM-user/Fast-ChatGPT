from datetime import datetime

from langchain.chains.llm import LLMChain
from langchain.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

from common.memory import memoryUtil


class TongYi:
    _template = f"""
    ---背景知识--
    你的名字：小度
    当前世界时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    当前地点：中国重庆
    ---历史聊天记录---
    {{chat_history}}
    ---对话内容---
    人类: {{human_input}}
    机器人:
    """

    _base_prompt = PromptTemplate(
        input_variables = ["chat_history", "human_input"], template = _template
    )

    llm = ChatTongyi(model = "qwen-1.8b-chat", incremental_output = True)
    llm_chain = LLMChain(
        llm = llm,
        prompt = _base_prompt,
        verbose = True
    )

    def talk(self, sender: str, prompt: str):
        memory = memoryUtil.get_history(sender)

        self.llm_chain.memory = memory

        response = self.llm_chain.predict(human_input = prompt)

        return response
