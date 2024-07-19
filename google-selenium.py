# import libraries
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

# set the path to Chrome driver
CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

###
### Function: navigate_chrome
### navigate to the URL
###
def navigate_chrome(url):
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    # to close the browser when done
    # driver.quit()

### Example usage
if __name__=="main":
    target_url = "https://www.google.com"
    navigate_chrome(target_url)
