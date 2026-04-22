import MySQLdb
import os
from config import Config

def run_sql_file(filename, connection):
    with open(filename, 'r') as f:
        sql = f.read()
    
    cur = connection.cursor()
    # MySQLdb doesn't handle multiple statements in one execute call well
    # We'll split by semicolon, but this is naive
    statements = sql.split(';')
    for statement in statements:
        if statement.strip():
            cur.execute(statement)
    connection.commit()
    cur.close()

try:
    # Connect without DB first to create it
    conn = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
    conn.commit()
    cur.close()
    conn.close()

    # Reconnect with DB
    conn = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB
    )
    
    print("Running schema.sql...")
    run_sql_file('db/schema.sql', conn)
    
    print("Running seed.sql...")
    run_sql_file('db/seed.sql', conn)
    
    print("Database setup complete!")
    conn.close()

except Exception as e:
    print(f"Error: {e}")
