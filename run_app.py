import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main_window import MainWindow
    from setup_database import create_database_schema
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required files are in the same directory")
    sys.exit(1)

def main():
    """Main application entry point"""
    
    # Create root window (hidden initially)
    root = tk.Tk()
    root.withdraw()
    
    # Ask user if they want to set up database first
    setup_db = messagebox.askyesno(
        "Database Setup", 
        "Do you want to set up the database schema first?\n\n"
        "Choose 'Yes' if this is your first time running the application.\n"
        "Choose 'No' if the database is already set up."
    )
    
    if setup_db:
        print("Setting up database...")
        if create_database_schema():
            messagebox.showinfo("Success", "Database setup completed successfully!")
        else:
            messagebox.showerror("Error", "Database setup failed! Check your database connection.")
            root.destroy()
            return
    
    # Show the main window
    root.deiconify()
    
    # Create and run the application
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Application Error", f"An error occurred: {e}")
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()