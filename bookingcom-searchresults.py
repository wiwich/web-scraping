from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import datetime
import time

CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

if __name__ == "main":
    # TODO: set variable
    search_city = "Sydney"
    checkin_date = str(datetime.date.today()+ datetime.timedelta(days=1))
    checkout_date = str(datetime.date.today()+ datetime.timedelta(days=2))
    adults_no = 2
    child_no = 0
    rooms_no = 1
    currency = "AUD"
    export_filename = "<filename.csv>"

    target_url = "https://www.booking.com/searchresults.en-gb.html?ss="+search_city+"&dest_type=city&checkin="+checkin_date+"&checkout="+checkout_date+"&group_adults="+str(adults_no)+"&group_children="+str(child_no)+"&no_rooms="+str(rooms_no)+"&selected_currency="+currency

    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(target_url)
    time.sleep(5)

    html_content = driver.page_source

    soup = BeautifulSoup(html_content,'html.parser')
    allData = soup.find_all("div",{"data-testid":"property-card"})

    hotel_list = []
    for i in range(len(allData)):
        tmp_info = {}
        try:
            tmp_info["name"] = allData[i].find('div',{'data-testid':'title'}).text
        except:
            tmp_info["name"] = None
        try:
            tmp_info["rating"] = allData[i].find('div',{'class':'d0522b0cca fd44f541d8'}).text.split(" ")[-1] # get the last index
        except:
            tmp_info["rating"] = None
        try:
            tmp_info["stars"] = allData[i].find('div',{'class':'f97c3d5c2f'}).attrs['aria-label']  # get value in aira-label
        except:
            tmp_info["stars"] = None
        try:
            tmp_info["price"] = allData[i].find('span',{'data-testid':'price-and-discounted-price'}).text.replace(u'\xa0',' ')
        except:
            tmp_info["price"] = None

        hotel_list.append(tmp_info)

    hotel_df = pd.DataFrame(hotel_list)
    hotel_df.to_csv(export_filename,index=False)
    
