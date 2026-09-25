import os

from dotenv import load_dotenv
from psycopg import Connection
from langgraph.checkpoint.postgres import PostgresSaver


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def get_postgres_connection():
    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL is not configured in the .env file."
        )

    return Connection.connect(
        DATABASE_URL,
        autocommit=True,
    )


def create_checkpointer():
    connection = get_postgres_connection()

    checkpointer = PostgresSaver(connection)

    checkpointer.setup()

    return checkpointer