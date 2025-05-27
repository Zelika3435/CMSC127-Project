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

def setup_database():
    """Set up the database if it doesn't exist"""
    try:
        if create_database_schema():
            print("Database setup completed successfully!")
            return True
        else:
            messagebox.showerror("Database Error", "Failed to set up database!")
            return False
    except Exception as e:
        messagebox.showerror("Database Error", f"Error setting up database: {str(e)}")
        return False

def main():
    # Create root window
    root = tk.Tk()

    # Create and run the application
    try:
        app = MainWindow(root)  
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Application Error", f"An error occurred: {e}")
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()
