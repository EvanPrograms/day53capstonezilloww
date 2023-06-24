#Beautiful soup to parse for search results
#selenium to fill out form

import requests
from bs4 import BeautifulSoup
import re
from time import sleep

# Links for your google docs sheet
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSd5TIRJ2BEdDbS6JZQtBdncYtXuaFFkvtqV6NqC6K_YPu8Cfw/viewform?usp=sf_link"
SHORT_FORM = "https://forms.gle/LgPZtswVejZsmNBJ7"
# Link to area you want to search in Zillow
ZILLOW = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A40.208531982823544%2C%22east%22%3A-104.25978984472654%2C%22south%22%3A39.3282139832305%2C%22west%22%3A-105.86654033300779%7D%2C%22customRegionId%22%3A%22d7ef464966X1-CRq1nrm5lkl5fp_1cce33%22%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A397303%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A1500%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

response = requests.get(ZILLOW, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

links = soup.find_all('a', {"class": "property-card-link"})
zillowplain = "https://www.zillow.com"
zillow_links = []
for tag in links:
    tag = tag.get("href")
    if tag.startswith("/"):
        tag = zillowplain + tag
    zillow_links.append(tag)
zillow_links_true = zillow_links[1::2]
print(zillow_links_true)

prices = soup.find_all(attrs={"data-test": "property-card-price"})
print("Length of list" + " " + str((len(prices))))
house_prices = []
for houses in prices:
    house_prices.append(houses.text.split()[0].replace('+', '').replace('/mo', ''))
print(house_prices)

addresses = soup.find_all("address")
address_list = []
for address in addresses:
    clean_addy = address.text.split(' | ')[-1]
    if clean_addy[0].isdigit() == False:
        clean_addy = re.sub(r'^.*?,', '', clean_addy)
        clean_addy = clean_addy.lstrip()
    address_list.append(clean_addy)
print(address_list)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
SERVICE = Service(CHROME_DRIVER_PATH)



#### MY CODE BELOW ####
driver = webdriver.Chrome(service=SERVICE)
driver.get(FORM)
sleep(1)


for n in range(len(zillow_links_true)):
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(address_list[n])
    price_per_month = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_per_month.send_keys(house_prices[n])
    property_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_link.send_keys(zillow_links_true[n])
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()
    sleep(1)
    submit_again = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_again.click()
    sleep(1)

# view speedsheet: 'https://docs.google.com/forms/d/1bPt4UtaYq0cU2pTx4cpIlKx_zi7GNDue775L34qXaEM/edit')

