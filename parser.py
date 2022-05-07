from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
import time

from selenium.webdriver.chrome.options import Options


def get_html(url, tag, clas):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(r'C:\Users\user\webdriver\chromedriver.exe', options=options)
    driver.get(url)
    html = driver.page_source
    driver.close()
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(tag, class_=clas)
    return items


def add_to_db(lst, title_of_table):
    for el in lst:
        connection = sqlite3.connect("steam_db.sqlite")
        cursor = connection.cursor()
        cursor.execute(f"""
            INSERT INTO '{title_of_table}' (title, quantity)
            VALUES (?, ?)
        """, (el['title'], el['quantity']))
        connection.commit()



def parser_cycle(sec=2):
    if sec >= 2:
        while True:
            for item in get_html(f'https://steamcommunity.com/market/search?q=#p1_popular_desc', 'div', 'market_listing_row'):
                lst = []
                lst.append({
                    "title": item.find('span', class_="market_listing_item_name").get_text(),
                    "quantity": item.find('span', class_="market_listing_num_listings_qty").get_text(),
                })
                add_to_db(lst, 'steam')
            time.sleep(sec)
    else:
        raise ValueError("You don't need to use the parser more than once every second")


def parser_pages(default, x):
    page = default
    while page <= x:
        for item in get_html(f'https://steamcommunity.com/market/search?q=#p{page}_popular_desc', 'div', 'market_listing_row'):
            lst = []
            lst.append({
                "title": item.find('span', class_="market_listing_item_name").get_text(),
                "quantity": item.find('span', class_="market_listing_num_listings_qty").get_text(),
            })
            add_to_db(lst, 'steam')
        page += 1


parser_pages(1, 10)



