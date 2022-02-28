import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


URL_FORM = 'https://forms.gle/zUE4zNv27yVoMDdn7'
ZILLOW_URL = 'https://www.zillow.com/new-york-ny/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22' \
             'usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.54135702539061%2' \
             'C%22east%22%3A-73.41800497460936%2C%22south%22%3A40.559753375988365%2C%22north%22%3A40.8356640592369%7' \
             'D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%' \
             '22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A1198828%7D%2C%22beds%22%3A%7B%22min%' \
             '22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A4500%7D%2C%22ah%22%3A%7' \
             'B%22value%22%3Atrue%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2' \
             'C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value' \
             '%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'

response = requests.get(ZILLOW_URL, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/98.0.4758.109 Safari/537.36',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'})
data = response.text

soup = BeautifulSoup(data, 'html.parser')
prices = soup.find_all(name='div', class_='list-card-price')
addresses = soup.find_all(name='address', class_='list-card-addr')
links = soup.find_all(name='a', class_='list-card-link list-card-link-top-margin')

price_list = [price.getText().replace('/mo', '').replace('+ 1 bd', '') for price in prices]
addresses_list = [address.getText().replace('#', '').replace('(undisclosed Address),', '') for address in addresses]
links_list = []

for link in links:
    href = link['href']
    if 'http' not in href:
        links_list.append(f'https://www.zillow.com{href}')
    else:
        links_list.append(href)

chrome_driver_path = Service('/Users/macbookpro/Desktop/chromedriver')
form_page = webdriver.Chrome(service=chrome_driver_path)

for n in range(len(links_list)):
    form_page.get(URL_FORM)
    time.sleep(2)
    address = form_page.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/'
                                     'div[2]/div/div[1]/div/div[1]/input')
    price = form_page.find_element(By.XPATH,
                                   '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div'
                                   '[2]/div/div[1]/div/div[1]/input')
    link = form_page.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]'
                                  '/div/div[1]/div/div[1]/input')
    submit_button = form_page.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(addresses_list[n])
    price.send_keys(price_list[n])
    link.send_keys(links_list[n])
    submit_button.click()

time.sleep(10)
