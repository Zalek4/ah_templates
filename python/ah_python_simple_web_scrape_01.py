import requests
import time
from bs4 import BeautifulSoup

# This function checks to make sure we're not requesting too often. 
# Requesting from a site too much in a short period of time can result in an IP ban.
# HTTP codes:
# 200 - everything went smoothly.
# 429 - you've sent too many requests in a given amount of time.
# 403 - access forbidden.
# 503 - server is unavailable.
def respectful_requester(url, delay_interval=60):
    global request_count
    response = requests.get(url)

    # If the status code indicates rate limiting, sleep for a bit and then retry
    if response.status_code == 429:
        print(f"Hitting a rate limit. Exiting... : Request #{request_count}")

        return
        
    elif response.status_code != 200:
        print(f"Error: {response.status_code}. Try a different proxy or user-agent.")
        request_count += 1
        return

    else:
        print(f"Request good! Requesting again... : Request #{request_count}")
        time.sleep(30)
        request_count += 1
        return respectful_requester(url, delay_interval)

request_count = 1
url_base = "https://www.google.com/finance"
url_index = "NASDAQ"
url_ticker = "AMD"
url_language = "en"
url_complete = f"{url_base}/quote/{url_ticker}:{url_index}?hl={url_language}"

respectful_requester(url_complete, 1)

"""print("Please enter a stock ticker:")
ticker = input()

url_base = "https://www.google.com/finance"
url_index = "NASDAQ"
url_ticker = ticker.upper()
url_language = "en"
url_complete = f"{url_base}/quote/{url_ticker}:{url_index}?hl={url_language}"

# Make a respectful HTTP request to our complete URL
respectful_requester(url_complete, 1)

# Grab the content from the page
soup = BeautifulSoup(page.content, "html.parser")

# get the items that describe the stock
stock_items = soup.find_all("div", {"class": "gyFHrc"})

# create a dictionary to store the stock description
stock_description = {}

# iterate over the items and append them to the dictionary
for item in stock_items:
    item_description = item.find("div", {"class": "mfs7Fc"}).text
    item_description = item_description.lower()
    item_description = item_description.replace(" ", "_")
    item_value = item.find("div", {"class": "P6K39c"}).text
    stock_description[item_description.lower()] = item_value

for i in stock_description:
    print(f"{i} : {stock_description[i]}")"""

print("Press 'Enter' to exit...")
input()