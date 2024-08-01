from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup


CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

if __name__ == "main":
    target_url = "https://www.expedia.com.au/<hotel-url-path>"

    options = webdriver.ChromeOptions()

    # options setting
    options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36')
    options.add_argument('accept-encoding=gzip, deflate, br')
    options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    options.add_argument('referer=https://www.expedia.com/')
    options.add_argument('upgrade-insecure-requests=1')

    # options = webdriver.ChromeOptions()
    service = ChromeService(executable_path = CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    # go to target_url page
    driver.get(target_url)

    # get the page source
    resp = driver.page_source
    
    soup=BeautifulSoup(resp,'html.parser')
    
    # get hotel information
    hotel_info = {}
    try:
        hotel_info["hotel"]=soup.find("h1").text
        hotel_info["desc"] = soup.find("div",{"class":"uitk-spacing uitk-spacing-margin-inlinestart-unset uitk-spacing-padding-blockstart-unset"}).text
        hotel_info["address"] = soup.find("div",{"class":"uitk-text uitk-type-start uitk-type-300 uitk-text-default-theme"}).text
        hotel_info["rating"] = soup.find("span",{"class":"uitk-badge-base-text"}).text

    except:
        hotel_info["hotel"] = None
        hotel_info["desc"] = None
        hotel_info["address"] = None
        hotel_info["rating"] = None

    print(hotel_info) # return dict 

    # scrape the room-type data
    try:
        allOffers = soup.find("div",{"data-stid":"section-room-list"})
    except:
        allOffers = None
        print('..allOffers no data!')
    
    offers_room = allOffers.find_all("div",{"class":"uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between uitk-card uitk-card-roundcorner-all uitk-card-has-border uitk-card-has-overflow uitk-card-has-primary-theme"})
    for offer in offers_room:
        try:
            # get room name
            name_type = offer.find("h3",{"class":"uitk-heading uitk-heading-6"}).text
        except:
            name_type = None
        try: 
            # get guests
            rm_info = offer.find("ul",{"class":"uitk-typelist uitk-typelist-orientation-stacked uitk-typelist-size-2 uitk-typelist-spacing uitk-spacing uitk-spacing-margin-blockstart-three"})
            for tmp in rm_info:
                if "Sleeps" in tmp.text:
                    guests = tmp.text
        except:
            guests = None
        try:
            # get room price
            price_room = offer.find("div",{"class":"uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme"}).text
        except:
            price_room = None
    
        print(name_type)
        print(room_info)
        print(price_room)
        print("---------")
