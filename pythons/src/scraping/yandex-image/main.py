import time
import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)
driver.maximize_window()

driver.get("https://yandex.ru/images/search?text=%EC%9A%B0%EC%98%81%EC%9A%B0")
time.sleep(3)

body = driver.find_element(By.TAG_NAME, "body")
for _ in range(5):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

html = driver.page_source
bs = BeautifulSoup(html, "html.parser")
result = bs.find_all("div", {"class": "serp-item"})
for item in result:
    try:
        data = json.loads(item["data-bem"])
        url = data["serp-item"]["img_href"]
        filename = url.split("/")[-1]
        urllib.request.urlretrieve(url, f"images/{filename}")
    except Exception as e:
        print(e, filename)
