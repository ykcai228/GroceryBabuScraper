from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.navi_bar_xpath = '//nav[@aria-label="Main Navigation for Shop by AISLES"]/ul'
        self.category_xpath = './li'

    def navigate_to_homepage(self):
        self.driver.get("https://www.grocerybabu.com/")
    
    def getNaviBarList(self):
        naviBar = self.driver.find_element(By.XPATH, self.navi_bar_xpath)
        categoryList = naviBar.find_elements(By.XPATH, self.category_xpath)
        print(categoryList)
        # return [cat.text.strip() for cat in categories if cat.text.strip()]
