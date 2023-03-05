import timeit
import uuid

from _ssl import SSLEOFError
from loguru import logger as log
from retrying import retry
from revChatGPT.V1 import Error, Chatbot

log.add('log/ChatGPT_runtime_{time}.log', rotation='1 day', encoding='utf-8')


class ChatGPT:
    _userSet = {}
    _userDict = {'conversation_id': None, 'parent_id': None}
    _chatbot = Chatbot(config={
        "email": "z2657272578@gmail.com",
        "password": "ZJL20010516",
        # "proxy": "127.0.0.1:7890",
        # "paid": True
        # "email": "372551896@qq.com",
        # "password": "xlh981010"
    })

    @log.catch
    def talk(
            self,
            sender: str,
            prompt: str
    ) -> str:

        if sender not in self._userSet:
            copy = self._userDict.copy()
            self._chatbot.conversation_id = None
            self._chatbot.parent_id = str(uuid.uuid4())
            self._userSet[sender] = copy

        user = self._userSet.get(sender)

        start = timeit.default_timer()
        # 中间写代码块
        resp = self.request(user, prompt)
        end = timeit.default_timer()
        log.debug('Running time: {:.2f} Seconds'.format(end - start))

        if resp["conversation_id"]:
            user['conversation_id'] = resp["conversation_id"]
            user['parent_id'] = resp["parent_id"]
            # print(resp)
            message_ = resp["message"]
            log.info(f'ChatGPT：{message_}')
            return message_

        log.critical(f"故障排查: {resp}")
        return ""

    @log.catch
    @retry(stop_max_attempt_number=6)
    def request(
            self,
            user: dict,
            prompt: str):

        try:
            resp = ''
            for data in self._chatbot.ask(
                    prompt, user['conversation_id'], user['parent_id']
            ):
                # 流式的 1->12->123
                log.trace(data["message"])
                resp = data
        except Error as e:
            if e.code == 2:
                log.warning(f"频率限制 {e}")
                return "我被限制了哦，你可以等一个小时后再来"
        except SSLEOFError as ssl:
            log.error(f"网络波动: {ssl}")
            raise ssl
        except Exception as e:
            log.critical(f"严重故障: {e}")
            raise e

        return resp


if __name__ == '__main__':
    chatGPT = ChatGPT()
    chatGPT.talk("X某", "你好")
