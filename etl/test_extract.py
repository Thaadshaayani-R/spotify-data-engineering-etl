# etl/test_extract.py

from etl.spotify_client import SpotifyClient


def main():
    print("\n🔄 Testing Spotify Extraction...")
    client = SpotifyClient()

    # Force authentication (for debugging)
    client.authenticate()
    print("\n🔑 Access Token Successfully Retrieved!")
    print(client.access_token[:30], "...")

    # Use one playlist for initial test
    playlist_name = "bts_all_songs"
    playlist_id = "4U9cBN9vcM4rmDmgjfTSQH"
    print(f"\n📌 Fetching tracks for playlist: {playlist_name} ({playlist_id})")

    tracks = client.get_playlist_tracks(playlist_id)
    print(f"✅ Tracks extracted: {len(tracks)}")

    # Show first track info
    if tracks:
        first_track = tracks[0].get("track", {})
        print("\n🎵 First Track Extracted:")
        print(f"- Track Name: {first_track.get('name')}")
        print(f"- Artist: {first_track['artists'][0]['name']}")
        print(f"- Popularity: {first_track.get('popularity')}")
        print(f"- Duration (ms): {first_track.get('duration_ms')}")

    # Collect up to 5 valid track IDs that have audio features available
    valid_track_ids = []
    for t in tracks:
        if t.get("track") and t["track"].get("id"):
            valid_track_ids.append(t["track"]["id"])
            if len(valid_track_ids) == 5:
                break




if __name__ == "__main__":
    main()

