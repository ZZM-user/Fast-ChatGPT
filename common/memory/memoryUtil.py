from urllib.parse import urlparse

import redis
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from common import configReader

redis_url = configReader.ReadConfigFile().read_config("redis", "url")
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = RedisChatMessageHistory(session_id = session_id,
                                                    url = redis_url,
                                                    ttl = 10000)
    return store[session_id]


def get_redis() -> redis.Redis:
    parsed_url = urlparse(redis_url)
    # 解析得到的信息
    host = parsed_url.hostname  # 主机名
    port = parsed_url.port  # 端口号
    password = parsed_url.password  # 密码（明文形式）

    return redis.Redis(host = host, port = port, password = password)


def clear_history(sender: str):
    get_redis().delete(sender)
    history = get_session_history(sender)
    history.clear()
