SELECT
    game_genre,
    COUNT(*) AS players,
    ROUND(AVG(sessions_per_week), 2) AS avg_sessions_per_week,
    ROUND(AVG(play_time_hours_per_week), 2) AS avg_weekly_playtime,
    ROUND(AVG(avg_session_duration_minutes), 2) AS avg_session_duration,
    ROUND(100.0 * AVG(purchase_flag), 2) AS purchase_rate_pct,
    ROUND(SUM(total_revenue_usd), 2) AS total_revenue
FROM players
GROUP BY game_genre
ORDER BY total_revenue DESC;