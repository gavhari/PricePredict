from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import threading
import pandas as pd
import datetime
from sklearn import linear_model
from time import sleep
import joblib
import sys
#####################################################

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENOC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

symbol = "EURUSD"
url = f"https://www.tradingview.com/symbols/{symbol}"

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
    print(u'\u2717' + "Status market atau harga pasar tidak ditemukan ")
    driver.quit()
    
def getprice(sleep_time=60):
    sleep(sleep_time)
    # quote = web.get_quote_yahoo(label)
    # price = quote["price"].values[0]
    price = driver.find_element(By.CLASS_NAME, 'last-JWoJqCpY')
    price = float(price.text)
    current_time = datetime.datetime.now()
    return tuple([price, current_time])

def train(input):
    print("\nModel updating...", end=" ")
    featureMat = input.iloc[:, : len(input.columns)-1]
    label = input[input.columns[-1]]
    model = linear_model.LinearRegression()
    model.fit(featureMat, label)
    joblib.dump(model, "modelLR.pkl")
    print("[Completed]")
    
number_of_features = 7
training_record_criterian = 7
number_of_predictions = 3

data = pd.DataFrame(columns=range(number_of_features))
predict_input = list()

while 1:
    feature = list()
    for i in range(number_of_features):
        price = getprice()[0]
        feature.append(price)
        predict_input.append(price)
        
        try:
            first_predict = True
            model = joblib.load("modelLR.pkl")
            print("")
            inputlist = predict_input.copy()
            for feature_value in inputlist[-(3):]:
                print(f"{bcolors.WARNING} --> ", float(feature_value * 100) / 100, end=" ")
            price = getprice(sleep_time=0)[0]
            for i in range(number_of_predictions):
                pre_price = model.predict([inputlist[-(number_of_features - 1):]])
                print(f"{bcolors.OKBLUE} --> ","{:.5f}".format(float(pre_price[0] * 100)/100), end=" ")
                if first_predict:
                    if pre_price[0] - inputlist[-1] > 0:
                        print(f"{bcolors.OKGREEN} \u2191", end="")
                        print(f"{bcolors.BOLD}[", int((pre_price[0]-price)*1000000/price)," %]", end=" ")
                        print(f"{bcolors.OKCYAN} Actual: ", price, end="")
                    elif pre_price[0] - inputlist[-1] == 0:
                        print(f"{bcolors.HEADER} \u2022", end="")
                        print(f"{bcolors.BOLD}[", int((pre_price[0] - price) * 1000000/price)," %]", end=" ")
                        print(f"{bcolors.OKCYAN} Actual: ", price, end="")
                    else:
                        print(f"{bcolors.FAIL} \u2193", end="")
                        print(f"{bcolors.BOLD}[", int(-(pre_price[0] - price) * 1000000/price)," %]", end=" ")
                        print(f"{bcolors.OKCYAN} Actual: ", price, end="")
                        
                    if price - inputlist[-1] > 0:
                        print(f"{bcolors.OKGREEN} \u2191", end=" ")
                    elif price - inputlist[-1] == 0:
                        print(f"{bcolors.HEADER} \u2022", end="")
                    else:
                        print(f"{bcolors.FAIL} \u2193", end=" ")
                    
                    first_predict = False
                    
        except:
            print("Please Wait while the model is getting ready...")
            
    data.loc[len(data.index)] = feature
    if len(data.index) % training_record_criterian == 0:
        trainer = threading.Thread(target=train, args=(data,))
        trainer.start()
        trainer.join()