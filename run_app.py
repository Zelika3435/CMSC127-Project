import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main_window import MainWindow
    from database import DatabaseManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required files are in the same directory")
    sys.exit(1)

def main():
    """Main application entry point"""
    
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