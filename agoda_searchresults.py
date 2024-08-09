from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import datetime

CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

if __name__ == "main":
    target_url ="https://www.agoda.com/en-au/search?<url>"

    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(target_url)
    time.sleep(5)   

    html_content = driver.page_source

    soup = BeautifulSoup(html_content,'html.parser')
    allData = soup.find_all("div",{"data-element-name":"PropertyCardBaseJacket"})

    
    for i in range(len(allData)):
        tmp_info = {}
        try:
            tmp_info["name"] = allData[i].find('h3',{'class':'spacing-sc-tu168e-0 Typographystyled__TypographyStyled-sc-1uoovui-0 gfaUTV cYUUCV'}).text
            # tmp_info["name"] = allData[i].find('h3',{'class':'spacing-sc-tu168e-0 Typographystyled__TypographyStyled-sc-1uoovui-0 gfaUTV cYUUCV'})
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
            print(tmp_info) 

    # limitation of item lists
