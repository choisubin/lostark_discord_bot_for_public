#세레니움 관련해서 chromedriver 경로 따로 보관
#여기는 .gitignore
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

#chromedriver = os.environ.get("CHROMEDRIVER_PATH")
#options = webdriver.ChromeOptions()
#options.add_argument("headless")

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

