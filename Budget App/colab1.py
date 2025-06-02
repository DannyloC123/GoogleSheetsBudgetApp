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
expensesCategories = pd.DataFrame(expenses.get_all_records())
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


# Gets all the income in the month chosen
def monthIncome(month):
    monthNum = ''

    # I will find a more effective way of doing this later
    if month.lower() == 'january':
        monthNum = '-01-'
    elif month.lower() == 'february':
        monthNum = '-02-'
    elif month.lower() == 'march':
        monthNum = '-03-'
    elif month.lower() == 'april':
        monthNum = '-04-'
    elif month.lower() == 'may':
        monthNum = '-05-'
    elif month.lower() == 'june':
        monthNum = '-06-'
    elif month.lower() == 'july':
        monthNum = '-07-'
    elif month.lower() == 'august':
        monthNum = '-08-'
    elif month.lower() == 'september':
        monthNum = '-09-'
    elif month.lower() == 'october':
        monthNum = '-10-'
    elif month.lower() == 'november':
        monthNum = '-11-'
    elif month.lower() == 'december':
        monthNum = '-12-'
    return loopsDataFrame[loopsDataFrame['Date'].str.contains(monthNum, case=False)]

# Gets all the income from the person chosen
def personIncome(person):
    return loopsDataFrame[loopsDataFrame['Client Name/Golfer'].str.contains(person, case=False)]

# Gets the total sum of income in a month
def totalMonthIncome(monthNum):
    return monthIncome(monthNum)['Money Earned'].sum().round(2)

# Gets the total sum of income from a person
def totalPersonIncome(person):
    return personIncome(person)['Money Earned'].sum().round(2)

# Gets the total life time amount of income earned
def incomeLoops():
    return loopsDataFrame['Money Earned'].sum().round(2)

def bagRoomHours(month):
    monthNum = 0
    # I will find a more effective way of doing this later
    if month.lower() == 'january':
        monthNum = '-01-'
    elif month.lower() == 'february':
        monthNum = '-02-'
    elif month.lower() == 'march':
        monthNum = '-03-'
    elif month.lower() == 'april':
        monthNum = '-04-'
    elif month.lower() == 'may':
        monthNum = '-05-'
    elif month.lower() == 'june':
        monthNum = '-06-'
    elif month.lower() == 'july':
        monthNum = '-07-'
    elif month.lower() == 'august':
        monthNum = '-08-'
    elif month.lower() == 'september':
        monthNum = '-09-'
    elif month.lower() == 'october':
        monthNum = '-10-'
    elif month.lower() == 'november':
        monthNum = '-11-'
    elif month.lower() == 'december':
        monthNum = '-12-'
    return bagroomDataFrame[bagroomDataFrame['Hours Worked'].str.contains(month, case=False)]

def totalbagRoomHours(monthNum):
    return bagRoomHours(monthNum)['Hours Worked'].sum().round(2)

def bagRoomTips(month):
    MonthNum = 0
    # I will find a more effective way of doing this later
    if month.lower() == 'january':
        monthNum = '-01-'
    elif month.lower() == 'february':
        monthNum = '-02-'
    elif month.lower() == 'march':
        monthNum = '-03-'
    elif month.lower() == 'april':
        monthNum = '-04-'
    elif month.lower() == 'may':
        monthNum = '-05-'
    elif month.lower() == 'june':
        monthNum = '-06-'
    elif month.lower() == 'july':
        monthNum = '-07-'
    elif month.lower() == 'august':
        monthNum = '-08-'
    elif month.lower() == 'september':
        monthNum = '-09-'
    elif month.lower() == 'october':
        monthNum = '-10-'
    elif month.lower() == 'november':
        monthNum = '-11-'
    elif month.lower() == 'december':
        monthNum = '-12-'
    return bagroomDataFrame[bagroomDataFrame['Tips'].str.contains(month, case=False)]

def totalbagRoomTips(monthNum):
    return bagRoomTips(monthNum)['Tips'].sum().round(2)

def moneyEarned(month):
    MonthNum = 0
    # I will find a more effective way of doing this later
    if month.lower() == 'january':
        monthNum = '-01-'
    elif month.lower() == 'february':
        monthNum = '-02-'
    elif month.lower() == 'march':
        monthNum = '-03-'
    elif month.lower() == 'april':
        monthNum = '-04-'
    elif month.lower() == 'may':
        monthNum = '-05-'
    elif month.lower() == 'june':
        monthNum = '-06-'
    elif month.lower() == 'july':
        monthNum = '-07-'
    elif month.lower() == 'august':
        monthNum = '-08-'
    elif month.lower() == 'september':
        monthNum = '-09-'
    elif month.lower() == 'october':
        monthNum = '-10-'
    elif month.lower() == 'november':
        monthNum = '-11-'
    elif month.lower() == 'december':
        monthNum = '-12-'
    return bagroomDataFrame[bagroomDataFrame['Money Earned'].str.contains(month, case=False)]

def totalMoneyEarned(monthNum):
    return moneyEarned(monthNum)['Money Earned'].sum().round(2)


# Using matpltlib to create a bar graph
# Gathers the total amount of income per month

# Months
months = 'may', 'june', 'july', 'august', 'september'

# Amount earned
amount = [
    totalMonthIncome('may'),
    totalMonthIncome('june'),
    totalMonthIncome('july'),
    totalMonthIncome('august'),
    totalMonthIncome('september'),
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
        #totalIncome = income(),
        january = totalMonthIncome('january'),
        february = totalMonthIncome('february'),
        march = totalMonthIncome('march'),
        april = totalMonthIncome('april'),
        may = totalMonthIncome('may'),
        june = totalMonthIncome('june'),
        july = totalMonthIncome('july'),
        august = totalMonthIncome('august'),
        september = totalMonthIncome('september'),
        october = totalMonthIncome('october'),
        november = totalMonthIncome('november'),
        december = totalMonthIncome('december'),
        #mayHours = totalbagRoomHours('may'),
        #juneHours = totalbagRoomHours('june'),
        #julyHours = totalbagRoomHours('july')
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
        laundryTotal = expenseSum('Laundry'))

@app.route("/goals")
def goals():
    return render_template("goals.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

# Runs the website
if __name__ == "__main__":
    app.run(debug=True)
