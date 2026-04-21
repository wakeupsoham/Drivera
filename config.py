import os

class Config:
    """Base configuration for Drivera Flask app."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'drivera-secret-key-change-in-production')

    # MySQL Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '$0ham027')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'drivera')
    MYSQL_CURSORCLASS = 'DictCursor'
