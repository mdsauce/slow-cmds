from selenium import webdriver
import selenium.common.exceptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from sauceclient import SauceClient
import traceback
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("SAUCE_USER") 
access_key = os.getenv("SAUCE_KEY")
sauce_client = SauceClient(username, access_key)

desired_caps = {
    'platformName': "mac 10.15",
    'browserName': "firefox",
    'browserVersion': "81",
    'moz:firefoxOptions': {
        'profile': "UEsDBBQACAAIAPZxT1EAAAAAAAAAABINAAAHACAAdXNlci5qc1VUDQAHAbyIX7K+iF+xvohfdXgLAAEE9QEAAAQUAAAAnVZNb9s4EL33Vyx86gJrImnaS3vKpimwQNAENYIeCYocSYwpkssPK/73OxSl2LFkKdlTInlIzbx5895ED45aB+XHVeFMi0/EsxK6/6WuSMNUyxwQ0KxQIFZ//VEy5eHPbx/i4aRgAWOscSEdqYGpUOdngkE7yRfOawitcVtSh2CJraWv9+v0s2XerxXoKtR48NOXL6+PDQk7YAL/CAjAA4gf0vlwjblwBXgsuHiarmmwrmfKa2caoJ47aQN1UdMgm3Tk6mL6Q4EVniAc+l7fKONhupohWphWK8MEfkuzKgFbm/Z3DXqDaCWkpo9bTMoGnz5GGyOYWsAedsEY5Qk4Zxw32ht1DPe4fC8rbTSi1kBTgNt0j/5MMuAa6b3EAMS3ZFEFUoHB4Mvpoj3k6GCQNA58RIBLrIhyx3w9D5iSekuMBU3hOYDTTKWuv5tqZer/r6inP9ZCIZzc4TPjHLDvUSNEHnlDObjgJyF7aan0VrE9iNvLi81PgxRLHPg8HYyvxL3+LTUSwV9eEIkfMo+/7vDEihUmhq+FYnq7GpMzF0SZUvTJIxgpT5l7NM7t2UqEG2NJW8sASvqAF/wbpTtHmcSXrQykH7uBnlhcIs0sAIphY3BS5jnpE8GjJTWOl8W7aQuKp1GLLrV0dVJy6rbOHIsWGwxEI7Tl/hFD3i040aaZu51ND3h0MuyRKQrwP+KDkzxQ42QlNbVGSb6fp6qGFueT9PXMdPNVovlmkl5uYtEP1kP38roj49sEdvKa2YpfprNvTGoKRp6RucMcYpltx9/xIJqyxDhYM2s9QfaZlhZ72mvEtO4MsHNve/5MZzvmwzzbhnvvbzYPR6EX06zHEUHlC25PstJ2sZ+WYmczGIC7fby7JleEHXo5RuGJ7Vh2nFmRPu3YMErzdBuMlDMUjB2sE2OYWr/JhMc1O3jqDHU2wTwJKbX564+aymIw37PYbDjyLOna5bLl3iMjF+8ulOHbTgPf1DEPzPG6p9mSnTckDwMRsbGz3cOheBN1XxHHoCk5KaYFeKRZp2J1Nc2ELO7rYVqRTiGe8fohmT72jBL1u9Py0tSAkIxUjV0PBpMRuZ3B7cicfbc6HMwZVS52djCLdqLWdOJHc2eym3b72D/6Jq9MZzfF3hZpJ4gCodcVTRazQKwa0JF5DXz7PWvi3/mX9zsmYULIlDFbMJvJBf7/Lu7KVFV62W+Us/ZyNH9dxTeoqyzIQqrEWC2rOqgFQx0BMEwDaXCX7Ni4Souqg5OiD+tP2muR3bh0Luw/h+FXpY82rw0vm8l/UEsHCAujrKTJAwAAEg0AAFBLAwQUAAgACAD2cU9RAAAAAAAAAADVAAAAEgAgAF9fTUFDT1NYLy5fdXNlci5qc1VUDQAHAbyIX7K+iF+Dv4hfdXgLAAEE9QEAAAQUAAAAY2AVY2dgYmDwTUxW8A9WiFCAApAYAycQGwHxYiAG8a8yEAUcQ0KCoEyQjhlAbIumhBEhLpqcn6uXWFCQk6pXWJpYlJhXkpmXylCob2BgYWhtmmZhkZSaZGDtllmUmpZfYe1q5mbk5GxsoOvsauGoa+JmbKprYW5kqets5GZoYenq5OToaMkAAFBLBwhRZYXpiAAAANUAAABQSwECFAMUAAgACAD2cU9RC6OspMkDAAASDQAABwAgAAAAAAAAAAAApIEAAAAAdXNlci5qc1VUDQAHAbyIX7K+iF+xvohfdXgLAAEE9QEAAAQUAAAAUEsBAhQDFAAIAAgA9nFPUVFlhemIAAAA1QAAABIAIAAAAAAAAAAAAKSBHgQAAF9fTUFDT1NYLy5fdXNlci5qc1VUDQAHAbyIX7K+iF+Dv4hfdXgLAAEE9QEAAAQUAAAAUEsFBgAAAAACAAIAtQAAAAYFAAAAAA==",
    },
    'sauce:options': {
        'name': "Growing Build Duration Test",
        'parentTunnel': "huluadmin",
        'tunnelIdentifier': "ha-parent-robocop-saucelabs",
        'build':"sauce_debug",
        'seleniumVersion': "3.141.59",
        'screenResolution': "2360x1770",
        'username': username,
        'accessKey': access_key,
        # 'extendedDebugging': True,
    },
}

def ready_state_check(driver):
    """
    checks if readyState has fired.
    """
    driver.execute_script("return document.readyState")

driver = webdriver.Remote(command_executor="https://ondemand.us-west-1.saucelabs.com/wd/hub", desired_capabilities=desired_caps)
try:
    wait = WebDriverWait(driver, 25)
    driver.maximize_window()
    driver.get("https://develop.prod.hulu.com")
    # some cookie manipulation goes here, but doesn't look critical.
    # Update: I was wrong, was critical. keep geo in there
    # May also change from build to build
    # driver.add_cookie({'name': "SI_5pdZmGAW2IbA4p7_intercept", 'value': "1", 'secure': False, 'domain': "develop.prod.hulu.com", 'path': "/", 'httpOnly': False})
    driver.add_cookie({'name': "geo", 'value': "34.0418%26-118.4692%261602026251171", 'secure': False, 'domain': "develop.prod.hulu.com", 'path': "/", 'httpOnly': False})
    ready_state_check(driver)
    ready_state_check(driver)
    driver.refresh()
    ready_state_check(driver)
    ready_state_check(driver)
    driver.get_cookies()

    # does something to the modals + banner? looks non-vital
    # driver.execute_script("window.localStorage.setItem('_hulu_welcome_modal','1000000');")
    # driver.execute_script("window.localStorage.setItem('_hulu_banner_notifications','{'chrome-retirement':2,'legal-updates':1}');")
    driver.refresh()
    ready_state_check(driver)

    # trigger login modal and login
    driver.find_element_by_css_selector(".navigation__action-button").click()
    ready_state_check(driver)
    ready_state_check(driver)
    email_field = driver.find_element_by_css_selector("*[name='email']")
    email_field.send_keys(os.getenv("APP_USER"))
    pw_field = driver.find_element_by_css_selector("*[name='password']")
    pw_field.send_keys(os.getenv("APP_PW"))
    pw_field.send_keys(Keys.ENTER)
    ready_state_check(driver)
    ready_state_check(driver)

    # select a profile
    # Max is branching from Hulu's steps here. They use an API to progrommatically create/update the profile
    # with that said I am still repro-ing the issue.
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Site NOAH LIVE")]'))).click()
    except TimeoutException as e:
        pass
    # wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "New_Profile")]'))).click()

    home_thing = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cu-hub-collections-home")))
    # do something with js?
    # driver.execute_script(cmd 66. omitted god awful long uglified js)
    ready_state_check(driver)

    LIVE_BTN_ID = "[data-automationid='globalnav-live']"
    global_nav_live = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LIVE_BTN_ID)))
    # driver.execute_script(cmd 68. omitted god awful long uglified js)
    global_nav_live = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LIVE_BTN_ID)))
    # driver.execute_script(cmd 69. omitted god awful long uglified js)
    global_nav_live = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LIVE_BTN_ID)))
    # driver.execute_script(cmd 73. omitted god awful long uglified js)
    # GET some ELEMENT? Can't find element ID in selenium log...
    # Click aforementioned mystery element, looks like they're clickingthe LIVE button?
    global_nav_live.click()


    # OK finish test
    print(">>>Job finished OK<<<")
    sauce_client.jobs.update_job(driver.session_id, passed=True)
    driver.quit()
except Exception:
    sauce_client.jobs.update_job(driver.session_id, passed=False)
    print(traceback.format_exc())
    driver.quit()
