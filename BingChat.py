import asyncio

from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from loguru import logger as log

log.add('log/BingChat_runtime_{time}.log', rotation = '1 week', encoding = 'utf-8')


class BingChat:
    @log.catch
    async def talk(self, prompt):
        bot = await Chatbot.create()  # Passing cookies is "optional", as explained above
        response = await bot.ask(prompt = prompt, conversation_style = ConversationStyle.creative,
                                 simplify_response = True)
        print(response.get('text'))  # Returns
        # await bot.close()
        return response.get('text')


if __name__ == "__main__":
    bing = BingChat()
    while True:
        an = input("you: ")
        asyncio.run(bing.talk(an))
