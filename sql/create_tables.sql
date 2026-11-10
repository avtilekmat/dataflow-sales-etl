CREATE TABLE IF NOT EXISTS sales (
    order_id INTEGER PRIMARY KEY,
    product VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2),
    quantity INTEGER,
    order_date DATE,
    total_price NUMERIC(12, 2)
);

##analysis_history----------------

CREATE TABLE IF NOT EXISTS analysis_history (
    id BIGSERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    analyzed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_rows INTEGER NOT NULL,
    valid_rows INTEGER NOT NULL,
    removed_rows INTEGER NOT NULL,
    total_revenue NUMERIC(12, 2) NOT NULL,
    average_order NUMERIC(12, 2) NOT NULL,
    products_sold INTEGER NOT NULL
);











GRANT USAGE, SELECT ON SEQUENCE analysis_history_id_seq
TO dataflow_user;

GRANT SELECT, INSERT ON TABLE analysis_history
TO dataflow_user;