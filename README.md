# Drivera: B2B Fleet Rental Platform

Drivera is a comprehensive business-to-business platform designed to connect corporate clients with verified vehicle fleet suppliers across major Indian cities. The application facilitates bulk vehicle rentals, supplier management, and secure booking lifecycles.

## Key Features

*   **Advanced Fleet Search**: Users can search for suppliers using a dynamic, interactive map interface with real-time filtering by location, vehicle type, and fleet size.
*   **Supplier Profiles**: Dedicated pages for each supplier showcasing their available fleet, pricing, and contact information.
*   **Bulk Booking System**: Customers can book multiple vehicles at once, with automatic cost calculation based on fleet size and rental duration.
*   **Interactive Admin Dashboard**: Administrators can actively manage the platform by verifying or rejecting new supplier applications and confirming or cancelling pending bookings.
*   **Secure Authentication**: Role-based access control (Admin, Renter, Supplier) with secure password hashing and session management.

## Technology Stack

*   **Backend**: Python, Flask
*   **Database**: MySQL (using mysql-connector-python)
*   **Frontend**: HTML5, Vanilla CSS3, JavaScript (Vanilla)
*   **Integrations**: Leaflet.js (Interactive Maps)

## Local Setup and Installation

Follow these steps to run the application on your local machine.

### Prerequisites
*   Python 3.8 or higher
*   MySQL Server running locally on default port 3306

### 1. Clone and Configure
Clone the repository to your local machine. Open `config.py` and ensure the MySQL credentials match your local setup.

### 2. Install Dependencies
It is recommended to use a virtual environment. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database
The project includes a script to automatically build the schema and populate the database with dummy suppliers and vehicles.

```bash
PYTHONPATH=. python3 scratch/populate_data.py
```

### 4. Run the Server
Start the Flask development server:

```bash
python3 app.py
```

The application will be accessible in your web browser at `http://127.0.0.1:5000`.

## Administrative Access

To access the administrative dashboard and operational controls, you must log in using the designated admin account:

*   **Email**: admin@drivera.in
*   **Password**: supplier123 (or as defined in the seed data)

## Project Documentation

For a detailed breakdown of the application architecture, the technology stack, and the practical application of Database Management System (DBMS) concepts, please refer to the `explanation.md` file included in this repository.
