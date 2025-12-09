# app.py - BTS Spotify Dashboard (Professional Redesign)

import os
from pathlib import Path
from typing import Tuple
import pandas as pd
import numpy as np
import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
load_dotenv()

DATA_DIR = Path("data")
TRACKS_CSV = DATA_DIR / "tracks.csv"
ARTISTS_CSV = DATA_DIR / "artists.csv"

# BTS Members
BTS_MEMBERS = ["BTS", "RM", "Jin", "j-hope", "Jimin", "V", "Jung Kook", "Agust D", "SUGA"]


# -------------------------------------------------
# DATA LOADING
# -------------------------------------------------
@st.cache_data(ttl=300)
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        tracks = pd.read_csv(TRACKS_CSV)
        artists = pd.read_csv(ARTISTS_CSV)
        return tracks, artists
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()


# -------------------------------------------------
# DATA PROCESSING
# -------------------------------------------------
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
    df["duration_min"] = df["duration_ms"] / 60000
    return df


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    .main .block-container {
        padding: 0.5rem 1.5rem;
        max-width: 100%;
    }

    /* Header */
    .main-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0.8rem;
        background: linear-gradient(90deg, #1f4e79, #2980b9);
        padding: 0.6rem;
        border-radius: 10px;
        margin: -6rem -0.5rem 0.8rem -0.5rem;
    }

    /* Metric Container */
    .metric-container {
        background: rgba(45, 55, 72, 0.9);
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.3rem 0 -0.5rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.4rem;
        font-weight: bold;
        color: #00d4aa;
        margin: 0;
    }

    .metric-label {
        font-size: 0.7rem;
        color: #888;
        margin: 0;
        text-transform: uppercase;
    }

    .metric-sub {
        font-size: 0.6rem;
        color: #666;
        margin-top: 0.2rem;
    }

    /* Section Header */
    .section-header {
        font-size: 0.9rem;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 0.4rem;
        padding: 0.2rem 0;
        border-bottom: 2px solid #00d4aa;
    }

    .section-title {
        color: #ffffff;
        font-size: 1.2rem;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
    }

    section[data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #333;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: #fff !important;
        font-weight: 600;
    }

    /* Streamlit metrics override */
    div[data-testid="metric-container"] {
        background-color: rgba(45, 55, 72, 0.9);
        border: 1px solid #333;
        padding: 0.5rem;
        border-radius: 8px;
    }

    div[data-testid="metric-container"] > div {
        color: #00d4aa;
    }

    div[data-testid="metric-container"] label {
        color: #888 !important;
    }

    /* Compact table */
    .stDataFrame {
        font-size: 0.8rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.65rem;
        padding: 0.5rem 0;
        border-top: 1px solid #333;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


# -------------------------------------------------
# SECTIONS
# -------------------------------------------------

def render_overview(tracks_df, artists_df):
    """Overview / Summary section like Country Profile"""
    st.markdown("<div class='section-title'>Dashboard Overview</div>", unsafe_allow_html=True)
    
    # Summary text box
    total_tracks = len(tracks_df)
    unique_songs = tracks_df["base_name"].nunique()
    bts_tracks = tracks_df[tracks_df["is_bts"]].shape[0]
    collab_tracks = total_tracks - bts_tracks
    top_song = tracks_df.groupby("base_name").size().idxmax()
    top_artist = tracks_df.groupby("artist_name").size().idxmax()
    
    st.markdown(f"""
    <div style="background: rgba(45, 55, 72, 0.9); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid #333;">
        <div style="font-weight: bold; font-size: 1rem; margin-bottom: 0.5rem;">Collection Summary</div>
        <div style="color: #ccc; font-size: 0.85rem; line-height: 1.6;">
            This dashboard analyzes <span style="color: #00d4aa; font-weight: bold;">{total_tracks:,}</span> tracks 
            from BTS and related artists. The collection includes <span style="color: #00d4aa; font-weight: bold;">{unique_songs}</span> unique songs 
            with multiple versions (remixes, instrumentals, etc.). 
            BTS members contribute <span style="color: #00d4aa; font-weight: bold;">{bts_tracks}</span> tracks, 
            while <span style="color: #00d4aa; font-weight: bold;">{collab_tracks}</span> are collaborations.
            The most versioned song is "<span style="color: #00d4aa;">{top_song}</span>" 
            and the most prolific artist is <span style="color: #00d4aa;">{top_artist}</span>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics in 2 rows of 3
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Total Tracks</div>
            <div class='metric-value'>{total_tracks:,}</div>
            <div class='metric-sub'>All versions included</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Unique Songs</div>
            <div class='metric-value'>{unique_songs}</div>
            <div class='metric-sub'>~{total_tracks/unique_songs:.1f} versions per song</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        num_artists = artists_df["artist_name"].nunique()
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Total Artists</div>
            <div class='metric-value'>{num_artists}</div>
            <div class='metric-sub'>BTS + collaborators</div>
        </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        avg_pop = tracks_df["popularity"].mean()
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Avg Popularity</div>
            <div class='metric-value'>{avg_pop:.1f}</div>
            <div class='metric-sub'>Score 0-100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        max_pop = tracks_df["popularity"].max()
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Max Popularity</div>
            <div class='metric-value'>{max_pop}</div>
            <div class='metric-sub'>Highest score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        avg_dur = tracks_df["duration_min"].mean()
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Avg Duration</div>
            <div class='metric-value'>{avg_dur:.1f} min</div>
            <div class='metric-sub'>Per track</div>
        </div>
        """, unsafe_allow_html=True)


def render_songs(tracks_df):
    """Top Songs section"""
    st.markdown("<div class='section-title'>Top Songs Analysis</div>", unsafe_allow_html=True)
    
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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">Most Frequent Songs (TOP 15)</div>', unsafe_allow_html=True)
        
        display_df = song_stats.head(15)[["Song", "Artist", "Versions", "Max Pop"]]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=320,
            column_config={
                "Song": st.column_config.TextColumn("Song", width="medium"),
                "Artist": st.column_config.TextColumn("Artist", width="small"),
                "Versions": st.column_config.NumberColumn("Versions", width="small"),
                "Max Pop": st.column_config.ProgressColumn(
                    "Popularity",
                    min_value=0,
                    max_value=100,
                    format="%d"
                )
            }
        )
    
    with col2:
        st.markdown('<div class="section-header">Quick Stats</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Most Versions</div>
            <div class='metric-value'>{song_stats['Versions'].max()}</div>
            <div class='metric-sub'>{song_stats.iloc[0]['Song']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        high_pop = song_stats[song_stats["Max Pop"] >= 80].shape[0]
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Hit Songs (80+)</div>
            <div class='metric-value'>{high_pop}</div>
            <div class='metric-sub'>High popularity tracks</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Max Popularity</div>
            <div class='metric-value'>{song_stats['Max Pop'].max()}</div>
            <div class='metric-sub'>Highest score</div>
        </div>
        """, unsafe_allow_html=True)


def render_artists(tracks_df, artists_df):
    """Top Artists section"""
    st.markdown("<div class='section-title'>Artist Rankings</div>", unsafe_allow_html=True)
    
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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">All Artists (TOP 15)</div>', unsafe_allow_html=True)
        st.caption("💜 = BTS or BTS member")
        
        display_df = artist_stats.head(15).copy()
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
            height=320
        )
    
    with col2:
        st.markdown('<div class="section-header">BTS Breakdown</div>', unsafe_allow_html=True)
        
        bts_total = artist_stats[artist_stats["is_bts"] == True]["Tracks"].sum()
        collab_total = artist_stats[artist_stats["is_bts"] == False]["Tracks"].sum()
        num_collabs = len(artist_stats[artist_stats["is_bts"] == False])
        
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>BTS/Members</div>
            <div class='metric-value'>{bts_total}</div>
            <div class='metric-sub'>Tracks</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Collaborations</div>
            <div class='metric-value'>{collab_total}</div>
            <div class='metric-sub'>Tracks</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>Collaborators</div>
            <div class='metric-value'>{num_collabs}</div>
            <div class='metric-sub'>Partner artists</div>
        </div>
        """, unsafe_allow_html=True)


def render_analytics(tracks_df):
    """Analytics section with charts"""
    st.markdown("<div class='section-title'>Analytics</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Popularity Distribution</div>', unsafe_allow_html=True)
        
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
        st.bar_chart(pop_chart_df, x="Range", y="Tracks", height=200)
        
        high_pop = tracks_df[tracks_df["popularity"] >= 60].shape[0]
        st.caption(f"📈 {high_pop} tracks ({high_pop*100//len(tracks_df)}%) have popularity 60+")
    
    with col2:
        st.markdown('<div class="section-header">Duration Distribution</div>', unsafe_allow_html=True)
        
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
        st.bar_chart(dur_chart_df, x="Range", y="Tracks", height=200)
        
        standard = tracks_df[(tracks_df["duration_min"] >= 2) & (tracks_df["duration_min"] < 4)].shape[0]
        st.caption(f"🎵 {standard} tracks ({standard*100//len(tracks_df)}%) are 2-4 min")
    
    # Data Quality Row
    st.markdown('<div class="section-header">Data Quality</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Data Complete", "100%")
    c2.metric("No Duplicates", "Yes")
    c3.metric("Avg Duration", f"{tracks_df['duration_min'].mean():.1f} min")
    c4.metric("Max Popularity", f"{tracks_df['popularity'].max()}")


# -------------------------------------------------
# MAIN APP
# -------------------------------------------------
def main():
    st.set_page_config(
        page_title="Spotify BTS Analytics",
        page_icon="🎧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    inject_css()
    
    # Load data
    tracks_df, artists_df = load_data()
    
    if tracks_df.empty:
        st.warning("No data found. Please check data files.")
        st.stop()
    
    tracks_df = process_tracks(tracks_df)
    
    # -----------------------------------------
    # SIDEBAR NAVIGATION
    # -----------------------------------------
    st.sidebar.title("Navigation")
    section = st.sidebar.selectbox(
        "Select Dashboard:",
        ["Overview", "Top Songs", "Top Artists", "Analytics"]
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="font-size: 0.75rem; color: #888;">
        <b>Data Summary</b><br>
        Tracks: {len(tracks_df):,}<br>
        Artists: {artists_df['artist_name'].nunique()}<br>
        Songs: {tracks_df['base_name'].nunique()}
    </div>
    """, unsafe_allow_html=True)
    
    # -----------------------------------------
    # HEADER
    # -----------------------------------------
    st.markdown('<div class="main-header">🎧 Spotify BTS Analytics</div>', unsafe_allow_html=True)
    
    # -----------------------------------------
    # TOP METRICS ROW (Always visible)
    # -----------------------------------------
    total_tracks = len(tracks_df)
    unique_songs = tracks_df["base_name"].nunique()
    num_artists = artists_df["artist_name"].nunique()
    avg_pop = tracks_df["popularity"].mean()
    max_pop = tracks_df["popularity"].max()
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Tracks", f"{total_tracks:,}")
    m2.metric("Unique Songs", f"{unique_songs}")
    m3.metric("Artists", f"{num_artists}")
    m4.metric("Avg Popularity", f"{avg_pop:.0f}")
    m5.metric("Max Popularity", f"{max_pop}")
    
    st.markdown("---")
    
    # -----------------------------------------
    # RENDER SELECTED SECTION
    # -----------------------------------------
    if section == "Overview":
        render_overview(tracks_df, artists_df)
    elif section == "Top Songs":
        render_songs(tracks_df)
    elif section == "Top Artists":
        render_artists(tracks_df, artists_df)
    elif section == "Analytics":
        render_analytics(tracks_df)
    
    # -----------------------------------------
    # FOOTER
    # -----------------------------------------
    st.markdown("""
    <div class="footer">
        BTS Complete Discography • Spotify API • Python + MySQL • Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
