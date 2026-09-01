import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit


load_dotenv()

DB_NAME = "ecommerce.db"

def get_sql_agent():
    # Make sure GROQ_API_KEY is in environment
    if "GROQ_API_KEY" not in os.environ:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please set it.")

    # We use sqlite:/// prefix for SQLAlchemy
    db_uri = f"sqlite:///{DB_NAME}"
    db = SQLDatabase.from_uri(db_uri)

    # Initialize Groq LLM
    llm = ChatGroq(temperature=0, model_name="qwen/qwen3.8-27b")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
    )
    return agent_executor

def query_data(question: str) -> str:
    agent = get_sql_agent()
    try:
        response = agent.invoke({"input": question})
        return response.get("output", str(response))
    except Exception as e:
        return f"Error executing query: {str(e)}"
