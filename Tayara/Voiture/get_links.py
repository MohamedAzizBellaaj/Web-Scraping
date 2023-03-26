import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

LINKS_FILE = "links.json"


def write_json(new_data, filename=LINKS_FILE):
    with open(LINKS_FILE, "r+") as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=2)


with open(LINKS_FILE, "w") as file:
    json.dump([], file)
browser = webdriver.Chrome()
browser.get(
    "https://www.tayara.tn/search/?q=VOITURE&category=V%C3%A9hicules&subCategory=Voitures"
)
nb_items = 0
last_height = browser.execute_script("return document.body.scrollHeight;")
target_count = 10000
time.sleep(10)
while nb_items < target_count:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_height = browser.execute_script("return document.body.scrollHeight;")
    if new_height == last_height:
        break
    last_height = new_height
    elements = browser.find_elements(By.CSS_SELECTOR, "article > a")
    for element in elements:
        nb_items += 1
        write_json(element.get_attribute("href"))
browser.quit()
