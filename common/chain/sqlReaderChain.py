from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from common import configReader
from common.llm import tongYi

template = """根据下面的表结构，编写一个SQL查询来回答用户的问题:
{schema}

---
Question: {question}
SQL Query:
"""
prompt = ChatPromptTemplate.from_template(template)

tongYiChat = tongYi.TongYi()

db_uri = configReader.ReadConfigFile().read_config("mysql", "uri")
db = SQLDatabase.from_uri(db_uri)


def get_schema(_):
    info = db.get_table_info()
    print(info)
    return info


sql_response = (
        RunnablePassthrough.assign(schema = get_schema)
        | prompt
        | tongYiChat.llm.bind(stop = ["\nSQLResult:"])
        | StrOutputParser()
)

response_invoke = sql_response.invoke({"question": "查询有多少张表了"})
print(response_invoke)
if __name__ == '__main__':
    pass
