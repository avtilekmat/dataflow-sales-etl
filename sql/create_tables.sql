CREATE TABLE IF NOT EXISTS sales (
    order_id INTEGER PRIMARY KEY,
    product VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2),
    quantity INTEGER,
    order_date DATE,
    total_price NUMERIC(12, 2)
);