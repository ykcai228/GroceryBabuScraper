# GroceryBabuScraper

This project is a Python-based web scraper that extracts all product SKUs from the [GroceryBabu](https://www.grocerybabu.com) website by navigating through each subcategory using a combination of `BeautifulSoup` and `Selenium`.

## 🚀 Features

- Uses `requests` and `BeautifulSoup` to extract subcategory URLs from the homepage navigation menu.
- Automates browser interactions with `Selenium` and `ChromeDriver` to:
  - Visit each subcategory page
  - Open individual product pages
  - Extract SKUs
  - Close product detail modals
- Includes explicit waits to ensure elements are present and interactable before performing actions.
- Collects and prints the total SKU count per subcategory and the complete SKU list.

## 🧰 Technologies Used

- Python 3.x
- [requests](https://pypi.org/project/requests/)
- [BeautifulSoup (bs4)](https://pypi.org/project/beautifulsoup4/)
- [Selenium](https://pypi.org/project/selenium/)

## 📦 Installation

Install the required dependencies:

<pre> ```pip install requests beautifulsoup4 selenium``` </pre>

## ✅ To-Do

- [ ] Format SKU output with associated subcategory names  
- [ ] Write results to a CSV file  
- [ ] Add retry/backoff for slow-loading pages or failures  
- [ ] Add support for running the browser headlessly  
- [ ] Improve logging and error reporting  
