import asyncio

from EdgeGPT import Chatbot, ConversationStyle
from nb_log import get_logger

log = get_logger("Bing")


class BingChat:
    async def talk(self, prompt):
        bot = Chatbot(cookiePath='./cookie.json')
        resp = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative)
        msg_list = resp.get("item").get("messages")
        message_ = msg_list[1].get('text')
        print(message_)
        await bot.close()


if __name__ == "__main__":
    bing = BingChat()
    asyncio.run(bing.talk("你好"))
