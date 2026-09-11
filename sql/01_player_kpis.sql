SELECT
    COUNT(*) AS total_players,
    ROUND(AVG(sessions_per_week), 2) AS avg_sessions_per_week,
    ROUND(AVG(play_time_hours_per_week), 2) AS avg_weekly_playtime,
    ROUND(AVG(avg_session_duration_minutes), 2) AS avg_session_duration,
    ROUND(SUM(total_revenue_usd), 2) AS total_revenue,
    ROUND(100.0 * AVG(purchase_flag), 2) AS purchase_rate_pct,
    ROUND(100.0 * AVG(at_risk), 2) AS at_risk_rate_pct
FROM players;