import mariadb
from typing import Optional

class DatabaseConfig:
    # Database configuration and connection management
    
    # Database connection parameters
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWORD = "achillesjohn24"  # ← Change this to the password of your root user
    DB_NAME = "student_membership_db"
    
    @classmethod
    def get_connection(cls) -> Optional[mariadb.Connection]:
        # Create and return a database connection
        try:
            connection = mariadb.connect(
                user=cls.DB_USER,
                password=cls.DB_PASSWORD,
                host=cls.DB_HOST,
                port=cls.DB_PORT,
                database=cls.DB_NAME
            )
            return connection
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            return None