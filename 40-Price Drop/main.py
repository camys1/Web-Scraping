import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

URL = "https://www.amazon.com/Yves-Saint-Laurent-Libre-Parfum/dp/B0B9T35NCJ/ref=sr_1_2?crid=1YJ4AZTHQEH1X&dib=eyJ2IjoiMSJ9.GEa01O0ulmG1YsmnvLIFrDO-roTbzYzKXMLjOu1iikEA-Nj-U7Jwa-yAD7fRWyXT6fL1YjaU_yBshqMSddF_E3CEv-JPTqXrKvCftuIsanxTySG1X9BnOdQFBOJ5t5Xuqabc4aQNcjM3mchaaUTfRmC2Mr92Lk0cJBM69MZrCNzIRkdZjrYq9qpGihD2GKVLMwx0Ij9g0DwcSZ1gBDkgz4foKJGeRGMtiGKIBfUhedgwRZT587DffuUGUcDUX9VXK6dnO0E1XSfsK_iVKNxFVpsEvT48-oyaUK52Ybz2pNA.3yE1bPIw0LwVaD58aJQMaSDbDqL0g3UE1qzOymRoWRE&dib_tag=se&keywords=libre+intense+yves+saint+laurent&qid=1724361080&sprefix=libre+inte%2Caps%2C209&sr=8-2"

MY_EMAIL = os.getenv("MY_EMAIL")
MY_EMAIL_PASSWORD = os.getenv("MY_EMAIL_PASSWORD")
EMAIL_PROVIDER_SMTP_ADDRESS = os.getenv("EMAIL_PROVIDER_SMTP_ADDRESS")


try:
    r = requests.get(URL, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36", "Accept-Language":"en-US,en;q=0.9"})
    r.raise_for_status()
    amazon_webpage = r.text

    soup = BeautifulSoup(amazon_webpage, "html.parser")
    
    price_element = soup.find(name="span", class_="a-offscreen")
    if price_element:
        price = price_element.getText().split("$")[1]
    else:
        print("Could not find the price on the page. There may be an issue.")
        price = None

    name_element = soup.find(name="span", id="productTitle")
    if name_element:
        name = name_element.getText().strip()
    else:
        print("Could not find the product name on the page.")
        name = "Unknown Product"
    
    if price:
        low_price = input("What is the lowest you want to buy this item for: ")
    if float(price) < float(low_price):
        with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)          
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="samuilac@gmail.com",
                msg=f"Subject:Amazon Price Alert!\n\n{name} is now ${price}\n {URL}")
            print("The email has been sent.")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    print("There might be a CAPTCHA or other issue preventing the request.")