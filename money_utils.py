import json
import os

MONEY_FILE = 'money_data.json'

if os.path.exists(MONEY_FILE):
    with open(MONEY_FILE, 'r') as f:
        money_data = json.load(f)
else:
    money_data = {}

def save_data():
    with open(MONEY_FILE, 'w') as f:
        json.dump(money_data, f, indent=4)

def get_user_data(user_id: str):
    if str(user_id) not in money_data:
        money_data[str(user_id)] = {"balance": 0, "last_daily": None}
    return money_data[str(user_id)]
