import requests
import time
from datetime import datetime, timedelta

BITCOIN_PRICE_THRESHOLD = 9000
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{YOUR-IFTTT-KEY}'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])  # Convert the price to a floating point number

def get_bitcoin_24percent():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['percent_change_24h'])  # Convert the price to a floating point number

def get_bitcoin_1percent():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['percent_change_1h'])  # Convert the price to a floating point number

def post_ifttt_webhook(event, value):
    data = {'value1': value}  # The payload that will be sent to IFTTT service
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)  # Inserts our desired event
    requests.post(ifttt_event_url, json=data)  # Sends a HTTP POST request to the webhook URL

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        percent1 = get_bitcoin_1percent();
        date = datetime.now()

        if percent1 >= 2:
            mes = "BTC price increased <b>" + str(percent1) + "%<b> the last 1h! " + date.strftime('%d.%m.%Y %H:%M') + ' $' + str(price)
            #print(mes)
            post_ifttt_webhook('bitcoin_percent_update', mes)
        elif percent1 <= -2:
            mes = "BTC price decreased <b>" + str(percent1) + "%<b> the last 1h! " + date.strftime('%d.%m.%Y %H:%M') + ' $' + str(price)
            #print(mes)
            post_ifttt_webhook('bitcoin_percent_update', mes)

        #Send every day the 24h percent
        if datetime.now().hour == 6 and datetime.now().minute == 30 and datetime.now().second == 0:
            time.sleep(1)
            percent24 = get_bitcoin_24percent()
            #print(percent24)
            post_ifttt_webhook('bitcoin_price_update', percent24)

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            #print('emergency')
            post_ifttt_webhook('bitcoin_price_emergency', price)


if __name__ == '__main__':
    main()