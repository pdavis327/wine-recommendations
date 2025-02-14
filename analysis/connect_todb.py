# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: hflc
#     language: python
#     name: python3
# ---

# %%
from langchain_community.utilities import SQLDatabase
import sys
import getpass
import os
sys.path.append(os.path.abspath(".."))  

from util import query
# %load_ext autoreload
# %autoreload 2

# %%
DATABASE_URI = "postgresql+psycopg2://petedavis@localhost:5432/wine-dataset"

# %%
db = SQLDatabase.from_uri(DATABASE_URI)

# %%
print(db.dialect)
print(db.get_usable_table_names())

# %%
query = "SELECT * from winemag LIMIT 10;"
db.run(query)

# %%
from typing_extensions import TypedDict


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


# %%
from langchain.chat_models import init_chat_model

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

# %%
from langchain import hub
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

assert len(query_prompt_template.messages) == 1
# query_prompt_template.messages[0].pretty_print()

# %%
from typing_extensions import Annotated


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}


# %%
write_query({"question": "Which wines are red?"})

# %%
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool


def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}


# %%
execute_query({'query': "SELECT designation, winery, price_dollars FROM winemag WHERE variety = 'Portuguese Red' OR variety LIKE '%Red%' OR designation LIKE '%Red%'"})


# %%
def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}


# %%
from langgraph.graph import START, StateGraph

graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()

# %%
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

# %%
for step in graph.stream(
    {"question": "what wines are the most expensive?"}, stream_mode="updates"
):
    print(step)

# %%
