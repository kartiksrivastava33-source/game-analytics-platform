SELECT
    player_id,
    game_genre,
    engagement_level,
    total_playtime_hours,
    total_revenue_usd,
    RANK() OVER (
        ORDER BY total_revenue_usd DESC
    ) AS revenue_rank,
    RANK() OVER (
        PARTITION BY game_genre
        ORDER BY total_revenue_usd DESC
    ) AS genre_revenue_rank
FROM players
ORDER BY revenue_rank
LIMIT 50;