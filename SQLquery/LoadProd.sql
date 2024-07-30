-- Use the kpop_trading_card database
USE kpop_trading_card;

-- Insert Users
INSERT INTO `User` (`name`, `email`, `password`) VALUES
('Alice Smith', 'alice@example.com', 'password123'),
('Bob Johnson', 'bob@example.com', 'password456'),
('Carol Williams', 'carol@example.com', 'password789'),
('David Brown', 'david@example.com', 'password101'),
('Eva Green', 'eva@example.com', 'password102'),
('Frank White', 'frank@example.com', 'password103'),
('Grace Adams', 'grace@example.com', 'password104'),
('Henry Wilson', 'henry@example.com', 'password105'),
('Irene King', 'irene@example.com', 'password106'),
('Jack Lee', 'jack@example.com', 'password107'),
('Karen Hall', 'karen@example.com', 'password108'),
('Leo Turner', 'leo@example.com', 'password109'),
('Mona Wright', 'mona@example.com', 'password110'),
('Nancy Perez', 'nancy@example.com', 'password111'),
('Oscar Young', 'oscar@example.com', 'password112'),
('Paul Baker', 'paul@example.com', 'password113'),
('Quinn Scott', 'quinn@example.com', 'password114'),
('Rachel Evans', 'rachel@example.com', 'password115'),
('Steve Harris', 'steve@example.com', 'password116'),
('Tina Martin', 'tina@example.com', 'password117');

-- Insert Cards
INSERT INTO `Card` (`card_name`, `artist`, `group`, `album`, `price`, `description`, `image_url`) VALUES
('Blue Rose', 'Lisa', 'BlackPink', 'The Album', 10.99, 'A rare card featuring Lisa from BlackPink.', 'url_to_image1'),
('Red Sun', 'Jennie', 'BlackPink', 'The Album', 12.99, 'A rare card featuring Jennie from BlackPink.', 'url_to_image2'),
('Golden Hour', 'Jisoo', 'BlackPink', 'The Album', 11.99, 'A rare card featuring Jisoo from BlackPink.', 'url_to_image3'),
('Purple Moon', 'Rosé', 'BlackPink', 'The Album', 13.99, 'A rare card featuring Rosé from BlackPink.', 'url_to_image4'),
('Silver Star', 'Lisa', 'BlackPink', 'The Album', 14.99, 'A rare card featuring Lisa from BlackPink.', 'url_to_image5'),
('Golden Star', 'V', 'BTS', 'Map of the Soul: 7', 15.99, 'A rare card featuring V from BTS.', 'url_to_image6'),
('Purple Heart', 'Jimin', 'BTS', 'Map of the Soul: 7', 16.99, 'A rare card featuring Jimin from BTS.', 'url_to_image7'),
('Silver Moon', 'RM', 'BTS', 'Map of the Soul: 7', 17.99, 'A rare card featuring RM from BTS.', 'url_to_image8'),
('Red Heart', 'Jin', 'BTS', 'Map of the Soul: 7', 18.99, 'A rare card featuring Jin from BTS.', 'url_to_image9'),
('Blue Moon', 'Suga', 'BTS', 'Map of the Soul: 7', 19.99, 'A rare card featuring Suga from BTS.', 'url_to_image10');

-- Insert Orders
INSERT INTO `Order` (`user_id`, `order_date`, `total_amount`) VALUES
(1, '2024-07-01 10:00:00', 25.98),
(2, '2024-07-02 12:00:00', 10.99),
(3, '2024-07-03 14:00:00', 30.99),
(4, '2024-07-04 16:00:00', 40.99),
(5, '2024-07-05 18:00:00', 50.99),
(6, '2024-07-06 09:00:00', 60.99),
(7, '2024-07-07 11:00:00', 70.99),
(8, '2024-07-08 13:00:00', 80.99),
(9, '2024-07-09 15:00:00', 90.99),
(10, '2024-07-10 17:00:00', 100.99),
(11, '2024-07-11 10:00:00', 110.99),
(12, '2024-07-12 12:00:00', 120.99),
(13, '2024-07-13 14:00:00', 130.99),
(14, '2024-07-14 16:00:00', 140.99),
(15, '2024-07-15 18:00:00', 150.99),
(16, '2024-07-16 09:00:00', 160.99),
(17, '2024-07-17 11:00:00', 170.99),
(18, '2024-07-18 13:00:00', 180.99),
(19, '2024-07-19 15:00:00', 190.99),
(20, '2024-07-20 17:00:00', 200.99);

-- Insert Payments
INSERT INTO `Payment` (`order_id`, `payment_date`, `payment_method`, `payment_status`) VALUES
(1, '2024-07-01 10:05:00', 'Credit Card', 'Completed'),
(2, '2024-07-02 12:05:00', 'PayPal', 'Completed'),
(3, '2024-07-03 14:05:00', 'Credit Card', 'Completed'),
(4, '2024-07-04 16:05:00', 'Debit Card', 'Completed'),
(5, '2024-07-05 18:05:00', 'Credit Card', 'Completed'),
(6, '2024-07-06 09:05:00', 'PayPal', 'Completed'),
(7, '2024-07-07 11:05:00', 'Credit Card', 'Completed'),
(8, '2024-07-08 13:05:00', 'Debit Card', 'Completed'),
(9, '2024-07-09 15:05:00', 'Credit Card', 'Completed'),
(10, '2024-07-10 17:05:00', 'PayPal', 'Completed'),
(11, '2024-07-11 10:05:00', 'Credit Card', 'Completed'),
(12, '2024-07-12 12:05:00', 'Debit Card', 'Completed'),
(13, '2024-07-13 14:05:00', 'Credit Card', 'Completed'),
(14, '2024-07-14 16:05:00', 'PayPal', 'Completed'),
(15, '2024-07-15 18:05:00', 'Credit Card', 'Completed'),
(16, '2024-07-16 09:05:00', 'Debit Card', 'Completed'),
(17, '2024-07-17 11:05:00', 'Credit Card', 'Completed'),
(18, '2024-07-18 13:05:00', 'PayPal', 'Completed'),
(19, '2024-07-19 15:05:00', 'Credit Card', 'Completed'),
(20, '2024-07-20 17:05:00', 'Debit Card', 'Completed');

-- Insert Inventory
INSERT INTO `Inventory` (`card_id`, `quantity_available`) VALUES
(1, 50),
(2, 30),
(3, 20),
(4, 15),
(5, 25),
(6, 40),
(7, 60),
(8, 70),
(9, 35),
(10, 45);

-- Insert Admins
INSERT INTO `Admin` (`name`, `email`, `password`) VALUES
('Admin User', 'admin@example.com', 'adminpass'),
('Super Admin', 'superadmin@example.com', 'superpass'),
('Manager', 'manager@example.com', 'managerpass'),
('Support', 'support@example.com', 'supportpass');

-- Insert CartItems
INSERT INTO `CartItem` (`user_id`, `card_id`, `quantity`) VALUES
(1, 1, 2),
(2, 3, 1),
(3, 2, 3),
(4, 4, 1),
(5, 5, 2),
(6, 6, 1),
(7, 7, 2),
(8, 8, 3),
(9, 9, 1),
(10, 10, 1),
(11, 1, 2),
(12, 3, 1),
(13, 2, 3),
(14, 4, 1),
(15, 5, 2),
(16, 6, 1),
(17, 7, 2),
(18, 8, 3),
(19, 9, 1),
(20, 10, 1);

-- Insert OrderItems
INSERT INTO `OrderItem` (`order_id`, `card_id`, `quantity`) VALUES
(1, 1, 2),
(2, 3, 1),
(3, 2, 3),
(4, 4, 1),
(5, 5, 2),
(6, 6, 1),
(7, 7, 2),
(8, 8, 3),
(9, 9, 1),
(10, 10, 1),
(11, 1, 2),
(12, 3, 1),
(13, 2, 3),
(14, 4, 1),
(15, 5, 2),
(16, 6, 1),
(17, 7, 2),
(18, 8, 3),
(19, 9, 1),
(20, 10, 1);
