USE kpop_trading_card;

CREATE TABLE `User` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(150) UNIQUE NOT NULL,
    `password` VARCHAR(150) NOT NULL
);

CREATE TABLE `Card` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `card_name` VARCHAR(150) NOT NULL,
    `artist` VARCHAR(150) NOT NULL,
    `group` VARCHAR(150) NOT NULL,
    `album` VARCHAR(150),
    `price` FLOAT NOT NULL,
    `description` VARCHAR(500),
    `image_url` VARCHAR(200)
);

CREATE TABLE `Order` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `order_date` DATETIME NOT NULL,
    `total_amount` FLOAT NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `User`(`id`)
);

CREATE TABLE `Payment` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `order_id` INT NOT NULL,
    `payment_date` DATETIME NOT NULL,
    `payment_method` VARCHAR(50) NOT NULL,
    `payment_status` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`order_id`) REFERENCES `Order`(`id`)
);

CREATE TABLE `Inventory` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `card_id` INT NOT NULL,
    `quantity_available` INT NOT NULL,
    FOREIGN KEY (`card_id`) REFERENCES Card(`id`)
);

CREATE TABLE `Admin` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(150),
    `email` VARCHAR(150) UNIQUE,
    `password` VARCHAR(150)
);

CREATE TABLE `CartItem` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `card_id` INT NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    FOREIGN KEY (`user_id`) REFERENCES User(`id`),
    FOREIGN KEY (`card_id`) REFERENCES Card(`id`)
);

CREATE TABLE OrderItem (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    card_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `Order`(id),
    FOREIGN KEY (card_id) REFERENCES Card(id)
);

