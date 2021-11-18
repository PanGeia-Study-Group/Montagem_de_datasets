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


ser = Service("C:\Program Files (x86)\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

#Captando notícias com a tag "presidente lula"
driver.get("https://g1.globo.com/busca/?q=presidente+lula")

try:
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )
    
   #XPATHS
   # Fonte(programa): //section[@id='content']/div/div/ul/li[2]/div[3]/div
   # Título: //section[@id='content']/div/div/ul/li[2]/div[3]/a/div
   # Descrição: //section[@id='content']/div/div/ul/li[2]/div[3]/a/p/span
   # Data: //section[@id='content']/div/div/ul/li[2]/div[3]/a/div[2]

    fonte = driver.find_element_by_xpath("//section[@id='content']/div/div/ul/li[2]/div[3]/div").text
    titulo = driver.find_element_by_xpath("//section[@id='content']/div/div/ul/li[2]/div[3]/a/div").text
    descricao = driver.find_element_by_xpath("//section[@id='content']/div/div/ul/li[2]/div[3]/a/p/span").text
    data = driver.find_element_by_xpath("//section[@id='content']/div/div/ul/li[2]/div[3]/a/div[2]").text
    print(fonte)
    print(titulo)
    print(descricao)
    print(data)

except:
    driver.quit()