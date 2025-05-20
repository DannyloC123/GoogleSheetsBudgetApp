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



# Gathers all of the data on the expenses sheet
expensesCategories = pd.DataFrame(expenses.get_all_records())



# filters the data so that it only gets the expenses under the Food category
filteredExpensesFood = expensesCategories[expensesCategories['Category'].str.contains('Food', case=False)]

# filters the data so that it only gets the expenses under the Subscription category
filteredExpensesSubs = expensesCategories[expensesCategories['Category'].str.contains('Subscription', case=False)]

# filters the data so that it only gets the expenses under the Golf Round category
filteredExpensesGolfR = expensesCategories[expensesCategories['Category'].str.contains('Golf Round', case=False)]

# filters the data so that it only gets the expenses under the Golf Practice category
filteredExpensesGolfP = expensesCategories[expensesCategories['Category'].str.contains('Golf Practice', case=False)]

# filters the data so that it only gets the expenses under the Golf Equipment category
filteredExpensesGolfE = expensesCategories[expensesCategories['Category'].str.contains('Golf Equipment', case=False)]

# filters the data so that it only gets the expenses under the Gigi category
filteredExpensesGigi = expensesCategories[expensesCategories['Category'].str.contains('Gigi', case=False)]

# filters the data so that it only gets the expenses under the Laundry category
filteredExpensesLaundry = expensesCategories[expensesCategories['Category'].str.contains('Laundry', case=False)]


# Adds the total amount of money spent in each category
foodSum = filteredExpensesFood['Amount'].sum()
subsSum = filteredExpensesSubs['Amount'].sum().round(2)
golfRSum = filteredExpensesGolfR['Amount'].sum()
golfPSum = filteredExpensesGolfP['Amount'].sum()
golfESum = filteredExpensesGolfE['Amount'].sum()
gigiSum = filteredExpensesGigi['Amount'].sum()
laundrySum = filteredExpensesLaundry['Amount'].sum()
totalExpenses = (foodSum + subsSum + golfRSum + golfPSum + golfESum + gigiSum + laundrySum).round(2)


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
        total_expenses = totalExpenses,
        foodTotal = foodSum,
        subTotal = subsSum,
        golfRTotal = golfRSum,
        golfPTotal = golfPSum,
        golfETotal = golfESum,
        gigiTotal = gigiSum,
        laundryTotal = laundrySum)

if __name__ == "__main__":
    app.run(debug=True)
