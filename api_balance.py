import os
from dotenv import load_dotenv
import requests
from web3 import Web3
import time

# Load environment variables from .env file
load_dotenv()

BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
BASESCAN_URL = os.getenv("BASESCAN_URL")
FT_ADDRESS = os.getenv("FT_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# this function will generate the API URL call based on our need
def make_api_url(module, action, address, tag, apikey):
    url = "https://api.basescan.org/api"
    url += (
        f"?module={module}&action={action}&address={address}&tag={tag}&apikey={apikey}"
    )
    return url


def run_api(url):
    # HTTP call
    response = requests.get(url)
    # api call was successful if we get code 200
    if response.status_code == 200:
        data = response.json()
        # 1 eth  = 10**18 wei
        data = int(data["result"]) / 10**18
        print(f"Balance: {data} eth")


def get_balance(address):
    get_balance_url = make_api_url(
        "account", "balance", address, "latest", BASESCAN_API_KEY
    )
    run_api(get_balance_url)


def main():
    # try getting the balance
    input_address = input("please enter address: ")
    get_balance(input_address)


if __name__ == "__main__":
    main()
