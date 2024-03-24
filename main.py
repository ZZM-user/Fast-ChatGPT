import uvicorn
from fastapi import FastAPI
from loguru import logger as log
from pydantic import BaseModel

from common.llm import tongYi

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

    answer = tongYi.TongYi().talk(item.sender, item.prompt)

    log.debug(answer)
    return {'answer': answer}


if __name__ == '__main__':
    uvicorn.run("main:app", host = "0.0.0.0", port = 8459, reload = True)
