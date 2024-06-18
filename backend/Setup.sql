-- Use the database
USE kpop_trading;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS Shipping;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Warehouse;
DROP TABLE IF EXISTS Branch;
DROP TABLE IF EXISTS Delivery;
DROP TABLE IF EXISTS KpopGroup;

-- Create tables first without foreign keys
CREATE TABLE IF NOT EXISTS KpopGroup (
    GroupID INT AUTO_INCREMENT PRIMARY KEY,
    GroupName VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Delivery (
    DeliveryID INT AUTO_INCREMENT PRIMARY KEY,
    DeliveryMethod VARCHAR(255) NOT NULL,
    Cost DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Branch (
    BranchID INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Warehouse (
    WarehouseID INT AUTO_INCREMENT PRIMARY KEY,
    WarehouseLocation VARCHAR(255) NOT NULL,
    ProductName VARCHAR(255),
    NumberInStock INT
);

CREATE TABLE IF NOT EXISTS Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    PhoneNumber VARCHAR(255),
    Address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Product (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    SellingPrice DECIMAL(10, 2) NOT NULL,
    GroupID INT
);

CREATE TABLE IF NOT EXISTS `Order` (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    OrderNumber VARCHAR(255) NOT NULL,
    ProductID INT,
    NumberOfItems INT,
    Price DECIMAL(10, 2),
    Branch VARCHAR(255),
    Date DATETIME,
    Time TIME,
    EmployeeID INT,
    CustomerID INT,
    Status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Employee (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    KPI VARCHAR(255),
    Warehouse VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Shipping (
    ShippingNumber INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    NumberOfItems INT,
    `From` VARCHAR(255),
    `To` VARCHAR(255),
    EmployeeID INT,
    CustomerID INT,
    Status VARCHAR(255)
);

-- Add foreign key constraints after all tables are created
ALTER TABLE Product
ADD CONSTRAINT fk_product_group
FOREIGN KEY (GroupID) REFERENCES KpopGroup(GroupID);

ALTER TABLE `Order`
ADD CONSTRAINT fk_order_product
FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
ADD CONSTRAINT fk_order_employee
FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
ADD CONSTRAINT fk_order_customer
FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID);

ALTER TABLE Shipping
ADD CONSTRAINT fk_shipping_order
FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
ADD CONSTRAINT fk_shipping_product
FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
ADD CONSTRAINT fk_shipping_employee
FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
ADD CONSTRAINT fk_shipping_customer
FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID);
