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

from matplotlib.dates import MONTHLY
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
expensesCategories = pd.DataFrame(expenses.get_all_records())
bagroomDataFrame = pd.DataFrame(bagroom.get_all_records())

# Function for organizing the months
def monthNumbers(month:str):
    months = {
        'january': '-01-',
        'february': '-02-',
        'march': '-03-',
        'april': '-04-',
        'may': '-05-',
        'june': '-06-',
        'july': '-07-',
        'august': '-08-',
        'september': '-09-',
        'october': '-10-',
        'november': '-11-',
        'december': '-12-',
    }
    return months.get(month.lower(), '')

# Gathers all of the expenses for the specific type of expense
def expense(type):
    return expensesCategories[expensesCategories['Category'].str.contains(type, case=False)]

# Sums the total amount spent on the expense type
def expenseSum(type):
    return round(expense(type)['Amount'].sum(), 2)

# List of all of the expenses
expenseTypes = ['Food', 'Subscriptions', 'Golf Round', 'Golf Practice', 'Golf Equipment', 'Gigi', 'Laundry', 'Education', 'Bills', 'Car']

# Gets the total expenses across all types
def totalExpense():
    totalExpenseSum = 0
    for expense in expenseTypes:
        val = expenseSum(expense)
        totalExpenseSum += val
    return round(totalExpenseSum, 2)


# Gets all the income in the month chosen
def monthlyLoopIncome(month):
    monthNum = monthNumbers(month)
    return loopsDataFrame[loopsDataFrame['Date'].str.contains(monthNum, case=False)]

# Gets all the income from the person chosen
def personIncome(person):
    return loopsDataFrame[loopsDataFrame['Client Name/Golfer'].str.contains(person, case=False)]

# Gets the total sum of income in a month
def totalMonthlyLoopIncome(month):
    return round(monthlyLoopIncome(month)['Money Earned'].sum(), 2)

# Gets the total sum of income from a person
def totalPersonIncome(person):
    return round(personIncome(person)['Money Earned'].sum(), 2)

# Gets the total life time amount of income earned
def incomeLoops():
    return round(loopsDataFrame['Money Earned'].sum(), 2)

def bagRoomHours(month):
    monthNum = monthNumbers(month)
    return bagroomDataFrame[bagroomDataFrame['Date'].str.contains(month, case=False)]

# Using the number of a mont, this function will return the total hours worked in bagroom for that month
def totalbagRoomHours(month):
    monthNum = monthNumbers(month)
    return round(bagRoomHours(monthNum)['Hours Worked'].sum(), 2)

def bagRoomTips(month):
    MonthNum = monthNumbers(month)
    return bagroomDataFrame[bagroomDataFrame['Date'].str.contains(month, case=False)]

# Using the number of the month, this function returns the total amount of tip money earned in that month
def totalbagRoomTips(month):
    monthNum = monthNumbers(month)
    return round(bagRoomTips(monthNum)['Tips'].sum(), 2)

def totalbagRoomEarned(month):
    monthNum = monthNumbers(month)
    return round(bagRoomTips(monthNum)['Money Earned'].sum(), 2)

########################################

def moneyEarned(month):
    MonthNum = monthNumbers()
    return bagroomDataFrame[bagroomDataFrame['Date'].str.contains(month, case=False)]

def totalMonthlyIncome(month):
    total = 0
    loopIncome = totalMonthlyLoopIncome(month)
    tip = totalbagRoomTips(month)
    bagroomEarned = totalbagRoomEarned(month)
    total += loopIncome + bagroomEarned + tip
    return round(total, 2)

monthList = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def totalMoneyEarned():
    runningTotal = 0
    for individualMonth in monthList:
        loopIncome = totalMonthlyLoopIncome(individualMonth)
        tip = totalbagRoomTips(individualMonth)
        bagroomEarned = totalbagRoomEarned(individualMonth)
        runningTotal += loopIncome + bagroomEarned + tip
    return round(runningTotal, 2)


# Using matpltlib to create a bar graph
# Gathers the total amount of income per month

# Months
months = 'may', 'june', 'july', 'august', 'september'

# Amount earned
amount = [
    totalMonthlyIncome('may'),
    totalMonthlyIncome('june'),
    totalMonthlyIncome('july'),
    totalMonthlyIncome('august'),
    totalMonthlyIncome('september'),
]


fig, ax = plt.subplots()

# Uses matpltlib to create bar graph
plt.bar(months, amount, color='green')


# White axis borders
for spine in ax.spines.values():
    spine.set_color('white')

# White ticks
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# White labels
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')

# White title
ax.set_title("Monthly Income", color='white')


# Saves the bar graph in files
bar_image_path = os.path.join('static', 'images', 'bar_chart.png')
plt.savefig(bar_image_path, transparent=True)
plt.close()



# Using matplotlib, create pie chart
# Categories
labels = 'Food', 'Subscriptions', 'Golf Rounds', 'Golf Practice', 'Golf Equipment', 'Gigi', 'Laundry', 'Education', 'Bills', 'Car'
# Amount spent
sizes = [expenseSum('Food'), expenseSum('Subscriptions'), expenseSum('Golf Rounds'), expenseSum('Golf Practice'), expenseSum('Golf Equipment'), expenseSum('Gigi'), expenseSum('Laundry'), expenseSum('Education'), expenseSum('Bills'), expenseSum('Car')]

# Using a dictionary, every category is given a total amount spent
dictionary = {'sizes':sizes, 'labels':labels}
pieChart = pd.DataFrame(dictionary)

# Displays the pie chart
plt.pie(x=pieChart.sizes)
# Dispays the pie chart legend
plt.legend(labels=pieChart.labels, loc=[0.95,0.35])

# Title
plt.title('Monthly Expenses', color='white')

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
    return render_template("income.html",
        totalIncome = totalMoneyEarned(),
        january = totalMonthlyIncome('january'),
        february = totalMonthlyIncome('february'),
        march = totalMonthlyIncome('march'),
        april = totalMonthlyIncome('april'),
        may = totalMonthlyIncome('may'),
        june = totalMonthlyIncome('june'),
        july = totalMonthlyIncome('july'),
        august = totalMonthlyIncome('august'),
        september = totalMonthlyIncome('september'),
        october = totalMonthlyIncome('october'),
        november = totalMonthlyIncome('november'),
        december = totalMonthlyIncome('december'),
        mayHours = totalbagRoomHours('may'),
        juneHours = totalbagRoomHours('june'),
        julyHours = totalbagRoomHours('july'),
        augustHours = totalbagRoomHours('august')
        )

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
        laundryTotal = expenseSum('Laundry'),
        billsTotal = expenseSum('Bills'),
        carTotal = expenseSum('Car'),
        educationTotal = expenseSum('Education'))

@app.route("/goals")
def goals():
    return render_template("goals.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

# Runs the website
if __name__ == "__main__":
    app.run(debug=True)
