import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageDraw
import os
import win32print  # For printer functions
import win32api
from wrestling_matchup.matchups import fixed_weight_classes_matchup, maddison_system_matchup
import pandas as pd
from wrestling_matchup.data_handler import export_to_excel, import_data  # Ensure import_data is included

class WrestlingMatchUpApp:
    def __init__(self, master):
        self.master = master
        master.title("Wrestling Match-Up Program")
        master.geometry("900x600")
        master.config(bg="#2c3e50")
    
        self.home_wrestlers_data = None
        self.away_wrestlers_data = None
        self.matchups = []
        self.exported_file_path = None

        # Centered Title Frame with Logo
        title_frame = tk.Frame(master, bg="#2c3e50")
        title_frame.pack(pady=10)

        # Load and resize the logo image
        self.logo_image = Image.open("logo.png").resize((70, 70), Image.LANCZOS)
        self.logo_image = self.make_circle(self.logo_image)
        self.logo = ImageTk.PhotoImage(self.logo_image)

        # Logo label
        logo_label = tk.Label(title_frame, image=self.logo, bg="#2c3e50")
        logo_label.pack(side=tk.LEFT, padx=(0, 10))

        # Title label
        title = tk.Label(title_frame, text="Wrestling Match-Up Program", font=("Arial", 24, "bold"), fg="#ecf0f1", bg="#2c3e50")
        title.pack(side=tk.LEFT)

        # Sidebar for Notes
        sidebar_frame = tk.Frame(master, bg="#2c3e50", width=200, bd=4, relief=tk.RIDGE)
        sidebar_frame.pack(side=tk.LEFT, fill="y", padx=5, pady=20)

        tk.Label(sidebar_frame, text="Notes", font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=5)
        self.note_entry = tk.Entry(sidebar_frame, font=("Arial", 12))
        self.note_entry.pack(pady=5, padx=10, fill="x")
        tk.Button(sidebar_frame, text="Add Note", command=self.add_note, bg="#2980b9", fg="white").pack(pady=5)

        # Notes display area
        self.note_listbox = tk.Listbox(sidebar_frame, font=("Arial", 12), bg="#34495e", fg="white")
        self.note_listbox.pack(pady=5, padx=10, fill="both", expand=True)

        # Clear Notes Button
        tk.Button(sidebar_frame, text="Clear Notes", command=self.clear_notes, bg="#c0392b", fg="white").pack(pady=(5, 10))

        # Main Content Frame
        content_frame = tk.Frame(master, bg="#34495e", bd=2, relief=tk.RAISED)
        content_frame.pack(side=tk.LEFT, padx=(5, 40), pady=20, fill="both", expand=True)

        # Import Frame
        import_frame = self.create_section(content_frame, "Data Import")
        self.import_home_button = self.create_hover_button(import_frame, "Import Home Wrestlers", self.import_home_data)
        self.import_away_button = self.create_hover_button(import_frame, "Import Away Wrestlers", self.import_away_data)

        # Match-Up Frame
        matchup_frame = self.create_section(content_frame, "Create Match-Ups")
        self.create_fixed_button = self.create_hover_button(matchup_frame, "Fixed Weight Classes", self.create_fixed_matchups)
        self.create_maddison_button = self.create_hover_button(matchup_frame, "Maddison System", self.create_maddison_matchups)

        # Export Frame
        export_frame = self.create_section(content_frame, "Export Data")
        self.export_button = self.create_hover_button(export_frame, "Export to Excel", self.export_matchups)
        self.show_exported_button = self.create_hover_button(export_frame, "Show Exported File", self.show_exported_file)
        self.print_button = self.create_hover_button(export_frame, "Print Exported File", self.print_exported_file)

        
        # Add Print Button in Export Frame
        # self.print_button = self.create_hover_button(export_frame, "Print Exported File", self.print_file)
        
        # Status Label
        self.status_label = tk.Label(master, text="", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.status_label.pack(pady=20)
        
        # Quit Button
        self.quit_button = self.create_hover_button(content_frame, "Quit", master.quit, bg="#c0392b")
        self.quit_button.pack(pady=(10, 0), ipadx=10, ipady=5)

        self.home_file_name = None  # To store the name of the home file
        self.away_file_name = None  # To store the name of the away file


    def create_section(self, parent, title):
        frame = tk.Frame(parent, bg="#2c3e50", bd=4, relief=tk.RIDGE)
        frame.pack(pady=10, fill="x")
        tk.Label(frame, text=title, font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=10)
        return frame

    def create_hover_button(self, parent, text, command, bg="#2980b9", fg="white"):
        button = tk.Button(parent, text=text, command=command, font=("Arial", 12), bg=bg, fg=fg, width=20)
        button.pack(pady=10, ipadx=10, ipady=5)

        # Bind hover events
        button.bind("<Enter>", lambda e: button.config(bg="#1abc9c"))
        button.bind("<Leave>", lambda e: button.config(bg=bg))

        return button

    def make_circle(self, image):
        width, height = image.size
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)

        circular_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        circular_image.paste(image.convert("RGBA"), (0, 0), mask)
        return circular_image
    


    def add_note(self):
        note = self.note_entry.get()
        if note:
            self.note_listbox.insert(tk.END, note)
            self.note_entry.delete(0, tk.END)

    def clear_notes(self):
        self.note_listbox.delete(0, tk.END)

    def import_home_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
        if file_path:
            new_file_name = os.path.basename(file_path)
            if new_file_name == self.away_file_name:
                messagebox.showerror("Error", "Cannot import. The home file name cannot be the same as the away file name.")
                return
            
            self.home_wrestlers_data = import_data(file_path)
            if self.home_wrestlers_data is not None:
                self.home_file_name = new_file_name
                self.status_label.config(text="Home wrestlers data imported successfully!")
                messagebox.showinfo("Success", "Home wrestlers data imported successfully!")
            else:
                self.status_label.config(text="Failed to import home wrestlers data.")
                messagebox.showerror("Error", "Failed to import home wrestlers data.")

    def import_away_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
        if file_path:
            new_file_name = os.path.basename(file_path)
            if new_file_name == self.home_file_name:
                messagebox.showerror("Error", "Cannot import. The away file name cannot be the same as the home file name.")
                return
            
            self.away_wrestlers_data = import_data(file_path)
            if self.away_wrestlers_data is not None:
                self.away_file_name = new_file_name
                self.status_label.config(text="Away wrestlers data imported successfully!")
                messagebox.showinfo("Success", "Away wrestlers data imported successfully!")
            else:
                self.status_label.config(text="Failed to import away wrestlers data.")
                messagebox.showerror("Error", "Failed to import away wrestlers data.")

    def create_fixed_matchups(self):
        if self.home_wrestlers_data is not None and self.away_wrestlers_data is not None:
            weight_classes = [0, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
            self.matchups = fixed_weight_classes_matchup(self.home_wrestlers_data, self.away_wrestlers_data, weight_classes)
            self.status_label.config(text="Created mixed match-ups.")
            messagebox.showinfo("Match-Ups Created", "Mixed match-ups created.")
        else:
            messagebox.showerror("Error", "Please import data for both home and away wrestlers.")

    def create_maddison_matchups(self):
        if self.home_wrestlers_data is not None and self.away_wrestlers_data is not None:
            self.matchups = maddison_system_matchup(self.home_wrestlers_data, self.away_wrestlers_data)
            self.status_label.config(text="Created Maddison match-ups.")
            messagebox.showinfo("Match-Ups Created", "Maddison match-ups created.")
        else:
            messagebox.showerror("Error", "Please import data for both home and away wrestlers.")

    def export_matchups(self):
        if self.matchups:
            self.exported_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
            if self.exported_file_path:
                export_to_excel(self.matchups, self.exported_file_path)  # Use correct args
                self.status_label.config(text="Match-ups exported successfully!")
                messagebox.showinfo("Exported", "Match-ups exported to Excel.")
            else:
                messagebox.showerror("Error", "No file selected for export.")
        else:
            messagebox.showerror("Error", "No match-ups to export. Please create match-ups first.")


    def show_exported_file(self):
        if self.exported_file_path and os.path.exists(self.exported_file_path):
            os.startfile(self.exported_file_path)
        else:
            messagebox.showerror("Error", "No exported file found. Please export match-ups first.")

    def print_exported_file(self):
        if self.exported_file_path and os.path.exists(self.exported_file_path):
            try:
                win32api.ShellExecute(0, "print", self.exported_file_path, None, ".", 0)
                messagebox.showinfo("Print", "Print dialog opened. Please select a printer or save as PDF.")
            except Exception as e:
                messagebox.showerror("Print Error", f"An error occurred while opening the print dialog: {e}")
        else:
            messagebox.showerror("Print Error", "No exported file found. Please export match-ups first.")



if __name__ == "__main__":
    root = tk.Tk()
    app = WrestlingMatchUpApp(root)
    root.mainloop()
