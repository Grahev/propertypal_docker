from models import Property, KeyInfo, Address
import httpx
from dataclasses import dataclass
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
import re
import time
import pandas as pd

from scraper import extract_text

@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict


BASE_URL = 'https://www.justia.com'
url = 'https://www.justia.com/lawyers/personal-injury/florida'



client = httpx.Client()

def get_page(client ,url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    resp = client.get(url, headers=headers, timeout=15)
    # print(url)
    
    html = HTMLParser(resp.text)

    n_page = html.css_first('div#pagination > span > a')
    next_page = urljoin( BASE_URL, n_page.attributes['href'])
    return Response(body_html=html, next_page=next_page)

def is_premium(item):
    text = extract_text(item, 'div.lawyer-status', 0)
    if text == 'PREMIUM':
        return True
    else:
        False


def get_items(html):
    items = html.css('div.jcard')
    return items

def get_data(item):
    
    if is_premium(item):
        name = extract_text(item, 'strong.lawyer-name',0) 
        phone = extract_text(item, 'li.-phone',0)
        description = extract_text(item, 'div.lawyer-description', 0)
        tagline = extract_text(item, 'div.lawyer-tagline', 0)
        group = item.css_first('div.lawyer-control-group--premium')
        links = group.css('a')
        www = links[0].attributes['href']
        contact_form_url = links[-1].attributes['href']
        profile_url = links[1].attributes['href']
        data = {
            'name': name,
            'phone' : phone,
            'description': description,
            'tagline': tagline,
            'www': www,
            'contact_form_url': contact_form_url,
            'profile_url': profile_url
        }
        return data



def main():
    counter = 1
    df = pd.DataFrame()
    url = 'https://www.justia.com/lawyers/personal-injury/florida'
    html = get_page(client,url).body_html
    # while True:
    while counter <5:
        page = get_page(client, url)

        if page.next_page is None:
            client.close()
            break
        else:
            url = page.next_page
            html = get_page(client,url)
            items = get_items(html.body_html)
            for item in items:
        
                df = df._append(get_data(item),ignore_index=True)
                df.to_csv('data.csv', index=False)


            time.sleep(1)


    
    

        print(df.info())
        counter = counter+ 1
        print(counter)
        df.to_csv('data.csv')
    

if __name__ == "__main__":
    main()