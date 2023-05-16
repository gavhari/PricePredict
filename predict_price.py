from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import sys
#import tensorflow as tf
#import numpy as np
import pandas as pd
import requests
import time

symbol = "EURUSD"
url = f"https://www.tradingview.com/symbols/{symbol}"

data = []
df = pd.DataFrame(columns=['p1','p2','p3','p4','p5','p6','p7','p8'])

driver = webdriver.Chrome('PricePredict/chromedriver')
driver.get(url)

wait = WebDriverWait(driver,10)
try:
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'content-VzJVlozY')))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'text-VzJVlozY')))
    try:
        market_open = driver.find_element(By.XPATH, "//*[text()='Market open']")
        print(u'\u2713' + " Market open")
    except NoSuchElementException:
        print(u'\u2717' + " Tidak menemukan status pasar")
        driver.quit()
        sys.exit()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'last-JWoJqCpY')))
    print(u'\u2713' + " Harga ditemukan")
except TimeoutException:
    print("u'\u2717' + Status market atau harga pasar tidak ditemukan ")
    driver.quit()
    
while True:
    try:
        harga_pasar = driver.find_element(By.CLASS_NAME, 'last-JWoJqCpY')
    except NoSuchElementException:
        print(u'\u2717' + ' Harga pasar tidak ditemukan')
        break
    data.append(float(harga_pasar.text))
    if len(data) == 8:
        df.loc[len(df.index),:] = data
        data.pop(0)
        if len(df) > 0:
            print(df)
            df.to_excel('dataFrame.xlsx', index=False)
    time.sleep(60)
    
 