from selenium import webdriver
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

# building this test to mimic this one: https://app.saucelabs.com/tests/430b8dd272c14d5b85888d152cf238e6?auth=67726b6af21a8b008d4eef513de8ba4b#106

username = os.getenv("SAUCE_USER") 
access_key = os.getenv("SAUCE_KEY")
sauce_client = SauceClient(username, access_key)

chrome_desired_caps = {
    'platformName': "mac 10.15",
    'browserName': "chrome",
    'browserVersion': "latest",
    # 'moz:firefoxOptions': {
    #     'profile': "UEsDBBQAAAAIAGNiU1FuBzPD5wMAAKwNAAAHABwAdXNlci5qc1VUCQADquaNX6vmjV91eAsAAQT1AQAABBQAAACdV01v4zYQvfdXFD61QE0km+6le0qzKVBg0SzWCPZIUORIYkyRLD+s+N93KEprx5Yppydb8gw58+bNm3H04Kh1UP+yqpzp8Yl4VsPwXeqGdEz1zAEBzSoFYvXbzzVTHn799FM8eAoW0MYaF5JLC0yFNj8TNNpJvuCvIfTGbUkbgiW2lb7dr9PPlnm/VqCb0KLjh48f37pNATtgAj8EBOABxF/S+XCPsXAF6BZcPA3XdJjXK+WtMx1Qz520gbqoaZBdcrm7mb8osMoThEM/6QdlPMxnM1kL02tlmMC7NGsSsK3pv7egN4hWQmre3WJQNvh0Ge2MYGoBe9gFY5Qn4Jxx3Ghv1DHcM+lPHjn/62wFVLFJSeTw1niRRrSl0Vf6OehMgHXpMi8bbXSyhK4Ctxke/QWUwHXSe7w/3VGzqAJpwKDx7Xw1PGTrYJDNDnzEyteYC+WO+bZcSSX1lhgLmsJrAKeZSnR8dw/UiZjfop6/rIdKOLnDZ8Y5ICGjRog8EppycMHPQvaDa9JbxfYgHm9vNv8Y5H4i5+/zxvhKPOnvUiND/e0NkXiRef72BT1WrDIx/FEpprer867JCVGmFH3xCEaKU+Yancf2aiXCjbakb2UAJX3AA/6N0l3icqLMVgYy6sHUN5hcIk0RAMWwMNjC5WbxqfOiJS3y3uLZtAfFkwZEl0q6Okk5VVtnjkWLBQaiEdp6/4wm71bCaJMYPBbDAx6dDHtkigL8RnxwkgdqnGykptYoyfdlqmroUTjImE+hmm8CzSeT9HITq7Gxvg4v7wcyXqf8s8cUM/7RnWNhUlHQ8oL+HvoQ0+wH/p43oqlrtIM1s9YTZJ/pabWno0bM684EO/d25M98tOd8KLNtOvfpYfP1yPRmnvXYIqh8we1HjR1sPyzZFiOYgHt8/nJP7gg71PIchRe2Y3kUFifCacWmVirTbZrwnKFg7GCdGMPU+qrt4DxnBy/DpC8GmDshhVY+/qioLAbzOYvNhiPPkq7dLu8CT8jIxbMrZfh20MCrKuaBOd6ONFvaMzqSm4GI2Nli9bAprqLuG+IYHEpOinkBPtOsU7G6m2dCFvf11K1IpxAvzPopmNH2ghKNS93yNteBkIw0nV1PAyYj8ljA7Wg4+2F1OAxnVLk4jIMi2ola84Ef9Z3J03RYFP/WD3mXu7jCjmORDoIoEHrd0DRiFojVAk5k3gLffs6a+Gf+5f0TkzAhZIqYLQyb2X8W//cfhTJNk16Oq25xvBz135DxA+oqC7KSKjFWy6YNamGgngEwdQPpcJcc2LhKi6qDk6QP60/aa5HduHQu7D+H5le1jzavDYfN5D9QSwECHgMUAAAACABjYlNRbgczw+cDAACsDQAABwAYAAAAAAABAAAApIEAAAAAdXNlci5qc1VUBQADquaNX3V4CwABBPUBAAAEFAAAAFBLBQYAAAAAAQABAE0AAAAoBAAAAAA=",
    #     # 'args': [
    #     #     "-start-debug-server",
    #     #     "9222"
    #     # ]
    # },
    'sauce:options': {
        'build':"sauce_debug10/20:chrome",
        'name': "Slow Selenium CMDs",
        'parentTunnel': "huluadmin",
        'tunnelIdentifier': "ha-parent-robocop-saucelabs",
        # 'seleniumVersion': "3.141.59",
        'screenResolution': "2360x1770",
        'username': username,
        'accessKey': access_key,
        # 'extendedDebugging': True,
    },
}

firefox_desired_caps = {
    'platformName': "mac 10.15",
    'browserName': "firefox",
    'browserVersion': "latest",
    'moz:firefoxOptions': {
        'profile': "UEsDBBQAAAAIAGNiU1FuBzPD5wMAAKwNAAAHABwAdXNlci5qc1VUCQADquaNX6vmjV91eAsAAQT1AQAABBQAAACdV01v4zYQvfdXFD61QE0km+6le0qzKVBg0SzWCPZIUORIYkyRLD+s+N93KEprx5Yppydb8gw58+bNm3H04Kh1UP+yqpzp8Yl4VsPwXeqGdEz1zAEBzSoFYvXbzzVTHn799FM8eAoW0MYaF5JLC0yFNj8TNNpJvuCvIfTGbUkbgiW2lb7dr9PPlnm/VqCb0KLjh48f37pNATtgAj8EBOABxF/S+XCPsXAF6BZcPA3XdJjXK+WtMx1Qz520gbqoaZBdcrm7mb8osMoThEM/6QdlPMxnM1kL02tlmMC7NGsSsK3pv7egN4hWQmre3WJQNvh0Ge2MYGoBe9gFY5Qn4Jxx3Ghv1DHcM+lPHjn/62wFVLFJSeTw1niRRrSl0Vf6OehMgHXpMi8bbXSyhK4Ctxke/QWUwHXSe7w/3VGzqAJpwKDx7Xw1PGTrYJDNDnzEyteYC+WO+bZcSSX1lhgLmsJrAKeZSnR8dw/UiZjfop6/rIdKOLnDZ8Y5ICGjRog8EppycMHPQvaDa9JbxfYgHm9vNv8Y5H4i5+/zxvhKPOnvUiND/e0NkXiRef72BT1WrDIx/FEpprer867JCVGmFH3xCEaKU+Yancf2aiXCjbakb2UAJX3AA/6N0l3icqLMVgYy6sHUN5hcIk0RAMWwMNjC5WbxqfOiJS3y3uLZtAfFkwZEl0q6Okk5VVtnjkWLBQaiEdp6/4wm71bCaJMYPBbDAx6dDHtkigL8RnxwkgdqnGykptYoyfdlqmroUTjImE+hmm8CzSeT9HITq7Gxvg4v7wcyXqf8s8cUM/7RnWNhUlHQ8oL+HvoQ0+wH/p43oqlrtIM1s9YTZJ/pabWno0bM684EO/d25M98tOd8KLNtOvfpYfP1yPRmnvXYIqh8we1HjR1sPyzZFiOYgHt8/nJP7gg71PIchRe2Y3kUFifCacWmVirTbZrwnKFg7GCdGMPU+qrt4DxnBy/DpC8GmDshhVY+/qioLAbzOYvNhiPPkq7dLu8CT8jIxbMrZfh20MCrKuaBOd6ONFvaMzqSm4GI2Nli9bAprqLuG+IYHEpOinkBPtOsU7G6m2dCFvf11K1IpxAvzPopmNH2ghKNS93yNteBkIw0nV1PAyYj8ljA7Wg4+2F1OAxnVLk4jIMi2ola84Ef9Z3J03RYFP/WD3mXu7jCjmORDoIoEHrd0DRiFojVAk5k3gLffs6a+Gf+5f0TkzAhZIqYLQyb2X8W//cfhTJNk16Oq25xvBz135DxA+oqC7KSKjFWy6YNamGgngEwdQPpcJcc2LhKi6qDk6QP60/aa5HduHQu7D+H5le1jzavDYfN5D9QSwECHgMUAAAACABjYlNRbgczw+cDAACsDQAABwAYAAAAAAABAAAApIEAAAAAdXNlci5qc1VUBQADquaNX3V4CwABBPUBAAAEFAAAAFBLBQYAAAAAAQABAE0AAAAoBAAAAAA=",
        # 'args': [
        #     "-start-debug-server",
        #     "9222"
        # ]
    },
    'sauce:options': {
        'build':"sauce_debug10/20",
        'name': "Slow Selenium CMDs",
        'parentTunnel': "huluadmin",
        'tunnelIdentifier': "ha-parent-robocop-saucelabs",
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

driver = webdriver.Remote(command_executor="https://ondemand.us-west-1.saucelabs.com/wd/hub", desired_capabilities=firefox_desired_caps)
try:
    wait = WebDriverWait(driver, 12)
    find_by_css = lambda css_selector: wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
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
    action_btn = find_by_css(".navigation__action-button")
    action_btn.click()
    ready_state_check(driver)
    ready_state_check(driver)
    email_field = find_by_css("*[name='email']")
    email_field.send_keys(os.getenv("APP_USER"))
    pw_field = find_by_css("*[name='password']")
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

    find_by_css(".cu-hub-collections-home")
    # do something with js?
    # driver.execute_script(cmd 66. omitted god awful long uglified js)
    ready_state_check(driver)

    global_nav_live = find_by_css("[data-automationid='globalnav-live']")
    # driver.execute_script(cmd 68. omitted god awful long uglified js)
    global_nav_live
    # driver.execute_script(cmd 69. omitted god awful long uglified js)
    global_nav_live
    # driver.execute_script(cmd 73. omitted god awful long uglified js)
    # GET some ELEMENT? Can't find element ID in selenium log...
    # Click aforementioned mystery element, looks like they're clickingthe LIVE button?
    global_nav_live.click()

    global_home = find_by_css(".GlobalNavigation__logo")
    global_home.click()
    ready_state_check(driver)
    ready_state_check(driver)

    maximize_pip = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".MaximizeButton")))
    maximize_pip.click()

    # OK finish test
    print("Job finished OK")
    sauce_client.jobs.update_job(driver.session_id, passed=True)
    driver.quit()
except Exception:
    sauce_client.jobs.update_job(driver.session_id, passed=False)
    print(traceback.format_exc())
    driver.quit()
