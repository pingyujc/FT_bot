# import the needed libraries
import os
from dotenv import load_dotenv
import requests
from web3 import Web3
import time
from tg import send_telegram_message
import base_api

# Load environment variables from .env file
load_dotenv()

BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
BASESCAN_URL = os.getenv("BASESCAN_URL")
FT_ADDRESS = os.getenv("FT_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# other global variables

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


def scan_one_block(block_num, w3):
    block = w3.eth.get_block(block_num)
    print("BLOCK NUMBER:", block_num)
    for tx_hash in block["transactions"]:
        # get the transaction
        tx = w3.eth.get_transaction(tx_hash)
        # print(f"tx: {tx} \n")

        # get the transaction receipt to check if failed
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)

        # status code is 0, it failed
        if tx_receipt["status"] == 0:
            # print("failed")
            continue

        # decode the tx data
        input_data = tx["input"]

        # the address that is executing this action
        address = tx["from"]

        # only tracking whale so far: balance more than 1 eth
        balance = base_api.get_balance(address)
        if balance < 1:
            continue

        # get the method ID to filter
        # transformed to hex, and get the first 10 letters only
        method_ID = input_data[:10].hex()[:10]

        if method_ID == buying_share:
            print("buy share")
            buyer = address
            buyerlink = "https://www.friend.tech/rooms/" + buyer
            price = wei_to_eth(tx["value"])
            # get the room owner, the key that is being bought
            try:
                room = base_api.get_room_owner(tx_hash.hex())
                keylink = "https://www.friend.tech/rooms/" + room
            except:
                keylink = "failed to get key link"

            # keylink = "https://www.friend.tech/rooms/" + room

            if price < 0.01 or price > 0.15:
                continue
            print("buying price:", price)
            print("key address:", room)

            # check if it is self buying
            if buyerlink == keylink:
                message = "\U0001F6A8 WHALE SELF BUYING ALERT \U0001F6A8\n"
            else:
                message = "\U0001F6A8 WHALE BUYING ALERT \U0001F6A8\n"

            # the message sending to tg
            message += f"Buyer: {buyerlink} \n"
            message += f"Wallet balance: {balance} eth\n"
            message += f"Share price: {price} eth\n"
            message += f"Key: {keylink}"

            # for key in tx:
            #     print(key)

            send_telegram_message(message)
        # elif method_ID == selling_share:
        #     seller = tx["from"]
        #     print("sell share")
        # print(tx)

        # send_telegram_message(f"Seller {seller} is selling share")

        # print(f"method ID: {method_ID}")


def main():
    # connect first
    w3 = connect_to_base()

    # scan_one_block(5008508, w3)
    while True:
        newest = w3.eth.block_number
        scan_one_block(newest, w3)

    time.sleep(2)


if __name__ == "__main__":
    main()
