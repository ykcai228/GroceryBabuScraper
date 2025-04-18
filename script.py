import time
import logging
import requests
import numpy as np
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

date_today = date.today().isoformat()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("./log/grocerybabu scraper" + ' ' + date_today + ".log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

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
wait = WebDriverWait(driver, timeout)

# Go through all the categories
main_cat_df = pd.DataFrame(columns=["Main Category", "Sub Category", "SKU", "Product Title"])
for cat, sub_cat_map in cat_titles.items():
    logging.info(f"Processing category: {cat}")
    curr_cat_df = pd.DataFrame(columns=["Main Category", "Sub Category", "SKU", "Product Title"])
    # Loop through each sub category
    for sub_cat, href in sub_cat_map.items():
        logging.info(f"Processing sub category: {sub_cat}")
        driver.get(href)
        # Select show 36 items in each page
        dropDown = Select(wait.until(
                EC.presence_of_element_located((By.XPATH, '//select[@name="count"]'))
        ))
        dropDown.select_by_value("36")
        # Render time for page update
        time.sleep(2)
        # Catch the sub category name
        sub_cat_name = wait.until(
                EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "current")]/span'))
        ).text
        skus = []
        product_titles = []
        # Loop through all the pages under current subcategory
        while True:
            logging.info(f"Scraping page in subcategory: {sub_cat_name}")
            # Locate the products
            items = driver.find_elements(By.XPATH, '//figure//a[@class="openQuickView"]')
            logging.info(f"Found {len(items)} items in subcategory: {sub_cat}")
            # Loop through all the products in current page and get their sku
            for item in items:
                try:
                    # Open product detail page
                    item.click()
                    product_title = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//a[@class="product-title"]'))
                    ).text
                    sku = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//li[contains(text(), "SKU")]/strong'))
                    ).text
                    close_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@title="Close (Esc)"]'))
                    )
                    skus.append(sku)
                    product_titles.append(product_title)
                    # Close current product detail page
                    close_button.click()
                except Exception as e:
                    logging.info(f"Failed to extract item: {e}")
                    continue
            # Check if there is a next page
            try:
                next_btn = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Next »"]'))
                )
                if "disabled" in next_btn.get_attribute("class"):
                    logging.info(f"No more pages in subcategory: {sub_cat_name}")
                    break
                else:
                    next_btn.click()
                    time.sleep(2)
            except:
                logging.info(f"No Next button found — end of pagination for {sub_cat_name}")
                break
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
    curr_cat_df.to_csv('./output/' + cat + ' ' + date_today + '.csv', index=False, encoding='utf-8-sig')
main_cat_df.to_csv('./output/GroceryBabu Inventory' + ' ' + date_today + '.csv', index=False, encoding='utf-8-sig')