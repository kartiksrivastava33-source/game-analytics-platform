from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]

DB_FILE = ROOT / "data" / "processed" / "game_analytics.db"
SEGMENT_FILE = ROOT / "data" / "processed" / "players_segmented.csv"
ANOMALY_FILE = ROOT / "data" / "processed" / "players_anomalies.csv"
FORECAST_FILE = ROOT / "data" / "processed" / "player_acquisition_forecast.csv"

st.set_page_config(
    page_title="Game Analytics Platform",
    page_icon="🎮",
    layout="wide"
)


@st.cache_data
def load_data():
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM players", conn)
    segments = pd.read_csv(SEGMENT_FILE)
    anomalies = pd.read_csv(ANOMALY_FILE)
    forecast = pd.read_csv(FORECAST_FILE)
    return df, segments, anomalies, forecast

df, segments, anomalies, forecast = load_data()


st.title("🎮 Game Analytics Platform")
st.caption("Player engagement, monetization and behavioral analytics")


st.sidebar.header("Filters")

genres = ["All"] + sorted(df["game_genre"].unique().tolist())

selected_genre = st.sidebar.selectbox(
    "Game Genre",
    genres
)

engagements = ["All"] + sorted(
    df["engagement_level"].unique().tolist()
)

selected_engagement = st.sidebar.selectbox(
    "Engagement Level",
    engagements
)


filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["game_genre"] == selected_genre
    ]

if selected_engagement != "All":
    filtered_df = filtered_df[
        filtered_df["engagement_level"] == selected_engagement
    ]


st.header("Key Player Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Players",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Avg Sessions / Week",
        f"{filtered_df['sessions_per_week'].mean():.2f}"
    )

with col3:
    st.metric(
        "Avg Weekly Playtime",
        f"{filtered_df['play_time_hours_per_week'].mean():.2f} hrs"
    )

with col4:
    st.metric(
        "Total Revenue",
        f"${filtered_df['total_revenue_usd'].sum():,.0f}"
    )


st.divider()


col1, col2 = st.columns(2)

with col1:
    st.subheader("Players by Engagement")

    engagement_counts = (
        filtered_df["engagement_level"]
        .value_counts()
    )

    st.bar_chart(engagement_counts)


with col2:
    st.subheader("Revenue by Genre")

    genre_revenue = (
        filtered_df
        .groupby("game_genre")["total_revenue_usd"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(genre_revenue)


st.divider()


st.header("Player Segmentation")

segment_display = (
    segments
    .groupby("segment")
    .agg(
        players=("player_id", "count"),
        avg_sessions=("sessions_per_week", "mean"),
        avg_playtime=("play_time_hours_per_week", "mean"),
        avg_revenue=("total_revenue_usd", "mean"),
        avg_days_inactive=("days_since_last_seen", "mean")
    )
    .round(2)
)

st.dataframe(
    segment_display,
    use_container_width=True
)


st.divider()


st.header("Anomaly Detection")

anomaly_count = anomalies["is_anomaly"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Detected Anomalies",
        f"{anomaly_count:,}"
    )

with col2:
    st.metric(
        "Anomaly Rate",
        f"{100 * anomaly_count / len(anomalies):.2f}%"
    )


anomaly_players = anomalies[
    anomalies["is_anomaly"] == 1
].sort_values("anomaly_score")


st.dataframe(
    anomaly_players[
        [
            "player_id",
            "game_genre",
            "engagement_level",
            "sessions_per_week",
            "play_time_hours_per_week",
            "total_events",
            "total_revenue_usd",
            "anomaly_score"
        ]
    ].head(50),
    use_container_width=True
)


st.divider()


st.header("Top Revenue Players")

top_players = (
    filtered_df[
        [
            "player_id",
            "game_genre",
            "engagement_level",
            "sessions_per_week",
            "total_playtime_hours",
            "total_revenue_usd"
        ]
    ]
    .sort_values(
        "total_revenue_usd",
        ascending=False
    )
    .head(20)
)
st.divider()

st.header("Player Acquisition Forecast")

forecast["week"] = pd.to_datetime(forecast["week"])

historical = forecast[
    forecast["new_players"].notna()
][["week", "new_players"]]

future = forecast[
    forecast["forecast_new_players"].notna()
][["week", "forecast_new_players"]]

st.subheader("Weekly New Players")

st.line_chart(
    historical.set_index("week")["new_players"]
)

st.subheader("Next 8 Weeks Forecast")

st.dataframe(
    future,
    use_container_width=True
)

st.dataframe(
    top_players,
    use_container_width=True
)