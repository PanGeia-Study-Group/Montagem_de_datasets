import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


#PATH = "C:\Program Files (x86)\chromedriver.exe"
ser = Service("C:\Program Files (x86)\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
#driver = webdriver.Chrome(PATH)

#Captando notícias com a tag "presidente lula"
driver.get("https://g1.globo.com/busca/?q=presidente+lula")

try:
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )
    
    articles = content.find_element(By.CLASS_NAME, "widget--info__title product-color ")
    #for article in articles:
     #   header = article.find_element
    print(articles)
except:
    #print(articles)
    driver.quit()

