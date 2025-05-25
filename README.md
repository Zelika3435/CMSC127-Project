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
   - Run `mysql -uroot -p {your password} < test.sql` to populate test data

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