import pytest
from app import app, mysql

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_homepage_loads(client):
    """(1) homepage loads 200"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Fleet Rentals' in rv.data

def test_booking_returns_json(client):
    """(2) /booking returns supplier list JSON"""
    rv = client.get('/booking', headers={'Accept': 'application/json'})
    assert rv.status_code == 200
    assert rv.is_json
    
    data = rv.get_json()
    assert isinstance(data, list)
    if len(data) > 0:
        # Check supplier shape
        assert len(data[0]) >= 8 # Contains id, name, location, etc.

def test_unauthenticated_dashboard_redirects(client):
    """(3) unauthenticated /dashboard redirects to /login"""
    rv = client.get('/dashboard', follow_redirects=False)
    # Flask-Login redirects to login view with 302
    assert rv.status_code == 302
    assert '/login' in rv.location

def test_book_creates_row(client):
    """(4) POST /book creates a booking row in DB"""
    # First, login with our seed data credentials
    rv_login = client.post('/login', data=dict(
        email='arjun@techcorp.in',
        password='customer123'
    ), follow_redirects=True)
    assert rv_login.status_code == 200

    # Get current bookings count
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Booking")
        initial_count = cur.fetchone()[0]

        # Post a new booking
        # We need a valid supplier and vehicle in the DB. Based on seed:
        # Supplier 1 has Vehicle 1 (Sedan)
        rv_book = client.post('/book', data=dict(
            supplier_id='1',
            vehicle_type='Sedan',
            start_date='2026-10-01',
            end_date='2026-10-05',
            fleet_size='2'
        ), follow_redirects=True)
        assert rv_book.status_code == 200

        # Verify DB updated
        cur.execute("SELECT COUNT(*) FROM Booking")
        final_count = cur.fetchone()[0]
        cur.close()

        assert final_count == initial_count + 1

def test_login_wrong_credentials(client):
    """(5) login with wrong credentials returns 401"""
    rv = client.post('/login', data=dict(
        email='arjun@techcorp.in',
        password='wrongpassword'
    ))
    assert rv.status_code == 401
    assert b'Invalid email or password' in rv.data
