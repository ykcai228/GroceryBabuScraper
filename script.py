from datetime import date
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Base url & header setting
url = "https://www.grocerybabu.com"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# requests & BeautifulSoup setup
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Get sub category links
sub_cat_links = []
cat_titles = dict()
for li in soup.select("ul.menu > li"):
    # Skip Home and empty categories
    if li.find("div", recursive=False) is not None:
        curr_title = li.select_one("a").text
        cat_subtitles = dict()
        for sub_li in li.select("ul.submenu > li"):
            a_tag = sub_li.select_one("a")
            if a_tag and "all" not in a_tag.text.lower():
                cat_subtitles[a_tag.text] = a_tag.get("href")
                sub_cat_links.append(a_tag.get("href"))
        cat_titles[curr_title] = cat_subtitles

# chromedriver and timeout setup
driver = webdriver.Chrome()
timeout = 10

# Go through all the categories
main_cat_df = pd.DataFrame(columns=["Main Category", "Sub Category", "SKU", "Product Title"])
for cat, sub_cat_map in cat_titles.items():
    print(cat)
    curr_cat_df = pd.DataFrame(columns=["Main Category", "Sub Category", "SKU", "Product Title"])
    # Loop through each sub category
    for sub_cat, href in sub_cat_map.items():
        print(sub_cat)
        driver.get(href)
        # Explicit wait for the page to load
        WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "current")]/span'))
        )
        # Locate the products
        items = driver.find_elements(By.XPATH, '//figure//a')
        # Catch the sub category name
        sub_cat_name = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "current")]/span'))
        ).text
        skus = []
        product_titles = []
        # Loop through all the products in the current sub category and get their sku
        """
        To-Do:
            Handle pagination
            1. Choose "36" for Show
            2. Go through all pages
            3. Improve timeout accommodation
        """
        for item in items:
            # Open product detail page
            item.click()
            product_title = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="product-title"]'))
            ).text
            sku = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//li[contains(text(), "SKU")]/strong'))
            ).text
            close_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@title="Close (Esc)"]'))
            )
            skus.append(sku)
            product_titles.append(product_title)
            # Close current product detail page
            close_button.click()
        # Use object dtype to prevent truncation
        cat_col = np.full(len(skus), cat, dtype=object)
        sub_cat_col = np.full(len(skus), sub_cat, dtype=object)
        sub_cat_product_data = {
            "Main Category": cat_col,
            "Sub Category": sub_cat_col,
            "SKU": skus,
            "Product Title": product_titles
        }
        sub_cat_product_df = pd.DataFrame(sub_cat_product_data)
        curr_cat_df = pd.concat([curr_cat_df, sub_cat_product_df], ignore_index=True)
    main_cat_df = pd.concat([main_cat_df, curr_cat_df], ignore_index=True)
    curr_cat_df.to_csv('./output/' + cat + '.csv', index=False, encoding='utf-8-sig')
main_cat_df.to_csv('./output/GroceryBabu Inventory' + date.today() + '.csv', index=False, encoding='utf-8-sig')