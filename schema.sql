-- --------------------------------------------------
-- DATABASE SETUP
-- --------------------------------------------------
CREATE DATABASE IF NOT EXISTS spotify_bts;
USE spotify_bts;

-- --------------------------------------------------
-- TABLE: artists
-- --------------------------------------------------
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR(50) PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genres TEXT,
    followers INT,
    artist_popularity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------
-- TABLE: tracks
-- --------------------------------------------------
CREATE TABLE IF NOT EXISTS tracks (
    track_id VARCHAR(50) PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,
    album_name VARCHAR(255),
    artist_id VARCHAR(50),
    popularity INT,
    duration_ms INT,
    
    -- FIXED: Spotify timestamps can contain T / Z / timezone offsets
    added_at VARCHAR(30),

    playlist_name VARCHAR(255),
    playlist_id VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);
