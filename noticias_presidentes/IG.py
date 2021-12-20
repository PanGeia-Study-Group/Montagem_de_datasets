'''
41 notícias por pagina
XPATH da notícia:  //*[@id="empbusca"]/ul[1]/div[i]
URL: https://busca.ig.com.br/buscar/?q=presidente%20lula&o=IG*&c=all&t=all&d=all&p=1&s=ig_content
Programa: class="author-container"
Título: class="noticia-titulo-h1-ig_V04"
Subtitulo: class="noticia-olho"
Data: //*[@id="dataHTML"]/time 
'''

import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

ser = Service("C:\Program Files (x86)\chromedriver.exe")
op = webdriver.ChromeOptions()
op.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=ser, options=op)


pesquisa_url = "https://busca.ig.com.br/buscar/?q=presidente%20lula&o=IG*&c=all&t=all&d=all&p=1&s=ig_content"
driver.get(pesquisa_url)

try:
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "915A13F3-0072-477D-BDBF-48DE03AE50A3"))
    )

    noticias = []

    for i in range(1,15):

        XPATH_noticia = "//*[@id='empbusca']/ul[1]/div["+str(i)+"]"
        

        try:
            noticia = driver.find_element(By.XPATH, XPATH_noticia)
            #driver.execute_script("arguments[0].scrollIntoView();", noticia)
            time.sleep(2)

            noticia.click()

            time.sleep(2)

            try: 
                titulo = driver.find_element(By.CLASS_NAME, "noticia-titulo-h1-ig_V04").text
            except:
                titulo = -1
                NoSuchElementException

            try:
                subtitulo = driver.find_element(By.ID, "noticia-olho").text
            except:
                subtitulo = -1
                NoSuchElementException

            noticias.append({
                "Titulo": titulo,
                "Subtitulo": subtitulo
            })

        except:
            NoSuchElementException

    print(pd.DataFrame(noticias))

except:
    driver.quit()


