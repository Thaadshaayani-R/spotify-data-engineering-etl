# etl/load.py

import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
    future=True,
)


def _get_table(table_name: str) -> Table:
    metadata = MetaData()
    metadata.reflect(bind=engine, only=[table_name])
    return metadata.tables[table_name]


def upsert_df(df: pd.DataFrame, table_name: str, pk: str):
    if df.empty:
        print(f"No data for table {table_name}. Skipping.")
        return

    table = _get_table(table_name)

    with engine.begin() as conn:
        for _, row in df.iterrows():
            row_dict = row.to_dict()

            stmt = insert(table).values(**row_dict)
            update_dict = {col: row_dict[col] for col in row_dict if col != pk}
            stmt = stmt.on_duplicate_key_update(**update_dict)

            conn.execute(stmt)

    print(f"Loaded {len(df)} rows into {table_name}")


def load_to_mysql(tracks_df, artists_df):
    print("Loading into MySQL…")

    upsert_df(artists_df, "artists", "artist_id")
    upsert_df(tracks_df, "tracks", "track_id")

    print("Load complete!")
