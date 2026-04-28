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
    
    # First check Customer table
    cur.execute("SELECT customer_id, name, email, role FROM Customer WHERE customer_id = %s", (user_id,))
    row = cur.fetchone()
    if row:
        cur.close()
        db.close()
        return User(id=row['customer_id'], name=row['name'], email=row['email'], role=row['role'])
    
    # Then check Supplier table (we'll prefix supplier IDs with 's_' to avoid collisions in session)
    if str(user_id).startswith('s_'):
        s_id = str(user_id)[2:]
        cur.execute("SELECT supplier_id, company_name, email FROM Supplier WHERE supplier_id = %s", (s_id,))
        row = cur.fetchone()
        cur.close()
        db.close()
        if row:
            return User(id=f"s_{row['supplier_id']}", name=row['company_name'], email=row['email'], role='supplier')
            
    cur.close()
    db.close()
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
        
        # Check Customer table
        cur.execute("SELECT customer_id, name, email, password_hash, role FROM Customer WHERE email = %s", (email,))
        row = cur.fetchone()
        
        if row and bcrypt.checkpw(password.encode('utf-8'), row['password_hash'].encode('utf-8')):
            user = User(id=row['customer_id'], name=row['name'], email=row['email'], role=row['role'])
            login_user(user)
            cur.close()
            db.close()
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('admin' if user.role == 'admin' else 'dashboard'))
        
        # Check Supplier table
        cur.execute("SELECT supplier_id, company_name, email, password_hash FROM Supplier WHERE email = %s", (email,))
        row = cur.fetchone()
        
        if row and bcrypt.checkpw(password.encode('utf-8'), row['password_hash'].encode('utf-8')):
            user = User(id=f"s_{row['supplier_id']}", name=row['company_name'], email=row['email'], role='supplier')
            login_user(user)
            cur.close()
            db.close()
            flash(f'Supplier Login Successful: {user.name}', 'success')
            return redirect(url_for('dashboard'))

        cur.close()
        db.close()
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
               s.verified, s.description,
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
        ORDER BY s.verified DESC
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
    
    # Get supplier details
    cur.execute("SELECT * FROM Supplier WHERE supplier_id = %s", (supplier_id,))
    supplier = cur.fetchone()
    
    if not supplier:
        cur.close()
        db.close()
        flash('Supplier not found.', 'danger')
        return redirect(url_for('suppliers'))
        
    # Get vehicles listed by this supplier
    cur.execute("""
        SELECT v.*, f.available_count 
        FROM Vehicle v
        JOIN Fleet f ON v.vehicle_id = f.vehicle_id
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
    password = request.form.get('password')
    
    if not password:
        flash('Password is required.', 'danger')
        return redirect(url_for('suppliers'))

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db = get_db()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO Supplier (company_name, location, email, password_hash, verified) VALUES (%s, %s, %s, %s, 0)",
            (company_name, location, email, password_hash)
        )
        db.commit()
        flash('Application submitted! You can now log in to your dashboard.', 'success')
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
        
        # Find a vehicle of that type belonging to the supplier and check inventory
        cur.execute("""
            SELECT v.vehicle_id, v.price_per_day, f.available_count
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
        available_count = int(vehicle[2])

        if fleet_size > available_count:
            cur.close()
            db.close()
            flash(f'Insufficient inventory. Only {available_count} vehicles available for this type.', 'warning')
            return redirect(url_for('booking'))
        
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
        
        flash('The request is pending for confirmation by the fleet supplier.', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f'Booking failed: {str(e)}', 'danger')
        return redirect(url_for('booking'))


# ── Dashboard (Supplier/Renter History) ─────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        flash('Admins should use the Admin Panel.', 'info')
        return redirect(url_for('admin'))
        
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    if current_user.role == 'supplier':
        # Supplier view: see bookings received
        supplier_id = current_user.id.split('_')[1]
        cur.execute("""
            SELECT b.booking_id, c.name as customer_name, c.company_name as customer_company,
                   v.brand, v.model, v.type, b.fleet_size, b.start_date, b.end_date,
                   b.total_cost, b.status, b.created_at
            FROM Booking b
            JOIN Customer c ON b.customer_id = c.customer_id
            JOIN Vehicle v ON b.vehicle_id = v.vehicle_id
            WHERE b.supplier_id = %s
            ORDER BY b.created_at DESC
        """, (supplier_id,))
        bookings = cur.fetchall()
        cur.close()
        db.close()
        return render_template('dashboard.html', bookings=bookings, is_supplier=True)
    else:
        # Renter view: see bookings made
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
        return render_template('dashboard.html', bookings=bookings, is_supplier=False)


# ── Booking Status Actions (For Suppliers) ───────────────────────
@app.route('/booking/action/<int:booking_id>/<action>')
@login_required
def booking_action(booking_id, action):
    if current_user.role != 'supplier':
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('index'))
        
    supplier_id = current_user.id.split('_')[1]
    
    db = get_db()
    cur = db.cursor()
    try:
        if action == 'approve':
            # Get booking details to decrement fleet count
            cur.execute("SELECT vehicle_id, fleet_size, status FROM Booking WHERE booking_id = %s", (booking_id,))
            booking = cur.fetchone()
            
            if booking and booking[2] == 'pending':
                v_id = booking[0]
                f_size = booking[1]
                
                # Update status
                cur.execute("UPDATE Booking SET status = 'confirmed' WHERE booking_id = %s AND supplier_id = %s", 
                           (booking_id, supplier_id))
                
                # Decrement Fleet count
                cur.execute("UPDATE Fleet SET available_count = available_count - %s WHERE supplier_id = %s AND vehicle_id = %s",
                           (f_size, supplier_id, v_id))
                
                db.commit()
                flash(f'Booking #{booking_id} approved. Inventory updated.', 'success')
            else:
                flash('Booking already processed or not found.', 'warning')
        else:
            cur.execute("UPDATE Booking SET status = 'cancelled' WHERE booking_id = %s AND supplier_id = %s", 
                       (booking_id, supplier_id))
            db.commit()
            flash(f'Booking #{booking_id} has been cancelled.', 'success')
    except Exception as e:
        flash(f'Action failed: {str(e)}', 'danger')
    finally:
        cur.close()
        db.close()
        
    return redirect(url_for('dashboard'))


# ── Admin Panel ──────────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
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
        SELECT s.supplier_id, s.company_name, s.email, s.location, s.verified
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


# ── Admin Panel Actions ──────────────────────────────────────────
@app.route('/admin/supplier/verify/<int:supplier_id>/<int:status>')
@login_required
def admin_verify_supplier(supplier_id, status):
    if current_user.role != 'admin':
        flash('Unauthorized.', 'danger')
        return redirect(url_for('index'))
        
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("UPDATE Supplier SET verified = %s WHERE supplier_id = %s", (status, supplier_id))
        db.commit()
        msg = "Supplier verified!" if status == 1 else "Supplier verification removed."
        flash(msg, 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        db.close()
    return redirect(url_for('admin'))

@app.route('/admin/booking/delete/<int:booking_id>')
@login_required
def admin_delete_booking(booking_id):
    if current_user.role != 'admin':
        flash('Unauthorized.', 'danger')
        return redirect(url_for('index'))
        
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM Booking WHERE booking_id = %s", (booking_id,))
        db.commit()
        flash(f'Booking #{booking_id} deleted.', 'info')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        db.close()
    return redirect(url_for('admin'))

@app.route('/admin/supplier/delete/<int:supplier_id>')
@login_required
def admin_delete_supplier(supplier_id):
    if current_user.role != 'admin':
        flash('Unauthorized.', 'danger')
        return redirect(url_for('index'))
        
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM Supplier WHERE supplier_id = %s", (supplier_id,))
        db.commit()
        flash(f'Supplier #{supplier_id} and their fleet records deleted.', 'info')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cur.close()
        db.close()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
