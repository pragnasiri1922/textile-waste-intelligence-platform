-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    email VARCHAR(100) UNIQUE,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Waste Batches Table
CREATE TABLE waste_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id VARCHAR(50) UNIQUE NOT NULL,
    fabric_type VARCHAR(50) NOT NULL,
    source VARCHAR(100) NOT NULL,
    quantity_kg FLOAT NOT NULL,
    color VARCHAR(30),
    condition VARCHAR(50),
    waste_category VARCHAR(50),
    recyclability_score FLOAT,
    contamination_level VARCHAR(30),
    damage_level VARCHAR(30),
    registered_by INTEGER,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (registered_by) REFERENCES users(id)
);

-- Textile Analyses Table
CREATE TABLE textile_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    image_url VARCHAR(255),
    analysis_results TEXT,
    confidence_score FLOAT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES waste_batches(id)
);

-- Collection Records Table
CREATE TABLE collection_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    collection_date DATE NOT NULL,
    location VARCHAR(100),
    collector_id INTEGER,
    status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (batch_id) REFERENCES waste_batches(id),
    FOREIGN KEY (collector_id) REFERENCES users(id)
);

CREATE INDEX idx_waste_batches_batch_id ON waste_batches(batch_id);
CREATE INDEX idx_users_username ON users(username);
