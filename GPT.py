import uuid
from copy import deepcopy

from revChatGPT.V1 import Chatbot, Error


class ChatGPT:
    userSet = {}
    userDict = {'conversation_id': None, 'parent_id': None}
    chatbot = Chatbot(config={
        "email": "z2657272578@gmail.com",
        "password": "ZJL20010516",
        "proxy": "127.0.0.1:7890",
        "paid": True
        # "email": "372551896@qq.com",
        # "password": "xlh981010"
    })

    def talk(
            self,
            sender: str,
            prompt: str
    ) -> str:

        if sender not in self.userSet:
            copy = deepcopy(self.userDict.copy())
            self.chatbot.conversation_id = None
            self.chatbot.parent_id = str(uuid.uuid4())
            self.userSet[sender] = deepcopy(copy)

        user = self.userSet.get(sender)

        try:
            resp = ''
            for data in self.chatbot.ask(
                    prompt, user['conversation_id'], user['parent_id']
            ):
                # 流式的 1->12->123
                resp = data
        except Error as e:
            if e.code == 2:
                print("频率限制", e)
                return "我被限制了哦，你可以等一个小时后再来"
        except Exception as e:
            print('ChatGPT：我坏了', e)
            return ""

        user['conversation_id'] = deepcopy(resp["conversation_id"])
        user['parent_id'] = deepcopy(resp["parent_id"])
        self.userSet[sender] = deepcopy(user)
        # print(resp)
        message_ = resp["message"]
        print('ChatGPT：' + message_)
        return message_


if __name__ == '__main__':
    chatGPT = ChatGPT()
    chatGPT.talk("X某", "你好")
