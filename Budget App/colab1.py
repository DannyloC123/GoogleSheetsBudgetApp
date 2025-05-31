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
import matplotlib.pyplot as plt


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

# Gathers all of the expenses for the specific type of expense
def expense(type):
    return expensesCategories[expensesCategories['Category'].str.contains(type, case=False)]

# Sums the total amount spent on the expense type
def expenseSum(type):
    return expense(type)['Amount'].sum().round(2)

# List of all of the expenses
expenseTypes = ['Food', 'Subscriptions', 'Golf Round', 'Golf Practice', 'Golf Equipment', 'Gigi', 'Laundry']

# Gets the total expenses across all types
def totalExpense():
    totalExpenseSum = 0
    for expense in expenseTypes:
        val = expenseSum(expense)
        totalExpenseSum += val
    return totalExpenseSum.round(2)


# Gathers all of the data on the expenses sheet
expensesCategories = pd.DataFrame(expenses.get_all_records())


# Using matplotlib, create pie chart
# Categories
labels = 'Food', 'Subsrciptions', 'Golf Rounds', 'Golf Practice', 'Golf Equipment', 'Gigi', 'Laundry'
# Amount spent
sizes = [expenseSum('Food'), expenseSum('Subscriptions'), expenseSum('Golf Rounds'), expenseSum('Golf Practice'), expenseSum('Golf Equipment'), expenseSum('Gigi'), expenseSum('Laundry')]

# Using a dictionary, every category is given a total amount spent
dictionary = {'sizes':sizes, 'labels':labels}
pieChart = pd.DataFrame(dictionary)

# Displays the pie chart
plt.pie(x=pieChart.sizes)
# Dispays the pie chart legend
plt.legend(labels=pieChart.labels, loc=[0.95,0.35])

# Saves the image as png, in a specific folder to be accessed later by html file
image_path = os.path.join('static', 'images', 'pie_chart.png')
plt.savefig(image_path, transparent=True)
plt.close



# Website Pages
app = Flask(__name__)

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Income Page
@app.route("/income")
def income():
    return render_template("income.html")

# Expenses Page
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

# Runs the website
if __name__ == "__main__":
    app.run(debug=True)
