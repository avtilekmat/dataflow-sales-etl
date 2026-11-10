import os
from pathlib import Path
from sqlalchemy import text

from dotenv import load_dotenv
from sqlalchemy import create_engine

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import MetaData, Table


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def get_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    database_url = (
        f"postgresql+psycopg://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    engine = create_engine(database_url)

    return engine


def load_data(df):
    engine = get_engine()

    metadata = MetaData()

    sales = Table(
        "sales",
        metadata,
        autoload_with=engine
    )

    records = df.to_dict(orient="records")

    if not records:
        engine.dispose()
        return

    with engine.begin() as connection:
        stmt = insert(sales).values(records)

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["order_id"]
        )

        connection.execute(stmt)

    engine.dispose()



