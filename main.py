import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from GPT import ChatGPT

app = FastAPI()
chatGPT = ChatGPT()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class Item(BaseModel):
    sender: str
    prompt: str


@app.post("/ChatGPT/api")
async def talk(
        item: Item
):
    print(item)
    answer = chatGPT.talk(item.sender, item.prompt)
    return {'answer': answer}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8459, reload=True)
