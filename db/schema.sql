-- ============================================
-- Drivera Database Schema
-- B2B Fleet Rental Platform
-- ============================================

CREATE DATABASE IF NOT EXISTS drivera;
USE drivera;

-- --------------------------------------------
-- Supplier Table
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS Supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    location VARCHAR(200),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    verified TINYINT(1) DEFAULT 0,
    rating DECIMAL(2, 1) DEFAULT 0.0,
    description TEXT,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------
-- Customer Table
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20),
    email VARCHAR(100) NOT NULL UNIQUE,
    license_no VARCHAR(50),
    company_name VARCHAR(150),
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('renter', 'admin') DEFAULT 'renter',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------
-- Vehicle Table
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS Vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    brand VARCHAR(80) NOT NULL,
    price_per_day DECIMAL(10, 2) NOT NULL,
    status ENUM('available', 'rented', 'maintenance') DEFAULT 'available',
    image_url VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------
-- Fleet Table (links Suppliers to Vehicles)
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS Fleet (
    fleet_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    available_count INT DEFAULT 0,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id) ON DELETE CASCADE
);

-- --------------------------------------------
-- Booking Table
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS Booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    supplier_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    fleet_size INT DEFAULT 1,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_cost DECIMAL(12, 2),
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id) ON DELETE CASCADE
);
