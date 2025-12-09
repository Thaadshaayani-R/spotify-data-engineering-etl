import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "spotify_bts")

DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

def export_table(engine, table, path):
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"Saved {table} -> {path} ({len(df)} rows)")

def main():
    engine = create_engine(DB_URL)
    export_table(engine, "tracks", Path("data/tracks.csv"))
    export_table(engine, "artists", Path("data/artists.csv"))

if __name__ == "__main__":
    from pathlib import Path
    main()
