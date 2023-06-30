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
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from sys import platform

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
actions = ActionChains(driver)

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
    CONTROL = Keys.COMMAND if platform == 'darwin' else Keys.CONTROL
    user_input = input('Send keys:')
    if user_input == '1':
        actions.send_keys(Keys.ENTER).perform()
    elif user_input == '2':
        actions.send_keys(Keys.TAB).perform()
    elif user_input == '3':
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
    elif user_input == '4':
        actions.key_down(CONTROL).send_keys('a').key_up(CONTROL).perform()
    elif user_input == '5':
        actions.send_keys(Keys.DELETE).perform()
    else:
        actions.send_keys(user_input).perform()
    return user_input

google_login_url = 'https://accounts.google.com'
driver.get(google_login_url)

print(f'''Please check the screenshot file and send the appropriate keys to control the browser.

Your screenshot: {os.path.join(os.getcwd(), 'screenshot.png')}

Some keyboard shortcuts you can use:
1. ENTER
2. TAB
3. SHIFT TAB
4. SELECT ALL (CONTROL A)
5. DELETE
6. Stop the loop of sending keys and exit the program.
''')

while google_login_url in driver.current_url:
    driver.save_screenshot('screenshot.png')
    current_keys = user_send_keys()
    if current_keys == '6':
        break

driver.close()
