from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import sys
import tensorflow as tf
import numpy as np
import pandas as pd
import requests
import time
import matplotlib.pyplot as plt

loaded_model = tf.keras.models.load_model('/home/gabe/DeepLearningProject/PricePredict/model.h5')

symbol = "EURUSD"
url = f"https://www.tradingview.com/symbols/{symbol}"

data = []
df = pd.DataFrame(columns=['p1','p2','p3','p4','p5','p6','p7','p8'])

driver = webdriver.Chrome('PricePredict/chromedriver')
driver.get(url)
harga_sebelumnya = None
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
        harga_pasar = float(harga_pasar.text)
    except NoSuchElementException:
        print(u'\u2717' + ' Harga pasar tidak ditemukan')
        break
    data.append(harga_pasar)
    if len(data) == 7:
        data_np = np.array(data).reshape(1,7)
        data.pop(0)
        prediksi = loaded_model.predict(data_np)
        print(f"Harga pasar saat ini : {harga_pasar}")
        print(f"Harga prediksi : {prediksi}")
        print(f"Harga sebelumnya : {harga_sebelumnya}")
        if harga_pasar - prediksi > -0.001:
            print("NAIK!!!!!")
        harga_sebelumnya = prediksi
    time.sleep(1)