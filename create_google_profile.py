# Import packages
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# Auto install driver
from webdriver_manager.chrome import ChromeDriverManager

# Build driver
options = Options()

## Google user
google_profile = os.path.join(os.getcwd(), 'profile')
options.add_argument(f'user-data-dir={google_profile}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

google_login_url = 'https://accounts.google.com'

driver.get(google_login_url)

while google_login_url not in driver.current_url:
    time.sleep(3)
    break

driver.close()