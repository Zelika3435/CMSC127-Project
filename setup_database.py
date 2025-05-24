import mariadb
from config import DatabaseConfig

def create_database_schema():
    """Create the database schema"""
    
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
        
        # Create tables
        tables = [
            """
            CREATE TABLE IF NOT EXISTS student (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                gender ENUM('Male', 'Female', 'Other') NOT NULL,
                degree_program VARCHAR(255) NOT NULL,
                standing ENUM('Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate') NOT NULL
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS organization (
                org_id INT AUTO_INCREMENT PRIMARY KEY,
                org_name VARCHAR(255) NOT NULL UNIQUE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS member (
                student_id INT PRIMARY KEY,
                FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS membership (
                membership_id INT AUTO_INCREMENT PRIMARY KEY,
                batch VARCHAR(255) NOT NULL,
                mem_status ENUM('Active', 'Inactive', 'Suspended') NOT NULL DEFAULT 'Active',
                committee VARCHAR(255),
                org_id INT NOT NULL,
                student_id INT NOT NULL,
                FOREIGN KEY (org_id) REFERENCES organization(org_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES member(student_id) ON DELETE CASCADE,
                UNIQUE KEY unique_student_org (student_id, org_id)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS term (
                term_id INT AUTO_INCREMENT PRIMARY KEY,
                semester ENUM('First', 'Second', 'Summer') NOT NULL,
                term_start DATE NOT NULL,
                term_end DATE NOT NULL,
                acad_year YEAR NOT NULL,
                fee_amount DECIMAL(10,2) NOT NULL,
                fee_due DATE NOT NULL,
                membership_id INT NOT NULL,
                FOREIGN KEY (membership_id) REFERENCES membership(membership_id) ON DELETE CASCADE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS payment (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                payment_status ENUM('ON-TIME', 'LATE', 'PARTIAL') NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                payment_date DATE NOT NULL,
                term_id INT NOT NULL,
                FOREIGN KEY (term_id) REFERENCES term(term_id) ON DELETE CASCADE
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        # Insert sample data
        sample_data = [
            "INSERT IGNORE INTO organization (org_name) VALUES ('Computer Science Society'), ('Engineering Club'), ('Student Government')",
            """
            INSERT IGNORE INTO student (first_name, last_name, gender, degree_program, standing) VALUES 
            ('John', 'Doe', 'Male', 'Computer Science', 'Junior'),
            ('Jane', 'Smith', 'Female', 'Engineering', 'Senior'),
            ('Mike', 'Johnson', 'Male', 'Information Technology', 'Sophomore'),
            ('Sarah', 'Williams', 'Female', 'Computer Engineering', 'Freshman')
            """
        ]
        
        for data_sql in sample_data:
            cursor.execute(data_sql)
        
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
        print("Database setup completed successfully!")
    else:
        print("Database setup failed!")