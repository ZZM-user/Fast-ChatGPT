import uvicorn
from fastapi import FastAPI
from loguru import logger as log
from pydantic import BaseModel

from common.llm import tongYi
from common.memory import memoryUtil

log.add('log/main_runtime_{time}.log', rotation = '1 week', encoding = 'utf-8')
app = FastAPI()


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

    if item.prompt.__contains__("重新开始"):
        memoryUtil.clear_history(item.sender)
        return {'answer': '好的，已经重新开始啦！'}

    answer = tongYi.TongYi().talk(item.sender, item.prompt)

    log.debug(answer)
    return {'answer': answer}


@log.catch
@app.get("/clear")
async def talk(sender: str):
    log.info("请求清除历史记录：{}".format(sender))
    memoryUtil.clear_history(sender)


if __name__ == '__main__':
    uvicorn.run("main:app", host = "0.0.0.0", port = 8459, reload = True)
