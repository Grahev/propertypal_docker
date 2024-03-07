from models import Property, KeyInfo, Address
import httpx
from dataclasses import dataclass
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
import re
import time

from scraper import next_page, get_page, extract_text



BASE_URL = 'https://www.propertypal.com'
url = 'https://www.propertypal.com/6-mornington-view-ballinderry-road-lisburn/931541'



client = httpx.Client()
page = get_page(client,url)

html = page.body_html

image_element = html.css_first('section img')
if image_element:
    src_attribute = image_element.attributes.get('src')
    print(src_attribute)
else:
    src_attribute = None

price=extract_text(html, "strong.pp-property-price-bold", 0),
description=extract_text(html, "div.pp-property-description", 0),
# img=src_attribute,
#         # img=html.css_first("section.fixsrN > img").attributes['src'],
# # link= urljoin(BASE_URL, link),

print(image_element)