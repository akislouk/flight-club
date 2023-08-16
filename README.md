# Flight Club

A program that reads a Google Sheet with flight destinations and notifies users via email or SMS when there are cheap flights. It's based on the Flight Club capstone project from the [100 Days of Code - The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) course on Udemy.

- [Flight Club](#flight-club)
  - [Requirements](#requirements)
    - [Packages](#packages)
    - [APIs \& Services](#apis--services)
    - [Environment Variables](#environment-variables)
    - [Google Sheet](#google-sheet)
  - [Usage](#usage)
    - [Adding Users](#adding-users)
  - [To Do](#to-do)
  - [License](#license)

## Requirements

### Packages

The following packages are required to run the program:

- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [twilio](https://pypi.org/project/twilio/) (optional - only required if you want to send SMS notifications)

You can install them by running the following command:

```shell
pip install -r requirements.txt
```

### APIs & Services

You will need to have access to the following APIs/services:

- [Tequila by Kiwi](https://tequila.kiwi.com/): Used to search for airport IATA codes and flight prices. You can choose `Meta Search` when creating your account.
- [Sheety](https://sheety.co/): Used to read and write to a Google Sheet. Make sure to enable `GET`, `POST` and `PUT` requests for your sheets.
- [Twilio](https://www.twilio.com/): Optional. Used to send low price alerts via SMS.
- [Gmail](https://mail.google.com/): Optional. Used to send low price alerts via email.

### Environment Variables

The following environment variables need to be set, either manually or by creating a `.env` file in the project's root directory:

- `SHEETY_AUTH`: Sheety project authentication. Only needed if you set up authentication for your project.
- `SHEETY_URL`: Sheety API endpoint. The sheet name shouldn't be included. For example, if your file is called `Flight Deals`, the URL should be `https://api.sheety.co/your-api-key/flightDeals`.
- `TEQUILA_API`: Tequila API key.
- `TEQUILA_URL`: Tequila base API endpoint. Default value: `https://api.tequila.kiwi.com/`.
- `TWILIO_SID`: Twilio account SID.
- `TWILIO_TOKEN`: Twilio account token.
- `TWILIO_NUMBER`: Twilio phone number.
- `OWNER_NUMBER`: The phone number used to sign up for Twilio.
- `EMAIL`: Gmail email address.
- `PASSWORD`: Gmail app password. You can create one [here](https://myaccount.google.com/apppasswords).
- `ORIGIN`: The IATA code of the city or airport you are flying from. For example, `LON` for all London airports or `LHR` for Heathrow. Default value: `LON`.
- `SEARCH_DAYS_START`: The number of days from today to start searching for flights. Default value: `1` (tomorrow).
- `SEARCH_DAYS_END`: The number of days from `SEARCH_DAYS_START` to stop searching for flights. Default value: `182` (6 months).
- `DAYS_MIN`: The minimum number of days to stay at the destination. Default value: `7`.
- `DAYS_MAX`: The maximum number of days to stay at the destination. Default value: `28`.
- `NO_STOPS`: A flag that indicates whether to search for direct flights only or not. `False` or `Any`. Default value: `True`.
- `SEND_EMAILS`: A flag that indicates whether to send emails or not. `True` or `Any`. Default value: `False`.
- `SEND_SMS`: A flag that indicates whether to send SMS or not. `True` or `Any`. Default value: `False`.

You can use the `.env.template` file as a template. It includes all the environment variables, so you can simply fill in the values and rename it to `.env`.

### Google Sheet

Finally, you will need to create a Google Sheet with the following sheets and columns:

1. `Prices` sheet:
   - `City`: The name of the destination city. These are the cities that will be searched for.
   - `Code`: The IATA code of the destination city. It will be automatically populated by the program if you leave it blank.
   - `Price`: The cheapest price found for the destination city during the last search.
   - `Departure`: The date of departure associated with the `Price`.
   - `Return`: The date of return associated with the `Price`.
   - `Lowest Price`: The lowest price ever found for the destination city.
   - `Threshold`: The price threshold. If the price is lower than this value, a notification will be sent. Set to `0` to disable notifications for a specific destination. If you leave it blank, it will be set to the `Lowest Price` value.
2. `Users` sheet:
   - `First Name`: The user's first name.
   - `Last Name`: The user's last name.
   - `Email`: The user's email address.
   - `Phone`: The user's phone number.

Alternatively, you can make a copy of [this Google Sheet](https://docs.google.com/spreadsheets/d/1eZzcXpfiVEirV0ydPH-SyY9Bffyht4UfXvIXyp8BGso/).

## Usage

To run the program, simply execute the following command:

```shell
python main.py
```

Once executed, the program will start searching for flights for each of the entries in the Google Sheet and update the file with the flight details. If a flight is found with a price lower than the threshold, a notification will be sent to the users via email or SMS.

### Adding Users

The `users.py` script can be used to add users to the Google Sheet through the command line, like so:

```shell
python users.py
```

It's probably better to add users manually to the Google Sheet, though.

## To Do

- Add some methods to `DataManager` so that it can use local JSON files.
- Add some methods to `DataManager` so that it can use a local CSV files.
- Make it possible to search for multiple destinations at once, instead of doing it one by one.

## License

This project is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT).
