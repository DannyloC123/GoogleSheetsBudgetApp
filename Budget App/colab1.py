# Instructions for How to Code with GitHub

# git pull
# (Edit the code)
# (Save the code)
# git status
# git add colab1.py
# git commit -m "Describe what you did here"
# git push

#%% Import Google Sheets API & Load Data
import os
print("Current working directory:", os.getcwd())
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Step 1: Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Step 2: Load the credentials from the file
# Get absolute path to credentials file, based on this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "budget-app-459803-c519ac2d00c1.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)

# Step 3: Authorize the client
client = gspread.authorize(creds)

# Step 4: Open the Google Sheet by name
spreadsheet = client.open("Golf Tracker")

# Step 5: Access worksheets by name
loops = spreadsheet.worksheet("Loops")
expenses = spreadsheet.worksheet("Expenses")
bagroom = spreadsheet.worksheet("Bagroom")

# Step 6: Fetch the data
loopsDataFrame = pd.DataFrame(loops.get_all_records())
expensesDataFrame = pd.DataFrame(expenses.get_all_records())
bagroomDataFrame = pd.DataFrame(bagroom.get_all_records())

# Step 7: Print the data
print(loopsDataFrame)
print(expensesDataFrame)
print(bagroomDataFrame)

# Something
