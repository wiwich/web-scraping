from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime
import time

CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

if __name__ == "main":
    # TODO: set variable
    search_city = "Sydney--Australia"
    adults_no = 1
    checkin_date = str(datetime.date.today()+ datetime.timedelta(days=1))
    checkout_date = str(datetime.date.today()+ datetime.timedelta(days=2))
    currency = "AUD"
    export_filename = "<filename.csv>"
    
    target_url = "https://www.airbnb.co.in/s/"+search_city+"/homes?adults="+str(adults_no)+"&checkin="+checkin_date+"&checkout="+checkout_date+"&currency="+currency

    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(target_url)
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
    hotel_df.to_csv(export_filename,index=False)

    df.to_csv(export_filename,index=False)

    driver.close()
