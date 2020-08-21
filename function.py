from datetime import datetime, timedelta

import requests

from twilio.rest import Client
from dateutil.parser import parse


def get_country_confirmed_infected(country, start_date, end_date):
    resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed",
                        params={"from": start_date,
                                "to": end_date})
    return resp.json()


def send_whatsapp_message(msg):
    account_sid = 'AC1949902ebd984bbf53296de26e50c577'
    auth_token = '7a32957135dbdaa1bd4e79f13910de3c'
    Client(account_sid, auth_token).messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+5491123926384',
        body=msg
    )
def send_whatsapp_message2(msg):
    account_sid = 'AC1949902ebd984bbf53296de26e50c577'
    auth_token = '7a32957135dbdaa1bd4e79f13910de3c'
    Client(account_sid, auth_token).messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+5491126305595',
        body=msg
    )


def main():
    country = "Argentina"
    country2 = "Spain"
    today = datetime.now().date() #Fecha de hoy
    week_ago = today - timedelta(days=7) #Fecha de hace una semana
    print("Getting COVID data")
    cases = get_country_confirmed_infected(country, week_ago, today)
    cases2 = get_country_confirmed_infected(country2, week_ago, today)
    latest_day = cases[-1]
    latest_day2 = cases2[-1]
    earliest_day = cases[0]
    earliest_day2 = cases2[0]
    yesterday = cases[-2]
    yesterday2 = cases2[-2]
    percentage_increase = (latest_day['Cases'] - earliest_day['Cases']) / (earliest_day['Cases'] / 100)
    percentage_increase2 = (latest_day2['Cases'] - earliest_day2['Cases']) / (earliest_day2['Cases'] / 100)
    
    msg = f"{earliest_day['Cases']} cases where confirmed on {week_ago} and {latest_day['Cases']} " \
        f"cases where confirmed on {parse(latest_day['Date']).date()}. \n" \
        f"{latest_day['Cases'] - earliest_day['Cases']} COVID cases where confirmed last week. \n" \
        f"{latest_day['Cases'] - yesterday['Cases']} cases where confirmed yesterday. \n"
    if percentage_increase > 0:
        msg += f"This is {round(abs(percentage_increase), 2)}% increase over the cases a week ago. "
    else:
        msg += f"This is {round(abs(percentage_increase), 2)}% decrease over the cases a week ago. \n"
    
    msg2 = f"{earliest_day2['Cases']} cases where confirmed on {week_ago} and {latest_day2['Cases']} " \
        f"cases where confirmed on {parse(latest_day2['Date']).date()}. \n" \
        f"{latest_day2['Cases'] - earliest_day2['Cases']} COVID cases where confirmed last week. \n" \
        f"{latest_day2['Cases'] - yesterday2['Cases']} cases where confirmed yesterday. \n"
    if percentage_increase2 > 0:
        msg2 += f"This is {round(abs(percentage_increase2), 2)}% increase over the cases a week ago. "
    else:
        msg2 += f"This is {round(abs(percentage_increase2), 2)}% decrease over the cases a week ago. "
    print("Sending Whatsapp message")

    print("Argentina:\n" + msg + "\nSpain:\n" + msg2)

    # send_whatsapp_message("Argentina:\n" + msg + "\nSpain:\n" + msg2)
    # send_whatsapp_message2("Argentina:\n" + msg + "\nSpain:\n" + msg2)
    print("Job finished successfully")

