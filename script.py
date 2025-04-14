from home import HomePage
from selenium import webdriver

driver = webdriver.Chrome()
homePage = HomePage(driver)
homePage.navigate_to_homepage()
homePage.getNaviBarList()