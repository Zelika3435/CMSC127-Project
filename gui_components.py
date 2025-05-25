import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable

class DataTable(ttk.Frame):
    # --- Reusable data table component ---
    
    def __init__(self, parent, columns: List[str], **kwargs):
        super().__init__(parent, **kwargs)
        
        # Create treeview with scrollbars
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=100)
        
        # Store the complete data for each row
        self.row_data = {}
    
    def clear(self):
        # --- Clear all items from the table ---
        print("Clearing table items")  # Debug print
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.row_data.clear()
        self.update_idletasks()
    
    def insert_data(self, data: List[dict]):
        # --- Insert data into the table ---
        print(f"Inserting data into table: {data}")  # Debug print
        self.clear()
        
        if not data:
            print("No data to insert")  # Debug print
            return
            
        for row_data in data:
            values = []
            for col in self.tree['columns']:
                value = str(row_data.get(col, ''))
                values.append(value)
            print(f"Inserting row with values: {values}")  # Debug print
            item_id = self.tree.insert('', tk.END, values=values)
            # Store the complete data dictionary for this row
            self.row_data[item_id] = row_data
        
        self.update_idletasks()
        print("Data insertion complete")  # Debug print
    
    def get_selected_item(self) -> dict:
        # --- Get the currently selected item as a dictionary ---
        selection = self.tree.selection()
        if selection:
            item_id = selection[0]
            # Return the complete data dictionary for the selected row
            return self.row_data.get(item_id, {})
        return {}

class FormDialog(tk.Toplevel):
    # --- Base class for form dialogs ---
    
    def __init__(self, parent, title: str, fields: List[dict]):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self.fields = fields
        self.entries = {}
        
        self.create_form()
        self.create_buttons()
        
        # Center the dialog
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Focus on first entry
        if self.entries:
            first_entry = list(self.entries.values())[0]
            first_entry.focus_set()
    
    def create_form(self):
        # --- Create form fields ---
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        for i, field in enumerate(self.fields):
            label = ttk.Label(form_frame, text=field['label'])
            label.grid(row=i, column=0, sticky='w', pady=5)
            
            if field['type'] == 'entry':
                entry = ttk.Entry(form_frame, width=30)
                if 'default' in field:
                    entry.insert(0, field['default'])
            elif field['type'] == 'combobox':
                entry = ttk.Combobox(form_frame, values=field['values'], width=27)
                if 'default' in field:
                    entry.set(field['default'])
            elif field['type'] == 'text':
                entry = tk.Text(form_frame, width=30, height=3)
                if 'default' in field:
                    entry.insert('1.0', field['default'])
            
            entry.grid(row=i, column=1, pady=5, padx=(10, 0))
            self.entries[field['name']] = entry
    
    def create_buttons(self):
        # --- Create OK and Cancel buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
    
    def ok_clicked(self):
        # --- Handle OK button click ---
        self.result = {}
        for name, entry in self.entries.items():
            if isinstance(entry, tk.Text):
                self.result[name] = entry.get('1.0', tk.END).strip()
            else:
                self.result[name] = entry.get()
        self.destroy()
    
    def cancel_clicked(self):
        # --- Handle Cancel button click ---
        self.result = None
        self.destroy()