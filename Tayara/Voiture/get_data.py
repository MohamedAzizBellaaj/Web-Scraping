import json
import logging
from functools import wraps

import requests
from bs4 import BeautifulSoup

DATA_FILE = "data.json"
LINKS_FILE = "links.json"


def log_exception(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logging.exception("...")

    return _wrapper


@log_exception
def get_title(soup) -> str:
    return soup.select_one("main > div > div > div > h1").text


@log_exception
def get_price(soup) -> str:
    return soup.select_one("data")["value"]


@log_exception
def get_location(soup) -> str:
    return (
        soup.select_one(
            "div > main > div > div > div > div > span > div:nth-child(2) > span"
        )
        .text.split(",")[0]
        .strip()
    )


@log_exception
def get_description(soup) -> str:
    return soup.select_one("main > div > div > div:nth-child(3) > p").text.replace(
        "\n", " "
    )


def write_json(new_data, filename=DATA_FILE):
    with open(DATA_FILE, "r+") as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=2, ensure_ascii=False)


with open(DATA_FILE, "w") as file:
    json.dump([], file)

with open(LINKS_FILE, "r") as file:
    links = json.load(file)

for link in links:
    html = requests.get(link).text
    soup = BeautifulSoup(html, "lxml")
    data = {}
    data["title"] = get_title(soup)
    data["price"] = get_price(soup)
    data["location"] = get_location(soup)
    data["description"] = get_description(soup)
    data["link"] = link
    try:
        ul = soup.select_one("main > div > div > div:nth-child(4) > ul")
        for criteria in ul.findAll("li"):
            key = criteria.select_one("div > span > span:nth-child(1)").text
            value = criteria.select_one("div > span > span:nth-child(2)").text
            data[key] = value
    except Exception:
        pass
    finally:
        write_json(data)
