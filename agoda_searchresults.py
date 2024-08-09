from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

if __name__ == "main":
    # TODO: set variable
    export_filename = "<filename.csv>"
    target_url ="https://www.agoda.com/en-au/search?<url>"

    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(target_url)
    time.sleep(5)   

    # define the number of times to scrolls
    scroll_count = 20
    # continuous scrolling 
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
        time.sleep(1)  # Wait for the new results to load 

    html_content = driver.page_source

    soup = BeautifulSoup(html_content,'html.parser')
    allData = soup.find_all("div",{"data-element-name":"PropertyCardBaseJacket"})

    hotel_list = []
    for i in range(len(allData)):
        tmp_info = {}
        try:
            tmp_info["name"] = allData[i].find('h3',{'class':'spacing-sc-tu168e-0 Typographystyled__TypographyStyled-sc-1uoovui-0 gfaUTV cYUUCV'}).text
        except:
            tmp_info["name"] = None
        try:
            tmp_info["rating"] = allData[i].find('div',{'class':'Box-sc-kv6pi1-0 ggePrW'}).text
        except:
            tmp_info["rating"] = None
        try: 
            tmp_info["price"] = allData[i].find('div',{"class","Box-sc-kv6pi1-0 bWGdbw PropertyCardPrice PropertyCardPrice--Display"}).text.replace(u'\xa0',' ')
        except:
            tmp_info["price"] = None
            
        if tmp_info["name"] != None:
            hotel_list.append(tmp_info)
            print(tmp_info) 

    hotel_df = pd.DataFrame(hotel_list) # convert to DataFrame

    hotel_df.to_csv(export_filename,index=False)

    driver.close()
    driver.quit()
