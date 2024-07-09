SELECT 
    u.name AS customer_name,
    u.email AS customer_email,
    o.id AS order_id,
    o.order_date,
    p.payment_status
FROM 
    `Order` o
JOIN 
    `User` u ON o.user_id = u.id
LEFT JOIN 
    Payment p ON o.id = p.order_id
WHERE 
    o.order_date <= NOW() - INTERVAL 7 DAY
    AND (p.payment_status IS NULL OR p.payment_status != 'Completed');
