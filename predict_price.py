from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import tensorflow as tf
#import numpy as np
import pandas as pd
import requests
import time

symbol = "EURUSD"
url = f"https://www.tradingview.com/symbols/{symbol}"

xpath = {
    'market_status':'//*[@id="js-category-content"]/div[1]/div[1]/div/div/div/div[2]/button[4]/span/span[2]',
    'stock_price':'//*[@id="js-category-content"]/div[1]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/span[1]'
}

driver = webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver,10)
wait.until(EC.presence_of_element_located((By.XPATH, xpath['market_status'])))

market_open = driver.find_element(By.XPATH, xpath['market_status'])
if market_open.text == "Market open":
    print("Market is open")

data = []
df = pd.DataFrame(columns=['price1','price2','price3','price4','price5','price6','price7','price8'])

while market_open.text == "Market open":
    stock_price = driver.find_element(By.XPATH, xpath['stock_price'])
    data.append(float(stock_price.text))
    if len(data) == 8:
        df.loc[len(df.index)] = data
        data.pop(0)
    print(df)
    time.sleep(5)

 