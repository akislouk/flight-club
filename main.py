from dotenv import load_dotenv
from os import getenv as env
from datetime import datetime, timedelta
from utils.DataManager import DataManager
from utils.FlightSearch import FlightSearch
from utils.NotificationManager import NotificationManager

load_dotenv()

ORIGIN = env("ORIGIN") or "LON"
SEARCH_DAYS_START = int(env("SEARCH_DAYS_START") or 1)
SEARCH_DAYS_END = int(env("SEARCH_DAYS_END") or 365 // 2)
DAYS_MIN = int(env("DAYS_MIN") or 7)
DAYS_MAX = int(env("DAYS_MAX") or 28)
NO_STOPS = str(env("NO_STOPS")).lower() != "false"
SEND_EMAILS = str(env("SEND_EMAILS")).lower() == "true"
SEND_SMS = str(env("SEND_SMS")).lower() == "true"

dm = DataManager()
fs = FlightSearch()

# Get the users and their phone numbers
if SEND_EMAILS or SEND_SMS:
    nm = NotificationManager()
    users = dm.get_users()
    numbers = [user["phone"] for user in users if user.get("phone")]

# The dates for the search window (tomorrow - 6 months from now)
date_from = datetime.now() + timedelta(days=SEARCH_DAYS_START)
date_to = date_from + timedelta(days=SEARCH_DAYS_END)

need_update = False  # A flag that indicates whether the data needs to be updated or not
dm.get_data()  # Get the data from the sheet
for row in dm.data:
    # Find the IATA code of the city the user is flying to if it's not already in the data
    if not row.get("code"):
        need_update = True
        row["code"] = fs.get_code(row["city"])

    # Find the cheapest flight and update the data if it's cheaper than the saved one
    flight = fs.get_flight(
        ORIGIN, row["code"], date_from, date_to, DAYS_MIN, DAYS_MAX, NO_STOPS
    )
    if not flight:
        continue

    need_update = True
    row["price"] = flight.price
    row["departure"] = flight.out_date.strftime("%d/%m/%Y")
    row["return"] = flight.return_date.strftime("%d/%m/%Y")

    # Set the lowest price to the current price if it's not set yet
    # or if the current price is lower
    if not row.get("lowestPrice") or flight.price < row["lowestPrice"]:
        row["lowestPrice"] = flight.price

    # Set the threshold to the lowest price if it's not set yet
    if not row.get("threshold") and row.get("threshold") != 0:
        row["threshold"] = row["lowestPrice"]

    # Send an email or SMS if the price is lower than the threshold
    if flight.price <= row["threshold"]:
        SEND_EMAILS and nm.send_email(flight, users)
        SEND_SMS and nm.send_sms(flight, numbers)

# Update the data in the sheet if there were any changes
need_update and dm.update()
