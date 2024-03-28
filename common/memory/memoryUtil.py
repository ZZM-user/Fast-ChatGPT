from urllib.parse import urlparse

import redis
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory

from common import configReader

redis_url = configReader.ReadConfigFile().read_config("redis", "url")


def get_history(sender: str) -> RedisChatMessageHistory:
    message_history = RedisChatMessageHistory(
        url = redis_url, ttl = 1800, session_id = sender
    )

    memory = ConversationBufferMemory(
        memory_key = "chat_history", chat_memory = message_history
    )

    return memory


def get_redis() -> redis.Redis:
    parsed_url = urlparse(redis_url)
    # 解析得到的信息
    host = parsed_url.hostname  # 主机名
    port = parsed_url.port  # 端口号
    password = parsed_url.password  # 密码（明文形式）

    return redis.Redis(host = host, port = port, password = password)


def clear_history(sender: str):
    get_redis().delete(sender)
    history = get_history(sender)
    history.clear()
