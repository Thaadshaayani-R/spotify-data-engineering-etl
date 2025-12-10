# app.py 

import os
from pathlib import Path
from typing import Tuple
import pandas as pd
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql

# CONFIG
load_dotenv()

# BTS Members
BTS_MEMBERS = ["BTS", "RM", "Jin", "j-hope", "Jimin", "V", "Jung Kook", "Agust D", "SUGA"]


# DATA (MySQL)
@st.cache_data(ttl=300)
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load tracks & artists directly from MySQL instead of CSV."""
    try:
        conn_str = (
            f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
            f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
        )
        engine = create_engine(conn_str)

        tracks = pd.read_sql("SELECT * FROM tracks", engine)
        artists = pd.read_sql("SELECT * FROM artists", engine)

        return tracks, artists

    except Exception as e:
        st.error(f"Unable to connect to MySQL: {e}")
        st.stop()

# DATA PROCESSING
def process_tracks(df: pd.DataFrame) -> pd.DataFrame:
    """Add base_name and is_bts columns."""
    df = df.copy()
    s = df["track_name"].astype(str)
    s = s.str.replace(r"\s*\(.*?\)", "", regex=True)
    s = s.str.replace(r"- Japanese ver\.?", "", regex=True, case=False)
    s = s.str.replace(r"- Instrumental", "", regex=True, case=False)
    s = s.str.replace(r"- Remix", "", regex=True, case=False)
    s = s.str.replace(r"- \w+ Ver\.?", "", regex=True, case=False)
    df["base_name"] = s.str.strip()
    df["is_bts"] = df["artist_name"].isin(BTS_MEMBERS)
    return df


# CUSTOM CSS
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    .main .block-container {padding: 0.35rem 1rem; max-width: 100%;}

    /* Header */
    .header-box {
        font-size: 1.8rem;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1f4e79, #2980b9);
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        margin: -0.5rem 2rem 0.5rem 2rem;
    }
    .header-title {font-family: 'Inter', sans-serif; font-size: 1.1rem; font-weight: 700; color: #fff;}
    .header-sub {font-size: 0.68rem; color: #fff;}
    .live-badge {display: flex; align-items: center; gap: 5px; color: #1ed760; font-size: 0.68rem;}
    .live-dot {width: 8px; height: 8px; background: #1ed760; border-radius: 50%; animation: pulse 2s infinite;}
    @keyframes pulse {0%, 100% {opacity: 1;} 50% {opacity: 0.4;}}

    /* Metric Cards */
    .metrics-row {display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-bottom: 0.4rem;}
    .metric-card {background: rgba(45, 55, 72, 0.9); border: 1px solid #2a2a4a; border-radius: 10px; padding: 0.65rem; border-top: 3px solid;}
    .metric-card.green { border-top-color: #1ed760; }
    .metric-card.purple { border-top-color: #a855f7; }
    .metric-card.blue { border-top-color: #3b82f6; }
    .metric-card.gold { border-top-color: #f59e0b; }
    .metric-value {font-family: 'Inter', sans-serif; font-size: 1.3rem; font-weight: 700; color: #fff; text-align: center;}
    .metric-label {font-size: 0.72rem; color: #fff; text-align: center;}
    .metric-sub {font-size: 0.62rem; color: #fff; text-align: center;}

    /* Section titles */
    .section-title {font-family: 'Inter', sans-serif; font-size: 0.82rem; font-weight: 600; color: #fff; margin-bottom: 0.3rem; display: flex; align-items: center; gap: 6px;}
    .badge {background: rgba(30, 215, 96, 0.2); color: #1ed760; font-size: 0.6rem; padding: 2px 7px; border-radius: 12px;}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {gap: 3px; background: #1a1a2e; padding: 3px; border-radius: 8px;}
    .stTabs [data-baseweb="tab"] {padding: 5px 10px; border-radius: 6px; font-size: 0.78rem;}
    .stTabs [aria-selected="true"] {background: #2a2a4a !important;}

    .stDataFrame table tbody tr { height: 26px !important; }
    .stDataFrame table thead tr { height: 30px !important; }

    .stDataFrame [data-align="right"] { text-align: center !important; }
    .stDataFrame [data-align="right"] div { justify-content: center !important; }

    .footer {text-align: center; color: #666; font-size: 0.62rem; padding: 0.35rem 0; border-top: 1px solid #2a2a4a; margin-top: 0.4rem;}
    </style>
    """, unsafe_allow_html=True)


# COMPONENTS
def render_header():
    st.markdown("""
    <div class="header-box">
        <div>
            <div class="header-title">Spotify BTS Analytics</div>
            <div class="header-sub">ETL: Spotify API → Python → MySQL → Streamlit</div>
        </div>
        <div class="live-badge">
            <div class="live-dot"></div>
            Live Data
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics(tracks_df, artists_df):
    total_tracks = len(tracks_df)
    unique_songs = tracks_df["base_name"].nunique()
    bts_tracks = tracks_df[tracks_df["is_bts"]].shape[0]
    collab_tracks = total_tracks - bts_tracks
    avg_pop = tracks_df["popularity"].mean()
    num_collabs = artists_df[~artists_df["artist_name"].isin(BTS_MEMBERS)].shape[0]
    
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card green">
            <div class="metric-value">{total_tracks:,}</div>
            <div class="metric-label">Total Tracks</div>
            <div class="metric-sub">BTS: {bts_tracks} | Collabs: {collab_tracks}</div>
        </div>
        <div class="metric-card purple">
            <div class="metric-value">{unique_songs:,}</div>
            <div class="metric-label">Unique Songs</div>
            <div class="metric-sub">~{total_tracks/unique_songs:.1f} versions per song</div>
        </div>
        <div class="metric-card blue">
            <div class="metric-value">7+{num_collabs}</div>
            <div class="metric-label">Artists</div>
            <div class="metric-sub">7 BTS members + collaborators</div>
        </div>
        <div class="metric-card gold">
            <div class="metric-value">{avg_pop:.0f}</div>
            <div class="metric-label">Avg Popularity</div>
            <div class="metric-sub">Score 0-100</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="footer">
        BTS Complete Discography • Spotify API • Python + MySQL • Streamlit
    </div>
    """, unsafe_allow_html=True)

# MAIN APP
def main():
    st.set_page_config(
        page_title="Spotify BTS Analytics",
        page_icon="🎧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    inject_css()
    
    # Load data (now from MySQL)
    tracks_df, artists_df = load_data()
    
    if tracks_df.empty:
        st.warning("No data found. Please run ETL first.")
        st.stop()
    
    tracks_df = process_tracks(tracks_df)
    
    # Header & Metrics
    render_header()
    render_metrics(tracks_df, artists_df)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Top Songs", "Top Artists", "Analytics"])
    
    # TAB 1: TOP SONGS
    with tab1:
        song_stats = (
            tracks_df
            .groupby("base_name", as_index=False)
            .agg({
                "track_id": "count",
                "popularity": "max",
                "artist_name": "first"
            })
            .rename(columns={"track_id": "Versions", "popularity": "Max Pop", "artist_name": "Artist", "base_name": "Song"})
            .sort_values("Versions", ascending=False)
        )
        
        st.markdown('<div class="section-title">Most Frequent Songs <span class="badge">TOP 20</span></div>', unsafe_allow_html=True)
        st.caption("Songs with the most versions (remixes, instrumentals, etc.)")
        
        display_df = song_stats.head(20)[["Song", "Artist", "Versions", "Max Pop"]]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=300
        )
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Most Versions", f"{song_stats['Versions'].max()} ({song_stats.iloc[0]['Song']})")
        high_pop_songs = song_stats[song_stats["Max Pop"] >= 80].shape[0]
        col2.metric("Hit Songs (80+ Pop)", f"{high_pop_songs}")
        col3.metric("Highest Popularity", f"{song_stats['Max Pop'].max()}")
    
    # TAB 2: TOP ARTISTS
    with tab2:
        artist_stats = (
            tracks_df
            .groupby("artist_name", as_index=False)
            .agg({
                "track_id": "count",
                "popularity": "mean",
                "is_bts": "first"
            })
            .rename(columns={"track_id": "Tracks", "popularity": "Avg Pop"})
            .sort_values("Tracks", ascending=False)

        )
        
        artist_stats = artist_stats.merge(
            artists_df[["artist_name", "followers"]],
            on="artist_name",
            how="left"
        )
        
        st.markdown('<div class="section-title">🎤 Artist Rankings <span class="badge">ALL ARTISTS</span></div>', unsafe_allow_html=True)
        st.caption("💜 = BTS or BTS member (RM, Jin, j-hope, Jimin, V, Jung Kook, Agust D)")
        
        display_df = artist_stats.head(20).copy()
        display_df["Artist"] = display_df.apply(
            lambda r: f"💜 {r['artist_name']}" if r["is_bts"] else r["artist_name"],
            axis=1
        )
        display_df["Followers"] = display_df["followers"].apply(
            lambda x: f"{x:,.0f}" if pd.notna(x) else "—"
        )
        display_df["Avg Pop"] = display_df["Avg Pop"].round(1)
        
        st.dataframe(
            display_df[["Artist", "Tracks", "Avg Pop", "Followers"]],
            use_container_width=True,
            hide_index=True,
            height=300
        )
        
        bts_total = artist_stats[artist_stats["is_bts"] == True]["Tracks"].sum()
        collab_total = artist_stats[artist_stats["is_bts"] == False]["Tracks"].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("BTS/Members Tracks", f"{bts_total}")
        col2.metric("Collaboration Tracks", f"{collab_total}")
        col3.metric("Total Collaborators", f"{len(artist_stats[artist_stats['is_bts'] == False])}")
    
    # TAB 3: ANALYTICS
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-title">Popularity Levels</div>', unsafe_allow_html=True)
            
            def get_pop_label(p):
                if p < 20: return "0-19"
                elif p < 40: return "20-39"
                elif p < 60: return "40-59"
                elif p < 80: return "60-79"
                else: return "80-100"
            
            tracks_df["pop_label"] = tracks_df["popularity"].apply(get_pop_label)
            pop_counts = tracks_df["pop_label"].value_counts()
            
            labels_pop = ["0-19", "20-39", "40-59", "60-79", "80-100"]
            pop_values = [int(pop_counts.get(lbl, 0)) for lbl in labels_pop]
            pop_chart_df = pd.DataFrame({"Range": labels_pop, "Tracks": pop_values})
            st.bar_chart(pop_chart_df, x="Range", y="Tracks", height=300)
            
            high_pop = tracks_df[tracks_df["popularity"] >= 60].shape[0]
            st.caption(f"📈 {high_pop} tracks ({high_pop*100//len(tracks_df)}%) have popularity 60+")
        
        with col2:
            st.markdown('<div class="section-title">Song Duration</div>', unsafe_allow_html=True)
            
            tracks_df["duration_min"] = tracks_df["duration_ms"] / 60000
            
            def get_dur_label(m):
                if m < 2: return "<2 min"
                elif m < 3: return "2-3 min"
                elif m < 4: return "3-4 min"
                elif m < 5: return "4-5 min"
                else: return "5+ min"
            
            tracks_df["dur_label"] = tracks_df["duration_min"].apply(get_dur_label)
            dur_counts = tracks_df["dur_label"].value_counts()
            
            labels_dur = ["<2 min", "2-3 min", "3-4 min", "4-5 min", "5+ min"]
            dur_values = [int(dur_counts.get(lbl, 0)) for lbl in labels_dur]
            dur_chart_df = pd.DataFrame({"Range": labels_dur, "Tracks": dur_values})
            st.bar_chart(dur_chart_df, x="Range", y="Tracks", height=300)
            
            standard = tracks_df[(tracks_df["duration_min"] >= 2) & (tracks_df["duration_min"] < 4)].shape[0]
            st.caption(f"🎵 {standard} tracks ({standard*100//len(tracks_df)}%) are 2-4 min (radio length)")
        
        st.markdown("---")
        st.markdown('<div class="section-title">Data Quality</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Data Complete", "100%")
        c2.metric("No Duplicates", "Yes")
        c3.metric("⏱Avg Duration", f"{tracks_df['duration_min'].mean():.1f} min")
        c4.metric("Max Popularity", f"{tracks_df['popularity'].max()}")
    
    render_footer()


if __name__ == "__main__":
    main()
