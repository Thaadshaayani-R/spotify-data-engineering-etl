# etl/run_etl.py

from etl.spotify_client import SpotifyClient
from etl.transform import transform
from etl.load import load_to_mysql
from etl.config import DEFAULT_PLAYLIST_ID, DEFAULT_PLAYLIST_NAME


def main():
    print("\n🚀 Starting Spotify BTS ETL Pipeline...")

    # 1. Extract
    client = SpotifyClient()
    client.authenticate()
    print("🔑 Authenticated with Spotify API.")

    print(f"\n📌 Fetching playlist: {DEFAULT_PLAYLIST_NAME}")
    raw_tracks = client.get_playlist_tracks(DEFAULT_PLAYLIST_ID)
    print(f"🎧 Extracted {len(raw_tracks)} tracks.")

    # 2. Transform (includes artist enrichment)
    print("\n🔄 Transforming data...")
    tracks_df, artists_df = transform(
        raw_tracks,
        DEFAULT_PLAYLIST_NAME,
        DEFAULT_PLAYLIST_ID,
        client
    )

    print("📊 DataFrames:")
    print(f"- Tracks: {tracks_df.shape}")
    print(f"- Artists: {artists_df.shape}")

    # 3. Load
    load_to_mysql(tracks_df, artists_df)

    print("\n🎉 ETL Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()
