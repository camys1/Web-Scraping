import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

DOC_URL = "https://docs.google.com/forms/d/e/1FAIpQLSetXtGEPMoSP0Dn4SD3AGV7yFxhfjjSnS-qIFefhaF5hDT7pQ/viewform?usp=header"
ZILLOW_ENDPOINT = "https://www.zillow.com/new-york-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-74.474065765625%2C%22east%22%3A-73.485296234375%2C%22south%22%3A40.33401536473403%2C%22north%22%3A41.05971144017737%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A581444%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22usersSearchTerm%22%3A%22New%20York%20NY%22%7D"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36", "Accept-Language":"en-US,en;q=0.9"}

class ZillowData:
    def __init__(self):
        self.response = requests.get(url=ZILLOW_ENDPOINT, headers=HEADERS)
        if self.response.status_code == 200:
            print("Request successful!")
        else:
            print(f"Failed to retrieve data: {self.response.status_code}")
        self.soup = BeautifulSoup(self.response.text, "lxml")
        self.listings = self.soup.select('.property-card-data')  
        self.link_list = [listing.find_all("a") for listing in self.listings]  
        self.price_list = self.soup.select('span[data-test="property-card-price"]')
        self.url = []
        self.address = []
        self.price = []

    def get_endpoints(self):
        
        urls = []
        for link in self.link_list:
            link_url = link[0].get("href")
            if link_url.startswith("https"):
                urls.append(link_url)
            else:
                urls.append("https://www.zillow.com" + link_url)
        # print(f"Found URLs: {urls}")  # Debug print
        return urls

    def get_address(self):
        # Get the address of each listing
        addresses = []
        for link in self.link_list:
            address = link[0].get_text(strip=True)
            addresses.append(address)
        # print(f"Found Addresses: {addresses}")  # Debug print
        return addresses

    def get_price(self):
       
        prices = []
        for price in self.price_list:
            price_text = price.text.strip()  
            cleaned_price = price_text.split("+")[0].split("/mo")[0].strip()  
            prices.append(cleaned_price)
        # print(f"Found Prices: {prices}")  # Debug print
        return prices

    def get_all_data(self):
        
        all_urls = self.get_endpoints()
        all_addresses = self.get_address()
        all_prices = self.get_price()

        return zip(all_urls, all_addresses, all_prices)


zillow_scraper = ZillowData()

# for url, address, price in zillow_scraper.get_all_data():
#     print(f"URL: {url}")
#     print(f"Address: {address}")
#     print(f"Price: {price}")
#     print("-" * 50)

class fill_data :
    #ignore all the arguments and experimental stuffs. It just keep throwing errors in my console which is pretty annoying so we just add them to ignore them
    def __init__(self):
        self.option=Options()
        self.option.add_argument("--start-maximized")
        #this keeps the chrome window open even after the program is done
        self.option.add_experimental_option("detach",True)
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_argument('--ignore-ssl-errors')
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver=webdriver.Chrome(options=self.option)
        #getting the data which we will use to fill the form
        self.data= ZillowData()
        self.address=self.data.get_address()
        self.price=self.data.get_price()
        self.url=self.data.get_endpoints()

    def fill_form(self):
        self.driver.get(DOC_URL)

        for address, price, link in zip(self.address, self.price, self.url):
            time.sleep(1)
            address_keys = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address_keys.send_keys(address)

            price_keys = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_keys.send_keys(price)

            link_keys = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_keys.send_keys(link)

            submit = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
            submit.click()
            time.sleep(1)

            another_response = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            another_response.click()

    def close(self):
        self.driver.close()

fill = fill_data()
fill.fill_form()
fill.close()
    