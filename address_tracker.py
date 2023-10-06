# goals:
# users enter username
# will tell users if that address is valid (on FT or not)
# will give some information too
# give FT room link, twitter link, twitter followers maybe, wallet balance
# it will then start tracking all actions, including:
# buy/sell/deposit/withdraw

# import the needed libraries
import os
from dotenv import load_dotenv
import requests
from web3 import Web3
import time
import base_api

# Load environment variables from .env file
load_dotenv()

BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
BASESCAN_URL = os.getenv("BASESCAN_URL")
FT_ADDRESS = os.getenv("FT_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# other global variables

# the list of address we are watching
watching_address = []

# the method ID for buying and selling shares on FT:
buying_share = "0x6945b123"
selling_share = "0xb51d0534"


# converter from wei to eth
# leave 6 decimal places
def wei_to_eth(amount):
    eth_amount = amount / 10**18
    eth_amount = "{:.6f}".format(eth_amount)
    eth_amount = float(eth_amount)
    return eth_amount


# function to send a telegram message
def send_telegram_message(mess):
    # The message that will be sent
    message = mess

    # setting up the url
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

    # send it
    try:
        requests.get(url)
        # print("message sent")
    except:
        print("message failed to sent")


# connect to base mainnet
def connect_to_base():
    # Initialize a Web3 instance for the Base mainnet
    w3 = Web3(
        Web3.HTTPProvider(
            "https://base-mainnet.g.alchemy.com/v2/oak_cR7DLscbD9el9XMEEesA_HYD1Ov6"
        )
    )

    # Check if connected to the Base network
    if not w3.is_connected():
        raise Exception("Not connected to Base network")
    else:
        print("Connected to Base network")

    return w3


# this function should start tracking one address
# return some info about this address
# balance, FT link, twitter link
def add_to_list(address):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n")
    print(f"Adding {address} to the tracking list...")
    base_api.get_balance(address)
    watching_address.append(address)

    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n")


# FT API and
# def make_url_FT()


def main():
    # connect first
    w3 = connect_to_base()

    while True:
        temp = input("Enter the address you want to track: \n")
        add_to_list(temp)

        ans = input("Another one? \nY/N: ")

        if ans == "Y":
            continue
        else:
            break

    # add_to_list("0x1915AeC600e892614d00f6125A570a6bfCfdFFCA")

    print("RESULTS:")
    print("The addresses on the list so far:")
    for address in watching_address:
        print(address)

    # response = requests.get(
    #     "https://prod-api.kosetto.com/pingyujc/0x1915aec600e892614d00f6125a570a6bfcfdffca"
    # )
    response = requests.get(
        "https://prod-api.kosetto.com/portfolio/0x1915aec600e892614d00f6125a570a6bfcfdffca&auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHgxOTE1YWVjNjAwZTg5MjYxNGQwMGY2MTI1YTU3MGE2YmZjZmRmZmNhIiwiaWF0IjoxNjk0OTE0MDk1LCJleHAiOjE2OTc1MDYwOTV9.mBOPtXVnnpi-BSPXsMcw15Q0a8D04QPsDXohDuPHFoc"
    )
    # api call was successful if we get code 200
    if response.status_code == 200:
        data = response.json()
        # 1 eth  = 10**18 wei
        print(data)
    else:
        print(response.status_code)


if __name__ == "__main__":
    main()
