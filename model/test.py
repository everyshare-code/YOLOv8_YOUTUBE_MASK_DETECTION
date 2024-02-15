import requests,os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def chrome_drvier():
    driver_path=os.path.join('.','chromedriver.exe')
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def process_thumbnail():
    driver=chrome_drvier()
    # response=requests.get('https://www.youtube.com/watch?v=aECwQqBWfJM&ab_channel=%ED%85%8C%EB%94%94%EB%85%B8%ED%8A%B8TeddyNote')
    driver.get('https://www.youtube.com/watch?v=aECwQqBWfJM&ab_channel=%ED%85%8C%EB%94%94%EB%85%B8%ED%8A%B8TeddyNote')
    driver.implicitly_wait(2)
    player=EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#player'))
    print(player)
    print(type(player))
    print(dir(player))


    # newsList = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, content_xpath)))




process_thumbnail()