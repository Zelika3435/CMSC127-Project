import tkinter as tk
from tkinter import ttk, messagebox
from gui_components import DataTable, FormDialog
from database import DatabaseManager
from datetime import datetime, timedelta

from models import Membership, Payment, Student, Term

class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Organization Management System")
        self.root.geometry("1200x800")
        
        # Initialize database
        self.db = DatabaseManager()
        if not self.db.connect():
            messagebox.showerror("Error", "Could not connect to database")
            self.root.destroy()
            return
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_student_management_tab()
        self.create_membership_tab()
        self.create_financial_tab()
        self.create_reports_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Menu bar
        self.create_menu()
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def create_menu(self):
        menubar = tk.Menu(self)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.destroy)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_membership_tab(self):
        membership_frame = ttk.Frame(self.notebook)
        self.notebook.add(membership_frame, text="Membership Management")
        
        # Filter frame
        filter_frame = ttk.Frame(membership_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(filter_frame, text="Organization:").pack(side=tk.LEFT)
        self.org_combo = ttk.Combobox(filter_frame, state="readonly")
        self.org_combo.pack(side=tk.LEFT, padx=5)
        self.org_combo.bind('<<ComboboxSelected>>', self.load_members)
        
        # Add Organization button
        ttk.Button(filter_frame, text="Add Organization", command=self.add_organization).pack(side=tk.RIGHT, padx=5)
        
        # Create subtabs within membership tab
        membership_notebook = ttk.Notebook(membership_frame)
        membership_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Subtab 1: All Members
        all_members_frame = ttk.Frame(membership_notebook)
        membership_notebook.add(all_members_frame, text="All Members")
        
        all_members_frame.columnconfigure(0, weight=1)
        all_members_frame.columnconfigure(1, weight=0)
        all_members_frame.rowconfigure(0, weight=1)
        left_panel = ttk.Frame(all_members_frame)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Member list with all attributes
        columns = ['Student ID', 'First Name', 'Last Name', 'Gender', 'Degree Program', 'Standing', 'Status', 'Batch', 'Committee', 'Membership ID']
        self.member_table = DataTable(left_panel, columns, height=12)
        self.member_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel for actions
        right_panel = ttk.Frame(all_members_frame, width=200)
        right_panel.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        right_panel.pack_propagate(False)
        ttk.Button(right_panel, text="Add Member", command=self.add_member).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="Edit Member", command=self.edit_member).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="Remove Member", command=self.remove_member).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="View Details", command=self.view_member_details).pack(fill=tk.X, pady=2)
        
        # --- Membership Terms Subtab ---
        terms_frame = ttk.Frame(membership_notebook)
        membership_notebook.add(terms_frame, text="Membership Terms")
        
        terms_frame.columnconfigure(0, weight=1)
        terms_frame.columnconfigure(1, weight=0)
        terms_frame.rowconfigure(0, weight=1)
        left_panel_terms = ttk.Frame(terms_frame)
        left_panel_terms.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        # Only Semester and Academic Year dropdowns here
        org_frame_terms = ttk.Frame(left_panel_terms)
        org_frame_terms.pack(fill=tk.X, pady=5)
        ttk.Label(org_frame_terms, text="Semester:").pack(side=tk.LEFT)
        self.semester_combo = ttk.Combobox(org_frame_terms, values=["1st", "2nd", "Summer"], state="readonly")
        self.semester_combo.pack(side=tk.LEFT, padx=5)
        self.semester_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        ttk.Label(org_frame_terms, text="Academic Year:").pack(side=tk.LEFT, padx=(10,0))
        self.acad_year_combo = ttk.Combobox(org_frame_terms, state="readonly")
        self.acad_year_combo.pack(side=tk.LEFT, padx=5)
        self.acad_year_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        # Fee/term list (reuse fee_table for now)
        columns_terms = ['Student ID', 'Name', 'Status', 'Fee Amount', 'Amount Paid', 'Balance', 'Due Date']
        self.fee_table = DataTable(left_panel_terms, columns_terms)
        self.fee_table.pack(fill=tk.BOTH, expand=True)
        # Right panel for term actions
        right_panel_terms = ttk.Frame(terms_frame, width=200)
        right_panel_terms.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        right_panel_terms.pack_propagate(False)
        ttk.Button(right_panel_terms, text="Add Membership Term", command=self.create_terms).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel_terms, text="Edit Term Dates", command=self.edit_term_dates).pack(fill=tk.X, pady=2)
        # Load organizations
        self.load_organizations()
    
    def create_financial_tab(self):
        financial_frame = ttk.Frame(self.notebook)
        self.notebook.add(financial_frame, text="Financial Management")
        
        # Left panel for fee list
        left_panel = ttk.Frame(financial_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Organization and term selection
        filter_frame = ttk.Frame(left_panel)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Organization:").grid(row=0, column=0, padx=5)
        self.fin_org_combo = ttk.Combobox(filter_frame, state="readonly")
        self.fin_org_combo.grid(row=0, column=1, padx=5)
        self.fin_org_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        
        ttk.Label(filter_frame, text="Semester:").grid(row=0, column=2, padx=5)
        self.semester_combo = ttk.Combobox(filter_frame, values=["1st", "2nd", "Summer"], state="readonly")
        self.semester_combo.grid(row=0, column=3, padx=5)
        self.semester_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        
        ttk.Label(filter_frame, text="Academic Year:").grid(row=0, column=4, padx=5)
        self.acad_year_combo = ttk.Combobox(filter_frame, state="readonly")
        self.acad_year_combo.grid(row=0, column=5, padx=5)
        self.acad_year_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        
        # Fee list
        columns = ['Student ID', 'Name', 'Status', 'Fee Amount', 'Amount Paid', 'Balance', 'Due Date']
        self.fee_table = DataTable(left_panel, columns)
        self.fee_table.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for actions
        right_panel = ttk.Frame(financial_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Action buttons
        ttk.Button(right_panel, text="Record Payment", command=self.record_payment).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="View Late Payments", command=self.view_late_payments).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="View Highest Debt", command=self.view_highest_debt).pack(fill=tk.X, pady=2)
        
        # Load initial data
        self.load_organizations_financial()
    
    def create_reports_tab(self):
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Left panel for report selection and filters
        left_panel = ttk.Frame(reports_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Organization selection
        org_frame = ttk.Frame(left_panel)
        org_frame.pack(fill=tk.X, pady=5)
        ttk.Label(org_frame, text="Organization:").pack(side=tk.LEFT)
        self.report_org_combo = ttk.Combobox(org_frame, state="readonly")
        self.report_org_combo.pack(side=tk.LEFT, padx=5)
        
        # Academic year selection
        year_frame = ttk.Frame(left_panel)
        year_frame.pack(fill=tk.X, pady=5)
        ttk.Label(year_frame, text="Academic Year:").pack(side=tk.LEFT)
        self.report_year_combo = ttk.Combobox(year_frame, state="readonly")
        self.report_year_combo.pack(side=tk.LEFT, padx=5)
        
        # Semester selection
        semester_frame = ttk.Frame(left_panel)
        semester_frame.pack(fill=tk.X, pady=5)
        ttk.Label(semester_frame, text="Semester:").pack(side=tk.LEFT)
        self.report_semester_combo = ttk.Combobox(semester_frame, values=["1st", "2nd", "Summer"], state="readonly")
        self.report_semester_combo.pack(side=tk.LEFT, padx=5)
        
        # Report buttons
        ttk.Button(left_panel, text="Membership Status", command=self.show_membership_status).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Executive Committee", command=self.show_executive_committee).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Role History", command=self.show_role_history).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Alumni List", command=self.show_alumni).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Financial Summary", command=self.show_financial_summary).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Late Payments", command=self.show_late_payments_report).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Highest Debt", command=self.show_highest_debt_report).pack(fill=tk.X, pady=2)
        
        # Right panel for report display
        right_panel = ttk.Frame(reports_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Report display area
        self.report_table = DataTable(right_panel, ['No Data'])
        self.report_table.pack(fill=tk.BOTH, expand=True)
        
        # Load initial data
        self.load_report_filters()
    
    def create_student_management_tab(self):
        """Create the student management tab"""
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="Student Management")
        
        # Buttons frame
        buttons_frame = ttk.Frame(student_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Edit Student", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Delete Student", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_students).pack(side=tk.LEFT, padx=5)
        
        # Students table
        columns = ['Student ID', 'First Name', 'Last Name', 'Gender', 'Degree Program', 'Standing']
        self.students_table = DataTable(student_frame, columns)
        self.students_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load initial data
        self.refresh_students()
    
    def create_terms(self):
        """Add a member to the selected term (semester and academic year)"""
        org_name = self.fin_org_combo.get()
        semester = self.semester_combo.get()
        acad_year = self.acad_year_combo.get()
        
        if not all([org_name, semester, acad_year]):
            messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
            return
        
        # Get term dates from database
        query = """
        SELECT term_start, term_end 
        FROM term 
        WHERE semester = ? AND acad_year = ? 
        LIMIT 1
        """
        result = self.db.execute_query(query, (semester, acad_year))
        
        if not result:
            messagebox.showerror("Error", f"No term exists for {semester} {acad_year}. Please create the term first.")
            return
            
        term_start, term_end = result[0]
        
        # Create dialog for student ID input
        fields = [
            {'name': 'student_id', 'label': 'Student ID', 'type': 'entry'}
        ]
        
        dialog = FormDialog(self, "Add Member to Term", fields)
        self.wait_window(dialog)
        
        if not dialog.result:
            return  # User cancelled
            
        try:
            student_id = int(dialog.result['student_id'])
            
            # Get organization ID
            orgs = self.db.get_all_organizations()
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            # Check if student is a member of the organization and get their status
            query = """
            SELECT m.membership_id, m.mem_status
            FROM membership m
            JOIN member mb ON m.student_id = mb.student_id
            WHERE mb.student_id = ? AND m.org_id = ?
            """
            result = self.db.execute_query(query, (student_id, org_id))
            
            if not result:
                messagebox.showerror("Error", f"Student ID {student_id} is not a member of {org_name}")
                return
                
            membership_id, mem_status = result[0]
            
            # Check if member is expelled or alumni
            if mem_status in ['expelled', 'alumni']:
                messagebox.showerror("Error", f"Cannot add {mem_status} member to term")
                return
            
            # Check if member already has a term for this semester/year
            query = """
            SELECT COUNT(*) FROM term t
            WHERE t.membership_id = ? AND t.semester = ? AND t.acad_year = ?
            """
            result = self.db.execute_query(query, (membership_id, semester, acad_year))
            
            if result and result[0][0] > 0:
                messagebox.showwarning("Warning", f"Member already has a term for {semester} {acad_year}")
                return
            
            # Add member to the term
            term = Term(
                term_id=None,
                semester=semester,
                term_start=term_start,
                term_end=term_end,
                acad_year=acad_year,
                fee_amount=1000.0 if mem_status == 'active' else 500.0,  # Fee based on status
                fee_due=term_end,  # Due date is the end of term
                membership_id=membership_id
            )
            
            if self.db.add_term(term):
                messagebox.showinfo("Success", f"Added member to {semester} {acad_year}")
                self.load_financial_data()
            else:
                messagebox.showerror("Error", "Failed to add member to term")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid student ID. Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add member to term: {str(e)}")
    
    def load_organizations(self):
        orgs = self.db.get_all_organizations()
        self.org_combo['values'] = [org.org_name for org in orgs]
        if orgs:
            self.org_combo.set(orgs[0].org_name)
        # Populate academic years for membership terms subtab
        years = self.db.get_available_academic_years()
        self.acad_year_combo['values'] = years
        if years:
            self.acad_year_combo.set(years[0])
        self.semester_combo.set("1st")
    
    def load_organizations_financial(self):
        orgs = self.db.get_all_organizations()
        self.fin_org_combo['values'] = [org.org_name for org in orgs]
        if orgs:
            self.fin_org_combo.set(orgs[0].org_name)
        
        # Get academic years from database
        years = self.db.get_available_academic_years()
        self.acad_year_combo['values'] = years
        if years:
            self.acad_year_combo.set(years[0])
        
        # Set semester
        self.semester_combo.set("1st")
    
    def load_members(self, event=None):
        try:
            org_name = self.org_combo.get()
            if not org_name:
                return
            print(f"Loading members for organization: {org_name}")  # Debug print
            orgs = self.db.get_all_organizations()
            if not orgs:
                messagebox.showwarning("Warning", "No organizations found")
                return
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            members = self.db.get_members_by_organization(org_id)
            print(f"Found members: {members}")  # Debug print
            # Clear existing items
            self.member_table.clear()
            # Update table columns to match the data
            columns = ['Student ID', 'First Name', 'Last Name', 'Gender', 'Degree Program', 'Standing', 'Status', 'Batch', 'Committee', 'Membership ID']
            self.member_table.tree['columns'] = columns
            for col in columns:
                self.member_table.tree.heading(col, text=col)
                self.member_table.tree.column(col, width=100)
            # Hide Membership ID column
            self.member_table.tree.column('Membership ID', width=0, stretch=False, minwidth=0)
            self.member_table.tree.heading('Membership ID', text='', anchor='w')
            # Insert new data
            if members:
                formatted_members = []
                for member in members:
                    status = member['status']
                    if member['latest_semester'] and member['latest_acad_year']:
                        if member['status'] in ['expelled', 'alumni']:
                            status = f"{status} (Last Term: {member['latest_semester']} {member['latest_acad_year']})"
                        else:
                            status = f"{status} (Latest: {member['latest_semester']} {member['latest_acad_year']})"
                    formatted_member = {
                        'Student ID': member['student_id'],
                        'First Name': member['first_name'],
                        'Last Name': member['last_name'],
                        'Gender': member['gender'],
                        'Degree Program': member['degree_program'],
                        'Standing': member.get('standing', ''),
                        'Status': status,
                        'Batch': member['batch'],
                        'Committee': member.get('committee', ''),
                        'Membership ID': member.get('membership_id', '')
                    }
                    formatted_members.append(formatted_member)
                print(f"Formatted members for display: {formatted_members}")  # Debug print
                self.member_table.insert_data(formatted_members)
            else:
                print("No members found to display")  # Debug print
            self.member_table.update_idletasks()
            self.root.update_idletasks()
            self.status_bar.config(text=f"Loaded {len(members) if members else 0} members for {org_name}")
        except Exception as e:
            print(f"Error loading members: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to load members: {str(e)}")
            self.status_bar.config(text="Error loading members")
    
    def load_financial_data(self):
        try:
            org_name = self.org_combo.get()
            semester = self.semester_combo.get()
            acad_year = self.acad_year_combo.get()
            if not all([org_name, semester, acad_year]):
                messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
                return
            orgs = self.db.get_all_organizations()
            if not orgs:
                messagebox.showwarning("Warning", "No organizations found")
                return
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            members = self.db.get_members_with_unpaid_fees(org_id, semester, acad_year)
            
            # Clear existing items
            self.fee_table.clear()
            
            # Update table columns
            columns = ['Student ID', 'Name', 'Status', 'Fee Amount', 'Amount Paid', 'Balance', 'Due Date']
            self.fee_table.tree['columns'] = columns
            for col in columns:
                self.fee_table.tree.heading(col, text=col)
                self.fee_table.tree.column(col, width=100)
            
            # Insert new data
            if members:
                formatted_members = []
                for member in members:
                    formatted_member = {
                        'Student ID': member['student_id'],
                        'Name': f"{member['first_name']} {member['last_name']}",
                        'Status': member['status'],
                        'Fee Amount': f"₱{member['fee_amount']:.2f}",
                        'Amount Paid': f"₱{member['total_paid']:.2f}",
                        'Balance': f"₱{member['balance']:.2f}",
                        'Due Date': member.get('due_date', 'N/A')
                    }
                    formatted_members.append(formatted_member)
                
                self.fee_table.insert_data(formatted_members)
            
            # Force update of the UI
            self.fee_table.update_idletasks()
            self.root.update_idletasks()
            
            # Update status bar
            self.status_bar.config(text=f"Loaded {len(members) if members else 0} members with unpaid fees for {org_name}")
            
        except Exception as e:
            print(f"Error loading financial data: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to load financial data: {str(e)}")
            self.status_bar.config(text="Error loading financial data")
    
    def add_member(self):
        fields = [
            {'name': 'first_name', 'label': 'First Name', 'type': 'entry'},
            {'name': 'last_name', 'label': 'Last Name', 'type': 'entry'},
            {'name': 'gender', 'label': 'Gender', 'type': 'combobox', 'values': ['Male', 'Female', 'Other']},
            {'name': 'degree_program', 'label': 'Degree Program', 'type': 'entry'},
            {'name': 'standing', 'label': 'Standing', 'type': 'combobox', 'values': ['Freshman', 'Sophomore', 'Junior', 'Senior']},
            {'name': 'batch', 'label': 'Batch', 'type': 'entry'}
        ]
        
        dialog = FormDialog(self, "Add New Member", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # Create student
                student = Student(
                    student_id=None,
                    first_name=dialog.result['first_name'],
                    last_name=dialog.result['last_name'],
                    gender=dialog.result['gender'],
                    degree_program=dialog.result['degree_program'],
                    standing=dialog.result['standing']
                )
                
                # Add student to database
                if not self.db.add_student(student):
                    raise Exception("Failed to add student")
                
                # Get the student ID
                students = self.db.get_all_students()
                student_id = next(s.student_id for s in students if s.first_name == student.first_name and s.last_name == student.last_name)
                
                # Add to member table
                if not self.db.add_member(student_id):
                    raise Exception("Failed to add member")
                
                # Get organization ID
                org_name = self.org_combo.get()
                orgs = self.db.get_all_organizations()
                org_id = next(org.org_id for org in orgs if org.org_name == org_name)
                
                # Create membership
                membership = Membership(
                    membership_id=None,
                    batch=dialog.result['batch'],
                    mem_status='active',
                    committee=None,
                    org_id=org_id,
                    student_id=student_id
                )
                
                # Add membership
                if not self.db.add_membership(membership):
                    raise Exception("Failed to add membership")
                
                # Get the membership ID
                members = self.db.get_members_by_organization(org_id)
                membership_id = next(m['membership_id'] for m in members if m['student_id'] == student_id)
                
                # Determine current semester and academic year
                from datetime import date, timedelta
                current_date = date.today()
                month = current_date.month
                
                if month >= 6 and month <= 10:
                    semester = "1st"
                    acad_year = f"{current_date.year}-{current_date.year + 1}"
                elif month >= 11 or month <= 3:
                    semester = "2nd"
                    acad_year = f"{current_date.year}-{current_date.year + 1}"
                else:
                    semester = "Summer"
                    acad_year = f"{current_date.year}-{current_date.year + 1}"
                
                # Create term with fee for new active member
                term = Term(
                    term_id=None,
                    semester=semester,
                    term_start=current_date,
                    term_end=current_date + timedelta(days=180),
                    acad_year=acad_year,
                    fee_amount=1000.0,  # Active member fee
                    fee_due=current_date + timedelta(days=30),
                    membership_id=membership_id
                )
                
                if not self.db.add_term(term):
                    raise Exception("Failed to create term")
                
                messagebox.showinfo("Success", "Member added successfully with initial membership fee")
                self.load_members()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add member: {str(e)}")
    
    def edit_member(self):
        selected = self.member_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to edit")
            return
        
        # Extract just the status without any additional text
        current_status = selected['Status'].split(' (')[0] if ' (' in selected['Status'] else selected['Status']
        
        fields = [
            {'name': 'committee', 'label': 'Role', 'type': 'combobox', 
             'values': ['Member', 'President', 'Vice President', 'Secretary', 'Treasurer'],
             'default': selected['Committee']},
            {'name': 'mem_status', 'label': 'Status', 'type': 'combobox',
             'values': ['active', 'inactive', 'suspended', 'expelled', 'alumni'],
             'default': current_status}
        ]
        
        dialog = FormDialog(self, "Edit Member", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                membership_id = int(selected['Membership ID'])
                # Update both committee and status
                if not self.db.update_membership_status(membership_id, dialog.result['mem_status']):
                    raise Exception("Failed to update membership status")
                if not self.db.update_membership_committee(membership_id, dialog.result['committee']):
                    raise Exception("Failed to update committee")
                self.load_members()
                messagebox.showinfo("Success", "Member updated successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update member: {str(e)}")
    
    def remove_member(self):
        selected = self.member_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to remove")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this member?"):
            try:
                membership_id = int(selected['Membership ID'])
                if not self.db.delete_membership(membership_id):
                    raise Exception("Failed to delete membership")
                self.load_members()
                messagebox.showinfo("Success", "Member removed successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove member: {str(e)}")
    
    def view_member_details(self):
        selected = self.member_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to view details")
            return
        
        try:
            # Get member's unpaid fees
            unpaid_fees = self.db.get_member_unpaid_fees(selected['student_id'])
            
            # Create details window
            details_window = tk.Toplevel(self)
            details_window.title(f"Member Details - {selected['First Name']} {selected['Last Name']}")
            details_window.geometry("600x400")
            
            # Member info
            info_frame = ttk.LabelFrame(details_window, text="Member Information")
            info_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(info_frame, text=f"Student ID: {selected['Student ID']}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Name: {selected['First Name']} {selected['Last Name']}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Status: {selected['Status']}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Batch: {selected['Batch']}").pack(anchor=tk.W)
            
            # Unpaid fees
            fees_frame = ttk.LabelFrame(details_window, text="Unpaid Fees")
            fees_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            columns = ['Organization', 'Semester', 'Academic Year', 'Fee Amount', 'Amount Paid', 'Balance']
            fees_table = DataTable(fees_frame, columns)
            fees_table.pack(fill=tk.BOTH, expand=True)
            fees_table.insert_data(unpaid_fees)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load member details: {str(e)}")
    
    def record_payment(self):
        selected = self.fee_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to record payment")
            return
        
        fields = [
            {'name': 'amount', 'label': 'Amount', 'type': 'entry'},
            {'name': 'payment_date', 'label': 'Payment Date', 'type': 'entry', 'default': datetime.now().strftime('%Y-%m-%d')}
        ]
        
        dialog = FormDialog(self, "Record Payment", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # Create payment
                payment = Payment(
                    payment_id=None,
                    payment_status='completed',
                    amount=float(dialog.result['amount']),
                    payment_date=datetime.strptime(dialog.result['payment_date'], '%Y-%m-%d').date(),
                    term_id=selected['term_id']
                )
                
                # Add payment
                if not self.db.add_payment(payment):
                    raise Exception("Failed to record payment")
                
                messagebox.showinfo("Success", "Payment recorded successfully")
                self.load_financial_data()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to record payment: {str(e)}")
    
    def view_late_payments(self):
        org_name = self.fin_org_combo.get()
        semester = self.semester_combo.get()
        acad_year = self.acad_year_combo.get()
        
        if not all([org_name, semester, acad_year]):
            messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        late_payments = self.db.get_late_payments(org_id, semester, acad_year)
        self.fee_table.insert_data(late_payments)
    
    def view_highest_debt(self):
        org_name = self.fin_org_combo.get()
        semester = self.semester_combo.get()
        acad_year = self.acad_year_combo.get()
        
        if not all([org_name, semester, acad_year]):
            messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        highest_debt = self.db.get_highest_debt_members(org_id, semester, acad_year)
        self.fee_table.insert_data(highest_debt)
    
    def load_report_filters(self):
        # Load organizations
        orgs = self.db.get_all_organizations()
        self.report_org_combo['values'] = [org.org_name for org in orgs]
        if orgs:
            self.report_org_combo.set(orgs[0].org_name)
        
        # Set academic years (last 5 years)
        current_year = datetime.now().year
        years = [f"{year}-{year+1}" for year in range(current_year-4, current_year+1)]
        self.report_year_combo['values'] = years
        self.report_year_combo.set(years[-1])
        
        # Set semester
        self.report_semester_combo.set("1st")
    
    def show_membership_status(self):
        org_name = self.report_org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        status = self.db.get_membership_status_percentage(org_id, 2)  # Last 2 semesters
        
        # Update table columns for membership status
        columns = ['active_percentage', 'inactive_percentage', 'total_members']
        self.report_table.tree['columns'] = columns
        for col in columns:
            self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
            self.report_table.tree.column(col, width=100)
        
        # Format the data
        formatted_data = [{
            'active_percentage': f"{status['active_percentage']:.2f}%",
            'inactive_percentage': f"{status['inactive_percentage']:.2f}%",
            'total_members': status['total_members']
        }]
        self.report_table.insert_data(formatted_data)
    
    def show_executive_committee(self):
        org_name = self.report_org_combo.get()
        acad_year = self.report_year_combo.get()
        
        if not org_name or not acad_year:
            messagebox.showwarning("Warning", "Please select organization and academic year")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        committee = self.db.get_executive_committee(org_id, acad_year)
        
        # Update table columns for executive committee
        columns = ['student_id', 'first_name', 'last_name', 'role']
        self.report_table.tree['columns'] = columns
        for col in columns:
            self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
            self.report_table.tree.column(col, width=100)
        
        self.report_table.insert_data(committee)
    
    def show_role_history(self):
        org_name = self.report_org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        fields = [
            {'name': 'role', 'label': 'Role', 'type': 'combobox', 
             'values': ['President', 'Vice President', 'Secretary', 'Treasurer', 'Member']}
        ]
        
        dialog = FormDialog(self, "Select Role", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            orgs = self.db.get_all_organizations()
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            history = self.db.get_role_history(org_id, dialog.result['role'])
            
            # Update table columns for role history
            columns = ['student_id', 'first_name', 'last_name', 'academic_year']
            self.report_table.tree['columns'] = columns
            for col in columns:
                self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
                self.report_table.tree.column(col, width=100)
            
            self.report_table.insert_data(history)
    
    def show_alumni(self):
        org_name = self.report_org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        fields = [
            {'name': 'as_of_date', 'label': 'As of Date', 'type': 'entry', 
             'default': datetime.now().strftime('%Y-%m-%d')}
        ]
        
        dialog = FormDialog(self, "Select Date", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            orgs = self.db.get_all_organizations()
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            alumni = self.db.get_alumni_members(org_id, dialog.result['as_of_date'])
            
            # Update table columns for alumni
            columns = ['student_id', 'first_name', 'last_name', 'batch']
            self.report_table.tree['columns'] = columns
            for col in columns:
                self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
                self.report_table.tree.column(col, width=100)
            
            self.report_table.insert_data(alumni)
    
    def show_financial_summary(self):
        org_name = self.report_org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        fields = [
            {'name': 'as_of_date', 'label': 'As of Date', 'type': 'entry', 
             'default': datetime.now().strftime('%Y-%m-%d')}
        ]
        
        dialog = FormDialog(self, "Select Date", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            orgs = self.db.get_all_organizations()
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            summary = self.db.get_organization_financial_status(org_id, dialog.result['as_of_date'])
            
            # Update table columns for financial summary
            columns = ['total_fees', 'total_paid', 'total_unpaid']
            self.report_table.tree['columns'] = columns
            for col in columns:
                self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
                self.report_table.tree.column(col, width=100)
            
            # Format the data
            formatted_data = [{
                'total_fees': f"₱{summary['total_fees']:.2f}",
                'total_paid': f"₱{summary['total_paid']:.2f}",
                'total_unpaid': f"₱{summary['total_unpaid']:.2f}"
            }]
            self.report_table.insert_data(formatted_data)
    
    def show_late_payments_report(self):
        org_name = self.report_org_combo.get()
        semester = self.report_semester_combo.get()
        acad_year = self.report_year_combo.get()
        
        if not all([org_name, semester, acad_year]):
            messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        late_payments = self.db.get_late_payments(org_id, semester, acad_year)
        
        # Update table columns for late payments
        columns = ['student_id', 'first_name', 'last_name', 'payment_date', 'due_date', 'amount']
        self.report_table.tree['columns'] = columns
        for col in columns:
            self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
            self.report_table.tree.column(col, width=100)
        
        # Format the data
        formatted_data = []
        for payment in late_payments:
            formatted_data.append({
                'student_id': payment['student_id'],
                'first_name': payment['first_name'],
                'last_name': payment['last_name'],
                'payment_date': payment['payment_date'].strftime('%Y-%m-%d'),
                'due_date': payment['due_date'].strftime('%Y-%m-%d'),
                'amount': f"₱{payment['amount']:.2f}"
            })
        self.report_table.insert_data(formatted_data)
    
    def show_highest_debt_report(self):
        org_name = self.report_org_combo.get()
        semester = self.report_semester_combo.get()
        acad_year = self.report_year_combo.get()
        
        if not all([org_name, semester, acad_year]):
            messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        highest_debt = self.db.get_highest_debt_members(org_id, semester, acad_year)
        
        # Update table columns for highest debt
        columns = ['student_id', 'first_name', 'last_name', 'fee_amount', 'total_paid', 'balance']
        self.report_table.tree['columns'] = columns
        for col in columns:
            self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
            self.report_table.tree.column(col, width=100)
        
        # Format the data
        formatted_data = []
        for debt in highest_debt:
            formatted_data.append({
                'student_id': debt['student_id'],
                'first_name': debt['first_name'],
                'last_name': debt['last_name'],
                'fee_amount': f"₱{debt['fee_amount']:.2f}",
                'total_paid': f"₱{debt['total_paid']:.2f}",
                'balance': f"₱{debt['balance']:.2f}"
            })
        self.report_table.insert_data(formatted_data)
    
    def show_about(self):
        messagebox.showinfo("About", "Organization Management System\nVersion 1.0")
    
    def edit_term_dates(self):
        """Edit the start and end dates of the selected term"""
        try:
            org_name = self.fin_org_combo.get()
            semester = self.semester_combo.get()
            acad_year = self.acad_year_combo.get()
            
            if not all([org_name, semester, acad_year]):
                messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
                return
            
            # Get organization ID
            orgs = self.db.get_all_organizations()
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            # Get current term dates
            query = """
            SELECT term_start, term_end
            FROM term t
            JOIN membership m ON t.membership_id = m.membership_id
            WHERE m.org_id = ? AND t.semester = ? AND t.acad_year = ?
            LIMIT 1
            """
            result = self.db.execute_query(query, (org_id, semester, acad_year))
            
            if not result:
                messagebox.showwarning("Warning", f"No term found for {semester} {acad_year}")
                return
            
            current_start, current_end = result[0]
            
            # Create dialog for new dates
            fields = [
                {'name': 'term_start', 'label': 'Term Start Date', 'type': 'entry', 'default': current_start.strftime('%Y-%m-%d')},
                {'name': 'term_end', 'label': 'Term End Date', 'type': 'entry', 'default': current_end.strftime('%Y-%m-%d')}
            ]
            
            dialog = FormDialog(self, "Edit Term Dates", fields)
            self.wait_window(dialog)
            
            if dialog.result:
                try:
                    new_start = datetime.strptime(dialog.result['term_start'], '%Y-%m-%d').date()
                    new_end = datetime.strptime(dialog.result['term_end'], '%Y-%m-%d').date()
                    
                    if new_start >= new_end:
                        messagebox.showerror("Error", "Start date must be before end date")
                        return
                    
                    # Confirm update
                    if not messagebox.askyesno("Confirm", 
                        f"Update term dates for {semester} {acad_year}?\n"
                        f"Start: {new_start}\n"
                        f"End: {new_end}\n"
                        f"Due date will be set to the end date"):
                        return
                    
                    # Update term dates
                    if self.db.update_term_dates(org_id, semester, acad_year, new_start, new_end):
                        messagebox.showinfo("Success", "Term dates updated successfully")
                        # Reload financial data to show updated due dates
                        self.load_financial_data()
                    else:
                        messagebox.showerror("Error", "Failed to update term dates")
                    
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update term dates: {str(e)}")
    
    def add_organization(self):
        """Add a new organization"""
        fields = [
            {'name': 'org_name', 'label': 'Organization Name:', 'type': 'entry'}
        ]
        
        dialog = FormDialog(self, "Add Organization", fields)
        self.wait_window(dialog)
        
        if dialog.result and dialog.result['org_name']:
            try:
                if self.db.add_organization(dialog.result['org_name']):
                    messagebox.showinfo("Success", "Organization added successfully!")
                    # Refresh organization lists
                    self.load_organizations()
                    self.load_organizations_financial()
                    self.load_report_filters()
                else:
                    messagebox.showerror("Error", "Failed to add organization!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add organization: {str(e)}")
    
    def add_student(self):
        """Add a new student"""
        fields = [
            {'name': 'first_name', 'label': 'First Name:', 'type': 'entry'},
            {'name': 'last_name', 'label': 'Last Name:', 'type': 'entry'},
            {'name': 'gender', 'label': 'Gender:', 'type': 'combobox', 'values': ['Male', 'Female', 'Other']},
            {'name': 'degree_program', 'label': 'Degree Program:', 'type': 'entry'},
            {'name': 'standing', 'label': 'Standing:', 'type': 'combobox', 'values': ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']}
        ]
        
        dialog = FormDialog(self, "Add Student", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
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
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def edit_student(self):
        """Edit selected student"""
        selected = self.students_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        fields = [
            {'name': 'first_name', 'label': 'First Name:', 'type': 'entry', 'default': selected['First Name']},
            {'name': 'last_name', 'label': 'Last Name:', 'type': 'entry', 'default': selected['Last Name']},
            {'name': 'gender', 'label': 'Gender:', 'type': 'combobox', 'values': ['Male', 'Female', 'Other'], 'default': selected['Gender']},
            {'name': 'degree_program', 'label': 'Degree Program:', 'type': 'entry', 'default': selected['Degree Program']},
            {'name': 'standing', 'label': 'Standing:', 'type': 'combobox', 'values': ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate'], 'default': selected['Standing']}
        ]
        
        dialog = FormDialog(self, "Edit Student", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                student = Student(
                    student_id=int(selected['Student ID']),
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
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update student: {str(e)}")
    
    def delete_student(self):
        """Delete selected student"""
        selected = self.students_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        if messagebox.askyesno("Confirm", f"Delete student {selected['First Name']} {selected['Last Name']}?"):
            try:
                if self.db.delete_student(int(selected['Student ID'])):
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    self.refresh_students()
                else:
                    messagebox.showerror("Error", "Failed to delete student!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def refresh_students(self):
        """Refresh the students table"""
        students = self.db.get_all_students()
        student_data = [
            {
                'Student ID': s.student_id,
                'First Name': s.first_name,
                'Last Name': s.last_name,
                'Gender': s.gender,
                'Degree Program': s.degree_program,
                'Standing': s.standing
            }
            for s in students
        ]
        self.students_table.insert_data(student_data)
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect() 