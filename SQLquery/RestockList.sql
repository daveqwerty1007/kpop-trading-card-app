USE kpop_trading_card;
SELECT 
    c.card_name,
    c.artist,
    c.`group`,
    c.album,
    SUM(oi.quantity) AS total_quantity_sold,
    MAX(o.order_date) AS last_sold_date,
    i.quantity_available
FROM 
    `order` o
JOIN 
    `order_item` oi ON o.id = oi.order_id
JOIN 
    `card` c ON oi.card_id = c.id
JOIN 
    `inventory` i ON c.id = i.card_id
WHERE 
    o.order_date >= NOW() - INTERVAL 3 MONTH
GROUP BY 
    c.card_name, c.artist, c.`group`, c.album, i.quantity_available
HAVING 
    i.quantity_available < 2
ORDER BY 
    total_quantity_sold DESC, last_sold_date DESC
LIMIT 10;

