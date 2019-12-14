from selenium.webdriver.common.keys import Keys
import os
from multiprocessing import Process

import time

from app import Bot, log_info
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_driver = '/usr/local/bin/chromedriver'

# Get details
log_info("starting..")

# Get a list of proxies


def get_proxies(driver):
    url = "https://free-proxy-list.net/"
    driver.get(url)
    proxies = []
    proxy_table = driver.find_elements_by_xpath(
        '//*[@id="proxylisttable"]/tbody/tr')
    for x in proxy_table:
            row_data = x.find_elements_by_tag_name('td')
            proxy = row_data[0].text+":"+row_data[1].text
            proxies.append(str(proxy))
    return proxies

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)

# proxies = get_proxies(driver)
driver.close()

# print proxies
bot = Bot(chrome_driver)

url = "https://www.courir.com/fr/p/nike-air-force-1-low-undr-1462220.html"

bot.buy_product(url)

# time.sleep(5)
# Process.start(bot.login())

