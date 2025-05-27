# Organization Management System

## Prerequisites
- Python 3.11 or 3.12
- MariaDB Server
- Required Python packages:
  - mariadb (for database connectivity)
  - tkinter (for GUI, comes with Python installation)

## Installation

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd CMSC127-Project-STRONG_ENTITY
   ```

2. **Install Python Dependencies**
   ```bash
   pip install mariadb
   ```
   Note: tkinter usually comes pre-installed with Python. If not, install it through your system's package manager.

3. **Database Setup**
   - Create a MariaDB database named `student_membership_db`
   - Update database credentials in `config.py`
   - Run the setup script:
     ```bash
     python setup_database.py
     ```
   - Load test data (optional):
     ```bash
     # Using mysql command line
     mysql -uroot -p student_membership_db < new_model_test_data.sql

     # Using MariaDB client
     mariadb -uroot -p student_membership_db < new_model_test_data.sql
     ```

4. **Run the Application**
   ```bash
   python run_app.py
   ```

## Features

### Student Management
- Add, edit, and delete student records
- Track student information (name, gender, degree program, standing)
- Search and filter student records
- View student membership history

### Organization Management
- Create and manage organizations
- Track organization details and membership
- Search and filter organization records
- Manage organization committees

### Membership Management
- Add members to organizations
- Track membership status and roles
- Filter members by:
  - Role
  - Status
  - Gender
  - Degree Program
  - Batch (year of membership)
  - Committee
- View membership history

### Financial Management
- Track membership fees and payments
- Record and manage payments
- View payment history
- Generate payment receipts
- Track late payments and outstanding balances

### Term Management
- Create and manage academic terms
- Set term dates and fee amounts
- Track member status per term
- Manage term-specific memberships

### Comprehensive Reports
1. Member Reports
   - View all members with detailed filtering
   - Track membership status and roles
   - View committee assignments
   - Generate membership statistics

2. Financial Reports
   - Unpaid fees by organization
   - Unpaid fees by student
   - Late payments
   - Highest debt members
   - Financial summaries
   - Payment history reports

3. Executive Reports
   - Executive committee members
   - Role history
   - Alumni members
   - Active vs inactive member statistics
   - Committee performance reports

## Project Structure
```
CMSC127-Project-STRONG_ENTITY/
├── config.py           # Database configuration
├── database.py         # Database operations and queries
├── gui_components.py   # Custom GUI components
├── main_window.py      # Main application window and UI logic
├── models.py          # Data models and structures
├── run_app.py         # Application entry point
├── setup_database.py  # Database setup script
└── new_model_test_data.sql  # Test data for development
```