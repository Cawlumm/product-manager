
import requests
import sys
import json
from bs4 import BeautifulSoup as bs


# Save favorites array to a JSON file
def save_favorites_to_file(favorites):
    with open('favorites.json', 'w') as f:
        json.dump(favorites, f)

# Grab favorites array from JSON file


def grab_favorites_from_file():
    with open('favorites.json', 'r') as f:
        data = json.load(f)
        return data

# Function to search items given a keyword


def search_ebay_items(keyword, min_price=0, max_price=999999):
    url = f'https://www.ebay.com/sch/i.html?_nkw={keyword}&_ipg=100&_udlo={min_price}&_udhi={max_price}'

    # Set Headers
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Response from requests API
    response = requests.get(url, headers=headers)

    # Parsed HTML from BeautifulSoup API
    soup = bs(response.content, 'html.parser')

    # Return the parsed soup object
    return soup


def track_ebay_items():
    # Grabs items from storage
    ebay_items = grab_favorites_from_file()
    # Creates list that will be used to store all information
    # Will ultimatley be used to store back to file
    tracked_items = []
    # For each item in storage
    for item in ebay_items:
        # Set up item detail object
        # Results: all the search results with their title, price, sold
        item_details = {
            'item': item['item'],
            'checked': item['checked'],
            'results': []
        }
        # If the item is checked 'tracking'
        if item['checked'] == True:

            # Split items from strage from a single string to three varaibles
            # Titles, Prices, Sold
            split_items = item['item'].split(' | ')

            soup = search_ebay_items(split_items[0],)

            # Extract item titles
            item_titles = [item.get_text()
                           for item in soup.select(".s-item__title")]

            # Extract the item prices
            item_prices = [item.get_text()
                           for item in soup.select(".s-item__price")]

            # Extract the item quantity sold
            item_sold = [item.get_text()
                         for item in soup.select(".s-item__quantitySold")]

            # For each item in above lists
            # Since they all have the same amount of items we can use the zip class
            for title, price, sold in zip(item_titles, item_prices, item_sold):
                # Append each search result to tracker object
                existing_result = next(
                    (res for res in item['results'] if res['title'] == title), None)

                if existing_result:
                    print(
                        existing_result
                    )
                    old_price = existing_result['price']
                    if price != old_price:
                        change = "Increased" if float(price[1:]) > float(
                            old_price[1:]) else "Decreased"
                        print(change)
                        change_amount = abs(
                            float(price[1:]) - float(old_price[1:]))
                        existing_result['price'] = price
                        existing_result['price_change'] = {
                            'change': change,
                            'amount': change_amount
                        }
                item_details['results'].append(
                    {'title': title, 'price': price, 'sold': sold, 'price_change': []})

        # Append tracker objects to list and save list to storage
        tracked_items.append(item_details)
    save_favorites_to_file(tracked_items)
