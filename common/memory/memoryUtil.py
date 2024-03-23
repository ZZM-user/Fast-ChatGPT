from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory

from common import configReader

redis_url = configReader.ReadConfigFile().read_config("redis", "url")


def get_history(sender: str):
    message_history = RedisChatMessageHistory(
        url = redis_url, ttl = 1800, session_id = sender
    )

    memory = ConversationBufferMemory(
        memory_key = "chat_history", chat_memory = message_history
    )

    return memory
