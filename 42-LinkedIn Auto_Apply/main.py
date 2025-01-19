from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

chrome_driver_path = "/Users/cami/Documents/chromedriver"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4114624099&geoId=106670623&keywords=intership%20software&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true")

    # Click sign-in button
    sign_in = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')))
    sign_in.click()

    # Fill in credentials
    email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="base-sign-in-modal_session_key"]')))
    email.send_keys("your_email_here")

    passw = driver.find_element(By.XPATH, '//*[@id="base-sign-in-modal_session_password"]')
    passw.send_keys("your_password_here")

    # Click sign-in submit button
    sign_in2 = driver.find_element(By.XPATH, '//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button')
    sign_in2.click()

    # Easy apply process (update with correct XPaths)
    easy_apply = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ember46"]/span')))
    easy_apply.click()

    next_button = driver.find_element(By.XPATH, '//*[@id="ember554"]/span')
    next_button.click()

    next_button2 = driver.find_element(By.XPATH, '//*[@id="ember554"]/span')
    next_button2.click()

    submit = driver.find_element(By.XPATH, '//*[@id="ember569"]/span')
    submit.click()

    input("Press Enter to close the browser...")

finally:
    driver.quit()