import mariadb
from typing import List, Optional, Tuple
from config import DatabaseConfig
from models import Student, Organization, Member, Membership, Term, Payment

class DatabaseManager:
    # Handle all database operations
    
    def __init__(self):
        self.connection = None
    
    def connect(self) -> bool:
        # Establish database connection
        self.connection = DatabaseConfig.get_connection()
        return self.connection is not None
    
    def disconnect(self):
        # Close database connection
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[List]:
        # Execute a SELECT query and return results
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mariadb.Error as e:
            print(f"Query error: {e}")
            return None
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        # Execute INSERT, UPDATE, or DELETE query
        if not self.connection:
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except mariadb.Error as e:
            print(f"Update error: {e}")
            self.connection.rollback()
            return False
    
    # STUDENT OPERATIONS
    def add_student(self, student: Student) -> bool:
        # Add a new student
        query = """
        INSERT INTO student (first_name, last_name, gender, degree_program, standing)
        VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (
            student.first_name, student.last_name, student.gender,
            student.degree_program, student.standing
        ))
    
    def get_all_students(self) -> List[Student]:
        # Get all students
        query = "SELECT student_id, first_name, last_name, gender, degree_program, standing FROM student"
        results = self.execute_query(query)
        
        if results:
            return [Student(*row) for row in results]
        return []
    
    def update_student(self, student: Student) -> bool:
        # Update student information
        query = """
        UPDATE student 
        SET first_name=?, last_name=?, gender=?, degree_program=?, standing=?
        WHERE student_id=?
        """
        return self.execute_update(query, (
            student.first_name, student.last_name, student.gender,
            student.degree_program, student.standing, student.student_id
        ))
    
    def delete_student(self, student_id: int) -> bool:
        # Delete a student
        query = "DELETE FROM student WHERE student_id=?"
        return self.execute_update(query, (student_id,))
    
    # ORGANIZATION OPERATIONS
    def add_organization(self, org_name: str) -> bool:
        # Add a new organization
        query = "INSERT INTO organization (org_name) VALUES (?)"
        return self.execute_update(query, (org_name,))
    
    def get_all_organizations(self) -> List[Organization]:
        # Get all organizations
        query = "SELECT org_id, org_name FROM organization"
        results = self.execute_query(query)
        
        if results:
            return [Organization(*row) for row in results]
        return []
    
    # MEMBERSHIP OPERATIONS
    def add_member(self, student_id: int) -> bool:
        # Add student to member table
        query = "INSERT INTO member (student_id) VALUES (?)"
        return self.execute_update(query, (student_id,))
    
    def add_membership(self, membership: Membership) -> bool:
        # Add a new membership record
        query = """
        INSERT INTO membership (batch, mem_status, committee, org_id, student_id)
        VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (
            membership.batch, membership.mem_status, membership.committee,
            membership.org_id, membership.student_id
        ))
    
    def update_membership_status(self, membership_id: int, status: str) -> bool:
        # Update membership status
        query = "UPDATE membership SET mem_status=? WHERE membership_id=?"
        return self.execute_update(query, (status, membership_id))
    
    def get_members_by_organization(self, org_id: int = None) -> List[dict]:
        # Get all members with their membership status and organization
        if org_id:
            query = """
            SELECT s.student_id, s.first_name, s.last_name, 
                   m.mem_status, m.batch, m.committee, org.org_name, m.membership_id,
                   s.gender, s.degree_program
            FROM student s
            JOIN member mb ON s.student_id = mb.student_id
            JOIN membership m ON mb.student_id = m.student_id
            JOIN organization org ON m.org_id = org.org_id
            WHERE org.org_id = ?
            ORDER BY s.last_name, s.first_name
            """
            results = self.execute_query(query, (org_id,))
        else:
            query = """
            SELECT s.student_id, s.first_name, s.last_name, 
                   m.mem_status, m.batch, m.committee, org.org_name, m.membership_id,
                   s.gender, s.degree_program
            FROM student s
            JOIN member mb ON s.student_id = mb.student_id
            JOIN membership m ON mb.student_id = m.student_id
            JOIN organization org ON m.org_id = org.org_id
            ORDER BY org.org_name, s.last_name
            """
            results = self.execute_query(query)
        
        if results:
            return [
                {
                    'student_id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'status': row[3], 'batch': row[4], 'committee': row[5],
                    'organization': row[6], 'membership_id': row[7],
                    'gender': row[8], 'degree_program': row[9]
                }
                for row in results
            ]
        return []
    
    def get_members_with_unpaid_fees(self, org_id: int, semester: str, acad_year: str) -> List[dict]:
        # Get members with unpaid fees for a specific organization, semester, and academic year
        query = """
        SELECT s.student_id, s.first_name, s.last_name, 
               t.fee_amount, SUM(IFNULL(p.amount, 0)) as total_paid,
               (t.fee_amount - SUM(IFNULL(p.amount, 0))) as balance
        FROM student s
        JOIN member mb ON s.student_id = mb.student_id
        JOIN membership m ON mb.student_id = m.student_id
        JOIN organization org ON m.org_id = org.org_id
        JOIN term t ON m.membership_id = t.membership_id
        LEFT JOIN payment p ON t.term_id = p.term_id
        WHERE org.org_id = ? AND t.semester = ? AND t.acad_year = ?
        GROUP BY s.student_id, t.term_id
        HAVING balance > 0
        """
        results = self.execute_query(query, (org_id, semester, acad_year))
        
        if results:
            return [
                {
                    'student_id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'fee_amount': row[3], 'total_paid': row[4], 'balance': row[5]
                }
                for row in results
            ]
        return []
    
    def get_member_unpaid_fees(self, student_id: int) -> List[dict]:
        # Get all unpaid fees for a specific member across all organizations
        query = """
        SELECT org.org_name, t.semester, t.acad_year,
               t.fee_amount, SUM(IFNULL(p.amount, 0)) as total_paid,
               (t.fee_amount - SUM(IFNULL(p.amount, 0))) as balance
        FROM student s
        JOIN member mb ON s.student_id = mb.student_id
        JOIN membership m ON mb.student_id = m.student_id
        JOIN organization org ON m.org_id = org.org_id
        JOIN term t ON m.membership_id = t.membership_id
        LEFT JOIN payment p ON t.term_id = p.term_id
        WHERE s.student_id = ?
        GROUP BY org.org_id, t.term_id
        HAVING balance > 0
        """
        results = self.execute_query(query, (student_id,))
        
        if results:
            return [
                {
                    'organization': row[0], 'semester': row[1], 'acad_year': row[2],
                    'fee_amount': row[3], 'total_paid': row[4], 'balance': row[5]
                }
                for row in results
            ]
        return []
    
    def get_executive_committee(self, org_id: int, acad_year: str) -> List[dict]:
        # Get all executive committee members for a specific organization and academic year
        query = """
        SELECT s.student_id, s.first_name, s.last_name, m.committee
        FROM student s
        JOIN member mb ON s.student_id = mb.student_id
        JOIN membership m ON mb.student_id = m.student_id
        JOIN organization org ON m.org_id = org.org_id
        WHERE org.org_id = ? AND m.batch = ? AND m.committee IN ('President', 'Vice President', 'Secretary', 'Treasurer')
        """
        results = self.execute_query(query, (org_id, acad_year))
        
        if results:
            return [
                {
                    'student_id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'role': row[3]
                }
                for row in results
            ]
        return []
    
    def get_role_history(self, org_id: int, role: str) -> List[dict]:
        # Get history of members who held a specific role in an organization
        query = """
        SELECT s.student_id, s.first_name, s.last_name, m.batch
        FROM student s
        JOIN member mb ON s.student_id = mb.student_id
        JOIN membership m ON mb.student_id = m.student_id
        JOIN organization org ON m.org_id = org.org_id
        WHERE org.org_id = ? AND m.committee = ?
        ORDER BY m.batch DESC
        """
        results = self.execute_query(query, (org_id, role))
        
        if results:
            return [
                {
                    'student_id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'academic_year': row[3]
                }
                for row in results
            ]
        return []
    
    def get_late_payments(self, org_id: int, semester: str, acad_year: str) -> List[dict]:
        # Get all late payments for a specific organization, semester, and academic year
        query = """
        SELECT s.student_id, s.first_name, s.last_name,
               p.payment_date, t.fee_due, p.amount
        FROM student s
        JOIN member mb ON s.student_id = mb.student_id
        JOIN membership m ON mb.student_id = m.student_id
        JOIN organization org ON m.org_id = org.org_id
        JOIN term t ON m.membership_id = t.membership_id
        JOIN payment p ON t.term_id = p.term_id
        WHERE org.org_id = ? AND t.semester = ? AND t.acad_year = ?
        AND p.payment_date > t.fee_due
        """
        results = self.execute_query(query, (org_id, semester, acad_year))
        
        if results:
            return [
                {
                    'student_id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'payment_date': row[3], 'due_date': row[4], 'amount': row[5]
                }
                for row in results
            ]
        return []
    
    def get_membership_status_percentage(self, org_id: int, n_semesters: int) -> dict:
        # Get percentage of active vs inactive members for the last n semesters
        query = """
        SELECT 
            COUNT(CASE WHEN m.mem_status = 'active' THEN 1 END) as active_count,
            COUNT(CASE WHEN m.mem_status = 'inactive' THEN 1 END) as inactive_count,
            COUNT(*) as total_count
        FROM membership m
        JOIN organization org ON m.org_id = org.org_id
        WHERE org.org_id = ?
        AND m.batch >= (
            SELECT MAX(batch) - ?
            FROM membership
            WHERE org_id = ?
        )
        """
        results = self.execute_query(query, (org_id, n_semesters, org_id))
        
        if results and results[0]:
            active_count, inactive_count, total_count = results[0]
            if total_count > 0:
                return {
                    'active_percentage': (active_count / total_count) * 100,
                    'inactive_percentage': (inactive_count / total_count) * 100,
                    'total_members': total_count
                }
        return {'active_percentage': 0, 'inactive_percentage': 0, 'total_members': 0}
    
    def get_alumni_members(self, org_id: int, as_of_date: str) -> List[dict]:
        # Get all alumni members as of a specific date
        query = """
        SELECT s.student_id, s.first_name, s.last_name, m.batch
        FROM student s
        JOIN member mb ON s.student_id = mb.student_id
        JOIN membership m ON mb.student_id = m.student_id
        JOIN organization org ON m.org_id = org.org_id
        WHERE org.org_id = ? AND m.mem_status = 'alumni'
        AND m.batch <= ?
        """
        results = self.execute_query(query, (org_id, as_of_date))
        
        if results:
            return [
                {
                    'student_id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'batch': row[3]
                }
                for row in results
            ]
        return []
    
    def get_organization_financial_status(self, org_id: int, as_of_date: str) -> dict:
        # Get total paid and unpaid fees for an organization as of a specific date
        query = """
        SELECT 
            SUM(t.fee_amount) as total_fees,
            SUM(IFNULL(p.amount, 0)) as total_paid,
            SUM(t.fee_amount - IFNULL(p.amount, 0)) as total_unpaid
        FROM organization org
        JOIN membership m ON org.org_id = m.org_id
        JOIN term t ON m.membership_id = t.membership_id
        LEFT JOIN payment p ON t.term_id = p.term_id
        WHERE org.org_id = ? AND t.term_start <= ?
        """
        results = self.execute_query(query, (org_id, as_of_date))
        
        if results and results[0]:
            total_fees, total_paid, total_unpaid = results[0]
            return {
                'total_fees': total_fees or 0,
                'total_paid': total_paid or 0,
                'total_unpaid': total_unpaid or 0
            }
        return {'total_fees': 0, 'total_paid': 0, 'total_unpaid': 0}
    
    def get_highest_debt_members(self, org_id: int, semester: str, acad_year: str) -> List[dict]:
        # Get members with the highest debt for a specific organization, semester, and academic year
        query = """
        SELECT s.student_id, s.first_name, s.last_name,
               t.fee_amount, SUM(IFNULL(p.amount, 0)) as total_paid,
               (t.fee_amount - SUM(IFNULL(p.amount, 0))) as balance
        FROM student s
        JOIN member mb ON s.student_id = mb.student_id
        JOIN membership m ON mb.student_id = m.student_id
        JOIN organization org ON m.org_id = org.org_id
        JOIN term t ON m.membership_id = t.membership_id
        LEFT JOIN payment p ON t.term_id = p.term_id
        WHERE org.org_id = ? AND t.semester = ? AND t.acad_year = ?
        GROUP BY s.student_id, t.term_id
        HAVING balance > 0
        ORDER BY balance DESC
        """
        results = self.execute_query(query, (org_id, semester, acad_year))
        
        if results:
            return [
                {
                    'student_id': row[0], 'first_name': row[1], 'last_name': row[2],
                    'fee_amount': row[3], 'total_paid': row[4], 'balance': row[5]
                }
                for row in results
            ]
        return []
    
    # TERM AND PAYMENT OPERATIONS
    def add_term(self, term: Term) -> bool:
        # Add a new term
        query = """
        INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (
            term.semester, term.term_start, term.term_end, term.acad_year,
            term.fee_amount, term.fee_due, term.membership_id
        ))
    
    def add_payment(self, payment: Payment) -> bool:
        # Add a new payment
        query = """
        INSERT INTO payment (payment_status, amount, payment_date, term_id)
        VALUES (?, ?, ?, ?)
        """
        return self.execute_update(query, (
            payment.payment_status, payment.amount, payment.payment_date, payment.term_id
        ))
    
    def get_term_balances(self) -> List[dict]:
        # Get term payments and computed balance
        query = """
        SELECT t.term_id, t.semester, t.acad_year, t.fee_amount,
               SUM(IFNULL(p.amount, 0)) AS total_paid,
               (t.fee_amount - SUM(IFNULL(p.amount, 0))) AS balance
        FROM term t
        LEFT JOIN payment p ON t.term_id = p.term_id
        GROUP BY t.term_id
        """
        results = self.execute_query(query)
        
        if results:
            return [
                {
                    'term_id': row[0], 'semester': row[1], 'acad_year': row[2],
                    'fee_amount': row[3], 'total_paid': row[4], 'balance': row[5]
                }
                for row in results
            ]
        return []
    
    def get_financial_summary_by_org(self) -> List[dict]:
        # Get financial summary per organization
        query = """
        SELECT org.org_name,
               SUM(t.fee_amount) AS total_fees,
               SUM(IFNULL(p.amount, 0)) AS total_collected,
               SUM(t.fee_amount - IFNULL(p.amount, 0)) AS total_balance 
        FROM organization org
        JOIN membership m ON org.org_id = m.org_id
        JOIN term t ON m.membership_id = t.membership_id
        LEFT JOIN (
            SELECT term_id, SUM(amount) AS amount
            FROM payment
            GROUP BY term_id
        ) p ON t.term_id = p.term_id
        GROUP BY org.org_name
        """
        results = self.execute_query(query)
        
        if results:
            return [
                {
                    'organization': row[0], 'total_fees': row[1],
                    'total_collected': row[2], 'total_balance': row[3]
                }
                for row in results
            ]
        return []