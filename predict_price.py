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

data_collect = []
df = pd.DataFrame(columns=['sel1','julbe1','sel2','julbe2','sel3','julbe3','sel4','julbe4','sel5','julbe5','sel6','julb6','aksi'])

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
    data_collect.append(float(harga_pasar.text))
    if len(data_collect) == 8:
        data_olah = []
        for i in range(len(data_collect)):
            if i<6:
                selisih = data_collect[i+1] - data_collect[i]
                posneg = None
                if selisih > 0:
                    posneg = 1
                else:
                    posneg = 0
                data_olah.append(selisih)
                data_olah.append(posneg)
            elif i==6:
                if data_collect[i+1] - data_collect[i] > 0:
                    data_olah.append(1)
                else:
                    data_olah.append(0)
        df.loc[len(df),:] = data_olah
        data_collect.pop(0)
    print(df)
    if len(df) > 500:
        df.to_excel('dataFrame.xlsx', index=False)
    time.sleep(60)
    # data.append(float(harga_pasar.text))
    # if len(data) == 8:
    #     df.loc[len(df.index),:] = data
    #     data.pop(0)
    #     if len(df) > 500:
    #         print(df)
    #         df.to_excel('dataFrame.xlsx', index=False)
    # time.sleep(60)
    
 