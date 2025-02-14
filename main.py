import csv
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


ROOT_FOLDER = Path(__file__).parent
EXECUTABLE_PATH = ROOT_FOLDER / 'bin' / 'chromedriver.exe'


def make_chrome_driver(*options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()

    if chrome_options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_sevice = Service(
        executable_path=EXECUTABLE_PATH,
    )

    browser = webdriver.Chrome(
        service=chrome_sevice,
        options=chrome_options,
    )

    return browser


options = ()
browser = make_chrome_driver(*options)

browser.get('https://www.terabyteshop.com.br/monitores')

# Closing the banner.
sleep(5)
banner = browser.find_element(By.CLASS_NAME, 'modal-content')
button = banner.find_element(By.TAG_NAME, 'button')
button.send_keys(Keys.ENTER)

# Fetching product information.
results = browser.find_element(By.CLASS_NAME, 'products-grid')
items = results.find_elements(By.CLASS_NAME, 'product-item')

# List of dictionaries.
list_of_dicts = []

# Opening a new .csv file.
with open('monitors_and_prices.csv', 'w', newline='', encoding='utf8') as file:

    for item in items:
        try:
            # Fetching each product and adding them to the list of dictionaries
            # to send them to a .csv file.
            product_name = item.find_element(By.TAG_NAME, 'h2').text
            unformatted_price = item.find_element(
                By.CLASS_NAME, 'product-item__new-price').text
            formatted_price = unformatted_price[3:-8].replace(
                '.', '').replace(',', '.')

            product_information = dict(
                Product=product_name, Price=formatted_price)
            list_of_dicts.append(product_information)

        except Exception:
            break

    # Saving to .csv
    names_columns = list_of_dicts[0].keys()
    writer = csv.DictWriter(
        file,
        names_columns,
    )
    writer.writeheader()
    writer.writerows(list_of_dicts)
