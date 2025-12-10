# etl/transform.py

import pandas as pd
from typing import List, Dict, Any


# NORMALIZE TRACKS
def normalize_tracks(raw_items: List[Dict[str, Any]],
                     playlist_name: str,
                     playlist_id: str) -> pd.DataFrame:

    rows = []

    for item in raw_items:
        track = item.get("track")
        if not track:
            continue

        artist = track["artists"][0] if track.get("artists") else {}

        rows.append({
            "track_id": track.get("id"),
            "track_name": track.get("name"),
            "album_name": track.get("album", {}).get("name"),
            "artist_id": artist.get("id"),
            "artist_name": artist.get("name"),
            "popularity": track.get("popularity"),
            "duration_ms": track.get("duration_ms"),
            "added_at": item.get("added_at").replace("Z", ""),
            "playlist_name": playlist_name,
            "playlist_id": playlist_id,
        })

    df = pd.DataFrame(rows).drop_duplicates(subset=["track_id"])
    return df

# NORMALIZE ARTISTS
def normalize_artists(track_df: pd.DataFrame) -> pd.DataFrame:
    artists = track_df[["artist_id", "artist_name"]].drop_duplicates()
    artists["genres"] = None
    artists["followers"] = None
    artists["artist_popularity"] = None
    return artists


# ARTIST ENRICHMENT
def enrich_artists(artists_df: pd.DataFrame, client) -> pd.DataFrame:
    """Fetch genres, followers, popularity for each unique artist."""
    enriched_rows = []

    for _, row in artists_df.iterrows():
        artist_id = row["artist_id"]

        details = client.get_artist(artist_id)

        enriched_rows.append({
            "artist_id": artist_id,
            "artist_name": row["artist_name"],
            "genres": ", ".join(details.get("genres", [])),
            "followers": details.get("followers", {}).get("total"),
            "artist_popularity": details.get("popularity"),
        })

    return pd.DataFrame(enriched_rows)


# MAIN TRANSFORM PIPELINE
def transform(raw_tracks: List[Dict[str, Any]],
              playlist_name: str,
              playlist_id: str,
              client):

    tracks_df = normalize_tracks(raw_tracks, playlist_name, playlist_id)
    artists_df = normalize_artists(tracks_df)
    artists_df = enrich_artists(artists_df, client)

    return tracks_df, artists_df
