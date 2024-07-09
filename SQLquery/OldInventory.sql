USE kpop_trading_card;
SELECT 
    c.card_name,
    c.artist,
    c.`group`,
    c.album,
    COALESCE(SUM(oi.quantity), 0) AS total_quantity_sold,
    MAX(o.order_date) AS last_sold_date,
    i.quantity_available
FROM 
    Card c
LEFT JOIN 
    OrderItem oi ON c.id = oi.card_id
LEFT JOIN 
    `Order` o ON o.id = oi.order_id AND o.order_date >= NOW() - INTERVAL 3 MONTH
JOIN 
    Inventory i ON c.id = i.card_id
GROUP BY 
    c.card_name, c.artist, c.`group`, c.album, i.quantity_available
ORDER BY 
    total_quantity_sold ASC, last_sold_date ASC
LIMIT 5;
