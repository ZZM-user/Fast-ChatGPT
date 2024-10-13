from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from common import configReader

template = """根据下面的表结构，编写一个SQL查询来回答用户的问题:
{schema}

---
Question: {question}
SQL Query:
"""
prompt = ChatPromptTemplate.from_template(template)

template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(template)

tongYiChat = tongYi.ChatLLM()

db_uri = configReader.ReadConfigFile().read_config("mysql", "uri")
db = SQLDatabase.from_uri(db_uri)


def get_schema(_):
    info = db.get_table_info()
    # print(info)
    return info


sql_response = (
        RunnablePassthrough.assign(schema = get_schema)
        | prompt
        | tongYiChat.llm.bind(stop = ["\nSQLResult:"])
        | StrOutputParser()
)

full_chain = (
        RunnablePassthrough.assign(query = sql_response).assign(
            schema = get_schema,
            response = lambda x: db.run(x["query"]),
        )
        | prompt_response
        | tongYiChat.llm
)

# response_invoke = sql_response.invoke({"question": "查询所有作品最多的作者前十个"})
response_invoke = full_chain.invoke({"question": "有哪几张表"})
print(response_invoke)
if __name__ == '__main__':
    pass
