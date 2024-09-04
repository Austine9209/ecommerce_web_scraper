# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 01:43:22 2024

@author: abaraka
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=chrome_options)

product_list = []

# List of categories to scrape
categories = {
    "computing": "https://www.jumia.co.ke/computing/?page={page}#catalog-listing",
    "electronics": "https://www.jumia.co.ke/electronics/?page={page}#catalog-listing",
    "sporting goods": "https://www.jumia.co.ke/sporting-goods/?page={page}#catalog-listing",
    "toys games": "https://www.jumia.co.ke/toys-games/?page={page}#catalog-listing",
    "fashion": "https://www.jumia.co.ke/category-fashion-by-jumia/?page={page}#catalog-listing"
}

# Loop through each category
for category, url_pattern in categories.items():
    # Loop through the first 50 pages for each category
    for page in range(1, 51):
        url = url_pattern.format(page=page)
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Parse page content
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("article", class_="prd _fb col c-prd")

        for product in products:
            try:
                product_name = product.find("h3", class_="name").text.strip()
                price = product.find("div", class_="prc").text.strip()
                original_price_tag = product.find("div", class_="old")
                original_price = original_price_tag.text.strip() if original_price_tag else None
                discount_tag = product.find("div", class_="bdg _dsct _sm")
                discount = discount_tag.text.strip() if discount_tag else None

                # Only add the product to the list if there is a discount
                if discount:
                    product_list.append({
                        "product_name": product_name,
                        "price": price,
                        "original_price": original_price,
                        "discount": discount,
                        "category": category,  # Add category to the data
                    })
            except AttributeError:
                continue

driver.quit()

# Convert the list to a DataFrame
df = pd.DataFrame(product_list)

# Save the data to a CSV file
df.to_csv("jumia_products.csv", index=False)

# Connect to the PostgreSQL database
engine = create_engine('postgresql+psycopg2://postgres:admin@localhost/jumia_products')

# Store data in the database
df.to_sql('discounted_products', engine, if_exists='replace', index=False)

# Query the database to verify the data
conn = psycopg2.connect(
    dbname="jumia_products",
    user="postgres",
    password="admin",
    host="localhost"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM discounted_products LIMIT 5;")
records = cursor.fetchall()
for record in records:
    print(record)
conn.close()
