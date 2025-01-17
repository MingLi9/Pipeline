-- Create the user if it doesn't already exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'username'
    ) THEN
        CREATE ROLE username WITH LOGIN SUPERUSER PASSWORD 'password';
    END IF;
END $$;

-- Create the database if it doesn't already exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_database WHERE datname = 'auth_db'
    ) THEN
        CREATE DATABASE auth_db OWNER username;
    END IF;
END $$;

-- Connect to the auth_db database
\c auth_db;

-- Create necessary tables if they don't exist

-- Create users table based on User model
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- Increased size for hashed passwords
    first_name VARCHAR(128),  -- Optional
    last_name VARCHAR(128),   -- Optional
    age INTEGER,             -- Optional
    email VARCHAR(255) UNIQUE  -- Optional and unique
);

-- Create tokens table based on Token model
CREATE TABLE IF NOT EXISTS tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(512) UNIQUE NOT NULL,  -- Increased size for flexibility
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    issued_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,  -- Define expiration time
    revoked BOOLEAN DEFAULT FALSE
);
