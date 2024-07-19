# import libraries
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

# set the path to Chrome driver
CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

# initial the chrome driver
options = webdriver.ChromeOptions()
service = ChromeService(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# navigate to the URL 
driver.get("https://www.google.com")

# to close the browser when done
driver.quit()