from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
from random import randint
import sqlite3
from decimal import Decimal
import datetime

from latlong import get_lat_and_long

BASE_URL = 'https://www.propertypal.com'
url = 'https://www.propertypal.com/property-for-sale/lisburn'
url2 = 'https://www.propertypal.com/property-for-sale/northern-ireland/page-251'

def request_page(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout=15)
    return BeautifulSoup(r.html.html, 'html.parser')

def last_page(url:str):
    soup = request_page(url)
    bottom_nav = soup.find('nav', class_='sc-1829moy-1')
    last_page_button = bottom_nav.find_all('a')[-1]
    last_page = last_page_button['aria-label']
    link = last_page_button['href']
    if last_page == 'next page':
        return BASE_URL + link
    else:
        return None


def pagination_loop(url):
    while True:
        page = request_page(url)
        print(page.status)
        if last_page(url) is None:
            print('no last page')
            break

pagination_loop(url)

# #all listings container
# listings = soup.find_all('li', class_='pp-property-box')

# for listing in listings:
#     link = listing.find('a')['href']
#     img = listing.find('img')['src']
#     title = listing.find('h2').text
#     price = listing.find('p', class_='pp-property-price').text
#     desc = listing.find('p', class_='pp-property-price').find_next('p').text
    # print(desc)

# print(len(listings))