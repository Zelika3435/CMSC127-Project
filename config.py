import mariadb
from typing import Optional

class DatabaseConfig:
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_USER = ""              # Empty by default, user must input
    DB_PASSWORD = ""          # Empty by default
    DB_NAME = "student_membership_db"

    @classmethod
    def get_connection(cls) -> Optional[mariadb.Connection]:
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
