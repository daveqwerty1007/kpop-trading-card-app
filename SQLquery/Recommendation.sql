USE kpop_trading;
SELECT 
    c.card_name,
    c.artist,
    c.`group`,
    c.album,
    SUM(oi.quantity) AS total_quantity_sold,
    MAX(o.order_date) AS last_sold_date
FROM 
    `order` o
JOIN 
    order_item oi ON o.id = oi.order_id
JOIN 
    card c ON oi.card_id = c.id
WHERE 
    o.order_date >= NOW() - INTERVAL 3 MONTH
GROUP BY 
    c.card_name, c.artist, c.`group`, c.album
ORDER BY 
    total_quantity_sold DESC, last_sold_date DESC;
