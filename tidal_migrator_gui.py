import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
from tidal_migrator import TidalMigrator

class TidalMigratorGUI:
    """GUI for the TidalMigrator application."""

    def __init__(self, migrator):
        self.migrator = migrator
        self.root = tk.Tk()
        self.root.title("Tidal Mig")
    
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(padx=10, pady=10)

        self.status_label = tk.Label(main_frame, text="Not logged in", fg='red')
        self.status_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.login_button = tk.Button(main_frame, text="Log In", command=self.on_login_button_click)
        self.login_button.grid(row=1, column=0, sticky="ew", padx=5)

        self.save_button = tk.Button(main_frame, text="Save Favorites to CSV", command=self.on_save_button_click)
        self.save_button.grid(row=1, column=1, sticky="ew", padx=5)

        self.add_button = tk.Button(main_frame, text="Upload CSV to Tidal", command=self.on_add_button_click)
        self.add_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 10))

        favorites_frame = tk.LabelFrame(main_frame, text="Favorites Count", padx=10, pady=10)
        favorites_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.favorite_labels = {
            "tracks": tk.Label(favorites_frame, text="Tracks: 0"),
            "albums": tk.Label(favorites_frame, text="Albums: 0"),
            "artists": tk.Label(favorites_frame, text="Artists: 0"),
            "playlists": tk.Label(favorites_frame, text="Playlists: 0"),
            "videos": tk.Label(favorites_frame, text="Videos: 0"),
        }

        for i, label in enumerate(self.favorite_labels.values()):
            label.grid(row=i, column=0, sticky="w")
        
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
            # Update favorites count
            self.update_favorites_count()
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

    def update_favorites_count(self):
        """Update the count of favorites for each type."""
        if self.migrator.check_login():
            for favorite_type, label in self.favorite_labels.items():
                count = self.migrator.count_favorites(favorite_type)
                label.config(text=f"{favorite_type.capitalize()}: {count}")
            
    def run(self):
        """Run the Tkinter event loop."""
        self.root.mainloop()
        
if __name__ == '__main__':
    migrator = TidalMigrator()
    app = TidalMigratorGUI(migrator)
    app.run()
