import asyncio

from EdgeGPT import Chatbot, ConversationStyle
from loguru import logger as log

log.add('log/BingChat_runtime_{time}.log', rotation='1 day', encoding='utf-8')


class BingChat:
    @log.catch
    async def talk(self, prompt):
        bot = Chatbot(cookiePath='./cookie.json')
        resp = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative)
        msg_list = resp.get("item").get("messages")
        message_ = msg_list[1].get('text')
        log.debug(message_)
        await bot.close()


if __name__ == "__main__":
    bing = BingChat()
    asyncio.run(bing.talk("你好"))
