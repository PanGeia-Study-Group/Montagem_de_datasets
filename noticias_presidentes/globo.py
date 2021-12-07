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

#Captando notícias com a tag "presidente lula"
driver.get("https://g1.globo.com/busca/?q=presidente+lula")

programa = []
titulo = []
descricao = []
data = []

try:
    #Para garantir que o site carregou
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )

    botao_veja_mais_xpath = "//section[@id='content']/div/div/div/a"
 
 
    for i in range(2,20):

        xpath_teste = "//*[@id='content']/div/div/ul/li["+str(i)+"]" 
        time.sleep(2)           
                              
        try:
            driver.find_element(By.XPATH, xpath_teste).click()        
            time.sleep(5)
            print("Noticia:" + str(i-1))
            driver.back()      
        except:
            print("Nada")
            NoSuchElementException
                       
        time.sleep(2)

        #Como a página atualiza 15 notícias por vez, caso o i seja multiplo de 15, 
        # vou rolar para o fim da página para carregar mais notícias ou clicar no botão "Veja Mais"
        if(i%15 == 0 and i<60):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        elif(i%15 == 0 and i>=60):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            
            driver.find_element(By.XPATH,botao_veja_mais_xpath).click()
            time.sleep(3)
    
except:
    driver.quit()
    

#df_noticias_lula = pd.DataFrame(list(zip(programa, titulo, descricao, data)), columns = ['Programa', 'Titulo', 'Descricao','Data'])
#print(df_noticias_lula['Descricao'][0])
#print(i)
#print(len(df_noticias_lula))


#### to do / problemas ###
#1- As vezes a descrição tem mais de um <span>, então seriam 2 xpaths: 
#  //section[@id='content']/div/div/ul/li[i]/div[3]/a/p/span e //section[@id='content']/div/div/ul/li[i]/div[3]/a/p/span[2] 
# - As datas que estiverem no formato "há X dias" ou "há X horas" devem ser colocadas no formato "dd/mm/aaaa HHhMM"
# - Entrar em cada notícia e buscar o texto do corpo da notícia
# - Definir a função (url será "https://g1.globo.com/busca/?q=" + Keyword)

'''
Apagar quase tudo e começar do zero.

Entrar em cada notícia e buscar os objetos por class name.

'''