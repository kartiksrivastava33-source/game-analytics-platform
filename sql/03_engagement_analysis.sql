WITH engagement_metrics AS (
    SELECT
        engagement_level,
        COUNT(*) AS players,
        AVG(sessions_per_week) AS avg_sessions,
        AVG(play_time_hours_per_week) AS avg_playtime,
        AVG(total_revenue_usd) AS avg_revenue,
        AVG(purchase_flag) AS purchase_rate
    FROM players
    GROUP BY engagement_level
)
SELECT
    engagement_level,
    players,
    ROUND(avg_sessions, 2) AS avg_sessions,
    ROUND(avg_playtime, 2) AS avg_playtime,
    ROUND(avg_revenue, 2) AS avg_revenue,
    ROUND(100.0 * purchase_rate, 2) AS purchase_rate_pct
FROM engagement_metrics
ORDER BY
    CASE engagement_level
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
    END;