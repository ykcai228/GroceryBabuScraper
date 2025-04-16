import requests
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
for li in soup.select("ul.menu > li"):
    # Skip Home and empty categories
    if li.find("div", recursive=False) is not None:
        for sub_li in li.select("ul.submenu > li"):
            a_tag = sub_li.select_one("a")
            if a_tag and "all" not in a_tag.text.lower():
                sub_cat_links.append(a_tag.get("href"))

# chromedriver and timeout setup
driver = webdriver.Chrome()
timeout = 10

# the list to store all skus
skus = []

# Go through each sub category
for link in sub_cat_links:
    driver.get(link)
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
    sku_ct = 0
    # Loop through all the products in the current sub category and get their sku
    for item in items:
        # Open product detail page
        item.click()
        sku = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//li[contains(text(), "SKU")]/strong'))
        ).text
        close_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Close (Esc)"]'))
        )
        sku_ct += 1
        skus.append(sku)
        # Close current product detail page
        close_button.click()
    print("Total SKU # on " + sub_cat_name + "is: " + str(sku_ct))
print(skus)