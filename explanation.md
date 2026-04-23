# Drivera: B2B Fleet Rental Platform - Project Explanation

## 1. Application Structure
Drivera is built using a classic monolithic architecture based on the Model-View-Template (MVT/MVC) pattern. The backend handles secure routing, business logic, and database operations, while the frontend is responsible for the presentation layer and dynamic user interactions like map rendering and real-time filtering.

## 2. Technology Stack & Languages

### Frontend
- **Languages/Technologies**: HTML5, CSS3, JavaScript (Vanilla JS), Jinja2.
- **Explanation**: HTML and Jinja2 structure the web pages and dynamically inject data sent from the backend server. Custom CSS provides the modern, responsive dark-theme design, while Vanilla JavaScript handles interactive elements like the Leaflet.js map and real-time search filtering without requiring page reloads.

### Backend
- **Languages/Technologies**: Python (Flask Framework).
- **Explanation**: Python acts as the core engine processing client HTTP requests, handling secure authentication (bcrypt), and managing the database connection. The Flask framework is utilized for its lightweight nature, easily mapping URLs to specific Python functions and managing user session states securely.

---

## 3. Practical Application of DBMS Concepts

This project relies heavily on core Database Management System (DBMS) concepts to ensure data integrity, efficiency, and security using **MySQL**.

### A. Relational Schema & Normalization
- **Application**: The database is structured into 5 distinct tables (`Customer`, `Supplier`, `Vehicle`, `Fleet`, `Booking`) to minimize data redundancy (aiming for 3NF). For example, rather than storing vehicle brand and model inside every single booking record, the system stores a reference to a central `Vehicle` table.

### B. Foreign Keys & Referential Integrity
- **Application**: Tables like `Fleet` and `Booking` rely on Foreign Keys referencing `supplier_id`, `vehicle_id`, and `customer_id`. We utilize constraints like `ON DELETE CASCADE` so that if a supplier's account is removed, all their associated fleet listings are safely deleted without leaving broken, orphaned data behind.

### C. Joins (INNER & LEFT JOIN)
- **Application**: Fetching complex data requires combining multiple tables. A `LEFT JOIN` is used on the booking/search page to list suppliers alongside their fleet data, ensuring that even newly registered suppliers with zero vehicles currently listed are still successfully fetched and displayed.

### D. Aggregate Functions (COUNT, SUM, MIN, GROUP_CONCAT)
- **Application**: To optimize performance, the backend offloads computation to the database using SQL aggregation. `SUM(available_count)` calculates total vehicles, `MIN(price_per_day)` determines the "starting from" price, and `GROUP_CONCAT(DISTINCT type)` merges all available vehicle types into a single string for frontend filtering.

### E. Parameterized Queries (Security/SQL Injection Prevention)
- **Application**: All data insertions (registrations, bookings) and lookups use parameterized queries (e.g., `WHERE email = %s`). This is a critical security measure that prevents SQL Injection attacks by ensuring user inputs are treated strictly as literal strings rather than executable SQL commands.

### F. ACID Properties (Transactions)
- **Application**: When an admin verifies a supplier or a user creates a booking, the system uses explicit transactions (`db.commit()`). If an error occurs during the database execution phase, the `try...except` blocks ensure the transaction is ignored, preventing partial or corrupted data from being permanently saved (Atomicity).
