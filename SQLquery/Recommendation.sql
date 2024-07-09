USE kpop_trading_card;
SELECT 
    c.card_name,
    c.artist,
    c.`group`,
    c.album,
    SUM(oi.quantity) AS total_quantity_sold,
    MAX(o.order_date) AS last_sold_date
FROM 
    `Order` o
JOIN 
    OrderItem oi ON o.id = oi.order_id
JOIN 
    Card c ON oi.card_id = c.id
WHERE 
    o.order_date >= NOW() - INTERVAL 3 MONTH
GROUP BY 
    c.card_name, c.artist, c.`group`, c.album
ORDER BY 
    total_quantity_sold DESC, last_sold_date DESC;
