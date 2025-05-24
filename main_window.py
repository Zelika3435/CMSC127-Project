import tkinter as tk
from tkinter import ttk, messagebox
from gui_components import DataTable, FormDialog
from database import DatabaseManager
from datetime import datetime

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Organization Management System")
        self.geometry("1200x800")
        
        # Initialize database
        self.db = DatabaseManager()
        if not self.db.connect():
            messagebox.showerror("Error", "Could not connect to database")
            self.destroy()
            return
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_membership_tab()
        self.create_financial_tab()
        self.create_reports_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.destroy)
        
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
        
        # Fee list
        columns = ['Student ID', 'Name', 'Fee Amount', 'Amount Paid', 'Balance', 'Due Date']
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
        
        # Left panel for report selection
        left_panel = ttk.Frame(reports_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Report buttons
        ttk.Button(left_panel, text="Membership Status", command=self.show_membership_status).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Executive Committee", command=self.show_executive_committee).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Role History", command=self.show_role_history).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Alumni List", command=self.show_alumni).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Financial Summary", command=self.show_financial_summary).pack(fill=tk.X, pady=2)
        
        # Right panel for report display
        right_panel = ttk.Frame(reports_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Report display area
        self.report_table = DataTable(right_panel, ['No Data'])
        self.report_table.pack(fill=tk.BOTH, expand=True)
    
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
        org_name = self.org_combo.get()
        if not org_name:
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        members = self.db.get_members_by_organization(org_id)
        self.member_table.insert_data(members)
    
    def load_financial_data(self):
        org_name = self.fin_org_combo.get()
        semester = self.semester_combo.get()
        acad_year = self.acad_year_combo.get()
        
        if not all([org_name, semester, acad_year]):
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        members = self.db.get_members_with_unpaid_fees(org_id, semester, acad_year)
        self.fee_table.insert_data(members)
    
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
                
                messagebox.showinfo("Success", "Member added successfully")
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
    
    def show_membership_status(self):
        org_name = self.org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        status = self.db.get_membership_status_percentage(org_id, 2)  # Last 2 semesters
        self.report_table.insert_data([status])
    
    def show_executive_committee(self):
        org_name = self.org_combo.get()
        if not org_name:
            messagebox.showwarning("Warning", "Please select an organization")
            return
        
        orgs = self.db.get_all_organizations()
        org_id = next(org.org_id for org in orgs if org.org_name == org_name)
        
        committee = self.db.get_executive_committee(org_id, self.acad_year_combo.get())
        self.report_table.insert_data(committee)
    
    def show_role_history(self):
        org_name = self.org_combo.get()
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
            self.report_table.insert_data(history)
    
    def show_alumni(self):
        org_name = self.org_combo.get()
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
            self.report_table.insert_data(alumni)
    
    def show_financial_summary(self):
        org_name = self.org_combo.get()
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
            self.report_table.insert_data([summary])
    
    def show_about(self):
        messagebox.showinfo("About", "Organization Management System\nVersion 1.0")
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop() 