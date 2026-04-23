from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
from config import Config

# ── App Initialization ──────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

# ── MySQL Connection Helper ─────────────────────────────────────
def get_db():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# ── Flask-Login ──────────────────────────────────────────────────
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# ── User Model (for Flask-Login) ────────────────────────────────
class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT customer_id, name, email, role FROM Customer WHERE customer_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    db.close()
    if row:
        return User(id=row['customer_id'], name=row['name'], email=row['email'], role=row['role'])
    return None


# ══════════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════════

# ── Landing Page ─────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ── Auth: Register ───────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        contact = request.form.get('contact', '')
        license_no = request.form.get('license_no', '')
        company_name = request.form.get('company_name', '')

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        db = get_db()
        cur = db.cursor(dictionary=True)
        try:
            cur.execute(
                """INSERT INTO Customer (name, email, password_hash, contact, license_no, company_name)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (name, email, password_hash, contact, license_no, company_name)
            )
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
        finally:
            cur.close()
            db.close()
    return render_template('register.html')


# ── Auth: Login ──────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT customer_id, name, email, password_hash, role FROM Customer WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        db.close()

        if row and bcrypt.checkpw(password.encode('utf-8'), row['password_hash'].encode('utf-8')):
            user = User(id=row['customer_id'], name=row['name'], email=row['email'], role=row['role'])
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html'), 401
    return render_template('login.html')


# ── Auth: Logout ─────────────────────────────────────────────────
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


# ── Booking Page (Map + Search) ──────────────────────────────────
@app.route('/booking')
def booking():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT s.supplier_id, s.company_name, s.location, s.latitude, s.longitude,
               s.verified, s.rating, s.description,
               COUNT(f.fleet_id) AS fleet_types,
               SUM(f.available_count) AS total_vehicles,
               MIN(v.price_per_day) AS min_price,
               GROUP_CONCAT(DISTINCT v.type) AS vehicle_types
        FROM Supplier s
        LEFT JOIN Fleet f ON s.supplier_id = f.supplier_id
        LEFT JOIN Vehicle v ON f.vehicle_id = v.vehicle_id
        GROUP BY s.supplier_id
    """)
    suppliers = cur.fetchall()
    cur.close()
    db.close()
    
    if request.headers.get('Accept') == 'application/json':
        from flask import jsonify
        return jsonify(suppliers)
        
    return render_template('booking.html', suppliers=suppliers)


# ── Suppliers Listing ────────────────────────────────────────────
@app.route('/suppliers')
def suppliers():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT s.*, COUNT(f.fleet_id) AS fleet_types,
               SUM(f.available_count) AS total_vehicles
        FROM Supplier s
        LEFT JOIN Fleet f ON s.supplier_id = f.supplier_id
        GROUP BY s.supplier_id
        ORDER BY s.verified DESC, s.rating DESC
    """)
    suppliers = cur.fetchall()
    cur.close()
    db.close()
    return render_template('suppliers.html', suppliers=suppliers)


# ── Supplier Profile ──────────────────────────────────────────────
@app.route('/supplier/<int:supplier_id>')
def supplier_detail(supplier_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    cur.execute("SELECT * FROM Supplier WHERE supplier_id = %s", (supplier_id,))
    supplier = cur.fetchone()
    
    if not supplier:
        cur.close()
        db.close()
        flash('Supplier not found.', 'warning')
        return redirect(url_for('suppliers'))

    cur.execute("""
        SELECT v.vehicle_id, v.type, v.model, v.brand, v.price_per_day, v.status, f.available_count
        FROM Fleet f
        JOIN Vehicle v ON f.vehicle_id = v.vehicle_id
        WHERE f.supplier_id = %s
    """, (supplier_id,))
    vehicles = cur.fetchall()
    
    cur.close()
    db.close()
    
    return render_template('supplier_detail.html', supplier=supplier, vehicles=vehicles)


# ── Register Supplier ────────────────────────────────────────────
@app.route('/register_supplier', methods=['POST'])
def register_supplier():
    if not current_user.is_authenticated:
        flash('Please log in or register to apply as a supplier.', 'warning')
        return redirect(url_for('login'))

    company_name = request.form.get('company_name')
    location = request.form.get('location')
    email = request.form.get('email')
    
    # Optional: could also handle vehicle_type here to create an initial fleet/vehicle record
    
    db = get_db()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO Supplier (company_name, location, email, rating, verified) VALUES (%s, %s, %s, 4.0, 0)",
            (company_name, location, email)
        )
        db.commit()
        flash('Application sent and will be processed in 3 business days.', 'success')
    except Exception as e:
        flash(f'Registration failed: {str(e)}', 'danger')
    finally:
        cur.close()
        db.close()
        
    return redirect(url_for('suppliers'))


# ── Create Booking ───────────────────────────────────────────────
@app.route('/book', methods=['POST'])
@login_required
def book():
    supplier_id = request.form.get('supplier_id')
    vehicle_type = request.form.get('vehicle_type')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    fleet_size = request.form.get('fleet_size')

    if not all([supplier_id, vehicle_type, start_date, end_date, fleet_size]):
        flash('Please fill in all booking details (Dates, Vehicle Type, Fleet Size) and select a supplier.', 'danger')
        return redirect(url_for('booking'))

    try:
        fleet_size = int(fleet_size)
        db = get_db()
        cur = db.cursor() # Keep as tuple here since access is vehicle[0]
        
        # Find a vehicle of that type belonging to the supplier
        cur.execute("""
            SELECT v.vehicle_id, v.price_per_day 
            FROM Vehicle v
            JOIN Fleet f ON v.vehicle_id = f.vehicle_id
            WHERE f.supplier_id = %s AND v.type = %s
            LIMIT 1
        """, (supplier_id, vehicle_type))
        vehicle = cur.fetchone()
        
        if not vehicle:
            cur.close()
            db.close()
            flash('Selected supplier does not have the chosen vehicle type.', 'danger')
            return redirect(url_for('booking'))
            
        vehicle_id = vehicle[0]
        price_per_day = float(vehicle[1])
        
        # Calculate days 
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days
        if days <= 0:
            days = 1
            
        total_cost = days * price_per_day * fleet_size
        
        # Create booking
        cur.execute("""
            INSERT INTO Booking (customer_id, supplier_id, vehicle_id, fleet_size, start_date, end_date, total_cost, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
        """, (current_user.id, supplier_id, vehicle_id, fleet_size, start_date, end_date, total_cost))
        
        db.commit()
        cur.close()
        db.close()
        
        flash('Booking submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f'Booking failed: {str(e)}', 'danger')
        return redirect(url_for('booking'))


# ── Dashboard (Renter Booking History) ───────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT b.booking_id, s.company_name, v.brand, v.model, v.type,
               b.fleet_size, b.start_date, b.end_date, b.total_cost, b.status
        FROM Booking b
        JOIN Supplier s ON b.supplier_id = s.supplier_id
        JOIN Vehicle v ON b.vehicle_id = v.vehicle_id
        WHERE b.customer_id = %s
        ORDER BY b.created_at DESC
    """, (current_user.id,))
    bookings = cur.fetchall()
    cur.close()
    db.close()
    return render_template('dashboard.html', bookings=bookings)


# ── Admin Panel ──────────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin():
    if current_user.email != 'admin@drivera.in':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('index'))

    db = get_db()
    cur = db.cursor() # tuple cursor for simple aggregates
    
    cur.execute("SELECT COUNT(*) FROM Customer")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Supplier")
    total_suppliers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Booking")
    total_bookings = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(total_cost), 0) FROM Booking WHERE status = 'confirmed'")
    total_revenue = cur.fetchone()[0]
    cur.close()
    
    cur = db.cursor(dictionary=True) # Switch to dictionary for list data
    cur.execute("""
        SELECT s.supplier_id, s.company_name, s.email, s.location, s.verified, s.rating
        FROM Supplier s ORDER BY s.created_at DESC
    """)
    suppliers = cur.fetchall()

    cur.execute("""
        SELECT b.booking_id, c.name, s.company_name, v.model, b.fleet_size,
               b.start_date, b.end_date, b.total_cost, b.status
        FROM Booking b
        JOIN Customer c ON b.customer_id = c.customer_id
        JOIN Supplier s ON b.supplier_id = s.supplier_id
        JOIN Vehicle v ON b.vehicle_id = v.vehicle_id
        ORDER BY b.created_at DESC LIMIT 20
    """)
    bookings = cur.fetchall()

    cur.close()
    db.close()
    return render_template('admin.html',
                           total_customers=total_customers,
                           total_suppliers=total_suppliers,
                           total_bookings=total_bookings,
                           total_revenue=total_revenue,
                           suppliers=suppliers,
                           bookings=bookings)


# ── Admin Actions (Interactive Controls) ─────────────────────────
@app.route('/admin/supplier/<int:supplier_id>/<action>', methods=['POST'])
@login_required
def admin_manage_supplier(supplier_id, action):
    if current_user.email != 'admin@drivera.in':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    db = get_db()
    cur = db.cursor()
    
    if action == 'verify':
        cur.execute("UPDATE Supplier SET verified = 1 WHERE supplier_id = %s", (supplier_id,))
        flash(f'Supplier #{supplier_id} has been verified.', 'success')
    elif action == 'reject':
        cur.execute("DELETE FROM Supplier WHERE supplier_id = %s", (supplier_id,))
        flash(f'Supplier #{supplier_id} application rejected.', 'info')
        
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin'))


@app.route('/admin/booking/<int:booking_id>/<action>', methods=['POST'])
@login_required
def admin_manage_booking(booking_id, action):
    if current_user.email != 'admin@drivera.in':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    db = get_db()
    cur = db.cursor()
    
    valid_statuses = {'confirm': 'confirmed', 'cancel': 'cancelled', 'complete': 'completed'}
    
    if action in valid_statuses:
        new_status = valid_statuses[action]
        cur.execute("UPDATE Booking SET status = %s WHERE booking_id = %s", (new_status, booking_id))
        flash(f'Booking #{booking_id} status updated to {new_status}.', 'success')
    else:
        flash('Invalid action.', 'danger')
        
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin'))


# ── Run ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
