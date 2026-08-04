-- Textile Waste Intelligence Platform - Database Schema
-- This schema matches the SQLAlchemy ORM models in backend/app/models.py

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'operator',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Waste Batches Table
CREATE TABLE IF NOT EXISTS waste_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id VARCHAR(50) UNIQUE NOT NULL,
    fabric_type VARCHAR(50) NOT NULL,
    source VARCHAR(100) NOT NULL,
    quantity_kg FLOAT NOT NULL,
    color VARCHAR(30),
    condition VARCHAR(50),
    waste_category VARCHAR(50),
    recyclability_score FLOAT,
    contamination_level VARCHAR(30) DEFAULT 'None',
    damage_level VARCHAR(30) DEFAULT 'None',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Textile Analysis Table
CREATE TABLE IF NOT EXISTS textile_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    material_detected VARCHAR(50),
    confidence FLOAT,
    texture VARCHAR(50),
    pattern VARCHAR(50),
    fabric_color VARCHAR(30),
    damage_level VARCHAR(30),
    contamination_level VARCHAR(30),
    reuse_potential VARCHAR(50),
    disposal_recommendation VARCHAR(100),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES waste_batches(id)
);

-- Collection Records Table
CREATE TABLE IF NOT EXISTS collection_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name VARCHAR(100),
    collection_date DATE,
    total_weight_kg FLOAT,
    items_count INTEGER,
    status VARCHAR(30),
    collector_name VARCHAR(100),
    notes TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_waste_batches_batch_id ON waste_batches(batch_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
