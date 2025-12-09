
# etl/spotify_client.py

import base64
import requests
from typing import List, Dict, Any
from .config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    MAX_TRACKS_PER_REQUEST,
)


class SpotifyClientError(Exception):
    """Custom exception for Spotify client errors."""
    pass


class SpotifyClient:
    """Spotify API Client (Client Credentials Flow)."""

    def __init__(self):
        if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
            raise SpotifyClientError(
                "Missing Spotify credentials. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env"
            )

        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base = "https://api.spotify.com/v1"
        self.access_token = None

    # ----------------------------------------------------
    # AUTHENTICATION
    # ----------------------------------------------------
    def authenticate(self):
        """Authenticate using Client Credentials Flow."""
        auth_str = f"{self.client_id}:{self.client_secret}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}

        resp = requests.post(self.token_url, headers=headers, data=data)

        if resp.status_code != 200:
            raise SpotifyClientError(
                f"Failed to authenticate ({resp.status_code}): {resp.text}"
            )

        self.access_token = resp.json()["access_token"]

    def _auth_header(self):
        if not self.access_token:
            self.authenticate()
        return {"Authorization": f"Bearer {self.access_token}"}

    # ----------------------------------------------------
    # PLAYLIST TRACKS
    # ----------------------------------------------------
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Returns all track items from a playlist with pagination."""
        all_items = []
        offset = 0
        limit = MAX_TRACKS_PER_REQUEST

        while True:
            url = f"{self.api_base}/playlists/{playlist_id}/tracks"
            params = {"offset": offset, "limit": limit}
            headers = self._auth_header()

            resp = requests.get(url, headers=headers, params=params)
            if resp.status_code != 200:
                raise SpotifyClientError(
                    f"Error fetching playlist tracks ({resp.status_code}): {resp.text}"
                )

            data = resp.json()
            items = data.get("items", [])

            all_items.extend(items)

            if len(items) < limit:
                break

            offset += limit

        return all_items

    # ----------------------------------------------------
    # ARTIST DETAILS
    # ----------------------------------------------------
    def get_artist(self, artist_id: str) -> Dict[str, Any]:
        """Fetch detailed artist information."""
        url = f"{self.api_base}/artists/{artist_id}"
        headers = self._auth_header()

        resp = requests.get(url, headers=headers)

        if resp.status_code == 403:
            print("⚠️ Artist details unavailable (403 Forbidden)")
            return {}

        if resp.status_code != 200:
            raise SpotifyClientError(
                f"Error fetching artist details ({resp.status_code}): {resp.text}"
            )

        return resp.json()
