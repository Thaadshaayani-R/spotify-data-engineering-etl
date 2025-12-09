# etl/config.py

import os
from dotenv import load_dotenv

# Load .env credentials
load_dotenv()

# ---------------------------------------------------
# SPOTIFY API CREDENTIALS
# ---------------------------------------------------
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# ---------------------------------------------------
# GLOBAL ETL CONSTANTS
# ---------------------------------------------------
MARKET = "US"                   # Force US market to avoid region issues
MAX_TRACKS_PER_REQUEST = 100    # Spotify pagination limit

# ---------------------------------------------------
# PROJECT SETTINGS (BTS Project)
# ---------------------------------------------------
DEFAULT_PLAYLIST_NAME = "bts_all_songs"
DEFAULT_PLAYLIST_ID = "4U9cBN9vcM4rmDmgjfTSQH"
