import os
import time
from datetime import datetime
from http.cookies import SimpleCookie

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


def edit_rentry(url_id, text, edit_code):
    '''
    Edit Rentry with API
    Reference: https://github.com/radude/rentry/blob/master/rentry
    :param url_id: URL path without Rentry domain
    :param text: The content you want to update
    :param edit_code: The Edit code
    '''
    # We need to keep one session and use csrftoken to send API
    session = requests.Session()
    cookie = SimpleCookie()
    cookie.load(vars(session.get('https://rentry.co'))['headers']['Set-Cookie'])

    csrftoken = cookie['csrftoken'].value
    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'edit_code': edit_code,
        'text': text
    }

    session.post(url=f'https://rentry.co/api/edit/{url_id}', data=payload, headers={'Referer': 'https://rentry.co'})


def get_metabase_session(metabase_url, button_xpath, headless_mode=True):
    '''
    Get Metabase Session with Google profile that has been logged-in with your Google Workspace account
    :param metabase_url: Your Metabase URL
    :param button_xpath: Use Chrome Developer Tool to copy the "Sign in with Google" button XPATH
    :param headless_mode: Show or hide browser when getting Metabase Session
    :return: Metabase Session
    '''
    options = Options()

    # Fix error on Linux server (Ubuntu)
    options.add_argument('--no-sandbox')

    # Google user
    google_profile = os.path.join(os.getcwd(), 'profile')
    options.add_argument(f'user-data-dir={google_profile}')

    # Hide or show browser (If hide browser, we can be blocked by CloudFlare or firewall)
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
        _element = WebDriverWait(driver=driver, timeout=timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return _element

    # Check profile is working
    google_login_url = 'https://accounts.google.com'
    driver.get(google_login_url)
    time.sleep(3)
    if google_login_url in driver.current_url:
        raise Exception('Google profile is not working, please run the create_google_profile script.')

    # Get Metabse session
    driver.get(metabase_url)
    driver.delete_all_cookies()
    driver.get(metabase_url)
    time.sleep(3)
    login_button = get_element(xpath=button_xpath)
    login_button.click()
    time.sleep(5)
    metabase_session = driver.get_cookie('metabase.SESSION')['value']
    driver.close()
    return metabase_session


if __name__ == '__main__':
    with open('rentry.txt', 'r') as f:
        rentry = f.read().split()
        url_id = rentry[0]
        edit_code = rentry[1]
    with open('metabase.txt', 'r') as f:
        metabase = f.read().split()
        metabase_url = metabase[0]
        button_xpath = metabase[1]

    print(f'Start refresh Metabase session {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    metabase_session = get_metabase_session(metabase_url=metabase_url, button_xpath=button_xpath)
    print(metabase_session)
    print('Update Metabase session to Rentry')
    edit_rentry(url_id=url_id, text=metabase_session, edit_code=edit_code)