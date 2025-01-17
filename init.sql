-- Create the user if it doesn't already exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'marketplace'
    ) THEN
        CREATE ROLE marketplace WITH LOGIN PASSWORD 'marketplace';
    END IF;
END $$;

-- Create the database if it doesn't already exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_database WHERE datname = 'marketplace_db'
    ) THEN
        CREATE DATABASE marketplace_db OWNER marketplace;
    END IF;
END $$;

\c marketplace_db;

-- Create necessary tables if they don't exist

-- Create users table based on User model
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(128) NOT NULL UNIQUE,
    reputation_score INTEGER,
    -- Optional fields can be added here if needed
    created_at TIMESTAMPTZ DEFAULT NOW() -- Add timestamp for record creation
);

-- Create products table based on Product model
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    seller_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    average_rating FLOAT DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW() -- Add timestamp for record creation
);

-- Create transactions table based on Transaction model
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    status VARCHAR(50), -- Consider ENUM for status
    created_at TIMESTAMPTZ DEFAULT NOW() -- Add timestamp for record creation
);

-- Create reviews table based on Review model
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- Assuming rating is between 1 and 5
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() -- Add timestamp for record creation
);
