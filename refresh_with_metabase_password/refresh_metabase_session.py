import os
import time
from datetime import datetime
from http.cookies import SimpleCookie

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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


def get_metabase_session(metabase_url, username, password, headless_mode=True):
    '''
    Get Metabase Session with Metabase password
    :param metabase_url: Your Metabase URL
    :param headless_mode: Show or hide browser when getting Metabase Session
    :return: Metabase Session
    '''
    options = Options()

    # Fix error on Linux server (Ubuntu)
    options.add_argument('--no-sandbox')

    # Hide or show browser (If hide browser, we can be blocked by CloudFlare or firewall)
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

    # Get Metabse session
    driver.get(metabase_url)
    time.sleep(3)
    actions.send_keys(username).perform()
    time.sleep(1)
    actions.send_keys(Keys.TAB).perform()
    time.sleep(1)
    actions.send_keys(password).perform()
    time.sleep(1)
    actions.send_keys(Keys.ENTER).perform()
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
        username = metabase[1]
        password = metabase[2]

    print(f'Start refresh Metabase session {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    metabase_session = get_metabase_session(metabase_url=metabase_url, username=username, password=password)
    print(metabase_session)
    print('Update Metabase session to Rentry')
    edit_rentry(url_id=url_id, text=metabase_session, edit_code=edit_code)