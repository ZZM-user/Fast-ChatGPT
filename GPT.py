import uuid
from copy import deepcopy

from revChatGPT.V1 import Chatbot


class ChatGPT:
    userSet = {}
    userDict = {'conversation_id': None, 'parent_id': None}
    chatbot = Chatbot(config={
        "email": "372551896@qq.com",
        "password": "xlh981010"
    })

    def talk(
            self,
            sender: str,
            prompt: str
    ) -> str:
        resp = ''
        if sender not in self.userSet:
            copy = deepcopy(self.userDict.copy())
            self.chatbot.conversation_id = None
            self.chatbot.parent_id = str(uuid.uuid4())
            self.userSet[sender] = deepcopy(copy)

        user = self.userSet.get(sender)

        try:

            for data in self.chatbot.ask(
                    prompt, user['conversation_id'], user['parent_id']
            ):
                # 流式的 1->12->123
                resp = data
        except Exception as e:
            print('ChatGPT：我坏了', e)

        if not resp:
            print("出问题了")
            return ''

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
#
# prompt = "你上一句说的最后一个日期是多少"
# resp = ''
# last_conversation_id = ''
# last_parent_id = ''
#
# while True:
#     prompt = input("你：")
#     try:
#         for data in chatbot.ask(
#                 prompt, last_conversation_id, last_parent_id
#         ):
#             # 流式的 1->12->123
#             resp = data
#     except:
#         print('ChatGPT：我坏了')
#
#     last_conversation_id = resp["conversation_id"]
#     last_parent_id = resp["parent_id"]
#     # print(resp)
#     print('ChatGPT：' + resp["message"])
#
# print(os.getenv("HOME"))
# """
# 可用 但是需要自定义配置下 明晚再来
# """
