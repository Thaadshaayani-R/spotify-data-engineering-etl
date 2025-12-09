from etl.spotify_client import SpotifyClient

def main():
    print("\n🔍 Searching for playlists containing 'BTS'...\n")

    client = SpotifyClient()
    client.authenticate()

    results = client.search_playlists("BTS", limit=10)

    for p in results:
        if not p:
            continue  # skip None results

        name = p.get("name", "Unknown")
        playlist_id = p.get("id", "No ID")

        print(f"- {name}  |  ID: {playlist_id}")

if __name__ == "__main__":
    main()

