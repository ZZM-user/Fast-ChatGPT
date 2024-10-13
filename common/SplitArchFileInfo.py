# 创建数据库引擎
import json
import time

from langchain.chains.llm import LLMChain
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
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
# 身份
    书籍信息提取师
    
# 任务
    将文件名按照指定要求拆解，尽可能拆解出文件名中附带的书籍信息，比如作者，书名，相似的标签，文件后缀。
    请展开你的想象力，尽可能的从其中找出这些信息填充进去。
    如果无法拆分时，请确保书名必须要有

# 返回格式
```json
{{
 "bookName": "",
 "author": "",
 "tags": [],
 "fileType": ""
}}
```

# 参考示例
    ---
    示例1：
    输入：作者：远上白云间.zip
    输出：{{
     "bookName": "作者：远上白云间",
     "author": "远上白云间",
     "tags": [],
     "fileType": "zip"
    }}
    ---
    示例2：
    输入：《当渣受拥有假孕系统后》作者：月渡.txt
    输出：{{
     "bookName": "当渣受拥有假孕系统后",
     "author": "月渡",
     "tags": ['系统','渣受'],
     "fileType": "txt"
    }}
    ---
    示例3：
    输入：[废文 完结]《两主相遇必有一被》作者：沥竹lzz.txt
    输出：{{
     "bookName": "两主相遇必有一被",
     "author": "沥竹lzz",
     "tags": ['废文','完结'],
     "fileType": "txt"
    }}
    ---
    示例4：
    输入：[海棠]密室（1v1）yfzl密码yunfei.zip
    输出：{{
     "bookName": "密室（1v1）",
     "author": "沥竹lzz",
     "tags": ['海棠'],
     "fileType": "zip"
    }}
    ---
    示例5：
    输入：没有人爱代小京.zip
    输出：{{
     "bookName": "没有人爱代小京",
     "author": "",
     "tags": [],
     "fileType": "zip"
    }}
    ---
    示例6：
    输入：[完结+全番外]《批照错发给情敌之后（校园双性1v1 笨蛋美人学渣受x高冷闷骚学神攻）》作者：很好吃的糯米粽【补番】.zip
    输出：{{
     "bookName": "批照错发给情敌之后（校园双性1v1 笨蛋美人学渣受x高冷闷骚学神攻）",
     "author": "很好吃的糯米粽",
     "tags": ["完结", "全番外", "校园双性1v1", "笨蛋美人学渣受", "高冷闷骚学神攻"],
     "fileType": "zip"
    }}
    ---
    示例7：
    输入：快穿：黑莲花的千层套路【泷川】 作者：止水之庭.txt
    输出：{{
     "bookName": "黑莲花的千层套路【泷川】",
     "author": "止水之庭",
     "tags": ["快穿"],
     "fileType": "txt"
    }}
    ---
"""
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content = prompt_template),
        ("user", "{book}")
    ]
)
chain  = prompt | ChatLLM().llm


def is_valid_json_with_keys(json_string: str, required_keys) -> dict|None:
    # 尝试将字符串转换为JSON对象
    try:
        json_str = json_string.replace("```json", "").replace("```", "").replace("\n", "")
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None  # 如果解析失败，则不是有效的JSON字符串

# execute = session.execute(text("SELECT COUNT(1) FROM `archived_file`")).scalar()
# print(execute)
# execute = session.execute(text("SELECT id,name FROM `archived_file` ORDER BY RAND() limit 10"))
execute = session.execute(text("SELECT id,name FROM `archived_file_copy1` where author is null and book_name is null and tags is null ORDER BY archive_date asc "))
count = 0
for row in execute:
    print(f'id:{row.id},name:{row.name}')
    llm_invoke = chain.invoke(
        {
            "book": row.name,
        }
    )
    print(llm_invoke)
    print(llm_invoke.content)
    book_info = is_valid_json_with_keys(llm_invoke.content, ["author", "bookName", "tags", "fileType"])
    if book_info:
        # 修改数据库中的书名、作者和标签
        tags_str = ','.join(book_info['tags'])

        # 使用参数化查询
        session.execute(
            text(
                "UPDATE `archived_file_copy1` SET `book_name` = :book_name, `author` = :author, `tags` = :tags WHERE `id` = :row_id"
            ),
            {
                "book_name": book_info['bookName'],
                "author": book_info['author'],
                "tags": '',
                "row_id": str(row.id)
            }
        )
        # 提交事务
        session.commit()
    count += 1
    print("-" * 30)
    # time.sleep(1)
    print(count)

log.success(f"ok:{count}")
if __name__ == '__main__':
    pass
