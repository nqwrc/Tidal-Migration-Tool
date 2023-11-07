import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

class TidalMigratorGUI:
    """GUI for the TidalMigrator application."""

    def __init__(self, migrator):
        self.migrator = migrator
        self.root = tk.Tk()
        self.root.title("Tidal Favorites Migrator")

        self.status_label = tk.Label(self.root, text="Not logged in", fg='red')
        self.status_label.pack()

        self.login_button = tk.Button(self.root, text="Log In", command=self.on_login_button_click)
        self.login_button.pack()

        self.save_button = tk.Button(self.root, text="Save Favorites to CSV", command=self.on_save_button_click)
        self.save_button.pack()

        self.add_button = tk.Button(self.root, text="Add Favorites from CSV", command=self.on_add_button_click)
        self.add_button.pack()

    def copy_link(self):
        """Copy the login URL to the clipboard and update the login status."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.migrator.url_main)
        self.check_login_status()

    def on_login_button_click(self):
        """Handle the login button click event."""
        messagebox.showinfo("Login", "A new link has been copied to your clipboard. Open it in your browser.")
        self.copy_link()

    def check_login_status(self):
        """Check the login status and update the status label accordingly."""
        if self.migrator.check_login():
            self.status_label.config(text="Logged in successfully", fg='green')
            self.login_button.config(text=self.migrator.session.user.email)
        else:
            self.root.after(1000, self.check_login_status)

    def on_save_button_click(self):
        """Handle the save button click event."""
        if not self.migrator.check_login():
            messagebox.showwarning("Not Logged In", "Please log in to Tidal first.")
            return
        self.migrator.save_favorites()
        messagebox.showinfo("Success", "Favorites saved in CSV format.")

    def on_add_button_click(self):
        """Handle the add button click event."""
        if not self.migrator.check_login():
            messagebox.showwarning("Not Logged In", "Please log in to Tidal first.")
            return
        filepaths = [Path(file) for file in filedialog.askopenfilenames(title="Select CSV files with favorites")]
        errors = self.migrator.add_favorites(filepaths)
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
        else:
            messagebox.showinfo("Success", "Favorites added successfully.")

    def run(self):
        """Run the Tkinter event loop."""
        self.root.mainloop()
        
if __name__ == '__main__':
    migrator = TidalMigrator()
    app = TidalMigratorGUI(migrator)
    app.run()
