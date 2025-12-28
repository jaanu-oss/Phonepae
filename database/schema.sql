-- PhonePe Pulse Database Schema
-- Run this script to create all required tables

CREATE DATABASE IF NOT EXISTS phonepe_pulse;
USE phonepe_pulse;

-- Aggregated Transactions Table
CREATE TABLE IF NOT EXISTS aggregated_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    transaction_type VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_record (state, year, quarter, transaction_type)
);

-- Aggregated Users Table
CREATE TABLE IF NOT EXISTS aggregated_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    registered_users BIGINT,
    app_opens BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_record (state, year, quarter)
);

-- Map Transactions Table
CREATE TABLE IF NOT EXISTS map_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    district VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_record (state, year, quarter, district)
);

-- Map Users Table
CREATE TABLE IF NOT EXISTS map_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    district VARCHAR(100),
    registered_users BIGINT,
    app_opens BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_record (state, year, quarter, district)
);

-- Top Transactions Table
CREATE TABLE IF NOT EXISTS top_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    entity_type VARCHAR(50),
    entity_name VARCHAR(200),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_record (state, year, quarter, entity_type, entity_name)
);

-- Top Users Table
CREATE TABLE IF NOT EXISTS top_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    entity_type VARCHAR(50),
    entity_name VARCHAR(200),
    registered_users BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_record (state, year, quarter, entity_type, entity_name)
);

-- Create indexes for better query performance
CREATE INDEX idx_state_year_quarter ON aggregated_transactions(state, year, quarter);
CREATE INDEX idx_state_year_quarter_users ON aggregated_users(state, year, quarter);
CREATE INDEX idx_map_state_year ON map_transactions(state, year, quarter);
CREATE INDEX idx_top_entity ON top_transactions(entity_type, entity_name);

