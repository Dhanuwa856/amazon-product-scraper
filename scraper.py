from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import time
import os

# Set up the Chrome WebDriver
os.environ['PATH'] += r"C:\Python"
driver = webdriver.Chrome()

# SQlite setup
conn = sqlite3.connect('amazon_products_main.db')
cursor = conn.cursor()
cursor.execute('''
   CREATE TABLE IF NOT EXISTS Products (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT,
     price TEXT,
     rating TEXT,
     image_url TEXT,
     product_url TEXT,
     search_query TEXT
   )            
  ''')

def scrape_amazon_product_data(search_query,max_items=100):
  base_url = "https://www.amazon.com/s?k="+ search_query
  items_collected = 0
  page = 1
  
  while items_collected < max_items:
    url = f"{base_url}&page={page}"
    driver.get(url)
    time.sleep(3)
    
    # Extract product containers
    product_containers = driver.find_elements(By.CSS_SELECTOR,'div[data-component-type="s-search-result"]')
    
    for container in product_containers:
      if items_collected >= max_items:
        break
      
      # Extract product name
      try:
        name = container.find_element(By.TAG_NAME,"h2").text
        
      except:
        pass  
      
      # Extract product price
      try:
       price_whole = container.find_element(By.CSS_SELECTOR,'span.a-price-whole').text
       price_fraction = container.find_element(By.CSS_SELECTOR,'span.a-price-fraction').text
       price = f"${price_whole}.{price_fraction}"
      
      except:
       pass 
     
      # Extract product rating
      try:
       rating_count = container.find_element(By.CSS_SELECTOR,'span.a-size-base.s-underline-text').text
      except:
       pass      
     
      # Extract product image URL
      try:
        image_url = container.find_element(By.CSS_SELECTOR,'img.s-image').get_attribute("src")
      except:
        pass  
      
      # Extract product URL
      try:
       product_url = container.find_element(By.CSS_SELECTOR,'a.a-link-normal').get_attribute('href')
      except:
        pass 
      
      
      # Insert product data into the database
      cursor.execute('''
        INSERT INTO products (name, price, rating, image_url, product_url, search_query)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, rating_count, image_url, product_url, search_query))
            
      items_collected += 1

    # Move to the next page
    page += 1
    time.sleep(2) 
  
  # Commit the transaction and close the connection
  conn.commit()
  
     
  

search_variables = ["headphones","laptops","smartphones","Kitchen Appliances","Fitness Trackers"]

for variable in search_variables:
  scrape_amazon_product_data(variable,max_items=100)
  
print("Scraped data saved to amazon_products_main.db")
 
conn.close()  
driver.quit()   
  