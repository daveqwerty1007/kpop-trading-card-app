USE kpop_trading_card;
SELECT 
    u.id,
    u.name,
    u.email,
    SUM(o.total_amount) AS total_spent
FROM 
    `Order` o
JOIN 
    `User` u ON o.user_id = u.id
GROUP BY 
    u.id, u.name, u.email
ORDER BY 
    total_spent DESC
LIMIT 5;
