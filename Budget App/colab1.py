# git pull
# (edit)
# save code
# git status
# git add colab1.py
# git commit -m "Describe what you did here"
# git push

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Step 2: Load the credentials from the file
creds = ServiceAccountCredentials.from_json_keyfile_name("budget-app-459803-c519ac2d00c1.json", scope)

# Step 3: Authorize the client
client = gspread.authorize(creds)

# Step 4: Open the Google Sheet by name
sheet = client.open("Golf Tracker").sheet1  # Make sure it's a Google Sheet, not an .xlsx

# Step 5: Fetch the data
data = sheet.get_all_records()

# Step 6: Print the data
print(data)