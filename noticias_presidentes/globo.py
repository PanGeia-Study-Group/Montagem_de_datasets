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
subtitulo = []
data = []
corpo = []
'''
Nomes das classes:
Título: class="content-head__title"
Subtítulo: class="content-head__subtitle"
Data: class="content-publication-data__updated"
Corpo da notícia: class="mc-article-body"
'''


try:
    #Para garantir que o site carregou
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )

    botao_veja_mais_xpath = "//section[@id='content']/div/div/div/a"
 

    for i in range(2,20):

        xpath_teste = "//*[@id='content']/div/div/ul/li["+str(i)+"]" 
        programa_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/div"
        titulo_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/div"
        programa_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/div"
        titulo_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/a/div"
        time.sleep(2) 

                 
                              
        #Pegar título e programa antes de entrar na notícia
        #Dentro da notícia, pegar subtítulo, data e o que mais tiver (autor? mídia? duração do vídeo? etc)  
        #Mudar lógica dos Try/Excepts: o append deve vir depois. Primeiro armazena os objetos em variáveis                            
        try:
            noticia = driver.find_element(By.XPATH, xpath_teste)
            driver.execute_script("arguments[0].scrollIntoView();", noticia)

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

            noticia.click()
            time.sleep(5)

            try:
                subtitulo.append(driver.find_element(By.CLASS_NAME, "content-head__subtitle").text)
            except:
                subtitulo.append('-1')
                NoSuchElementException

            try:
                corpo.append(driver.find_element(By.CLASS_NAME, "mc-article-body").text)
            except:
                corpo.append('-1')
                NoSuchElementException


            print("Noticia: " + str(i-1))
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
    

df_noticias_lula = pd.DataFrame(list(zip(programa, titulo, subtitulo, data, corpo)), columns = ['Programa', 'Titulo', 'Subtitulo','Data', 'Corpo'])
#print(df_noticias_lula['Descricao'][0])
#print(i)
print(df_noticias_lula)


#### to do / problemas ### 
# - As datas que estiverem no formato "há X dias" ou "há X horas" devem ser colocadas no formato "dd/mm/aaaa HHhMM"
# - Entrar em cada notícia e buscar o texto do corpo da notícia
# - Definir a função (url será "https://g1.globo.com/busca/?q=" + Keyword)