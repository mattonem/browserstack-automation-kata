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
from behave.fixture import fixture, use_fixture_by_tag
from pprint import pprint

def before_feature(context, feature):
	now = datetime.now()
	context.buildName = now.strftime("%m/%d/%Y, %H:%M:%S")


@fixture
def browser_chrome(context):
	context.caps = { 
	"os" : "Windows",
	"os_version" : "10",
	"browser" : "Chrome",
	"browser_version" : "latest",
	"browserstack.local" : "false",
	"browserstack.selenium_version" : "3.141.59",
	"build" : context.buildName
	}
	context.browser = ini_driver(context.caps)
	yield context
	context.browser.quit()

@fixture
def browser_firefox(context):
	context.caps = { 
	"os" : "Windows",
	"os_version" : "10",
	"browser" : "Firefox",
	"browser_version" : "latest",
	"browserstack.local" : "false",
	"browserstack.selenium_version" : "3.141.59",
	"build" : context.buildName
	}
	context.browser = ini_driver(context.caps)
	yield context
	context.browser.quit()

fixture_registry = {
    "fixture.browser_chrome":   browser_chrome,
    "fixture.browser_firefox":   browser_firefox,
}

def ini_driver(caps):
	username = os.getenv("BROWSERSTACK_USERNAME")
	access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
	caps["browserstack.user"] = username
	caps["browserstack.key"] = access_key
	caps["project"] = 'CE-Challenge'
	caps["name"] = "amazon-scroller-behave-" + caps["browser"] 

	options = Options()
	profile = webdriver.FirefoxProfile()
	profile.set_preference("dom.disable_beforeunload", True)
	profile.update_preferences()
	options.profile = profile
	browser = webdriver.Remote(
		command_executor="https://hub-cloud.browserstack.com/wd/hub",
		desired_capabilities=caps,
		options=options)
	browser.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed"} }')
	return browser


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)
