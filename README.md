# CMSC127-Project

1. PREREQUISITES:
   - Python 3.11 or 3.12
   - MariaDB Server

2. INSTALL PYTHON DEPENDENCIES:
   ```
   pip install mariadb
   ```

3. DATABASE SETUP:
   - Create a MariaDB database named `student_membership_db`
   - Update database credentials in `config.py`
   - Run the SQL file using one of these methods:
     ```
     # Method 1: Using mysql command line
     mysql -uroot -p < test.sql

     # Method 2: Using MariaDB client
     mariadb -uroot -p < test.sql
     ```

4. RUN THE APPLICATION:
   ```
   python run_app.py
   ```

5. FEATURES:
   - Student Management
   - Organization Management
   - Membership Management
   - Financial Tracking
   - Term Management
   - Payment Processing
   - Comprehensive Reports