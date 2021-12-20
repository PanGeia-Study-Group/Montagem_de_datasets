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


'''
Nomes das classes:
Título: class="content-head__title"
Subtítulo: class="content-head__subtitle" // class="playkit-video-info__ep-description playkit-video-info__ep-description--show-all"
Data: class="content-publication-data__updated"
Corpo da notícia: class="mc-article-body"
'''

def noticias_g1(keyword, tamanho):
    ser = Service("C:\Program Files (x86)\chromedriver.exe")
    op = webdriver.ChromeOptions()
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ser, options=op)

    #Captando notícias com a tag "presidente lula"
    pesquisa_url = "https://g1.globo.com/busca/?q=" + keyword.replace(" ", "+")
    driver.get(pesquisa_url)

    noticias = []

    try:
        #Para garantir que o site carregou
        content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "content"))
        )

        botao_veja_mais_xpath = "//section[@id='content']/div/div/div/a"    

        for i in range(2,tamanho+2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            xpath_lista = "//*[@id='content']/div/div/ul/li["+ str(i) +"]" 

            #XPATHS das notícias com thumbnail
            programa_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/div"
            titulo_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/div"
            data_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[3]/a/div[2]"

            #XPATHS das notícias sem thumbnail
            programa_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/div"
            titulo_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/a/div"
            data_stn_xpath = "//section[@id='content']/div/div/ul/li["+ str(i) +"]/div[2]/a/div[2]"                
            
            time.sleep(2) 
                                
            collected_successfully = False
            
            while not collected_successfully:

                #Pegar título e programa fora da notícia
                #Dentro da notícia, pegar subtítulo, data, corpo e o que mais tiver (autor? mídia? duração do vídeo? etc)    
                try:
                    noticia = driver.find_element(By.XPATH, xpath_lista) #buscando o elemento da notícia i
                    driver.execute_script("arguments[0].scrollIntoView();", noticia) #scrollando até a notícia
                    time.sleep(2)
                    print("Captando dados da notícia " + str(i-1) + "/" + str(tamanho))

                    #tenta encontrar a notícia assumindo que ela possui o XPATH padrão com thumbnail
                    try:
                        programa = driver.find_element(By.XPATH,programa_xpath).text
                    except:
                        #se não encontrar, tenta achar a notícia com o XPATH sem thumbnail
                        try:
                            programa = driver.find_element(By.XPATH,programa_stn_xpath).text
                        except:
                            programa = -1
                            NoSuchElementException            
                    NoSuchElementException  

                    try:
                        titulo = driver.find_element(By.XPATH,titulo_xpath).text
                    except:
                        try:
                            titulo = driver.find_element(By.XPATH,titulo_stn_xpath).text
                        except:
                            titulo = -1
                            NoSuchElementException                    
                    NoSuchElementException        

                    try:
                        data = driver.find_element(By.XPATH,data_xpath).text
                    except:  
                        try:
                            data = driver.find_element(By.XPATH,data_stn_xpath).text
                        except:
                            data = -1
                            NoSuchElementException                      
                    NoSuchElementException  

                    noticia.click() #Abrindo a notícia               
                    time.sleep(5) #Esperando ela carregar

                    try:
                        subtitulo = driver.find_element(By.CLASS_NAME, "content-head__subtitle").text
                    except:
                        try: 
                            subtitulo = driver.find_element(By.CLASS_NAME, "playkit-video-info__ep-description playkit-video-info__ep-description--show-all").text
                        except:
                            subtitulo = -1
                            NoSuchElementException                
                    NoSuchElementException

                    try:
                        corpo = driver.find_element(By.CLASS_NAME, "mc-article-body").text
                    except:                    
                        corpo = -1
                    NoSuchElementException

                    try:
                        url = driver.current_url
                    except:
                        url = -1


                    print("Noticia " + str(i-1) + " sucesso!")
                    collected_successfully = True
                    driver.back() 
                    time.sleep(4)

                    noticias.append({
                        "Url" : url,
                        "Programa" : programa,
                        "Titulo" : titulo,
                        "Subtitulo" : subtitulo,
                        "Corpo" : corpo,
                        "Data" : data                    
                    })
                except:
                    print("Noticia " + str(i-1) + " falha :(")                
                    time.sleep(4)
                        
            time.sleep(2)
                                    
            #Como a página atualiza 15 notícias por vez, caso o i seja multiplo de 15, 
            # vou rolar para o fim da página para carregar mais notícias ou clicar no botão "Veja Mais"

            if(i%15 == 0 and i<60):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print('XPATH: ' + xpath_lista)
                print("i = " + str(i) + ", scrollou até o fim da página")
                time.sleep(3)
            elif(i%15 == 0 and i>=60):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            
                driver.find_element(By.XPATH,botao_veja_mais_xpath).click()
                print('XPATH: ' + xpath_lista)
                print("i = " + str(i) + ", scrollou até o fim da página e clicou no veja mais")                
                time.sleep(3)           

    except:
        driver.quit()

    return pd.DataFrame(noticias)



#print(noticias_g1("presidente lula", 10))
print(noticias_g1("presidente lula", 1))
#print(df_noticias_lula)


#### to do / problemas ### 
# - As datas que estiverem no formato "há X dias" ou "há X horas" devem ser colocadas no formato "dd/mm/aaaa HHhMM"