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
    # print(url)
    # print(response)

    # api call was successful if we get code 200
    if response.status_code == 200:
        data = response.json()
        # print(data)
        # print(data["result"])

        # we just return the result, process in other functions
        # print(data["result"])
        return data["result"]


# return the eth balance in the wallet
def get_balance(address):
    get_balance_url = make_api_url(
        "account", "balance", address, "latest", BASESCAN_API_KEY
    )
    data = run_api(get_balance_url)
    data = int(data) / 10**18
    # print(f"Balance: {data} eth")
    return data


# this function look at the internal tx and see where the eth is going to
# will print out the address that is being bought
# example: pingyu is buying kenshiro's key, this function will return kenshiro
def get_room_owner(hash):
    # here is setting up the api for getting internal tx
    url = "https://api.basescan.org/api"
    url += (
        f"?module=account&action=txlistinternal&txhash={hash}&apikey={BASESCAN_API_KEY}"
    )
    data = run_api(url)
    # print(data)

    room_owner = data[1]["to"]
    # print(f"Room owner is {room_owner}")
    return room_owner


def main():
    # try getting the balance
    input_address = input("please enter address: ")
    get_balance(input_address)

    input_hash = input("input buy share hash to check out the room owner")

    get_room_owner(input_hash)


if __name__ == "__main__":
    main()
