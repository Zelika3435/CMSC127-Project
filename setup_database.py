import mariadb
from config import DatabaseConfig

def create_database_schema():
    # Create the database schema
    
    # Connect without specifying database first
    try:
        connection = mariadb.connect(
            user=DatabaseConfig.DB_USER,
            password=DatabaseConfig.DB_PASSWORD,
            host=DatabaseConfig.DB_HOST,
            port=DatabaseConfig.DB_PORT
        )
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseConfig.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {DatabaseConfig.DB_NAME}")
        
        # Create tables with corrected schema
        tables = [
            """
            CREATE TABLE IF NOT EXISTS organization (
                org_id INT AUTO_INCREMENT PRIMARY KEY,
                org_name VARCHAR(255) NOT NULL UNIQUE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS student (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                gender VARCHAR(20) NOT NULL,
                degree_program VARCHAR(255) NOT NULL,
                standing VARCHAR(20) NOT NULL
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS member (
                member_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS membership (
                membership_id INT AUTO_INCREMENT PRIMARY KEY,
                batch VARCHAR(20),
                committee VARCHAR(50),
                org_id INT,
                student_id INT,
                FOREIGN KEY (org_id) REFERENCES organization(org_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
                UNIQUE KEY unique_student_org (student_id, org_id)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS has_membership (
                student_id INT,
                membership_id INT,
                PRIMARY KEY (student_id, membership_id),
                FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
                FOREIGN KEY (membership_id) REFERENCES membership(membership_id) ON DELETE CASCADE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS term (
                term_id INT AUTO_INCREMENT PRIMARY KEY,
                semester VARCHAR(20),
                payment_status VARCHAR(20) DEFAULT 'unpaid',
                mem_status VARCHAR(50) DEFAULT 'active',
                role VARCHAR(50) DEFAULT '',
                term_start DATE,
                term_end DATE,
                acad_year VARCHAR(20),
                fee_amount DECIMAL(10,2),
                fee_due DATE,
                balance DECIMAL(10,2) DEFAULT 0.0,
                membership_id INT,
                FOREIGN KEY (membership_id) REFERENCES membership(membership_id) ON DELETE CASCADE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS payment (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10,2),
                payment_date DATE,
                term_id INT,
                FOREIGN KEY (term_id) REFERENCES term(term_id) ON DELETE CASCADE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Database schema created successfully!")
        return True
        
    except mariadb.Error as e:
        print(f"Error creating database schema: {e}")
        return False

if __name__ == "__main__":
    print("Setting up database...")
    if create_database_schema():
        print("Database schema created successfully!")
        print("Database setup completed successfully!")
    else:
        print("Database setup failed!")