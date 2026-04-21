-- ============================================
-- Drivera Seed Data
-- B2B Fleet Rental Platform
-- ============================================

USE drivera;

-- --------------------------------------------
-- 5 Suppliers
-- All passwords are bcrypt hash of 'supplier123'
-- --------------------------------------------
INSERT INTO Supplier (company_name, contact_person, email, phone, location, latitude, longitude, verified, rating, description, password_hash) VALUES
('SpeedFleet India', 'Rajesh Sharma', 'rajesh@speedfleet.in', '9876543210', 'Mumbai, Maharashtra', 19.07600000, 72.87770000, 1, 4.5, 'Leading fleet provider in Mumbai with 200+ vehicles across sedans, SUVs, and mini-buses.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('DriveMax Logistics', 'Priya Patel', 'priya@drivemax.in', '9876543211', 'Pune, Maharashtra', 18.52040000, 73.85670000, 1, 4.2, 'Corporate travel specialists with a modern fleet of 150+ vehicles. ISO certified.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('GreenWheels Co.', 'Amit Deshmukh', 'amit@greenwheels.in', '9876543212', 'Bangalore, Karnataka', 12.97160000, 77.59460000, 0, 3.8, 'Eco-friendly fleet featuring hybrid and electric vehicles for sustainable corporate travel.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('RoadRunner Rentals', 'Sneha Kulkarni', 'sneha@roadrunner.in', '9876543213', 'Delhi, NCR', 28.70410000, 77.10250000, 1, 4.7, 'Premium fleet supplier for corporate events and long-term contracts. 300+ vehicles.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('FleetFirst Solutions', 'Vikram Joshi', 'vikram@fleetfirst.in', '9876543214', 'Hyderabad, Telangana', 17.38500000, 78.48670000, 0, 3.5, 'Affordable bulk vehicle rentals for SMEs and startups. Flexible contracts.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu');

-- --------------------------------------------
-- 10 Vehicles
-- --------------------------------------------
INSERT INTO Vehicle (type, model, brand, price_per_day, status, image_url) VALUES
('Sedan', 'Dzire', 'Maruti Suzuki', 1500.00, 'available', NULL),
('Sedan', 'City', 'Honda', 2200.00, 'available', NULL),
('SUV', 'Creta', 'Hyundai', 2800.00, 'available', NULL),
('SUV', 'Fortuner', 'Toyota', 5500.00, 'available', NULL),
('Hatchback', 'i20', 'Hyundai', 1200.00, 'available', NULL),
('Mini Bus', 'Traveller', 'Force', 4500.00, 'available', NULL),
('Van', 'Ertiga', 'Maruti Suzuki', 2000.00, 'available', NULL),
('Luxury', 'E-Class', 'Mercedes-Benz', 12000.00, 'available', NULL),
('Electric', 'Nexon EV', 'Tata', 3000.00, 'available', NULL),
('Pickup', 'Hilux', 'Toyota', 3500.00, 'available', NULL);

-- --------------------------------------------
-- Fleet Assignments (linking suppliers to vehicles)
-- --------------------------------------------
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES
(1, 1, 25), (1, 3, 15), (1, 6, 10),
(2, 2, 20), (2, 5, 30), (2, 7, 12),
(3, 9, 18), (3, 5, 10),
(4, 4, 8), (4, 8, 5), (4, 1, 40), (4, 3, 20),
(5, 1, 15), (5, 10, 10), (5, 7, 8);

-- --------------------------------------------
-- 3 Customers
-- All passwords are bcrypt hash of 'customer123'
-- --------------------------------------------
INSERT INTO Customer (name, contact, email, license_no, company_name, password_hash, role) VALUES
('Arjun Mehta', '9988776655', 'arjun@techcorp.in', 'MH01-2020-1234567', 'TechCorp Solutions', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu', 'renter'),
('Kavita Nair', '9988776656', 'kavita@eventpro.in', 'KA03-2019-7654321', 'EventPro India', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu', 'renter'),
('Admin User', '9988776600', 'admin@drivera.in', NULL, 'Drivera', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu', 'admin');

-- --------------------------------------------
-- Sample Bookings
-- --------------------------------------------
INSERT INTO Booking (customer_id, supplier_id, vehicle_id, fleet_size, start_date, end_date, total_cost, status) VALUES
(1, 1, 1, 5, '2026-05-01', '2026-05-07', 52500.00, 'confirmed'),
(1, 4, 4, 2, '2026-05-10', '2026-05-15', 55000.00, 'pending'),
(2, 2, 2, 10, '2026-06-01', '2026-06-03', 66000.00, 'confirmed');
