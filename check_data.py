# check_data.py - Diagnostic script to check your MySQL data

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

print("=" * 60)
print("DATABASE DIAGNOSTIC REPORT")
print("=" * 60)

try:
    engine = create_engine(DB_URL, echo=False)
    print(f"✅ Connected to: {MYSQL_DB}")
    print()
    
    # Load tracks
    tracks = pd.read_sql("SELECT * FROM tracks", con=engine)
    print(f"TRACKS TABLE: {len(tracks)} rows")
    print("-" * 40)
    print(f"Columns: {list(tracks.columns)}")
    print()
    
    # Check popularity column
    if "popularity" in tracks.columns:
        print("POPULARITY COLUMN:")
        print(f"  - Data type: {tracks['popularity'].dtype}")
        print(f"  - Min: {tracks['popularity'].min()}")
        print(f"  - Max: {tracks['popularity'].max()}")
        print(f"  - Mean: {tracks['popularity'].mean():.2f}")
        print(f"  - Null count: {tracks['popularity'].isna().sum()}")
        print(f"  - Sample values: {tracks['popularity'].head(10).tolist()}")
    else:
        print("❌ 'popularity' column NOT FOUND!")
    print()
    
    # Check duration_ms column
    if "duration_ms" in tracks.columns:
        print("DURATION_MS COLUMN:")
        print(f"  - Data type: {tracks['duration_ms'].dtype}")
        print(f"  - Min: {tracks['duration_ms'].min()}")
        print(f"  - Max: {tracks['duration_ms'].max()}")
        print(f"  - Mean: {tracks['duration_ms'].mean():.2f}")
        print(f"  - Null count: {tracks['duration_ms'].isna().sum()}")
        print(f"  - Sample values (in minutes): {(tracks['duration_ms'].head(10) / 60000).tolist()}")
    else:
        print("❌ 'duration_ms' column NOT FOUND!")
    print()
    
    # Check track_name column
    if "track_name" in tracks.columns:
        print("TRACK_NAME COLUMN:")
        print(f"  - Sample values: {tracks['track_name'].head(5).tolist()}")
    print()
    
    # Load artists
    artists = pd.read_sql("SELECT * FROM artists", con=engine)
    print(f"ARTISTS TABLE: {len(artists)} rows")
    print("-" * 40)
    print(f"Columns: {list(artists.columns)}")
    print()
    
    if "followers" in artists.columns:
        print("FOLLOWERS COLUMN:")
        print(f"  - Data type: {artists['followers'].dtype}")
        print(f"  - Min: {artists['followers'].min()}")
        print(f"  - Max: {artists['followers'].max()}")
        print(f"  - Sample values: {artists['followers'].head(5).tolist()}")
    print()
    
    # Show first few rows
    print("=" * 60)
    print("SAMPLE DATA - TRACKS (first 3 rows):")
    print("=" * 60)
    print(tracks.head(3).to_string())
    print()
    
    print("=" * 60)
    print("SAMPLE DATA - ARTISTS (first 3 rows):")
    print("=" * 60)
    print(artists.head(3).to_string())
    
except Exception as e:
    print(f"❌ ERROR: {e}")