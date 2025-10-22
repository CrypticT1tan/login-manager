# LOGIN MANAGER
A Python program using SQL to keep a database of a user's login information for various websites.  
Users can input their login information into the database or retrieve it from the database in the form of an Excel file.  
The program will save the login information and automatically delete the Excel file when the program closes while remembering the login information within. 

## INSTALLATION
Use package manager pip to install the following:

```bash
pip install openpyxl
pip install pillow
pip install platformdirs
pip install pyinstaller
```

## Usage
To build the executable file, use the terminal to go into the same directory as the main.py file and run the command below:

```bash
pyinstaller main.py --hidden-import=tkinter --onefile --windowed --add-data "../assets:assets" --icon=../assets/lock_icon.icns --name "<Desired Name of Executable>"
```

Open up the dist file to find an executable file with your desired name, and open it.

On program start, a file named "login_info.xlsx" will be on your Desktop.  

Enter text into the Website, Username, and Password entry fields.  

Press the "Record Login Info" button to record the info into the database and the file.  

Press the "Open Login File" button to open up the "login_info.xlsx" file and see the information in tabular format.  

Press the "Delete ALL Login Info" button to delete all login information off the database.  
(WARNING: All login information stored in the database will be deleted, your login info will be LOST FOREVER!)  
You will be prompted to click "Ok" or "Cancel" to prevent accidental data deletion.  

When you quit the program, the "login_info.xlsx" file is automatically deleted (but your info isn't!).  

## Contact
For any questions, contact me at gavinkiosco@gmail.com or CrypticT1tan on GitHub.