import tkinter as tk
from tkinter import ttk, messagebox
from gui_components import DataTable, FormDialog
from database import DatabaseManager
from datetime import datetime, timedelta

from models import Membership, Payment, Student, Term, Organization

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
        
        # Create status bar first
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_student_management_tab()
        self.create_organization_tab()
        self.create_membership_tab()
        self.create_financial_tab()
        self.create_reports_tab()
        
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
        
        # Create subtabs within membership tab
        membership_notebook = ttk.Notebook(membership_frame)
        membership_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Subtab 1: All Members with Filtering
        all_members_frame = ttk.Frame(membership_notebook)
        membership_notebook.add(all_members_frame, text="All Members")
        
        all_members_frame.columnconfigure(0, weight=1)
        all_members_frame.columnconfigure(1, weight=0)
        all_members_frame.rowconfigure(0, weight=1)
        left_panel = ttk.Frame(all_members_frame)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Search frame for All Members
        search_frame_members = ttk.Frame(left_panel)
        search_frame_members.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame_members, text="Search:").pack(side=tk.LEFT)
        self.member_search_var = tk.StringVar()
        self.member_search_var.trace('w', self.filter_member_data)  # Bind to search box changes
        member_search_entry = ttk.Entry(search_frame_members, textvariable=self.member_search_var)
        member_search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Advanced filtering frame
        filter_controls_frame = ttk.Frame(left_panel)
        filter_controls_frame.pack(fill=tk.X, pady=5)
        
        # Status filter
        ttk.Label(filter_controls_frame, text="Status:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.status_filter_combo = ttk.Combobox(filter_controls_frame, state="readonly", width=15)
        self.status_filter_combo.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.status_filter_combo.bind('<<ComboboxSelected>>', self.filter_member_data)
        
        # Gender filter
        ttk.Label(filter_controls_frame, text="Gender:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.gender_filter_combo = ttk.Combobox(filter_controls_frame, state="readonly", width=15)
        self.gender_filter_combo.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.gender_filter_combo.bind('<<ComboboxSelected>>', self.filter_member_data)
        
        # Degree Program filter
        ttk.Label(filter_controls_frame, text="Degree Program:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.degree_filter_combo = ttk.Combobox(filter_controls_frame, state="readonly", width=15)
        self.degree_filter_combo.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.degree_filter_combo.bind('<<ComboboxSelected>>', self.filter_member_data)
        
        # Batch filter
        ttk.Label(filter_controls_frame, text="Batch:").grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
        self.batch_filter_combo = ttk.Combobox(filter_controls_frame, state="readonly", width=15)
        self.batch_filter_combo.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        self.batch_filter_combo.bind('<<ComboboxSelected>>', self.filter_member_data)
        
        # Committee filter
        ttk.Label(filter_controls_frame, text="Committee:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.committee_filter_combo = ttk.Combobox(filter_controls_frame, state="readonly", width=15)
        self.committee_filter_combo.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        self.committee_filter_combo.bind('<<ComboboxSelected>>', self.filter_member_data)
        
        # Clear filters button
        ttk.Button(filter_controls_frame, text="Clear Filters", command=self.clear_member_filters).grid(row=2, column=2, padx=5, pady=2, sticky=tk.W)
        
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
        
        # Search frame
        search_frame = ttk.Frame(left_panel_terms)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_term_data)  # Bind to search box changes
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Only Semester and Academic Year dropdowns here
        org_frame_terms = ttk.Frame(left_panel_terms)
        org_frame_terms.pack(fill=tk.X, pady=5)
        ttk.Label(org_frame_terms, text="Semester:").pack(side=tk.LEFT)
        self.term_semester_combo = ttk.Combobox(org_frame_terms, values=["1st", "2nd", "Summer"], state="readonly")
        self.term_semester_combo.pack(side=tk.LEFT, padx=5)
        self.term_semester_combo.bind('<<ComboboxSelected>>', lambda e: self.load_term_data())
        ttk.Label(org_frame_terms, text="Academic Year:").pack(side=tk.LEFT, padx=(10,0))
        self.term_acad_year_combo = ttk.Combobox(org_frame_terms, state="readonly")
        self.term_acad_year_combo.pack(side=tk.LEFT, padx=5)
        self.term_acad_year_combo.bind('<<ComboboxSelected>>', lambda e: self.load_term_data())
        
        # Fee/term list
        columns_terms = [
            'Student ID', 'Name', 'Batch', 'Committee', 'Status',
            'Semester', 'Academic Year', 'Role',
            'Term Start', 'Term End', 'Due Date'
        ]
        self.term_table = DataTable(left_panel_terms, columns_terms)
        self.term_table.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for term actions
        right_panel_terms = ttk.Frame(terms_frame, width=200)
        right_panel_terms.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        right_panel_terms.pack_propagate(False)
        ttk.Button(right_panel_terms, text="Add Member to Term", command=self.add_member_to_term).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel_terms, text="Edit Member", command=self.edit_term_member).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel_terms, text="Edit Term Dates", command=self.edit_term_dates).pack(fill=tk.X, pady=2)
        
        # Load organizations
        self.load_organizations()
        
        # Store the original data for filtering
        self.original_term_data = []
        self.original_member_data = []
    
    def clear_member_filters(self):
        """Clear all member filters"""
        self.status_filter_combo.set("")
        self.gender_filter_combo.set("")
        self.degree_filter_combo.set("")
        self.batch_filter_combo.set("")
        self.committee_filter_combo.set("")
        self.filter_member_data()
    
    def populate_member_filters(self):
        """Populate filter comboboxes with unique values from the current data"""
        if not self.original_member_data:
            return
        
        # Get unique values for each filter
        statuses = sorted(set(member['Status'].split(' (')[0] for member in self.original_member_data if member['Status']))
        genders = sorted(set(member['Gender'] for member in self.original_member_data if member['Gender']))
        degrees = sorted(set(member['Degree Program'] for member in self.original_member_data if member['Degree Program']))
        batches = sorted(set(member['Batch'] for member in self.original_member_data if member['Batch']))
        committees = sorted(set(member['Committee'] for member in self.original_member_data if member['Committee']))
        
        # Populate comboboxes
        self.status_filter_combo['values'] = [''] + statuses
        self.gender_filter_combo['values'] = [''] + genders
        self.degree_filter_combo['values'] = [''] + degrees
        self.batch_filter_combo['values'] = [''] + batches
        self.committee_filter_combo['values'] = [''] + committees
    
    def filter_member_data(self, *args):
        """Filter the member table based on search text and filter criteria"""
        search_text = self.member_search_var.get().lower()
        status_filter = self.status_filter_combo.get()
        gender_filter = self.gender_filter_combo.get()
        degree_filter = self.degree_filter_combo.get()
        batch_filter = self.batch_filter_combo.get()
        committee_filter = self.committee_filter_combo.get()
        
        # Clear the table
        self.member_table.clear()
        
        # Filter and insert matching data
        if self.original_member_data:
            filtered_data = []
            for row in self.original_member_data:
                # Check search text
                if search_text and search_text not in f"{row['First Name']} {row['Last Name']}".lower():
                    continue
                
                # Check status filter (extract base status without additional info)
                if status_filter and not row['Status'].startswith(status_filter):
                    continue
                
                # Check gender filter
                if gender_filter and row['Gender'] != gender_filter:
                    continue
                
                # Check degree program filter
                if degree_filter and row['Degree Program'] != degree_filter:
                    continue
                
                # Check batch filter
                if batch_filter and row['Batch'] != batch_filter:
                    continue
                
                # Check committee filter
                if committee_filter and row['Committee'] != committee_filter:
                    continue
                
                filtered_data.append(row)
            
            self.member_table.insert_data(filtered_data)
            self.status_bar.config(text=f"Showing {len(filtered_data)} of {len(self.original_member_data)} members")

    def filter_term_data(self, *args):
        """Filter the term table based on search text"""
        search_text = self.search_var.get().lower()
        
        # Clear the table
        self.term_table.clear()
        
        # Filter and insert matching data
        if self.original_term_data:
            filtered_data = [
                row for row in self.original_term_data
                if search_text in row['Name'].lower()
            ]
            self.term_table.insert_data(filtered_data)

    def load_term_data(self):
        """Load data specifically for the terms subtab"""
        try:
            org_name = self.org_combo.get()
            semester = self.term_semester_combo.get()
            acad_year = self.term_acad_year_combo.get()
            if not all([org_name, semester, acad_year]):
                self.status_bar.config(text="Please select organization, semester, and academic year")
                return
                
            orgs = self.db.get_all_organizations()
            if not orgs:
                self.status_bar.config(text="No organizations found")
                return
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            # Get members for the selected semester with all relevant attributes
            query = """
            SELECT s.student_id, s.first_name, s.last_name, 
                   m.batch, m.committee,
                   t.mem_status, t.semester, t.acad_year, COALESCE(t.role, 'Member') as role,
                   t.term_start, t.term_end, t.fee_due,
                   t.term_id
            FROM student s
            JOIN membership m ON s.student_id = m.student_id
            JOIN organization org ON m.org_id = org.org_id
            JOIN term t ON m.membership_id = t.membership_id
            WHERE org.org_id = ? AND t.semester = ? AND t.acad_year = ?
            GROUP BY s.student_id, t.term_id
            """
            results = self.db.execute_query(query, (org_id, semester, acad_year))
            
            # Clear existing items
            self.term_table.clear()
            
            # Update table columns
            columns = [
                'Student ID', 'Name', 'Batch', 'Committee', 'Status',
                'Semester', 'Academic Year', 'Role',
                'Term Start', 'Term End', 'Due Date'
            ]
            self.term_table.tree['columns'] = columns
            for col in columns:
                self.term_table.tree.heading(col, text=col)
                self.term_table.tree.column(col, width=100)
            
            # Insert new data
            if results:
                formatted_members = []
                for row in results:
                    formatted_member = {
                        'Student ID': row[0],
                        'Name': f"{row[1]} {row[2]}",
                        'Batch': row[3],
                        'Committee': row[4],
                        'Status': row[5],
                        'Semester': row[6],
                        'Academic Year': row[7],
                        'Role': row[8] if row[8] else 'Member',  # Default to 'Member' if role is empty
                        'Term Start': row[9].strftime('%Y-%m-%d') if row[9] else 'N/A',
                        'Term End': row[10].strftime('%Y-%m-%d') if row[10] else 'N/A',
                        'Due Date': row[11].strftime('%Y-%m-%d') if row[11] else 'N/A',
                        'term_id': row[12]  # Store term_id for reference
                    }
                    formatted_members.append(formatted_member)
                
                # Store the original data for filtering
                self.original_term_data = formatted_members
                
                # Apply any existing search filter
                search_text = self.search_var.get().lower()
                if search_text:
                    formatted_members = [
                        row for row in formatted_members
                        if search_text in row['Name'].lower()
                    ]
                
                self.term_table.insert_data(formatted_members)
                self.status_bar.config(text=f"Loaded {len(results)} members for {semester} {acad_year}")
            else:
                self.status_bar.config(text=f"No members found for {semester} {acad_year}")
                self.original_term_data = []
            
            # Force update of the UI
            self.term_table.update_idletasks()
            self.root.update_idletasks()
            
        except Exception as e:
            print(f"Error loading term data: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to load term data: {str(e)}")
            self.status_bar.config(text="Error loading term data")
    
    def create_financial_tab(self):
        financial_frame = ttk.Frame(self.notebook)
        self.notebook.add(financial_frame, text="Financial Management")
        
        # Configure grid weights for the main frame
        financial_frame.columnconfigure(0, weight=3)  # Left panel gets more space
        financial_frame.columnconfigure(1, weight=1)  # Right panel gets less space
        financial_frame.rowconfigure(0, weight=1)
        
        # Left panel for fee list
        left_panel = ttk.Frame(financial_frame)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Organization and term selection
        filter_frame = ttk.Frame(left_panel)
        filter_frame.pack(fill=tk.X, pady=5)
        
        # Configure filter frame grid
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(3, weight=1)
        filter_frame.columnconfigure(5, weight=1)
        
        ttk.Label(filter_frame, text="Organization:").grid(row=0, column=0, padx=5)
        self.fin_org_combo = ttk.Combobox(filter_frame, state="readonly")
        self.fin_org_combo.grid(row=0, column=1, padx=5, sticky='ew')
        self.fin_org_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        
        ttk.Label(filter_frame, text="Semester:").grid(row=0, column=2, padx=5)
        self.semester_combo = ttk.Combobox(filter_frame, values=["1st", "2nd", "Summer"], state="readonly")
        self.semester_combo.grid(row=0, column=3, padx=5, sticky='ew')
        self.semester_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        
        ttk.Label(filter_frame, text="Academic Year:").grid(row=0, column=4, padx=5)
        self.acad_year_combo = ttk.Combobox(filter_frame, state="readonly")
        self.acad_year_combo.grid(row=0, column=5, padx=5, sticky='ew')
        self.acad_year_combo.bind('<<ComboboxSelected>>', lambda e: self.load_financial_data())
        
        # Search frame
        search_frame = ttk.Frame(left_panel)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.financial_search_var = tk.StringVar()
        self.financial_search_var.trace('w', self.filter_financial_data)  # Bind to search box changes
        financial_search_entry = ttk.Entry(search_frame, textvariable=self.financial_search_var)
        financial_search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Fee list
        columns = ['Student ID', 'Name', 'Status', 'Fee Amount', 'Amount Paid', 'Balance', 'Due Date']
        self.fee_table = DataTable(left_panel, columns)
        self.fee_table.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for actions
        right_panel = ttk.Frame(financial_frame, width=200)  # Set fixed width
        right_panel.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        right_panel.grid_propagate(False)  # Prevent the frame from shrinking
        
        # Action buttons with padding and proper spacing
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Record Payment", command=self.record_payment).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="View Late Payments", command=self.view_late_payments).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="View Highest Debt", command=self.view_highest_debt).pack(fill=tk.X, pady=2)
        
        # Store original financial data for filtering
        self.original_financial_data = []
        
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
        ttk.Button(left_panel, text="Unpaid Fees by Organization", command=self.show_unpaid_fees).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Unpaid Fees by Student", command=self.show_student_unpaid).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Member Roles by AY", command=self.show_member_in_role).pack(fill=tk.X, pady=2)
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
        
        # Search frame
        search_frame = ttk.Frame(student_frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.student_search_var = tk.StringVar()
        self.student_search_var.trace('w', self.filter_student_data)  # Bind to search box changes
        student_search_entry = ttk.Entry(search_frame, textvariable=self.student_search_var)
        student_search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
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
        
        # Store original student data for filtering
        self.original_student_data = []
        
        # Load initial data
        self.refresh_students()
    
    def create_organization_tab(self):
        """Create the organization management tab"""
        org_frame = ttk.Frame(self.notebook)
        self.notebook.add(org_frame, text="Organization Management")
        
        # Search frame
        search_frame = ttk.Frame(org_frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.org_search_var = tk.StringVar()
        self.org_search_var.trace('w', self.filter_organization_data)  # Bind to search box changes
        org_search_entry = ttk.Entry(search_frame, textvariable=self.org_search_var)
        org_search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Buttons frame
        buttons_frame = ttk.Frame(org_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Add Organization", command=self.add_organization).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Edit Organization", command=self.edit_organization).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Delete Organization", command=self.delete_organization).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_organizations).pack(side=tk.LEFT, padx=5)
        
        # Organizations table
        columns = ['Organization ID', 'Organization Name']
        self.organizations_table = DataTable(org_frame, columns)
        self.organizations_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Store original organization data for filtering
        self.original_org_data = []
        
        # Load initial data
        self.refresh_organizations()
    
    def create_terms(self):
        """Create a new term for the organization"""
        org_name = self.fin_org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
            
        # Get term details
        fields = [
            {'name': 'semester', 'label': 'Semester', 'type': 'combobox', 
             'values': ['1st', '2nd', 'Summer']},
            {'name': 'acad_year', 'label': 'Academic Year', 'type': 'entry', 
             'default': f"{datetime.now().year}-{datetime.now().year + 1}"},
            {'name': 'term_start', 'label': 'Term Start Date', 'type': 'entry', 
             'default': datetime.now().strftime('%Y-%m-%d')}
        ]
        
        dialog = FormDialog(self, "Create Term", fields)
        self.wait_window(dialog)
        
        if not dialog.result:
            return  # User cancelled
            
        try:
            semester = dialog.result['semester']
            acad_year = dialog.result['acad_year']
            term_start = datetime.strptime(dialog.result['term_start'], '%Y-%m-%d').date()
            term_end = term_start + timedelta(days=150)  # Automatically set end date to 150 days after start
            
            # Get organization ID
            orgs = self.db.get_all_organizations()
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            # Check if term already exists for this organization
            query = """
            SELECT COUNT(*) FROM term t
            JOIN membership m ON t.membership_id = m.membership_id
            WHERE m.org_id = ? AND t.semester = ? AND t.acad_year = ?
            """
            result = self.db.execute_query(query, (org_id, semester, acad_year))
            
            if result and result[0][0] > 0:
                messagebox.showwarning("Warning", f"Term already exists for {semester} {acad_year}")
                return
            
            messagebox.showinfo("Success", f"Term created for {semester} {acad_year}\nStart: {term_start}\nEnd: {term_end}")
            self.load_financial_data()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create term: {str(e)}")

    def add_member_to_term(self):
        """Add a member to an existing term"""
        org_name = self.org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
            
        # Get organization ID
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        # Get all members for this organization
        members = self.db.get_members_by_organization(org_id)
        if not members:
            messagebox.showwarning("Warning", "No members found in this organization")
            return
            
        # Create list of member options
        member_options = [f"{m['student_id']} - {m['first_name']} {m['last_name']}" for m in members]
        
        # Create dialog for member selection, term details, and role assignment
        fields = [
            {'name': 'member', 'label': 'Select Member', 'type': 'combobox', 'values': member_options},
            {'name': 'semester', 'label': 'Semester', 'type': 'combobox', 
             'values': ['1st', '2nd', 'Summer']},
            {'name': 'acad_year', 'label': 'Academic Year', 'type': 'entry', 
             'default': f"{datetime.now().year}-{datetime.now().year + 1}"},
            {'name': 'term_start', 'label': 'Term Start Date', 'type': 'entry', 
             'default': datetime.now().strftime('%Y-%m-%d')},
            {'name': 'role', 'label': 'Role', 'type': 'combobox', 
             'values': ['Member', 'President', 'Vice President', 'Secretary', 'Treasurer']},
            {'name': 'fee_amount', 'label': 'Fee Amount', 'type': 'entry', 'default': '1000.00'}
        ]
        
        dialog = FormDialog(self, "Add Member to Term", fields)
        self.wait_window(dialog)
        
        if not dialog.result:
            return  # User cancelled
            
        try:
            # Extract student ID from the selected option
            selected_member = dialog.result['member']
            student_id = int(selected_member.split(' - ')[0])
            semester = dialog.result['semester']
            acad_year = dialog.result['acad_year']
            
            # Get membership ID for the selected member
            membership_id = next(m['membership_id'] for m in members if m['student_id'] == student_id)
            
            # Check if member already has a term for this semester/year
            query = """
            SELECT COUNT(*) FROM term t
            WHERE t.membership_id = ? AND t.semester = ? AND t.acad_year = ?
            """
            result = self.db.execute_query(query, (membership_id, semester, acad_year))
            
            if result and result[0][0] > 0:
                messagebox.showwarning("Warning", f"Member already has a term for {semester} {acad_year}")
                return
            
            # Set term dates
            term_start = datetime.strptime(dialog.result['term_start'], '%Y-%m-%d').date()
            term_end = term_start + timedelta(days=150)  # 150 days term duration
            
            # Create term for member
            term = Term(
                term_id=None,
                semester=semester,
                term_start=term_start,
                term_end=term_end,
                acad_year=acad_year,
                fee_amount=float(dialog.result['fee_amount']),
                fee_due=term_end,
                role=dialog.result['role'],
                membership_id=membership_id
            )
            
            if self.db.add_term(term):
                messagebox.showinfo("Success", f"Added member to term {semester} {acad_year}")
                self.load_term_data()
            else:
                messagebox.showerror("Error", "Failed to add member to term")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add member to term: {str(e)}")
    
    def load_organizations(self):
        """Load organizations and initialize combo boxes for the membership tab"""
        orgs = self.db.get_all_organizations()
        self.org_combo['values'] = [org.org_name for org in orgs]
        if orgs:
            self.org_combo.set(orgs[0].org_name)
        
        # Populate academic years for membership terms subtab
        years = self.db.get_available_academic_years()
        self.term_acad_year_combo['values'] = years
        if years:
            self.term_acad_year_combo.set(years[0])
        self.term_semester_combo.set("1st")
        
        # Load initial members data
        self.load_members()
    
    def load_organizations_financial(self):
        """Load organizations and initialize combo boxes for the financial tab"""
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
        
        # Load initial financial data
        self.load_financial_data()
    
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
                
                # Store the original data for filtering
                self.original_member_data = formatted_members
                
                # Populate filter dropdowns
                self.populate_member_filters()
                
                # Apply any existing search filter
                self.filter_member_data()
            else:
                print("No members found to display")  # Debug print
                self.original_member_data = []
            self.member_table.update_idletasks()
            self.root.update_idletasks()
            self.status_bar.config(text=f"Loaded {len(members) if members else 0} members for {org_name}")
        except Exception as e:
            print(f"Error loading members: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to load members: {str(e)}")
            self.status_bar.config(text="Error loading members")
    
    def load_financial_data(self):
        """Load data specifically for the financial tab"""
        try:
            org_name = self.fin_org_combo.get()
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
            
            # Get members for the selected semester
            query = """
            SELECT s.student_id, s.first_name, s.last_name, 
                   m.mem_status, t.fee_amount, 
                   COALESCE(SUM(p.amount), 0) as total_paid,
                   (t.fee_amount - COALESCE(SUM(p.amount), 0)) as balance,
                   t.fee_due, t.term_id
            FROM student s
            JOIN membership m ON s.student_id = m.student_id
            JOIN organization org ON m.org_id = org.org_id
            JOIN term t ON m.membership_id = t.membership_id
            LEFT JOIN payment p ON t.term_id = p.term_id
            WHERE org.org_id = ? AND t.semester = ? AND t.acad_year = ?
            GROUP BY s.student_id, t.term_id
            """
            results = self.db.execute_query(query, (org_id, semester, acad_year))
            
            # Clear existing items
            self.fee_table.clear()
            
            # Update table columns
            columns = ['Student ID', 'Name', 'Status', 'Fee Amount', 'Amount Paid', 'Balance', 'Due Date']
            self.fee_table.tree['columns'] = columns
            for col in columns:
                self.fee_table.tree.heading(col, text=col)
                self.fee_table.tree.column(col, width=100)
            
            # Insert new data
            if results:
                formatted_members = []
                for row in results:
                    formatted_member = {
                        'Student ID': row[0],
                        'Name': f"{row[1]} {row[2]}",
                        'Status': row[3],
                        'Fee Amount': f"₱{row[4]:.2f}",
                        'Amount Paid': f"₱{row[5]:.2f}",
                        'Balance': f"₱{row[6]:.2f}",
                        'Due Date': row[7].strftime('%Y-%m-%d') if row[7] else 'N/A',
                        'term_id': row[8]  # Store term_id for reference
                    }
                    formatted_members.append(formatted_member)
                
                # Store original data for filtering
                self.original_financial_data = formatted_members
                
                # Apply any existing search filter
                search_text = self.financial_search_var.get().lower()
                if search_text:
                    formatted_members = [
                        row for row in formatted_members
                        if search_text in row['Name'].lower()
                    ]
                
                self.fee_table.insert_data(formatted_members)
            else:
                self.original_financial_data = []
            
            # Force update of the UI
            self.fee_table.update_idletasks()
            self.root.update_idletasks()
            
            # Update status bar
            self.status_bar.config(text=f"Loaded {len(results) if results else 0} members for {semester} {acad_year}")
            
        except Exception as e:
            print(f"Error loading financial data: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to load financial data: {str(e)}")
            self.status_bar.config(text="Error loading financial data")
    
    def add_member(self):
        # Get all students
        students = self.db.get_all_students()
        if not students:
            messagebox.showwarning("Warning", "No students available. Please add students first.")
            return

        # Create a list of student options for the combobox
        student_options = [f"{s.student_id} - {s.first_name} {s.last_name}" for s in students]
        
        fields = [
            {'name': 'student', 'label': 'Select Student', 'type': 'combobox', 'values': student_options},
            {'name': 'committee', 'label': 'Committee', 'type': 'combobox', 
             'values': ['Finance', 'Secretariat', 'Documentation', 'Externals', 
                       'Membership', 'Logistics', 'Education & Research', 'Publication']},
            {'name': 'semester', 'label': 'Semester', 'type': 'combobox', 
             'values': ['1st', '2nd', 'Summer']},
            {'name': 'acad_year', 'label': 'Academic Year', 'type': 'entry', 
             'default': f"{datetime.now().year}-{datetime.now().year + 1}"},
            {'name': 'term_start', 'label': 'Term Start Date', 'type': 'entry', 
             'default': datetime.now().strftime('%Y-%m-%d')},
            {'name': 'role', 'label': 'Role', 'type': 'combobox', 
             'values': ['Member', 'President', 'Vice President', 'Secretary', 'Treasurer']}
        ]
        
        dialog = FormDialog(self, "Add New Member", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # Extract student ID from the selected option
                selected_student = dialog.result['student']
                student_id = int(selected_student.split(' - ')[0])
                
                # Get organization ID
                org_name = self.org_combo.get()
                orgs = self.db.get_all_organizations()
                org_id = next(org.org_id for org in orgs if org.org_name == org_name)
                
                # Check if student is already a member
                query = """
                SELECT COUNT(*) FROM membership 
                WHERE student_id = ? AND org_id = ?
                """
                result = self.db.execute_query(query, (student_id, org_id))
                if result and result[0][0] > 0:
                    messagebox.showwarning("Warning", "This student is already a member of this organization")
                    return
                
                # Create membership without mem_status, using academic year as batch
                membership = Membership(
                    membership_id=None,
                    batch=dialog.result['acad_year'],  # Use academic year as batch
                    committee=dialog.result['committee'],
                    org_id=org_id,
                    student_id=student_id
                )
                
                # Add membership
                if not self.db.add_membership(membership):
                    raise Exception("Failed to add membership")
                
                # Get the membership ID of the newly created membership
                query = """
                SELECT membership_id FROM membership 
                WHERE student_id = ? AND org_id = ?
                """
                result = self.db.execute_query(query, (student_id, org_id))
                if not result:
                    raise Exception("Failed to get membership ID")
                membership_id = result[0][0]
                
                # Create term with mem_status
                term_start = datetime.strptime(dialog.result['term_start'], '%Y-%m-%d').date()
                term_end = term_start + timedelta(days=150)  # 150 days term duration
                
                term = Term(
                    term_id=None,
                    semester=dialog.result['semester'],
                    term_start=term_start,
                    term_end=term_end,
                    acad_year=dialog.result['acad_year'],
                    fee_amount=1000.00,  # Default fee amount
                    fee_due=term_end,
                    role=dialog.result['role'],
                    mem_status='active',  # Set initial status as active
                    membership_id=membership_id
                )
                
                if not self.db.add_term(term):
                    raise Exception("Failed to add term")
                
                messagebox.showinfo("Success", "Member added successfully with initial term.")
                self.load_members()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add member: {str(e)}")
    
    def edit_member(self):
        selected = self.member_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to edit")
            return
        
        # Get the student ID and membership ID from the selected member
        student_id = selected['Student ID']
        membership_id = selected['Membership ID']
        
        # Get the organization ID
        org_name = self.org_combo.get()
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        # Get current committee
        query = """
        SELECT committee
        FROM membership
        WHERE membership_id = ?
        """
        result = self.db.execute_query(query, (membership_id,))
        
        if not result:
            messagebox.showerror("Error", "Could not find membership record")
            return
            
        current_committee = result[0][0]
        
        fields = [
            {'name': 'committee', 'label': 'Committee', 'type': 'combobox', 
             'values': ['Finance', 'Secretariat', 'Documentation', 'Externals', 
                       'Membership', 'Logistics', 'Education & Research', 'Publication'],
             'default': current_committee}
        ]
        
        dialog = FormDialog(self, "Edit Member", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # Update committee in membership table
                if not self.db.update_membership_committee(membership_id, dialog.result['committee']):
                    raise Exception("Failed to update committee")
                
                self.load_members()  # Refresh the members table
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
            unpaid_fees = self.db.get_member_unpaid_fees(selected['Student ID'])
            
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
    
    def show_receipt(self, payment: Payment, member_info: dict, term_info: dict):
        """Display a simple receipt for the payment"""
        try:
            # Create a new window for the receipt
            receipt_window = tk.Toplevel(self)
            receipt_window.title("Payment Receipt")
            receipt_window.geometry("400x500")
            
            # Create a frame for the receipt content
            receipt_frame = ttk.Frame(receipt_window, padding="20")
            receipt_frame.pack(fill=tk.BOTH, expand=True)
            
            # Organization header
            org_name = self.fin_org_combo.get()
            ttk.Label(receipt_frame, text=org_name, font=('Helvetica', 14, 'bold')).pack(pady=(0, 10))
            ttk.Label(receipt_frame, text="PAYMENT RECEIPT", font=('Helvetica', 12, 'bold')).pack(pady=(0, 20))
            
            # Receipt details
            details_frame = ttk.Frame(receipt_frame)
            details_frame.pack(fill=tk.X, pady=10)
            
            # Member details
            ttk.Label(details_frame, text="Member Details:", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Name: {member_info['Name']}").pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Student ID: {member_info['Student ID']}").pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Status: {member_info['Status']}").pack(anchor=tk.W)
            
            # Term details
            ttk.Label(details_frame, text="\nTerm Details:", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Semester: {term_info['semester']}").pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Academic Year: {term_info['acad_year']}").pack(anchor=tk.W)
            
            # Payment details
            ttk.Label(details_frame, text="\nPayment Details:", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Date: {payment.payment_date.strftime('%Y-%m-%d')}").pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Fee Amount: ₱{term_info['fee_amount']:.2f}").pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Amount Paid: ₱{payment.amount:.2f}").pack(anchor=tk.W)
            ttk.Label(details_frame, text=f"Balance: ₱{float(term_info['fee_amount']) - payment.amount:.2f}").pack(anchor=tk.W)
            
            # Add a separator
            ttk.Separator(receipt_frame, orient='horizontal').pack(fill=tk.X, pady=20)
            
            # Add footer
            ttk.Label(receipt_frame, text="Thank you for your payment!", font=('Helvetica', 10, 'italic')).pack()
            ttk.Label(receipt_frame, text="This receipt serves as proof of payment.").pack()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show receipt: {str(e)}")

    def record_payment(self):
        selected = self.fee_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to record payment")
            return
        
        # Get the current balance
        try:
            balance = float(selected['Balance'].replace('₱', '').replace(',', ''))
            if balance <= 0:
                messagebox.showwarning("Warning", "This member has no outstanding balance")
                return
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Could not determine current balance")
            return
        
        # Debug print to check selected item
        print(f"Selected item: {selected}")
        
        fields = [
            {'name': 'amount', 'label': 'Amount', 'type': 'entry', 'default': str(balance)},
            {'name': 'payment_date', 'label': 'Payment Date', 'type': 'entry', 'default': datetime.now().strftime('%Y-%m-%d')}
        ]
        
        dialog = FormDialog(self, "Record Payment", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                from decimal import Decimal
                amount = Decimal(str(dialog.result['amount']))
                if amount <= 0:
                    messagebox.showerror("Error", "Payment amount must be greater than 0")
                    return
                if amount > Decimal(str(balance)):
                    messagebox.showerror("Error", "Payment amount cannot exceed the current balance")
                    return
                
                # Debug print to check term_id
                print(f"Term ID from selected item: {selected.get('term_id')}")
                term_id = selected['term_id']
                
                # Create payment record
                payment = Payment(
                    payment_id=None,
                    amount=float(amount),  # Convert back to float for storage
                    payment_date=datetime.strptime(dialog.result['payment_date'], '%Y-%m-%d').date(),
                    term_id=term_id
                )
                
                # Add payment
                if not self.db.add_payment(payment):
                    raise Exception("Failed to record payment")
                
                # Update payment status in term table
                # First check if this payment completes the balance
                query = """
                SELECT t.fee_amount, COALESCE(SUM(p.amount), 0) as total_paid,
                       t.semester, t.acad_year, t.fee_due
                FROM term t
                LEFT JOIN payment p ON t.term_id = p.term_id
                WHERE t.term_id = ?
                GROUP BY t.term_id
                """
                result = self.db.execute_query(query, (term_id,))
                
                if result:
                    fee_amount = Decimal(str(result[0][0]))
                    total_paid = Decimal(str(result[0][1]))
                    new_total_paid = total_paid + amount
                    
                    # Update payment status based on whether the balance is fully paid
                    payment_status = "paid" if new_total_paid >= fee_amount else "partial"
                    update_query = "UPDATE term SET payment_status = ? WHERE term_id = ?"
                    if not self.db.execute_update(update_query, (payment_status, term_id)):
                        raise Exception("Failed to update payment status")
                    
                    # Show success message first
                    messagebox.showinfo("Success", "Payment recorded successfully")
                    
                    # Then show receipt
                    term_info = {
                        'semester': result[0][2],
                        'acad_year': result[0][3],
                        'fee_amount': float(fee_amount)
                    }
                    self.show_receipt(payment, selected, term_info)
                
                # Refresh the financial data
                self.load_financial_data()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
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
            year = int(dialog.result['as_of_date'].split('-')[0])
            month = int(dialog.result['as_of_date'].split('-')[1])

            
            alumni = self.db.get_alumni_members(org_id, year, month)
            
            # Update table columns for alumni
            columns = ['student_id', 'first_name', 'last_name', 'batch']
            self.report_table.tree['columns'] = columns
            for col in columns:
                self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
                self.report_table.tree.column(col, width=100)

            formatted_data = []
            for alum in alumni:
                formatted_data.append({
                    'student_id': alum['student_id'],
                    'first_name': alum['first_name'],
                    'last_name': alum['last_name'],
                    'batch': alum['batch']
                })
            
            self.report_table.insert_data(alumni)

    def show_unpaid_fees(self):
        org_name = self.report_org_combo.get()
        semester = self.report_semester_combo.get()
        acad_year = self.report_year_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        unpaid = self.db.get_unpaid_fees(org_id, semester, acad_year) 
        
        # Update table columns for membership status
        columns = ['membership_id', 'first_name', 'last_name', 'total_balance']
        self.report_table.tree['columns'] = columns
        for col in columns:
            self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
            self.report_table.tree.column(col, width=100)
        
        # Format the data
        formatted_data = []
        for fee in unpaid:
            formatted_data.append({
                'membership_id': fee['membership_id'],
                'first_name': fee['first_name'],
                'last_name': fee['last_name'],
                'total_balance': f"₱{fee['total_balance']:.2f}"
            })
        self.report_table.insert_data(formatted_data)

    def show_student_unpaid(self):
        students = self.db.get_all_students()
        
        student_options = [f"{s.student_id} ({s.first_name} {s.last_name})" for s in students]

        fields = [
            {'name': 'student', 'label': 'Select Student', 'type': 'combobox', 'values': student_options},
        ]
        
        dialog = FormDialog(self, "Select Student", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            selected_student = dialog.result['student']
            student_id = int(selected_student.split(' ')[0])
        
            unpaid = self.db.get_student_unpaid(student_id) 
        
        # Update table columns for membership status
        columns = ['first_name', 'last_name', 'org_id', 'org_name', 'term_id', 'semester', 'acad_year', 'amount']
        self.report_table.tree['columns'] = columns
        for col in columns:
            self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
            self.report_table.tree.column(col, width=100)
        
        # Format the data
        formatted_data = []
        for fee in unpaid:
            formatted_data.append({
                'first_name': fee['first_name'],
                'last_name': fee['last_name'],
                'org_id': fee['org_id'],
                'org_name': fee['org_name'],
                'term_id': fee['term_id'],
                'semester': fee['semester'],
                'acad_year': fee['acad_year'],
                'payment_status': fee['payment_status'],
                'amount': fee['amount']
            })
        self.report_table.insert_data(formatted_data)

    def show_member_in_role(self):
        org_name = self.report_org_combo.get()
        acad_year = self.report_year_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        fields = [
            {'name': 'role', 'label': 'Role', 'type': 'combobox', 
             'values': ['President', 'Vice President', 'Secretary', 'Treasurer', 'Member']}
        ]

        dialog = FormDialog(self, "Select Executive Role", fields)
        self.wait_window(dialog)

        if dialog.result:
            role = dialog.result['role'].lower()
        
            officers = self.db.get_member_in_role(org_id, role, acad_year) 

        # Update table columns for membership status
        columns = ['membership_id', 'first_name', 'last_name', 'org_id', 'term_id', 'semester', 'term_start', 'term_end', 'acad_year', 'role']
        self.report_table.tree['columns'] = columns
        for col in columns:
            self.report_table.tree.heading(col, text=col.replace('_', ' ').title())
            self.report_table.tree.column(col, width=100)
        
        # Format the data
        formatted_data = []
        for officer in officers:
            formatted_data.append({
                'mebership_id': officer['membership_id'],
                'first_name': officer['first_name'],
                'last_name': officer['last_name'],
                'org_id': officer['org_id'],
                'term_id': officer['term_id'],
                'semester': officer['semester'],
                'term_start': officer['term_start'],
                'term_end': officer['term_end'],
                'acad_year': officer['acad_year'],
                'role': officer['role']
            })
        self.report_table.insert_data(formatted_data)


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
            org_name = self.org_combo.get()
            semester = self.term_semester_combo.get()
            acad_year = self.term_acad_year_combo.get()
            
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
                    
                    # Get count of terms to be updated
                    count_query = """
                    SELECT COUNT(*) 
                    FROM term t
                    JOIN membership m ON t.membership_id = m.membership_id
                    WHERE m.org_id = ? AND t.semester = ? AND t.acad_year = ?
                    """
                    count_result = self.db.execute_query(count_query, (org_id, semester, acad_year))
                    term_count = count_result[0][0] if count_result else 0
                    
                    # Confirm update
                    if not messagebox.askyesno("Confirm", 
                        f"Update term dates for {semester} {acad_year}?\n"
                        f"This will affect {term_count} members.\n"
                        f"Start: {new_start}\n"
                        f"End: {new_end}\n"
                        f"Due date will be set to the end date"):
                        return
                    
                    # Update term dates for all members in this term
                    update_query = """
                    UPDATE term t
                    JOIN membership m ON t.membership_id = m.membership_id
                    SET t.term_start = ?, t.term_end = ?, t.fee_due = ?
                    WHERE m.org_id = ? AND t.semester = ? AND t.acad_year = ?
                    """
                    if self.db.execute_update(update_query, (new_start, new_end, new_end, org_id, semester, acad_year)):
                        messagebox.showinfo("Success", f"Updated term dates for {term_count} members")
                        # Reload term data to show updated dates
                        self.load_term_data()
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
                    self.refresh_organizations()
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
        
        # Store original data for filtering
        self.original_student_data = student_data
        
        # Apply any existing search filter
        search_text = self.student_search_var.get().lower()
        if search_text:
            student_data = [
                row for row in student_data
                if search_text in f"{row['First Name']} {row['Last Name']}".lower()
            ]
        
        self.students_table.insert_data(student_data)
    
    def edit_organization(self):
        """Edit selected organization"""
        selected = self.organizations_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select an organization to edit")
            return
        
        fields = [
            {'name': 'org_name', 'label': 'Organization Name:', 'type': 'entry', 'default': selected['Organization Name']}
        ]
        
        dialog = FormDialog(self, "Edit Organization", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                org = Organization(
                    org_id=int(selected['Organization ID']),
                    org_name=dialog.result['org_name']
                )
                
                if self.db.update_organization(org):
                    messagebox.showinfo("Success", "Organization updated successfully!")
                    self.refresh_organizations()
                    # Also refresh other organization dropdowns
                    self.load_organizations()
                    self.load_organizations_financial()
                    self.load_report_filters()
                else:
                    messagebox.showerror("Error", "Failed to update organization!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update organization: {str(e)}")
    
    def delete_organization(self):
        """Delete selected organization"""
        selected = self.organizations_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select an organization to delete")
            return
        
        if messagebox.askyesno("Confirm", f"Delete organization {selected['Organization Name']}?"):
            try:
                if self.db.delete_organization(int(selected['Organization ID'])):
                    messagebox.showinfo("Success", "Organization deleted successfully!")
                    self.refresh_organizations()
                    # Also refresh other organization dropdowns
                    self.load_organizations()
                    self.load_organizations_financial()
                    self.load_report_filters()
                else:
                    messagebox.showerror("Error", "Failed to delete organization!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete organization: {str(e)}")
    
    def refresh_organizations(self):
        """Refresh the organizations table"""
        orgs = self.db.get_all_organizations()
        org_data = [
            {
                'Organization ID': org.org_id,
                'Organization Name': org.org_name
            }
            for org in orgs
        ]
        
        # Store original data for filtering
        self.original_org_data = org_data
        
        # Apply any existing search filter
        search_text = self.org_search_var.get().lower()
        if search_text:
            org_data = [
                row for row in org_data
                if search_text in row['Organization Name'].lower()
            ]
        
        self.organizations_table.insert_data(org_data)
    
    def filter_student_data(self, *args):
        """Filter the student table based on search text"""
        search_text = self.student_search_var.get().lower()
        
        # Clear the table
        self.students_table.clear()
        
        # Filter and insert matching data
        if self.original_student_data:
            filtered_data = [
                row for row in self.original_student_data
                if search_text in f"{row['First Name']} {row['Last Name']}".lower()
            ]
            self.students_table.insert_data(filtered_data)

    def filter_organization_data(self, *args):
        """Filter the organization table based on search text"""
        search_text = self.org_search_var.get().lower()
        
        # Clear the table
        self.organizations_table.clear()
        
        # Filter and insert matching data
        if self.original_org_data:
            filtered_data = [
                row for row in self.original_org_data
                if search_text in row['Organization Name'].lower()
            ]
            self.organizations_table.insert_data(filtered_data)

    def filter_financial_data(self, *args):
        """Filter the financial table based on search text"""
        search_text = self.financial_search_var.get().lower()
        
        # Clear the table
        self.fee_table.clear()
        
        # Filter and insert matching data
        if self.original_financial_data:
            filtered_data = [
                row for row in self.original_financial_data
                if search_text in row['Name'].lower()
            ]
            self.fee_table.insert_data(filtered_data)

    def edit_term_member(self):
        """Edit a member from the terms view"""
        selected = self.term_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to edit")
            return
        
        # Get the term ID from the selected item
        term_id = selected['term_id']
        
        # Get current values
        query = """
        SELECT role, mem_status
        FROM term
        WHERE term_id = ?
        """
        result = self.db.execute_query(query, (term_id,))
        
        if not result:
            messagebox.showerror("Error", "Could not find term record")
            return
            
        current_role, current_status = result[0]
        
        fields = [
            {'name': 'role', 'label': 'Role', 'type': 'combobox',
             'values': ['Member', 'President', 'Vice President', 'Secretary', 'Treasurer'],
             'default': current_role if current_role else 'Member'},
            {'name': 'mem_status', 'label': 'Status', 'type': 'combobox',
             'values': ['active', 'inactive', 'suspended', 'expelled', 'alumni'],
             'default': current_status}
        ]
        
        dialog = FormDialog(self, "Edit Member Term", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # Update role and status in term table
                update_query = """
                UPDATE term 
                SET role = ?, mem_status = ?
                WHERE term_id = ?
                """
                if not self.db.execute_update(update_query, (
                    dialog.result['role'],
                    dialog.result['mem_status'],
                    term_id
                )):
                    raise Exception("Failed to update term")
                
                self.load_term_data()  # Refresh the terms table
                messagebox.showinfo("Success", "Member term updated successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update member term: {str(e)}")
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()