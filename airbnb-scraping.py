from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

if __name__ == "main":
    target_url = "https://www.expedia.com.au/<hotel-url-path>"

    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.airbnb.co.in/s/Sydney--Australia/homes?adults=1&checkin=2024-12-17&checkout=2024-12-18&currency=AUD")
    time.sleep(5)

    html_content = driver.page_source

    # Parsing the data with BS4
    soup=BeautifulSoup(html_content,'html.parser')
    allData = soup.find_all("div",{"itemprop":"itemListElement"})
    
    hotel_list = []
    for i in range(len(allData)):
        tmp_info = {}
        try: 
            tmp_info["name"] = allData[i].find('div',{'data-testid':'listing-card-title'}).text.lstrip().rstrip()
        except:
            tmp_info["name"] = None
        try:
            tmp_info["rating"] = allData[i].find('div',{'class':'t1a9j9y7'}).text.split()[0]
        except:
            tmp_info["rating"] = None
        try:
            tmp_price = allData[i].find('div',{'class':'_i5duul'}).find('div',{"class":"_10d7v0r"}).text.split(" total")[0]
            tmp_price = tmp_price.split(u'\xa0')
            tmp_price = tmp_price[0] + " " + tmp_price[1]
            tmp_info["price"] =  tmp_price
        except:
            tmp_info["price"] = None
        
        hotel_list.append(tmp_info)
        
        hotel_df = pd.DataFrame(hotel_list)

        print(hotel_df)

        filename = "<filename.csv>"
        df.to_csv(filename,ignore_index=True)
