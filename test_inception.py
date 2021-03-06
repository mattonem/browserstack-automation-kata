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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import time

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
    caps["name"] = "BS-inception-" + request.param
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

def test_inception(driver):
    driver.get("https://www.browserstack.com/")
    driver.maximize_window()
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Sign in")))
    driver.find_element_by_link_text("Sign in").click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "user_password")))
    driver.find_element_by_id("user_email_login").send_keys(os.getenv("BROWSERSTACK_DUMMY_EMAIL"))
    driver.find_element_by_id("user_password").send_keys(os.getenv("BROWSERSTACK_DUMMY_PASSWORD"))

    driver.find_element_by_id("user_password").send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Live")))
    if(driver.find_element_by_id('skip-local-installation').is_displayed()):
        driver.find_element_by_id('skip-local-installation').click()
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, '//li[@data-os="win10"]')))
    driver.find_element_by_xpath('//li[@data-os="win10"]').click()
    driver.find_element_by_xpath('//li[@data-named-version="win10_chrome_latest"]').click()
    WebDriverWait(driver, 40).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "toolbar__list")))
    WebDriverWait(driver, 40).until(expected_conditions.presence_of_element_located((By.ID, "bslive_video")))
    WebDriverWait(driver, 40).until(expected_conditions.presence_of_element_located((By.ID, "flashlight-overlay")))
    canvas = driver.find_element_by_id('flashlight-overlay')
    canvas.click()

    ActionChains(driver)\
        .move_to_element_with_offset(canvas, 350, 390)\
        .click()\
        .perform()
    time.sleep(1)
    ActionChains(driver)\
        .send_keys("browserstack" + Keys.ENTER)\
        .release()\
        .perform()
    time.sleep(5)     
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed"} }')








