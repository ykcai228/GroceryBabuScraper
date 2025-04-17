# GroceryBabuScraper

This project is a Python-based web scraper that extracts all product SKUs and titles from the [GroceryBabu](https://www.grocerybabu.com) website by navigating through each subcategory using `BeautifulSoup` and `Selenium`.

---

## 🚀 Features

- Scrapes subcategory links from the homepage using `requests` and `BeautifulSoup`
- Uses `Selenium` and `ChromeDriver` to:
  - Load subcategory pages
  - Click into each product
  - Extract SKU and product title
  - Close product detail modals
- Structures scraped data into a clean CSV output
- Organizes data with associated main and subcategory names
- Handles dynamic content loading with explicit waits
- Saves both individual category CSVs and a full inventory export

---

## 🧰 Technologies Used

- **Python 3.x**
- [`requests`](https://pypi.org/project/requests/)
- [`BeautifulSoup4`](https://pypi.org/project/beautifulsoup4/)
- [`Selenium`](https://pypi.org/project/selenium/)
- [`pandas`](https://pypi.org/project/pandas/)
- [`numpy`](https://pypi.org/project/numpy/)
- **ChromeDriver** (installed separately)

---

## 🛠 How it Works

1. **Homepage Parsing**  
   - Sends an HTTP request to `https://www.grocerybabu.com`
   - Parses the navigation menu to extract all subcategory links grouped by their parent category

2. **Product Scraping**  
   - For each subcategory, launches the page using `Selenium`
   - Waits for the product list to load using explicit waits
   - Clicks into each product's detail modal
   - Extracts the **SKU** and **Product Title**
   - Closes the modal before moving to the next product

3. **Data Formatting**  
   - Compiles the scraped data into a structured `DataFrame`
   - Outputs individual CSVs by category and one master CSV with all results
   - Master file is named: `GroceryBabu Inventory<DATE>.csv` under `./output/`

---

## ✅ To-Do

- [x] Format SKU output with associated subcategory names  
- [x] Write results to a CSV file  
- [ ] Handle pagination (i.e., select "36" per page and loop through all pages)  
- [ ] Add retry/backoff logic for timeouts or failures  
- [ ] Add option for running the browser headlessly  
- [ ] Improve logging and error reporting  

---

## 📦 Installation

Install dependencies using pip:

```bash
pip install requests beautifulsoup4 selenium numpy pandas
```