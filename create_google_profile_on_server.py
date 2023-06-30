# Import packages
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# Bypass CloudFlare in headless mode (https://github.com/diprajpatra/selenium-stealth)
from selenium_stealth import stealth
# Auto install driver
from webdriver_manager.chrome import ChromeDriverManager

# Build driver
options = Options()

## Fix error on Linux server (Ubuntu)
## selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally
options.add_argument('--no-sandbox')

## Google user
google_profile = os.path.join(os.getcwd(), 'profile')
options.add_argument(f'user-data-dir={google_profile}')

## Hide or show browser (If hide browser, we can be blocked by CloudFlare or firewall)
headless_mode = True

if headless_mode:
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

if headless_mode:
    stealth(driver=driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )


def get_element(xpath, timeout=10):
    _element = WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return _element


def user_send_keys():
    guide = 'Input keys: type text or use shortcut number\n1.ENTER\n2.TAB\n3.CONTROL A\n4.DELETE\n6.Stop'
    keys_dict = {'1': Keys.ENTER, '2': Keys.TAB, '3': Keys.CONTROL + 'a', '4': Keys.DELETE}
    user_input = input(guide)
    if user_input in keys_dict:
        keys = keys_dict[user_input]
    else:
        keys = user_input
    actions.send_keys(keys).perform()
    return user_input


actions = ActionChains(driver)

google_login_url = 'https://accounts.google.com'

driver.get(google_login_url)

while google_login_url in driver.current_url:
    driver.save_screenshot('screenshot.png')
    current_keys = user_send_keys()
    if current_keys == '6':
        break
    time.sleep(3)

driver.close()
