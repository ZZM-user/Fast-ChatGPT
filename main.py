import uvicorn
from fastapi import FastAPI
from loguru import logger as log
from pydantic import BaseModel

from ChatGPT import ChatGPT

log.add('log/main_runtime_{time}.log', rotation='1 day', encoding='utf-8')
app = FastAPI()
chatGPT = ChatGPT()


# bingChat = BingChat()


class Item(BaseModel):
    sender: str
    prompt: str


@log.catch
@app.post("/ChatGPT/api")
async def talk(
        item: Item
):
    item.prompt = item.prompt.strip()
    log.debug(item)

    # if item.prompt.startswith("bing"):
    #     prompt = item.prompt.removeprefix("bing")
    #     print(prompt)
    #     answer = bingChat.talk(prompt)
    # else:
    answer = chatGPT.talk(item.sender, item.prompt)

    return {'answer': answer}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8459, reload=True)
