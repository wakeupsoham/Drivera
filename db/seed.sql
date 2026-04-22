-- ============================================
-- Drivera Seed Data
-- B2B Fleet Rental Platform
-- ============================================

USE drivera;

-- --------------------------------------------
-- 10 Suppliers in Major Indian Cities
-- All passwords are bcrypt hash of 'supplier123'
-- --------------------------------------------
INSERT INTO Supplier (company_name, contact_person, email, phone, location, latitude, longitude, verified, rating, description, password_hash) VALUES
('SpeedFleet Mumbai', 'Rajesh Sharma', 'rajesh@speedfleet.in', '9876543210', 'Mumbai, Maharashtra', 19.0760, 72.8777, 1, 4.8, 'Premier fleet provider in Mumbai with a focus on high-end sedans and SUVs.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Delhi Metro Fleets', 'Anita Gupta', 'anita@delhifleets.in', '9876543211', 'Delhi, NCR', 28.7041, 77.1025, 1, 4.6, 'Largest network of corporate vehicles in the capital region. 24/7 support.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Silicon Valley Rentals', 'Karthik Rao', 'karthik@svrentals.in', '9876543212', 'Bangalore, Karnataka', 12.9716, 77.5946, 1, 4.7, 'Specializing in tech-enabled fleet management for Bangalore startups and giants.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Charminar Chauffeurs', 'Mohammed Ali', 'ali@charminar.in', '9876543213', 'Hyderabad, Telangana', 17.3850, 78.4867, 0, 4.2, 'Reliable bulk rentals for events and corporate travel across Hyderabad.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Pune Prestige Wheels', 'Vikram Deshmukh', 'vikram@punewheels.in', '9876543214', 'Pune, Maharashtra', 18.5204, 73.8567, 1, 4.5, 'Luxury and executive fleet specialists based in the heart of Pune.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Marina Motors Chennai', 'Suresh Kumar', 'suresh@marinamotors.in', '9876543215', 'Chennai, Tamil Nadu', 13.0827, 80.2707, 1, 4.4, 'Leading supplier for automotive and logistics sectors in Southern India.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Victoria Fleet Kolkata', 'Joydeep Ghosh', 'joydeep@victoriafleet.in', '9876543216', 'Kolkata, West Bengal', 22.5726, 88.3639, 0, 4.1, 'Traditional excellence in fleet rentals for the cultural capital.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
 Sabarmati Services', 'Mehul Shah', 'mehul@sabarmati.in', '9876543217', 'Ahmedabad, Gujarat', 23.0225, 72.5714, 1, 4.3, 'Efficient and cost-effective bulk vehicle solutions for Gujarat businesses.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Pink City Rentals', 'Padma Singh', 'padma@pinkcity.in', '9876543218', 'Jaipur, Rajasthan', 26.9124, 75.7873, 0, 4.0, 'Bespoke fleet rentals for the tourism and hospitality hub of Jaipur.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu'),
('Diamond City Fleets', 'Rohan Mehta', 'rohan@diamondcity.in', '9876543219', 'Surat, Gujarat', 21.1702, 72.8311, 1, 4.4, 'Robust fleet inventory supporting the diamond and textile industries of Surat.', '$2b$12$LJ3m5ZQnJdGp1S5x5r5cTuO8X8Pk5JZ8YV7gN5wE2rA4bH6cK9dWu');

-- --------------------------------------------
-- 40 Vehicles with variable prices for search variety
-- --------------------------------------------
INSERT INTO Vehicle (type, model, brand, price_per_day, status) VALUES
('Sedan', 'Dzire', 'Maruti Suzuki', 1500.00, 'available'),
('Sedan', 'Dzire', 'Maruti Suzuki', 1600.00, 'available'),
('Sedan', 'City', 'Honda', 2200.00, 'available'),
('Sedan', 'City', 'Honda', 2400.00, 'available'),
('Sedan', 'Verna', 'Hyundai', 2000.00, 'available'),
('Sedan', 'Verna', 'Hyundai', 2100.00, 'available'),
('Sedan', 'Slavia', 'Skoda', 2500.00, 'available'),
('SUV', 'Creta', 'Hyundai', 2800.00, 'available'),
('SUV', 'Creta', 'Hyundai', 3000.00, 'available'),
('SUV', 'Seltos', 'Kia', 2900.00, 'available'),
('SUV', 'Seltos', 'Kia', 3100.00, 'available'),
('SUV', 'Fortuner', 'Toyota', 5500.00, 'available'),
('SUV', 'Fortuner', 'Toyota', 6000.00, 'available'),
('SUV', 'Scorpio-N', 'Mahindra', 3500.00, 'available'),
('SUV', 'XUV700', 'Mahindra', 4000.00, 'available'),
('Hatchback', 'Swift', 'Maruti Suzuki', 1200.00, 'available'),
('Hatchback', 'Swift', 'Maruti Suzuki', 1300.00, 'available'),
('Hatchback', 'i20', 'Hyundai', 1400.00, 'available'),
('Hatchback', 'i20', 'Hyundai', 1500.00, 'available'),
('Hatchback', 'Altroz', 'Tata', 1350.00, 'available'),
('Hatchback', 'Baleno', 'Maruti Suzuki', 1450.00, 'available'),
('Mini Bus', 'Traveller', 'Force', 4500.00, 'available'),
('Mini Bus', 'Traveller', 'Force', 4800.00, 'available'),
('Mini Bus', 'Traveller', 'Force', 5000.00, 'available'),
('Mini Bus', 'Winger', 'Tata', 4200.00, 'available'),
('Mini Bus', 'Winger', 'Tata', 4400.00, 'available'),
('Van', 'Ertiga', 'Maruti Suzuki', 2000.00, 'available'),
('Van', 'Ertiga', 'Maruti Suzuki', 2200.00, 'available'),
('Van', 'Carens', 'Kia', 2500.00, 'available'),
('Van', 'Carens', 'Kia', 2700.00, 'available'),
('Luxury', 'E-Class', 'Mercedes-Benz', 12000.00, 'available'),
('Luxury', 'E-Class', 'Mercedes-Benz', 13000.00, 'available'),
('Luxury', '5-Series', 'BMW', 11500.00, 'available'),
('Luxury', 'A6', 'Audi', 11000.00, 'available'),
('Electric', 'Nexon EV', 'Tata', 3000.00, 'available'),
('Electric', 'Nexon EV', 'Tata', 3200.00, 'available'),
('Electric', 'ZS EV', 'MG', 3500.00, 'available'),
('Electric', 'Tigor EV', 'Tata', 2500.00, 'available'),
('Pickup', 'Hilux', 'Toyota', 3500.00, 'available'),
('Pickup', 'V-Cross', 'Isuzu', 3200.00, 'available');

-- --------------------------------------------
-- Fleet Assignments
-- Each of the 10 suppliers gets ~20 vehicles (4 types x 5 each)
-- --------------------------------------------

-- S1: Mumbai (Sedan, SUV, Luxury, Electric)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(1, 1, 5), (1, 8, 5), (1, 31, 5), (1, 35, 5);

-- S2: Delhi (Sedan, SUV, Mini Bus, Van)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(2, 3, 5), (2, 10, 5), (2, 22, 5), (2, 27, 5);

-- S3: Bangalore (Electric, Sedan, Hatchback, SUV)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(3, 35, 5), (3, 37, 5), (3, 5, 5), (3, 16, 5), (3, 12, 5);

-- S4: Hyderabad (Sedan, SUV, Van, Pickup)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(4, 2, 5), (4, 14, 5), (4, 29, 5), (4, 39, 5);

-- S5: Pune (Luxury, Sedan, SUV, Electric)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(5, 33, 5), (5, 7, 5), (5, 15, 5), (5, 36, 5);

-- S6: Chennai (SUV, Pickup, Van, Sedan)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(6, 12, 5), (6, 40, 5), (6, 28, 5), (6, 4, 5);

-- S7: Kolkata (Hatchback, Sedan, SUV, Mini Bus)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(7, 18, 5), (7, 6, 5), (7, 9, 5), (7, 25, 5);

-- S8: Ahmedabad (Sedan, SUV, Van, Electric)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(8, 1, 5), (8, 11, 5), (8, 30, 5), (8, 38, 5);

-- S9: Jaipur (Luxury, SUV, Mini Bus, Sedan)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(9, 32, 5), (9, 13, 5), (9, 23, 5), (9, 7, 5);

-- S10: Surat (Van, Sedan, SUV, Hatchback)
INSERT INTO Fleet (supplier_id, vehicle_id, available_count) VALUES 
(10, 27, 5), (10, 2, 5), (10, 14, 5), (10, 21, 5);


-- --------------------------------------------
-- Customers
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
(1, 2, 3, 2, '2026-05-10', '2026-05-15', 22000.00, 'pending'),
(2, 3, 35, 10, '2026-06-01', '2026-06-03', 60000.00, 'confirmed');
