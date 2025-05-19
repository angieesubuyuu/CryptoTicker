CREATE DATABASE IF NOT EXISTS crypto_umg_db;
USE crypto_umg_db;

CREATE TABLE IF NOT EXISTS orders (
    name VARCHAR(100) NOT NULL,
    crypto_symbol VARCHAR(10) NOT NULL,
    order_type ENUM('BUY', 'SELL') NOT NULL,
    quantity DECIMAL(20,8) NOT NULL,
    price DECIMAL(20,2) NOT NULL,
    total_amount DECIMAL(20,2) NOT NULL,
    created_at DATETIME NOT NULL,
); 