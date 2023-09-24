# import the needed libraries
import os
from dotenv import load_dotenv
import requests



# Load environment variables from .env file
load_dotenv()

BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
BASESCAN_URL = os.getenv("BASESCAN_URL")
FT_ADDRESS = os.getenv("FT_ADDRESS")

params = {
    "address": FT_ADDRESS,
    "apikey": BASESCAN_API_KEY,  # Include your API key here if required
}

'''

https://api.basescan.org/api
   ?module=account
   &action=balance
   &address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   &tag=latest
   &apikey=YourApiKeyToken

'''
# this function will generate the API URL call based on our need
def make_api_url(module, action, address, tag, apikey):
    url = "https://api.basescan.org/api"
    url += f"?module={module}&action={action}&address={address}&tag={tag}&apikey={apikey}"
    return url

# try getting the balance
get_balance_url = make_api_url("account", "balance", FT_ADDRESS, "latest", BASESCAN_API_KEY)


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

