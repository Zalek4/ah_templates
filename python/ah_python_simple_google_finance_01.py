import requests
from bs4 import BeautifulSoup

print("Please enter a stock ticker.")
ticker = input()

url_base = "https://www.google.com/finance"
url_index = "NASDAQ"
url_ticker = ticker.upper()
url_language = "en"
url_complete = f"{url_base}/quote/{url_ticker}:{url_index}?hl={url_language}"

# Make an HTTP request to our complete URL
page = requests.get(url_complete)

# Grab the content from the page
soup = BeautifulSoup(page.content, "html.parser")

# get the items that describe the stock
stock_items = soup.find_all("div", {"class": "gyFHrc"})

# create a dictionary to store the stock description
stock_description = {}

# iterate over the items and append them to the dictionary
for item in stock_items:
    item_description = item.find("div", {"class": "mfs7Fc"}).text
    item_value = item.find("div", {"class": "P6K39c"}).text
    stock_description[item_description] = item_value

print(stock_description)

print("\nHit 'Enter' to close...")
input()