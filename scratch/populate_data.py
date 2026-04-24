import mysql.connector
import os
import sys
sys.path.append(os.getcwd())
from config import Config

def run_sql_file(filename, connection):
    with open(filename, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    cur = connection.cursor()
    # mysql-connector can handle multi=True to execute multiple statements
    results = cur.execute(sql, multi=True)
    if results:
        for result in results:
            pass # Iterate through results to ensure all are executed
    connection.commit()
    cur.close()

try:
    # Connect to MySQL
    print(f"Connecting to MySQL at {Config.MYSQL_HOST}...")
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD
    )
    cur = conn.cursor()
    
    print(f"Ensuring database {Config.MYSQL_DB} exists...")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
    conn.commit()
    cur.close()
    conn.close()

    # Reconnect with DB
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    
    print("Running schema.sql...")
    run_sql_file('db/schema.sql', conn)
    
    print("Running seed.sql...")
    run_sql_file('db/seed.sql', conn)
    
    print("Database population complete!")
    conn.close()

except Exception as e:
    print(f"Error: {e}")
