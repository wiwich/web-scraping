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

    # get hotel name
    hotel_info = {}
    soup=BeautifulSoup(resp,'html.parser')
    try:
        hotel_info["hotel"]=soup.find("h1").text
    except:
        hotel_info["hotel"]=None

    print(hotel_info["hotel"])