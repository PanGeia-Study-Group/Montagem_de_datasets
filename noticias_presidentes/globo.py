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
artigo_teste = ""


try:
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )

   #XPATHS
   # Programa: //section[@id='content']/div/div/ul/li[2]/div[3]/div
   # Título: //section[@id='content']/div/div/ul/li[2]/div[3]/a/div
   # Descrição: //section[@id='content']/div/div/ul/li[2]/div[3]/a/p/span
   # Data: //section[@id='content']/div/div/ul/li[2]/div[3]/a/div[2]
   # Botão "veja mais": //section[@id='content']/div/div/div/a

    botao_veja_mais_xpath = "//section[@id='content']/div/div/div/a"
    #testando nas 60 primeiras notícias
    
    for i in range(2,25):

        time.sleep(2)
        '''
        #Atualizando os xpaths para caminhar a lista de noticias
        programa_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/div"
        titulo_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/div"
        descricao_pt1_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/p/span"
        descricao_pt2_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/p/span[2]"
        data_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/div[2]"

        #XPATHS das notícias sem thumbnail (testando) // stn = sem thumbnail
        programa_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/div"
        titulo_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/a/div"
        descricao_stn_pt1_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/a/p/span"
        descricao_stn_pt2_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/a/p/span[2]"
        data_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/a/div[2]"                
        
        
        #tenta encontrar a notícia assumindo que ela possui o XPATH padrão com thumbnail
        try:
            programa.append(driver.find_element(By.XPATH,programa_xpath).text) 
        except:
            #se não encontrar, tenta achar a notícia com o XPATH sem thumbnail
            try:
                programa.append(driver.find_element(By.XPATH,programa_stn_xpath).text)
            except:
                NoSuchElementException            
        NoSuchElementException  

        try:
            titulo.append(driver.find_element(By.XPATH,titulo_xpath).text)
        except:
            try:
                titulo.append(driver.find_element(By.XPATH,titulo_stn_xpath).text)
            except:
                NoSuchElementException                    
        NoSuchElementException

        
        descr_1 = ""  
        descr_2 = ""                      
        descr_completa = ""
        try:      
            descr_1 = driver.find_element(By.XPATH,descricao_pt1_xpath).text
            descr_completa = descr_1      
            #descricao.append(driver.find_element(By.XPATH,descricao_pt1_xpath).text)
            try:                
                descr_2 = driver.find_element(By.XPATH,descricao_pt2_xpath).text
                descr_completa += " - " + descr_2
                descricao.append(descr_completa)
            except:
                descricao.append(descr_completa)
                NoSuchElementException              
        except:
            try:
                descr_1 = driver.find_element(By.XPATH,descricao_stn_pt1_xpath).text
                descr_completa = descr_1
                #descricao.append(driver.find_element(By.XPATH,descricao_stn_pt1_xpath).text)
                try:                
                    descr_2 = driver.find_element(By.XPATH,descricao_stn_pt2_xpath).text
                    descr_completa += " - " + descr_2
                    descricao.append(descr_completa)
                except:
                    descricao.append(descr_completa)
                    NoSuchElementException                 
            except:
                NoSuchElementException                    
        NoSuchElementException


        try:
            data.append(driver.find_element(By.XPATH,data_xpath).text)
        except:  
            try:
                data.append(driver.find_element(By.XPATH,data_stn_xpath).text)
            except:
                NoSuchElementException                      
        NoSuchElementException
        '''
        
        #TESTES
        actions = ActionChains(driver)

        xpath_teste = "//*[@id='content']/div/div/ul/li["+str(i)+"]"                          

        try:
            content = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "content"))
            )  

            noticia = driver.find_element(By.XPATH, xpath_teste)
            actions.move_to_element(noticia)
            actions.click()
            actions.perform()
            time.sleep(5)
            print("aham\n")         

        except:
            NoSuchElementException
               
        time.sleep(2)

        #Como a página atualiza 15 notícias por vez, caso o i seja multiplo de 15, 
        # vou rolar para o fim da página para carregar mais notícias
        if(i%15 == 0 and i<60):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        elif(i%15 == 0 and i>=60):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            
            botao_veja_mais = driver.find_element(By.XPATH,botao_veja_mais_xpath)
            botao_veja_mais.click()
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