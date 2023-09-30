# import the needed libraries
import os
from dotenv import load_dotenv
import requests
from web3 import Web3
import time
import telegram
from telegram.ext import Updater, CommandHandler



# Load environment variables from .env file
load_dotenv()

BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
BASESCAN_URL = os.getenv("BASESCAN_URL")
FT_ADDRESS = os.getenv("FT_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# this function will generate the API URL call based on our need
def make_api_url(module, action, address, tag, apikey):
    url = "https://api.basescan.org/api"
    url += f"?module={module}&action={action}&address={address}&tag={tag}&apikey={apikey}"
    return url

# try getting the balance
# input_address = input("please enter address: ")
get_balance_url = make_api_url("account", "balance", FT_ADDRESS, "latest", BASESCAN_API_KEY)

# get_balance_url = make_api_url("account", "balance", input_address, "latest", BASESCAN_API_KEY)


def run_api(url):
    # HTTP call
    response = requests.get(get_balance_url)
    # api call was successful if we get code 200
    if response.status_code == 200:
        data = response.json()
        # 1 eth  = 10**18 wei
        data = int(data['result'])/10**18
        print(f"Balance: {data} eth")


print("This is a FriendTech Arbitrage bot... \n")
run_api(get_balance_url)

# Initialize a Web3 instance for the Base mainnet
w3 = Web3(Web3.HTTPProvider('https://base-mainnet.g.alchemy.com/v2/oak_cR7DLscbD9el9XMEEesA_HYD1Ov6'))

# Check if connected to the Base network
if not w3.is_connected():
    raise Exception("Not connected to Base network")
else:
    print("Connected to Base network")

def testing_one_block(block_num):
    block_number = block_num
    block = w3.eth.get_block('latest')
    print("BLOCK NUMBER:", block_number)
    for tx_hash in block['transactions']:
        # get the transaction
        tx = w3.eth.get_transaction(tx_hash)
        # print(f"tx: {tx} \n")

        # decode the tx data
        input_data = tx['input']
        # get the method ID to filter
        # transformed to hex, and get the first 10 letters only
        method_ID = input_data[:10].hex()[:10]

        if method_ID == buying_share:
            print("buying share...")
        elif method_ID == selling_share:
            print("selling share...")

        print(f"method ID: {method_ID}")


# the method ID for buying and selling shares on FT:
buying_share = '0x6945b123'
selling_share = '0xb51d0534'

# time interval between loop
interval = 1

# while loop here to make sure it keeps running
while True:
    # get the latest block number
    block_number = w3.eth.block_number
    block = w3.eth.get_block('latest')
    print("BLOCK NUMBER:", block_number)
    for tx_hash in block['transactions']:
        # get the transaction
        tx = w3.eth.get_transaction(tx_hash)
        # print(f"tx: {tx} \n")

        # decode the tx data
        input_data = tx['input']
        # get the method ID to filter
        # transformed to hex, and get the first 10 letters only
        method_ID = input_data[:10].hex()[:10]

        if method_ID == buying_share:
            print("buying share...")
        elif method_ID == selling_share:
            print("selling share...")

        print(f"method ID: {method_ID}")
    print("\n")
    time.sleep(interval)
    


