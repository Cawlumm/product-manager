
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


def search_ebay_items(keyword):
    # URL With Searchword
    url = f'https://www.ebay.com/sch/i.html?_nkw={keyword}'

    # Set Headers
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Response from requests API
    response = requests.get(url, headers=headers)

    # Parsed HTML from BeautifySoup API
    soup = bs(response.content, 'html.parser')

    # Return Soup varaible in html format
    return soup
