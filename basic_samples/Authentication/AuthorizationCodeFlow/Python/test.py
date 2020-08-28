"""This script uses Selenium to perform a test of the program.py script"""

import configparser
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .program import main


class AuthPKCEPythonSampleTests(unittest.TestCase):
    """Tests for the Authorization Code + PKCE Python script"""

    @classmethod
    def test_main(cls):
        """Tests the program.py script using a Selenium script for browser actions"""

        main(selenium_script)


def selenium_script(auth_url):
    """Automatically performs browser actions for login"""

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get Config
    username = config.get('Test', 'Username')
    password = config.get('Test', 'Password')

    # Open Chrome Webdriver, go to Auth page
    print()
    print('Selenium 1: Open Chrome WebDriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(auth_url)
    time.sleep(2)

    # Use Personal Account (Must be enabled on Tenant)
    print()
    print('Selenium 2: Choose Personal Account')
    browser.find_element_by_xpath(
        xpath='descendant::a[@title="Personal Account"]').click()
    time.sleep(2)

    # Enter Username and submit
    print()
    print('Selenium 3: Enter Username')
    browser.find_element_by_xpath(
        '//*[@id="i0116"]').send_keys(username)
    browser.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    time.sleep(2)

    # Enter Password and submit
    print()
    print('Selenium 4: Enter Password')
    browser.find_element_by_xpath(
        '//*[@id="i0118"]').send_keys(password)
    browser.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    time.sleep(2)

    # Click Next to continue past prompt
    print()
    print('Selenium 5: Continue past prompt')
    elem = browser.find_element_by_xpath('//*[@id="idSIButton9"]')
    try:
        browser.set_page_load_timeout(2)
        elem.click()
    except Exception:
        print('Ignore time out, start the server...')


if __name__ == '__main__':
    unittest.main()
