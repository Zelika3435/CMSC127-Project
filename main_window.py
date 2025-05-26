import tkinter as tk
from tkinter import ttk, messagebox
from gui_components import DataTable, FormDialog
from database import DatabaseManager
from datetime import datetime

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
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_membership_tab()
        self.create_financial_tab()
        self.create_reports_tab()
        self.create_viewmem_tab()
        
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
        
        # Left panel for member list
        left_panel = ttk.Frame(membership_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Organization selection
        org_frame = ttk.Frame(left_panel)
        org_frame.pack(fill=tk.X, pady=5)
        ttk.Label(org_frame, text="Organization:").pack(side=tk.LEFT)
        self.org_combo = ttk.Combobox(org_frame, state="readonly")
        self.org_combo.pack(side=tk.LEFT, padx=5)
        self.org_combo.bind('<<ComboboxSelected>>', self.load_members)
        
        # Member list
        columns = ['Student ID', 'First Name', 'Last Name', 'Status', 'Role', 'Batch']
        self.member_table = DataTable(left_panel, columns)
        self.member_table.pack(fill=tk.BOTH, expand=True)
        
        # Right panel for actions
        right_panel = ttk.Frame(membership_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Action buttons
        ttk.Button(right_panel, text="Add Member", command=self.add_member).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="Edit Member", command=self.edit_member).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="Remove Member", command=self.remove_member).pack(fill=tk.X, pady=2)
        ttk.Button(right_panel, text="View Details", command=self.view_member_details).pack(fill=tk.X, pady=2)
        
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
        
        ttk.Label(filter_frame, text="Semester:").grid(row=0, column=2, padx=5)
        self.semester_combo = ttk.Combobox(filter_frame, values=["1st", "2nd", "Summer"], state="readonly")
        self.semester_combo.grid(row=0, column=3, padx=5)
        
        ttk.Label(filter_frame, text="Academic Year:").grid(row=0, column=4, padx=5)
        self.acad_year_combo = ttk.Combobox(filter_frame, state="readonly")
        self.acad_year_combo.grid(row=0, column=5, padx=5)
        
        ttk.Button(filter_frame, text="Apply Filter", command=self.load_financial_data).grid(row=0, column=6, padx=5)
        ttk.Button(filter_frame, text="Create Terms", command=self.create_terms).grid(row=0, column=7, padx=5)
        
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
    
    def create_terms(self):
        """Create terms for active members for the selected semester and academic year"""
        org_name = self.fin_org_combo.get()
        semester = self.semester_combo.get()
        acad_year = self.acad_year_combo.get()
        
        if not all([org_name, semester, acad_year]):
            messagebox.showwarning("Warning", "Please select organization, semester, and academic year")
            return
        
        if not messagebox.askyesno("Confirm", f"Create terms for {org_name} - {semester} {acad_year}?"):
            return
        
        try:
            # Get organization ID
            orgs = self.db.get_all_organizations()
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            
            # Get all active members
            members = self.db.get_members_by_organization(org_id)
            active_members = [m for m in members if m['status'] == 'active']
            
            # Create terms for each active member
            from datetime import date, timedelta
            current_date = date.today()
            term_end = current_date + timedelta(days=180)
            fee_due = current_date + timedelta(days=30)
            
            terms_created = 0
            for member in active_members:
                # Check if term already exists
                query = """
                SELECT COUNT(*) FROM term t
                JOIN membership m ON t.membership_id = m.membership_id
                WHERE m.membership_id = ? AND t.semester = ? AND t.acad_year = ?
                """
                result = self.db.execute_query(query, (member['membership_id'], semester, acad_year))
                if result and result[0][0] > 0:
                    continue  # Term already exists
                
                # Create new term
                term = Term(
                    term_id=None,
                    semester=semester,
                    term_start=current_date,
                    term_end=term_end,
                    acad_year=acad_year,
                    fee_amount=1000.0,  # Active member fee
                    fee_due=fee_due,
                    membership_id=member['membership_id']
                )
                
                if self.db.add_term(term):
                    terms_created += 1
            
            messagebox.showinfo("Success", f"Created {terms_created} new terms")
            self.load_financial_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create terms: {str(e)}")
    
    def load_organizations(self):
        orgs = self.db.get_all_organizations()
        self.org_combo['values'] = [org.org_name for org in orgs]
        if orgs:
            self.org_combo.set(orgs[0].org_name)
    
    def load_organizations_financial(self):
        orgs = self.db.get_all_organizations()
        self.fin_org_combo['values'] = [org.org_name for org in orgs]
        if orgs:
            self.fin_org_combo.set(orgs[0].org_name)
        
        # Set academic years (last 5 years)
        current_year = datetime.now().year
        years = [f"{year}-{year+1}" for year in range(current_year-4, current_year+1)]
        self.acad_year_combo['values'] = years
        self.acad_year_combo.set(years[-1])
        
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
                
            print(f"Found organizations: {[org.org_name for org in orgs]}")  # Debug print
            
            org_id = next(org.org_id for org in orgs if org.org_name == org_name)
            print(f"Selected org_id: {org_id}")  # Debug print
            
            members = self.db.get_members_by_organization(org_id)
            print(f"Found members: {members}")  # Debug print
            
            # Clear existing items
            self.member_table.clear()
            
            # Update table columns to match the data
            columns = ['Student ID', 'First Name', 'Last Name', 'Status', 'Role', 'Batch']
            self.member_table.tree['columns'] = columns
            for col in columns:
                self.member_table.tree.heading(col, text=col)
                self.member_table.tree.column(col, width=100)
            
            # Insert new data
            if members:
                formatted_members = []
                for member in members:
                    formatted_member = {
                        'Student ID': member['student_id'],
                        'First Name': member['first_name'],
                        'Last Name': member['last_name'],
                        'Status': member['status'],
                        'Role': member['committee'],
                        'Batch': member['batch']
                    }
                    formatted_members.append(formatted_member)
                
                print(f"Formatted members for display: {formatted_members}")  # Debug print
                self.member_table.insert_data(formatted_members)
            else:
                print("No members found to display")  # Debug print
            
            # Force update of the UI
            self.member_table.update_idletasks()
            self.root.update_idletasks()
            
            # Update status bar
            self.status_bar.config(text=f"Loaded {len(members) if members else 0} members for {org_name}")
            
        except Exception as e:
            print(f"Error loading members: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to load members: {str(e)}")
            self.status_bar.config(text="Error loading members")
    
    def load_financial_data(self):
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
            {'name': 'committee', 'label': 'Role', 'type': 'combobox', 'values': ['Member', 'President', 'Vice President', 'Secretary', 'Treasurer']},
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
                    committee=dialog.result['committee'],
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
        
        fields = [
            {'name': 'committee', 'label': 'Role', 'type': 'combobox', 
             'values': ['Member', 'President', 'Vice President', 'Secretary', 'Treasurer'],
             'default': selected['Role']},
            {'name': 'mem_status', 'label': 'Status', 'type': 'combobox',
             'values': ['active', 'inactive', 'suspended', 'expelled', 'alumni'],
             'default': selected['Status']}
        ]
        
        dialog = FormDialog(self, "Edit Member", fields)
        self.wait_window(dialog)
        
        if dialog.result:
            try:
                # Update membership status
                if not self.db.update_membership_status(selected['membership_id'], dialog.result['mem_status']):
                    raise Exception("Failed to update membership status")
                
                messagebox.showinfo("Success", "Member updated successfully")
                self.load_members()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update member: {str(e)}")
    
    def remove_member(self):
        selected = self.member_table.get_selected_item()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to remove")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this member?"):
            try:
                # Delete student (this will cascade delete related records)
                if not self.db.delete_student(selected['student_id']):
                    raise Exception("Failed to delete student")
                
                messagebox.showinfo("Success", "Member removed successfully")
                self.load_members()
                
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
            ttk.Label(info_frame, text=f"Role: {selected['Role']}").pack(anchor=tk.W)
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
    
    def create_viewmem_tab(self):
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="Reports (View Members)")

        # Organization dropdown
        ttk.Label(self.reports_frame, text="Organization:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.org_combobox = ttk.Combobox(self.reports_frame, state="readonly", width=30)
        self.org_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Filters labels and comboboxes
        filter_labels = ["Status", "Gender", "Degree Program", "Batch", "Committee"]
        self.filter_combos = {}
        for i, label in enumerate(filter_labels):
            ttk.Label(self.reports_frame, text=f"{label}:").grid(row=i+1, column=0, padx=5, pady=5, sticky=tk.W)
            combo = ttk.Combobox(self.reports_frame, state="readonly", width=30)
            combo.grid(row=i+1, column=1, padx=5, pady=5, sticky=tk.W)
            self.filter_combos[label.lower().replace(" ", "_")] = combo

        # View Members button
        self.view_members_btn = ttk.Button(self.reports_frame, text="View Members", command=self.view_members)
        self.view_members_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # Treeview for results
        columns = ("Name", "Role", "Status", "Gender", "Degree Program", "Batch")
        self.members_tree = ttk.Treeview(self.reports_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=150, anchor=tk.W)
        self.members_tree.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.reports_frame, orient=tk.VERTICAL, command=self.members_tree.yview)
        self.members_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=7, column=3, sticky='ns', pady=5)

        # Make the treeview expand
        self.reports_frame.rowconfigure(7, weight=1)
        self.reports_frame.columnconfigure(2, weight=1)

        # Load dropdown data
        self.load_org_for_view()
        self.load_filters()
    
    def load_org_for_view(self):
        try:
            # Assuming your DatabaseManager has this method
            orgs = self.db.execute_query("SELECT org_id, org_name FROM organization ORDER BY org_name")
            self.org_map = {org[1]: org[0] for org in orgs}  # name -> id map
            self.org_combobox['values'] = list(self.org_map.keys())
            if orgs:
                self.org_combobox.current(0)  # Select first org by default
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load organizations: {e}")

    def load_filters(self):
        # Fetch distinct values for each filter from the database
        # Use "All" as default first value to mean no filter on that field

        def fetch_distinct(column):
            query = f"SELECT DISTINCT {column} FROM membership ORDER BY {column}"
            results = self.db.execute_query(query)
            # Flatten and filter out None or empty strings, then add "All"
            values = ["All"] + sorted({row[0] for row in results if row[0]})
            return values

        self.filter_combos['status']['values'] = fetch_distinct("mem_status")
        self.filter_combos['gender']['values'] = ["All"] + sorted({row[0] for row in self.db.execute_query("SELECT DISTINCT gender FROM student WHERE gender IS NOT NULL")})
        self.filter_combos['degree_program']['values'] = ["All"] + sorted({row[0] for row in self.db.execute_query("SELECT DISTINCT degree_program FROM student WHERE degree_program IS NOT NULL")})
        self.filter_combos['batch']['values'] = fetch_distinct("batch")
        self.filter_combos['committee']['values'] = fetch_distinct("committee")

        # Set all combos to "All" by default
        for combo in self.filter_combos.values():
            combo.current(0)

    
    def view_members(self):
        org_name = self.org_combobox.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return

        org_id = self.org_map.get(org_name)
        if not org_id:
            messagebox.showerror("Error", "Selected organization not found")
            return

        # Build query with optional filters
        query = """
            SELECT 
                s.first_name, s.last_name,
                m.committee AS role,
                m.mem_status AS status,
                s.gender,
                s.degree_program,
                m.batch
            FROM membership m
            JOIN student s ON m.student_id = s.student_id
            WHERE m.org_id = ?
        """
        params = [org_id]

        # Add filters if not "All"
        filters = {
            "m.mem_status": self.filter_combos['status'].get(),
            "s.gender": self.filter_combos['gender'].get(),
            "s.degree_program": self.filter_combos['degree_program'].get(),
            "m.batch": self.filter_combos['batch'].get(),
            "m.committee": self.filter_combos['committee'].get(),
        }

        for col, val in filters.items():
            if val != "All":
                query += f" AND {col} = ?"
                params.append(val)

        query += " ORDER BY role, s.last_name, s.first_name"

        try:
            members = self.db.execute_query(query, tuple(params))

            # Clear previous rows
            for row in self.members_tree.get_children():
                self.members_tree.delete(row)

            for member in members:
                name = f"{member[0]} {member[1]}"
                role = member[2] if member[2] else "Member"
                status = member[3]
                gender = member[4]
                degree = member[5]
                batch = member[6]

                self.members_tree.insert("", "end", values=(name, role, status, gender, degree, batch))

            self.status_bar.config(text=f"Loaded {len(members)} members from {org_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {e}")


    def show_about(self):
        messagebox.showinfo("About", "Organization Management System\nVersion 1.0")
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect() 