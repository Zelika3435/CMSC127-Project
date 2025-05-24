import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from models import Student, Organization, Membership, Term, Payment
from gui_components import DataTable, FormDialog
from datetime import date, datetime

class StudentMembershipApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Membership Management System")
        self.root.geometry("1200x800")
        
        # Initialize database
        self.db = DatabaseManager()
        if not self.db.connect():
            messagebox.showerror("Database Error", "Could not connect to database!")
            return
        
        self.create_menu()
        self.create_main_interface()
        
        # Load initial data
        self.refresh_students()
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Members menu
        members_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Members", menu=members_menu)
        members_menu.add_command(label="Add Student", command=self.add_student)
        members_menu.add_command(label="Add Organization", command=self.add_organization)
        members_menu.add_command(label="Add Membership", command=self.add_membership)
        
        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Financial Summary", command=self.show_financial_summary)
        reports_menu.add_command(label="Term Balances", command=self.show_term_balances)
    
    def create_main_interface(self):
        """Create the main interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Students tab
        self.students_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.students_frame, text="Students")
        self.create_students_tab()
        
        # Members tab
        self.members_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.members_frame, text="Members")
        self.create_members_tab()
        
        # Organizations tab
        self.organizations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.organizations_frame, text="Organizations")
        self.create_organizations_tab()
    
    def create_students_tab(self):
        """Create students management tab"""
        # Buttons frame
        buttons_frame = ttk.Frame(self.students_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Edit Student", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Delete Student", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_students).pack(side=tk.LEFT, padx=5)
        
        # Students table
        columns = ['student_id', 'first_name', 'last_name', 'gender', 'degree_program', 'standing']
        self.students_table = DataTable(self.students_frame, columns)
        self.students_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_members_tab(self):
        """Create members management tab"""
        # Filter frame
        filter_frame = ttk.Frame(self.members_frame)
        filter_frame.pack(pady=10)
        
        ttk.Label(filter_frame, text="Filter by Organization:").pack(side=tk.LEFT, padx=5)
        self.org_filter = ttk.Combobox(filter_frame, width=20)
        self.org_filter.pack(side=tk.LEFT, padx=5)
        self.org_filter.bind('<<ComboboxSelected>>', self.filter_members)
        
        ttk.Button(filter_frame, text="Show All", command=self.show_all_members).pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.members_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Add Membership", command=self.add_membership).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Update Status", command=self.update_membership_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_members).pack(side=tk.LEFT, padx=5)
        
        # Members table
        columns = ['student_id', 'first_name', 'last_name', 'status', 'batch', 'committee', 'organization', 'membership_id']
        self.members_table = DataTable(self.members_frame, columns)
        self.members_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_organizations_tab(self):
        """Create organizations management tab"""
        # Buttons frame
        buttons_frame = ttk.Frame(self.organizations_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Add Organization", command=self.add_organization).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_organizations).pack(side=tk.LEFT, padx=5)
        
        # Organizations table
        columns = ['org_id', 'org_name']
        self.organizations_table = DataTable(self.organizations_frame, columns)
        self.organizations_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # STUDENT OPERATIONS
    def add_student(self):
        """Add new student"""
        fields = [
            {'name': 'first_name', 'label': 'First Name:', 'type': 'entry'},
            {'name': 'last_name', 'label': 'Last Name:', 'type': 'entry'},
            {'name': 'gender', 'label': 'Gender:', 'type': 'combobox', 'values': ['Male', 'Female', 'Other']},
            {'name': 'degree_program', 'label': 'Degree Program:', 'type': 'entry'},
            {'name': 'standing', 'label': 'Standing:', 'type': 'combobox', 'values': ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']}
        ]
        
        dialog = FormDialog(self.root, "Add Student", fields)
        self.root.wait_window(dialog)
        
        if dialog.result:
            student = Student(
                student_id=None,
                first_name=dialog.result['first_name'],
                last_name=dialog.result['last_name'],
                gender=dialog.result['gender'],
                degree_program=dialog.result['degree_program'],
                standing=dialog.result['standing']
            )
            
            if self.db.add_student(student):
                messagebox.showinfo("Success", "Student added successfully!")
                self.refresh_students()
            else:
                messagebox.showerror("Error", "Failed to add student!")
    
    def edit_student(self):
        """Edit selected student"""
        selected = self.students_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit!")
            return
        
        fields = [
            {'name': 'first_name', 'label': 'First Name:', 'type': 'entry', 'default': selected['first_name']},
            {'name': 'last_name', 'label': 'Last Name:', 'type': 'entry', 'default': selected['last_name']},
            {'name': 'gender', 'label': 'Gender:', 'type': 'combobox', 'values': ['Male', 'Female', 'Other'], 'default': selected['gender']},
            {'name': 'degree_program', 'label': 'Degree Program:', 'type': 'entry', 'default': selected['degree_program']},
            {'name': 'standing', 'label': 'Standing:', 'type': 'combobox', 'values': ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate'], 'default': selected['standing']}
        ]
        
        dialog = FormDialog(self.root, "Edit Student", fields)
        self.root.wait_window(dialog)
        
        if dialog.result:
            student = Student(
                student_id=int(selected['student_id']),
                first_name=dialog.result['first_name'],
                last_name=dialog.result['last_name'],
                gender=dialog.result['gender'],
                degree_program=dialog.result['degree_program'],
                standing=dialog.result['standing']
            )
            
            if self.db.update_student(student):
                messagebox.showinfo("Success", "Student updated successfully!")
                self.refresh_students()
            else:
                messagebox.showerror("Error", "Failed to update student!")
    
    def delete_student(self):
        """Delete selected student"""
        selected = self.students_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return
        
        if messagebox.askyesno("Confirm", f"Delete student {selected['first_name']} {selected['last_name']}?"):
            if self.db.delete_student(int(selected['student_id'])):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.refresh_students()
            else:
                messagebox.showerror("Error", "Failed to delete student!")
    
    def refresh_students(self):
        """Refresh students table"""
        students = self.db.get_all_students()
        student_data = [
            {
                'student_id': s.student_id, 'first_name': s.first_name,
                'last_name': s.last_name, 'gender': s.gender,
                'degree_program': s.degree_program, 'standing': s.standing
            }
            for s in students
        ]
        self.students_table.insert_data(student_data)
    
    # ORGANIZATION OPERATIONS
    def add_organization(self):
        """Add new organization"""
        fields = [
            {'name': 'org_name', 'label': 'Organization Name:', 'type': 'entry'}
        ]
        
        dialog = FormDialog(self.root, "Add Organization", fields)
        self.root.wait_window(dialog)
        
        if dialog.result and dialog.result['org_name']:
            if self.db.add_organization(dialog.result['org_name']):
                messagebox.showinfo("Success", "Organization added successfully!")
                self.refresh_organizations()
                self.refresh_org_filter()
            else:
                messagebox.showerror("Error", "Failed to add organization!")
    
    def refresh_organizations(self):
        """Refresh organizations table"""
        organizations = self.db.get_all_organizations()
        org_data = [
            {'org_id': o.org_id, 'org_name': o.org_name}
            for o in organizations
        ]
        self.organizations_table.insert_data(org_data)
    
    def refresh_org_filter(self):
        """Refresh organization filter combobox"""
        organizations = self.db.get_all_organizations()
        org_names = [org.org_name for org in organizations]
        self.org_filter['values'] = org_names
    
    # MEMBERSHIP OPERATIONS
    def add_membership(self):
        """Add new membership"""
        # Get available students and organizations
        students = self.db.get_all_students()
        organizations = self.db.get_all_organizations()
        
        if not students or not organizations:
            messagebox.showerror("Error", "Please add students and organizations first!")
            return
        
        student_choices = [f"{s.student_id}: {s.first_name} {s.last_name}" for s in students]
        org_choices = [f"{o.org_id}: {o.org_name}" for o in organizations]
        
        fields = [
            {'name': 'student', 'label': 'Student:', 'type': 'combobox', 'values': student_choices},
            {'name': 'organization', 'label': 'Organization:', 'type': 'combobox', 'values': org_choices},
            {'name': 'batch', 'label': 'Batch:', 'type': 'entry'},
            {'name': 'status', 'label': 'Status:', 'type': 'combobox', 'values': ['Active', 'Inactive', 'Suspended']},
            {'name': 'committee', 'label': 'Committee:', 'type': 'entry'}
        ]
        
        dialog = FormDialog(self.root, "Add Membership", fields)
        self.root.wait_window(dialog)
        
        if dialog.result:
            try:
                student_id = int(dialog.result['student'].split(':')[0])
                org_id = int(dialog.result['organization'].split(':')[0])
                
                # First add to member table if not exists
                self.db.add_member(student_id)
                
                # Then add membership
                membership = Membership(
                    membership_id=None,
                    batch=dialog.result['batch'],
                    mem_status=dialog.result['status'],
                    committee=dialog.result['committee'],
                    org_id=org_id,
                    student_id=student_id
                )
                
                if self.db.add_membership(membership):
                    messagebox.showinfo("Success", "Membership added successfully!")
                    self.refresh_members()
                else:
                    messagebox.showerror("Error", "Failed to add membership!")
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Invalid selection!")
    
    def update_membership_status(self):
        """Update membership status"""
        selected = self.members_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a membership to update!")
            return
        
        fields = [
            {'name': 'status', 'label': 'New Status:', 'type': 'combobox', 
             'values': ['Active', 'Inactive', 'Suspended'], 'default': selected['status']}
        ]
        
        dialog = FormDialog(self.root, "Update Membership Status", fields)
        self.root.wait_window(dialog)
        
        if dialog.result:
            membership_id = int(selected['membership_id'])
            if self.db.update_membership_status(membership_id, dialog.result['status']):
                messagebox.showinfo("Success", "Membership status updated successfully!")
                self.refresh_members()
            else:
                messagebox.showerror("Error", "Failed to update membership status!")
    
    def refresh_members(self):
        """Refresh members table"""
        members = self.db.get_members_by_organization()
        self.members_table.insert_data(members)
        self.refresh_org_filter()
    
    def filter_members(self, event=None):
        """Filter members by organization"""
        selected_org = self.org_filter.get()
        if selected_org:
            # Get org_id from the organization name
            organizations = self.db.get_all_organizations()
            org_id = None
            for org in organizations:
                if org.org_name == selected_org:
                    org_id = org.org_id
                    break
            
            if org_id:
                members = self.db.get_members_by_organization(org_id)
                self.members_table.insert_data(members)
    
    def show_all_members(self):
        """Show all members"""
        self.org_filter.set('')
        self.refresh_members()
    
    # REPORTS
    def show_financial_summary(self):
        """Show financial summary report"""
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Financial Summary by Organization")
        summary_window.geometry("800x600")
        
        columns = ['organization', 'total_fees', 'total_collected', 'total_balance']
        summary_table = DataTable(summary_window, columns)
        summary_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Get data
        financial_data = self.db.get_financial_summary_by_org()
        summary_table.insert_data(financial_data)
    
    def show_term_balances(self):
        """Show term balances report"""
        balance_window = tk.Toplevel(self.root)
        balance_window.title("Term Balances")
        balance_window.geometry("800x600")
        
        columns = ['term_id', 'semester', 'acad_year', 'fee_amount', 'total_paid', 'balance']
        balance_table = DataTable(balance_window, columns)
        balance_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Get data
        balance_data = self.db.get_term_balances()
        balance_table.insert_data(balance_data)
    
    def __del__(self):
        """Cleanup when app is destroyed"""
        if hasattr(self, 'db'):
            self.db.disconnect()