from models import Property, KeyInfo, Address
import httpx
from dataclasses import dataclass
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
import re
import time



BASE_URL = 'https://www.propertypal.com'
url = 'https://www.propertypal.com/property-for-sale/lisburn-area'

@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict

def next_page(html):

    for link in html.css('a'):
        if link.css_first('p'):
            p_text = link.css_first('p').text()
            if p_text == "Next":
                
                url = link.attributes['href']
                # print(url)
                next_url = urljoin(BASE_URL, url)
                return next_url
        else:
            next_url = None
    return next_url

def get_page(client ,url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    resp = client.get(url, headers=headers, timeout=15)
    # print(url)
    
    html = HTMLParser(resp.text)
    
    # next_page = next_page(html)
    
    # if html.css_first('a[aria-label="next page"]'):
    #     next_page = html.css_first('a[aria-label="next page"]').attributes
    # else:
    #     next_page = {"href": False}
    return Response(body_html=html, next_page=next_page(html))
    # return all_a_tags

def extract_text(html, selector, index ):
    try:
        return html.css(selector)[index].text(strip=True)
    except IndexError:
        return "none"
    
def parse_detail(html, link):
    def find_row_by_label(label):
        for row in html.css('table tr'):
            cells = row.css('td')
            if len(cells) == 2 and cells[0].text(strip=True) == label:
                return cells[1].text(strip=True)
        return None
    
    
    address_line1 = extract_text(html, 'div.sc-ccfad107-0 > h1',0)
    # print(address_line1)
    address_line2 = extract_text(html,'div.sc-ccfad107-0 > p',0)
    # print(address_line2)
    
    # Extracting the address elements from the address_line1 and address_line2
    try:
        no = re.search(r'\d+', address_line1).group()
    except AttributeError:
        no = None
    street = re.search(r'\D+', address_line1).group().strip()
    try:
        city = address_line2.split(',')[-2]
    except IndexError:
        city = None
    postcode = address_line2.split(',')[-1]

    # Select the first image element within the specified section class
    image_element = html.css_first('section img')
    # Get the src attribute value
    if image_element:
        src_attribute = image_element.attributes.get('src')
        # print(src_attribute)
    else:
        src_attribute = None
    
    
    new_property = Property(
        web_id = link.split('/')[-1],
        title=extract_text(html, "div.sc-53bec0d3-1 > h1", 0),
        price=extract_text(html, "p.pp-property-price", 0),
        description=extract_text(html, "div.sc-1898sr3-1 > p.FViVo", 0),
        img=src_attribute,
        # img=html.css_first("section.fixsrN > img").attributes['src'],
        link= urljoin(BASE_URL, link),
        key_info = KeyInfo(
            price=extract_text(html, "p.pp-property-price", 0),
            style = find_row_by_label("Style"),
            bedrooms= find_row_by_label("Bedrooms"),
            bathrooms= find_row_by_label("Bathrooms"),
            reception= find_row_by_label("Receptions"),
            heating= find_row_by_label("Heating"),
            epc= find_row_by_label("EPC"),
            size= find_row_by_label("Floor Area"),
            status= find_row_by_label("Status"),
            ),
        address = Address(
            no=no, 
            street=street, 
            city=city, 
            postcode=postcode
        )
    )
    Property.save(new_property)
    print(f"title: {new_property.web_id}")

def parse_links(html):
    links = html.css("div.iCRFOu > ul > li > div > a")
    # print(links)
    return {link.attributes['href'] for link in links}


def detail_page_loop(client, page):
    product_links = parse_links(page.body_html)
    for link in product_links:
        url = urljoin(BASE_URL, link)
        page = get_page(client, url)
        parse_detail(page.body_html, link)

def pagination_loop(client):
    url = 'https://www.propertypal.com/property-for-sale/lisburn-area'
    while True:
        page = get_page(client, url)
        detail_page_loop(client, page)
        if page.next_page is None:
            client.close()
            break
        else:
            url = page.next_page
            print(url)
            time.sleep(1)

def main():
    client = httpx.Client()
    pagination_loop(client)

    # url = 'https://www.propertypal.com/property-for-sale/lisburn'
    # a = get_page(client,url)
    # print(a.next_page)

    # for link in a:
    #     if link.css_first('p'):
    #         p_text = link.css_first('p').text()
    #         if p_text == "Next":
                
    #             next_url = link.attributes['href']
    #             print(next_url)
    #     else:
    #         print("this is not a Next page link")
        
            
        

if __name__ == "__main__":
    main()