# Standard Library Imports
import os
from pathlib import Path
import sqlite3
from sqlite3 import OperationalError

# Third Party Imports
from openpyxl import Workbook
from openpyxl.styles import Font
import platformdirs
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

# Local Application Imports
from util import resource_path


class Manager:
    def __init__(self):
        # Style Stuff
        self.font = "Suse Mono"
        self.title_size = 45
        self.prompt_size = 20
        self.button_size = 15
        self.prompt_width = 20
        self.entry_width = 20
        self.bg_color = "red"

        # Creating/Setting Up GUI Window
        self.root = tk.Tk()
        self.root.title("Login Manager")
        self.root.minsize(width=600, height=200)
        self.root.config(bg=self.bg_color)
        self.root.bind("<Destroy>", self.delete_file)

        # Converting the lock icon for Tkinter use
        lock_icon_image = Image.open(resource_path("assets/lock_icon.png"))
        lock_icon_image_resized = lock_icon_image.resize((90, 90))
        ##PhotoImage is finicky when not assigned to a global or instance variable
        self.lock_icon = ImageTk.PhotoImage(lock_icon_image_resized)

        ##Creating the canvas to hold the lock icon
        self.canvas = tk.Canvas(self.root, width=100, height=100, bg=self.bg_color, highlightbackground=self.bg_color)
        self.canvas.create_image(50, 50, image=self.lock_icon)
        self.canvas.grid(row=1, column=0, columnspan=2)

        # Creating/Setting Up Prompts
        self.prompt_frame = tk.Frame(self.root, bg=self.bg_color)
        self.prompt_frame.grid(row=2, column=0, columnspan=2)
        self.setup_labels() # Creating/Setting Up Prompt Labels

        # Creating/Setting Up Prompt entries
        self.website_entry = tk.Entry(self.prompt_frame, width=self.entry_width, font=(self.font, self.prompt_size),
                                 highlightbackground=self.bg_color)
        self.website_entry.grid(row=0, column=1)
        self.username_entry = tk.Entry(self.prompt_frame, width=self.entry_width, font=(self.font, self.prompt_size),
                                  highlightbackground=self.bg_color)
        self.username_entry.grid(row=1, column=1)
        self.password_entry = tk.Entry(self.prompt_frame, width=self.entry_width, font=(self.font, self.prompt_size),
                                       highlightbackground=self.bg_color)
        self.password_entry.grid(row=2, column=1)

        self.setup_buttons() # Creating/Setting Up GUI Buttons

        # Get the path of the login file destination
        self.db_name = "login_info"
        desktop_path = platformdirs.user_desktop_path()
        self.file_name = f"{self.db_name}.xlsx"
        self.file_path = Path(desktop_path) / self.file_name

        # Setting Up SQL Database
        # Connect to login info database and allow automatic commits (no manual con.commit())
        self.con = sqlite3.connect(resource_path(f"{self.db_name}.db"), autocommit=True)
        # Create Cursor object to execute commands to alter database and fetch data from it
        self.cur = self.con.cursor()
        # Databases cannot be created again once they are created
        try:
            # Create new data table for login info
            self.cur.execute(f"CREATE TABLE {self.db_name}(website, username, password)")
        except OperationalError:
            # Nothing will happen if we try to create the existing database again
            pass

        # Create the login file
        self.get_info()


    def setup_labels(self):
        """
        Sets up the labels used in the program
        """
        # Creating/Setting Up Title
        title = tk.Label(self.root, text="Login Manager", font=(self.font, self.title_size, "bold"),
                              fg="white", bg=self.bg_color, width=20)
        title.grid(row=0, column=0, columnspan=2)

        # Creating/Setting Up Prompt Labels
        website_label = tk.Label(self.prompt_frame, text="Enter Website/Application: ", justify="left", anchor="w",
                                       font=(self.font, self.prompt_size), fg="white", bg=self.bg_color, )
        website_label.grid(row=0, column=0)
        username_label= tk.Label(self.prompt_frame, text="Enter Username/Email: ", justify="left", anchor="w",
                                        font=(self.font, self.prompt_size), fg="white", bg=self.bg_color)
        username_label.grid(row=1, column=0)
        password_label = tk.Label(self.prompt_frame, text="Enter Password: ", justify="left", anchor="w",
                                        font=(self.font, self.prompt_size), fg="white", bg=self.bg_color)
        password_label.grid(row=2, column=0)


    def setup_buttons(self):
        """
        Sets up the buttons used in the program
        """
        # Creating/Setting Up Buttons
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.grid(row=5, column=0, columnspan=2)

        # Button for Inserting/Recording New Login Information
        record_info_button = tk.Button(button_frame, width=20, text="Record Login Info", justify="center",
                                       font=(self.font, self.button_size), highlightbackground=self.bg_color,
                                       command=self.record_info)
        record_info_button.grid(row=5, column=0)

        # Button for Opening the Login File
        open_file_button = tk.Button(button_frame, width=20, text="Open Login File", justify="center",
                                    font=(self.font, self.button_size), highlightbackground=self.bg_color,
                                    command=self.open_file)
        open_file_button.grid(row=6, column=0)

        # Button for Deleting Login Info Database
        delete_db_button = tk.Button(button_frame, width=20, text="Delete ALL Login Info", justify="center",
                                     font=(self.font, self.button_size), highlightbackground=self.bg_color,
                                     command=self.delete_database)
        delete_db_button.grid(row=7, column=0)


    def record_info(self):
        """
        Record a website's login info to the specified SQL database
        """
        # Prevent blank entries from being entered
        if self.website_entry.get() != "" and self.username_entry.get() != "" and self.password_entry.get() != "":
            # Prevent entries with only spaces from being entered
            if not self.website_entry.get().isspace() and not self.username_entry.get().isspace() and not self.password_entry.get().isspace():
                # Get all the info from the database
                self.cur.execute(f"SELECT * FROM {self.db_name}")
                all_info = self.cur.fetchall()
                if len(all_info) > 0:
                    # Search entire database for website name
                    for i in range(0, len(all_info)):
                        # If the website name is already in database
                        if all_info[i][0] == self.website_entry.get():
                            # Update the login info entry in the database
                            self.update_info()
                            break
                        elif i == len(all_info) - 1:
                            # Insert the login info entry into the database
                            self.insert_info()
                else:
                    # Insert the login info entry into the database
                    self.insert_info()

                # Clear text entries
                self.clear_entries()
                # Update the login file
                self.get_info()


    def insert_info(self):
        """
        Insert a website's login info into the specified SQL database
        """
        # Insert the login info entry into the database
        insert_info = (self.website_entry.get(), self.username_entry.get(), self.password_entry.get())
        command = f"INSERT INTO {self.db_name}(website, username, password) VALUES (?, ?, ?)"
        self.cur.execute(command, insert_info)

        # Update the login file
        self.get_info()


    def update_info(self):
        """
        Update the login info to a website already in the specified SQL database
        """
        update_info = (self.username_entry.get(), self.password_entry.get(), self.website_entry.get())
        command = f"UPDATE {self.db_name} SET username = ?, password = ? WHERE website = ?"
        self.cur.execute(command, update_info)

        # Update the login file
        self.get_info()


    def get_info(self):
        """
        Outputs the login info to all websites in the database
        """
        # Get all the info from the database
        self.cur.execute(f"SELECT * FROM {self.db_name}")
        all_info = self.cur.fetchall()

        # Open up a Worksheet from a Workbook to start adding stuff to Excel file
        workbook = Workbook()
        worksheet = workbook.active
        bold_font = Font(bold=True) # Column titles should be bold

        # Adding in column titles
        worksheet["A1"], worksheet["B1"], worksheet["C1"] = "Website", "Username", "Password"
        worksheet["A1"].font, worksheet["B1"].font , worksheet["C1"].font = bold_font, bold_font, bold_font

        # Adding in column values (website login info)
        for info in all_info:
            website_login_info = [info[0], info[1], info[2]]
            worksheet.append(website_login_info)

        # Save changes made to the file
        workbook.save(self.file_path)


    def clear_entries(self):
        """
        Clears the text entries by deleting all text within
        """
        self.website_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


    def open_file(self):
        """
        Opens the login file
        """
        os.system(f"open {self.file_path}")


    def delete_database(self):
        """
        Deletes login info database and the info it holds
        """
        # Prompt user by asking if they are sure they want to delete file (prevents accidental data deletion)
        if messagebox.askokcancel(message="Delete ALL Login Info?"):
            # In cases where there is no info inside the database (or database file doesn't exist yet)
            try:
                # Delete the rows inside the table
                self.cur.execute(f"DELETE FROM {self.db_name}")
            except OperationalError:
                pass

            # Update the login file
            self.get_info()


    def delete_file(self, event):
        """
        Deletes login info file (NOT DATABASE)
        """
        # Prevent this code from running when deleting every widget from root window
        if event.widget == self.root:
            # In cases where the Excel file is not created yet
            try:
                os.remove(self.file_path)
            except FileNotFoundError:
                pass



