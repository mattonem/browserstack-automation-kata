import os

from datetime import datetime
import pytest
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

now = datetime.now()
buildName = now.strftime("%m/%d/%Y, %H:%M:%S")

with open('browsers.json') as json_file:
    browsers = json.load (json_file)

@pytest.fixture(scope="module", params=browsers)
def driver(request):
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    caps = browsers[request.param]
    caps["browserstack.user"] = username
    caps["browserstack.key"] = access_key
    caps["project"] = 'CE-Challenge'
    caps["name"] = "amazon-scroller-" + request.param
    caps["build"] = buildName
    options = Options()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.disable_beforeunload", True)
    profile.update_preferences()
    options.profile = profile
    driver = webdriver.Remote(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=caps,
        options=options)
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed"} }')
    yield driver
    driver.quit()

def test_amazon(driver):
    driver.get("https://www.amazon.com/")
    searchInput = driver.find_element_by_class_name("nav-search-field").find_element_by_tag_name("input")
    searchInput.send_keys("iPhone X")
    driver.find_element_by_xpath("//input[@value='Go']").click()
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "low-price")))
    driver.find_element_by_id("low-price").send_keys("0")
    driver.find_element_by_id("high-price").send_keys("1000")
    driver.find_element_by_xpath("//input[@id='high-price']/parent::form//input[@type='submit']").click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "filters")))
    driver.find_element_by_id("filters").find_element_by_xpath("//span[text()='iOS']").click()


    driver.find_element_by_xpath("//span[text()='Sort by:']").click()
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Price: High to Low")))
    driver.find_element_by_link_text("Price: High to Low").click()
    
    items = driver.find_elements_by_xpath("//div[contains(@class,'s-main-slot')]//div[@data-component-type='s-search-result']")
    for item in items:
        name=item.find_element_by_tag_name("h2")
        print("====Name====")
        print(name.text)
        print("====Link====")
        print(name.find_element_by_tag_name('a').get_attribute("href"))
        prices = item.find_elements_by_xpath("//span[@class='a-price']")
        for price in prices:
            print("====price=====")
            print(price.find_element_by_class_name('a-price-symbol').text + price.find_element_by_class_name('a-price-whole').text + '.' + price.find_element_by_class_name("a-price-fraction").text)
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed"} }')






