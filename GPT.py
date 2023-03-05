import timeit
import uuid

from nb_log import get_logger
from retrying import retry
from revChatGPT.V1 import Error, Chatbot

log = get_logger("GPT")


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

    @retry(
        stop_max_attempt_number=5,
        # 最大延迟时间
        stop_max_delay=15000,
        # 重试停留时间
        wait_random_min=600,
        wait_random_max=3000,
        # 每调一次+1000ms
        wait_incrementing_increment=1000)
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
                resp = data
        except Error as e:
            if e.code == 2:
                log.warning(f"频率限制 {e}")
                return "我被限制了哦，你可以等一个小时后再来"
        except Exception as e:
            log.critical(f"严重故障: {e}")
            raise e

        return resp


if __name__ == '__main__':
    chatGPT = ChatGPT()
    chatGPT.talk("X某", "你好")
