from dotenv import load_dotenv
from utils.DataManager import DataManager

load_dotenv()  # Loads the environment variables needed by DataManager
dm = DataManager()
user: dict[str, str] = {}

print("Welcome to the Flight Club.")
print("We find the best flight deals and send them to you.")
user["firstName"] = input("What is your first name?\n> ").title()
user["lastName"] = input("What is your last name?\n> ").title()
user["email"] = input("What is your email?\n> ").lower()
while user["email"] != input("Type your email again.\n> ").lower():
    print("The emails don't match. Try again.")
    user["email"] = input("What is your email?\n> ").lower()
user["phone"] = input("What is your phone number?\n> ")

dm.add_user(user)
