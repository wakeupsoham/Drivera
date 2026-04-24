import mysql.connector
from config import Config

new_hash = '$2b$12$seqWi5GfK5yaXWmSnBXaTOM45ioecySOnCUbOYw0Zu1Ny3JVh.wqS'

try:
    db = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cur = db.cursor()
    
    # Update all customers and suppliers with the new hash for 'supplier123'
    cur.execute("UPDATE Customer SET password_hash = %s", (new_hash,))
    cur.execute("UPDATE Supplier SET password_hash = %s", (new_hash,))
    
    db.commit()
    print(f"Updated {cur.rowcount} records.")
    cur.close()
    db.close()
    print("Database updated successfully!")
except Exception as e:
    print(f"Error: {e}")
