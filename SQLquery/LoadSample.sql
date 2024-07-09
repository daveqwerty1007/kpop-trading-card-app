USE kpop_trading_card;
INSERT INTO `User` (`name`, `email`, `password`) VALUES
('Alice Smith', 'alice@example.com', 'password123'),
('Bob Johnson', 'bob@example.com', 'password456'),
('Carol Williams', 'carol@example.com', 'password789'),
('David Brown', 'david@example.com', 'password101'),
('Eva Green', 'eva@example.com', 'password102');

INSERT INTO `Card` (`card_name`, `artist`, `group`, `album`, `price`, `description`, `image_url`) VALUES
('Blue Rose', 'Lisa', 'BlackPink', 'The Album', 10.99, 'A rare card featuring Lisa from BlackPink.', 'url_to_image1'),
('Red Sun', 'Jennie', 'BlackPink', 'The Album', 12.99, 'A rare card featuring Jennie from BlackPink.', 'url_to_image2'),
('Golden Hour', 'Jisoo', 'BlackPink', 'The Album', 11.99, 'A rare card featuring Jisoo from BlackPink.', 'url_to_image3'),
('Purple Moon', 'Rosé', 'BlackPink', 'The Album', 13.99, 'A rare card featuring Rosé from BlackPink.', 'url_to_image4'),
('Silver Star', 'Lisa', 'BlackPink', 'The Album', 14.99, 'A rare card featuring Lisa from BlackPink.', 'url_to_image5');

INSERT INTO `Order` (`user_id`, `order_date`, `total_amount`) VALUES
(1, '2024-07-01 10:00:00', 25.98),
(2, '2024-07-02 12:00:00', 10.99),
(3, '2024-07-03 14:00:00', 30.99),
(4, '2024-07-04 16:00:00', 40.99),
(5, '2024-07-05 18:00:00', 50.99);

INSERT INTO `Payment` (`order_id`, `payment_date`, `payment_method`, `payment_status`) VALUES
(1, '2024-07-01 10:05:00', 'Credit Card', 'Completed'),
(2, '2024-07-02 12:05:00', 'PayPal', 'Completed'),
(3, '2024-07-03 14:05:00', 'Credit Card', 'Completed'),
(4, '2024-07-04 16:05:00', 'Debit Card', 'Completed'),
(5, '2024-07-05 18:05:00', 'Credit Card', 'Completed');

INSERT INTO `Inventory` (`card_id`, `quantity_available`) VALUES
(1, 50),
(2, 30),
(3, 20),
(4, 15),
(5, 25);

INSERT INTO `Admin` (`name`, `email`, `password`) VALUES
('Admin User', 'admin@example.com', 'adminpass'),
('Super Admin', 'superadmin@example.com', 'superpass');

INSERT INTO `CartItem` (`user_id`, `card_id`, `quantity`) VALUES
(1, 1, 2),
(2, 3, 1),
(3, 2, 3),
(4, 4, 1),
(5, 5, 2);

INSERT INTO `OrderItem` (`order_id`, `card_id`, `quantity`) VALUES
(1, 1, 2),
(2, 3, 1),
(3, 2, 3),
(4, 4, 1),
(5, 5, 2);
