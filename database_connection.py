import os
import re

from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine


DATABASE_NAME = os.getenv(
    "MYSQL_DATABASE",
    "tn_electronics_sales_analytics",
)


def create_database_engine() -> Engine:
    if not re.fullmatch(r"[A-Za-z0-9_]+", DATABASE_NAME):
        raise ValueError(
            "MYSQL_DATABASE must contain only letters, numbers, and underscores."
        )

    password = os.getenv("MYSQL_PASSWORD")
    if not password:
        raise RuntimeError(
            "MYSQL_PASSWORD is not set. Set it in your environment before running "
            "the pipeline."
        )

    username = os.getenv("MYSQL_USER", "root")
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    server_url = URL.create(
        drivername="mysql+pymysql",
        username=username,
        password=password,
        host=host,
        port=port,
    )

    server_engine = create_engine(server_url, pool_pre_ping=True)
    try:
        with server_engine.begin() as connection:
            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}` "
                    "CHARACTER SET utf8mb4"
                )
            )
    finally:
        server_engine.dispose()

    database_url = URL.create(
        drivername="mysql+pymysql",
        username=username,
        password=password,
        host=host,
        port=port,
        database=DATABASE_NAME,
    )
    return create_engine(database_url, pool_pre_ping=True)
