import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


ser = Service("C:\Program Files (x86)\chromedriver.exe")
op = webdriver.ChromeOptions()
op.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=ser, options=op)

#Captando notícias com a tag "presidente lula"
driver.get("https://g1.globo.com/busca/?q=presidente+lula")

programa = []
titulo = []
descricao = []
data = []



try:
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )
    
   #XPATHS
   # Programa: //section[@id='content']/div/div/ul/li[2]/div[3]/div
   # Título: //section[@id='content']/div/div/ul/li[2]/div[3]/a/div
   # Descrição: //section[@id='content']/div/div/ul/li[2]/div[3]/a/p/span
   # Data: //section[@id='content']/div/div/ul/li[2]/div[3]/a/div[2]

    #testando nas 60 primeiras notícias
    for i in range(2,61):
        time.sleep(2)
        #Atualizando os xpaths para caminhar a lista de noticias
        programa_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/div"
        titulo_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/div"
        descricao_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/p/span"
        data_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/div[2]"
                
        
        try:
            programa.append(driver.find_element(By.XPATH,programa_xpath).text) 
        except:
            NoSuchElementException  
        
        try:
            titulo.append(driver.find_element(By.XPATH,titulo_xpath).text)
        except:
            NoSuchElementException
        
        try:
            descricao.append(driver.find_element(By.XPATH,descricao_xpath).text)
        except:
            NoSuchElementException

        try:
            data.append(driver.find_element(By.XPATH,data_xpath ).text)
        except:
            NoSuchElementException

        #Como a página atualiza 15 notícias por vez, caso o i seja multiplo de 15, 
        # vou rolar para o fim da página para carregar mais notícias
        if(i%15 == 0):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

except:
    driver.quit()

dataframe = pd.DataFrame(list(zip(programa, titulo, descricao, data)), columns = ['Programa', 'Titulo', 'Descricao','Data'])
print(dataframe)
