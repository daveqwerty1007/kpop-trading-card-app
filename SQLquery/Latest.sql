USE kpop_trading_card;
SELECT 
    id,
    card_name,
    artist,
    `group`,
    album,
    price,
    description,
    image_url
FROM 
    Card
ORDER BY 
    id DESC
LIMIT 5;
