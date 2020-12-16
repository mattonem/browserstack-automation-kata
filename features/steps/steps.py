from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

@given('we are browsing amazon')
def step_impl(context):
    context.browser.get("https://www.amazon.com/")

@when('we search for "{something}"')
def step_impl(context, something):
    searchInput = context.browser.find_element_by_class_name("nav-search-field").find_element_by_tag_name("input")
    searchInput.send_keys(something)
    context.browser.find_element_by_xpath("//input[@value='Go']").click()

@when('we filter price "{min}" to "{max}"')
def step_impl(context, min, max):
    WebDriverWait(context.browser, 10).until(expected_conditions.presence_of_element_located((By.ID, "low-price")))
    context.browser.find_element_by_id("low-price").send_keys(min)
    context.browser.find_element_by_id("high-price").send_keys(max)
    context.browser.find_element_by_xpath("//input[@id='high-price']/parent::form//input[@type='submit']").click()

@when('we filter "{filtering}"')
def step_impl(context, filtering):
    WebDriverWait(context.browser, 10).until(expected_conditions.presence_of_element_located((By.ID, "filters")))
    context.browser.find_element_by_id("filters").find_element_by_xpath("//span[text()='" + filtering + "']").click()


@when('we sort by price "{sorting}"')
def step_impl(context, sorting):
    context.browser.find_element_by_xpath("//span[text()='Sort by:']").click()
    WebDriverWait(context.browser, 10).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Price: " + sorting)))
    context.browser.find_element_by_link_text("Price: High to Low").click()


@then('we log results')
def step_impl(context):
    items = context.browser.find_elements_by_xpath("//div[contains(@class,'s-main-slot')]//div[@data-component-type='s-search-result']")
    for item in items:
        name=item.find_element_by_tag_name("h2")
        print("====Name====")
        print(name.text)
        print("====Link====")
        print(name.find_element_by_tag_name('a').get_attribute("href"))
        prices = item.find_elements_by_xpath('.//span[@class="a-price"]')
        for price in prices:
            print("====Price====")
            print(price.find_element_by_class_name('a-price-symbol').text + price.find_element_by_class_name('a-price-whole').text + '.' + price.find_element_by_class_name("a-price-fraction").text)
    context.browser.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed"} }')


