import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.navi_bar_xpath = '//nav[@aria-label="Main Navigation for Shop by AISLES"]//ul'
        self.category_xpath = './li'

    def navigate_to_homepage(self):
        self.driver.get("https://www.grocerybabu.com/")

    def safe_find(self, element):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(element))

    def go_through_each_cat(self):
        navigation_bar = self.safe_find((By.XPATH, self.navi_bar_xpath))
        categories = navigation_bar.find_elements(By.XPATH, self.category_xpath)
        print(len(categories))
        for i in range(len(categories)):
            if i == 0 or i == 15:
                continue
            categories[i].click()
            time.sleep(2)