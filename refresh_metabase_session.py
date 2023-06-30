# Import packages
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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


# Prepare input
with open('metabase_url.txt', 'r') as f:
    metabase_url = f.read()  # 'https://metabase.your-domain.com'

with open('rentry.txt', 'r') as f:
    rentry = f.read().split()
    rentry_url = rentry[0]  # https://rentry.co/your-url/edit
    rentry_code = rentry[1]  # 123456

# Check profile is working
google_login_url = 'https://accounts.google.com'
driver.get(google_login_url)
time.sleep(3)
if google_login_url in driver.current_url:
    raise Exception('Google profile is not working, please run create_google_profile.py again.')

# Get Metabse session
driver.get(metabase_url)
driver.delete_all_cookies()
driver.get(metabase_url)
time.sleep(3)
login_button = get_element(xpath='//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div/a')
login_button.click()
time.sleep(5)
metabase_session = driver.get_cookie('metabase.SESSION')['value']

driver.get(rentry_url)
# Clear content and click to generate <pre><span>
xpath = '//*[@id="text"]/div/div[5]/div[1]/div/div/div/div[5]'
element = get_element(xpath=xpath)
element.send_keys(Keys.COMMAND + "a") # COMMAND for MacOS and CONTROL for Windows and Ubuntu
time.sleep(1)
element.send_keys(Keys.DELETE)
time.sleep(1)
element.click()
time.sleep(3)

# Input Credentials
element = get_element(xpath='//*[@id="text"]/div/div[5]/div[1]/div/div/div/div[5]/pre/span')
element.send_keys(metabase_session)
time.sleep(3)

# Click edit code
element = get_element(xpath='//*[@id="id_edit_code"]')
element.click()
element.send_keys(rentry_code)
time.sleep(3)

# Save
get_element(xpath='//*[@id="submitButton"]').click()
time.sleep(3)

# Wait to see success message
element = get_element(xpath='/html/body/div/div/div[1]/div[1]/div/ul/li')

driver.close()