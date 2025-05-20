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
from flask import Flask, render_template


# API Access

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


def expense(type):
    return expensesCategories[expensesCategories['Category'].str.contains(type, case=False)]

def expenseSum(type):
    return expense(type)['Amount'].sum().round(2)

expenseTypes = ['Food', 'Subscriptions', 'Golf Round', 'Golf Practice', 'Golf Equipment', 'Gigi', 'Laundry']

def totalExpense():
    totalExpenseSum = 0
    for expense in expenseTypes:
        val = expenseSum(expense)
        totalExpenseSum += val
    return totalExpenseSum.round(2)


# Gathers all of the data on the expenses sheet
expensesCategories = pd.DataFrame(expenses.get_all_records())



# Website Pages

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/income")
def income():
    return render_template("income.html")

@app.route("/expenses")
def expenses():
    return render_template(
        "expenses.html",
        total_expenses = totalExpense(),
        foodTotal = expenseSum('Food'),
        subTotal = expenseSum('Subscription'),
        golfRTotal = expenseSum('Golf Round'),
        golfPTotal = expenseSum('Golf Practice'),
        golfETotal = expenseSum('Golf Equipment'),
        gigiTotal = expenseSum('Gigi'),
        laundryTotal = expenseSum('Laundry'))

if __name__ == "__main__":
    app.run(debug=True)
