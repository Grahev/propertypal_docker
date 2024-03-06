#import optional from typing
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


#create address data class for address item
@dataclass
class Address:
    no: str
    street: str
    city: str
    postcode: str
    
    def __str__(self):
        return f"{self.no} {self.street}, {self.city}, {self.postcode}"

#dataclass for property key information
@dataclass
class KeyInfo:
    price: Optional[str]
    style: Optional[str]
    bedrooms: Optional[str]
    bathrooms: Optional[str]
    reception: Optional[str]
    heating: Optional[str]
    epc: Optional[str]
    size: Optional[str]
    status: Optional[str]

    def __str__(self):
        return f"{self.price} | {self.style} | {self.bedrooms} | {self.bathrooms} | {self.reception} | {self.heating} | {self.epc} | {self.size} | {self.status}"
    


#create model data class for property listing item
@dataclass
class Property:
    web_id: str
    title: str
    price: str
    link: str
    img: str
    description: str
    address: Optional[Address] = None
    key_info: Optional[KeyInfo] = None

    def __str__(self):
        return f"{self.title} | {self.price} | {self.link} | {self.img} | {self.description}"

    @classmethod
    def save(cls, property_obj):
        # Connect to the database
        # conn = sqlite3.connect('property.db')
        conn = psycopg2.connect(
            host = os.environ.get("DB_HOST"),
            dbname = os.environ.get("DB_NAME"),
            user = os.environ.get("DB_USER"),
            password = os.environ.get("DB_PASSWORD")
        )



        c = conn.cursor()

        # Create the table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS properties
                     (id SERIAL PRIMARY KEY, web_id TEXT, title TEXT, price TEXT, link TEXT, img TEXT, description TEXT,
                     address_no TEXT, address_street TEXT, address_city TEXT, address_postcode TEXT,
                     key_info_price TEXT, key_info_style TEXT, key_info_bedrooms TEXT, key_info_bathrooms TEXT, key_info_reception TEXT,
                     key_info_heating TEXT, key_info_epc TEXT, key_info_size TEXT, key_info_status TEXT, timestamp TIMESTAMP)''')

        # Check if the property already exists in the database
        c.execute("SELECT * FROM properties WHERE web_id=%s", (property_obj.web_id,))
        result = c.fetchone()
        if result:
            # Property exists, update its values
            print('Property in database')
            # pass
            # query = '''UPDATE properties SET title=?, price=?, link=?, img=?, description=?, 
            #            address_no=?, address_street=?, address_city=?, address_postcode=?,
            #            key_info_price=?, key_info_style=?, key_info_bedrooms=?, key_info_bathrooms=?, key_info_reception=?,
            #            key_info_heating=?, key_info_epc=?, key_info_size=?, key_info_status=?, timestamp=?
            #            WHERE id=?'''
            # params = (property_obj.title, property_obj.price, property_obj.link, property_obj.img, property_obj.description,
            #           property_obj.address.no, property_obj.address.street, property_obj.address.city, property_obj.address.postcode,
            #           property_obj.key_info.price, property_obj.key_info.style, property_obj.key_info.bedrooms,
            #           property_obj.key_info.bathrooms, property_obj.key_info.reception, property_obj.key_info.heating,
            #           property_obj.key_info.epc, property_obj.key_info.size, property_obj.key_info.status,
            #           datetime.now(), property_obj.id)
            # c.execute(query, params)
        else:
            # Property doesn't exist, insert it into the database
            query = '''INSERT INTO properties (web_id, title, price, link, img, description, 
                       address_no, address_street, address_city, address_postcode,
                       key_info_price, key_info_style, key_info_bedrooms, key_info_bathrooms, key_info_reception,
                       key_info_heating, key_info_epc, key_info_size, key_info_status, timestamp)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            params = (property_obj.web_id, property_obj.title, property_obj.price, property_obj.link, property_obj.img,
                      property_obj.description, property_obj.address.no, property_obj.address.street,
                      property_obj.address.city, property_obj.address.postcode, property_obj.key_info.price,
                      property_obj.key_info.style, property_obj.key_info.bedrooms, property_obj.key_info.bathrooms,
                      property_obj.key_info.reception, property_obj.key_info.heating, property_obj.key_info.epc,
                      property_obj.key_info.size, property_obj.key_info.status, datetime.now())
            c.execute(query, params)

            print(f"Added new property: {property_obj.title}")

        # Commit changes and close the connection
        conn.commit()
        conn.close()