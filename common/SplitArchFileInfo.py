# 创建数据库引擎
import json

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from loguru import logger as log
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from common import configReader
from common.llm.chatLLM import ChatLLM

db_uri = configReader.ReadConfigFile().read_config("mysql", "uri")

engine = create_engine(db_uri, echo = True, pool_recycle = 7200, pool_size = 5, max_overflow = 10, pool_timeout = 30)

# 创建DBSession类型
DBSession = sessionmaker(bind = engine)

# 创建一个session实例
session = DBSession()

prompt_template = """
请你将文件名按照指定要求拆解，并只返回一个json格式的对象，
---
示例：
输入：[废文 完结]雀归巢 作者：黄金圣斗士.txt
输出格式：
{{
 "author": "黄金圣斗士",
 "bookName": "雀归巢",
 "tags": ["废文","完结"],
 "fileType": "txt"
}}
---
现在的文件名是：{book}
输出：
"""
prompt = PromptTemplate(
    input_variables = ["book"], template = prompt_template
)
llm = LLMChain(llm = ChatLLM().llm, prompt = prompt)


def is_valid_json_with_keys(json_string: dict, required_keys) -> bool:
    # 尝试将字符串转换为JSON对象
    try:
        json_data = json.loads(json_string.get("text").replace("\\n", ""))
    except (json.JSONDecodeError, TypeError):
        return False  # 如果解析失败，则不是有效的JSON字符串

    # 检查JSON对象中是否存在所有必需的键
    for key in required_keys:
        if not json_data.get(key):
            return False  # 如果任意一个键不存在，则返回False

    return True  # 所有键都存在于JSON对象中，且字符串是有效的JSON


# execute = session.execute(text("SELECT COUNT(1) FROM `archived_file`")).scalar()
# print(execute)
execute = session.execute(text("SELECT id,name FROM `archived_file` ORDER BY RAND() limit 10"))
count = 0
for row in execute:
    print(row.name)
    llm_invoke = llm.invoke({"book": row.name})
    print(llm_invoke)
    isOk = is_valid_json_with_keys(llm_invoke, ["author", "bookName", "tags", "fileType"])
    if not isOk:
        log.error(f"错了哦")
        count = count + 1
    print("-" * 10)

log.error(f"错了{count}次")
if __name__ == '__main__':
    pass
