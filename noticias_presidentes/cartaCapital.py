########### Visão geral do scritp e estrutura do site ###########
# O scripts acessa as páginas da Revista Carta Capital.
# Apenas acessadas são desse tipo https://www.cartacapital.com.br/page/1/?s=presidente+lula
# Cada página dessa possui 10 manchetes.
# As tags de busca são pré-definidos em "tags_lista"
# O número de páginas é definido em "num_pages_to_extract"
# Então, o número de notícias a ser coletadas é definida por:
    # num_pages_to_extract*len_tags_lista*10 = num_pages_to_extract*len_tags_lista*num_manchetes
    
########### Funcionamento ###########    
    # 1) Acessa www.cartacapital.com.br/tag/NOME_TAG/page/X, 
            # em que nome_tag pode ser, por exemplo, "lula" ou "jair-bolsonaro" e X é o número da páginas
    # 2) Coleta todos os titulos, subtitulos, datas e urls das noticiais
    # 3) Os passos anteriores são executados de acordo com o número de páginas estabelecido (num_pages_to_extract)
    # 4) Após essa coleta, cada um dos links das noticias sao acessados e o corpo da noticia (corpo_noticia) é extraido
    # 5) Por fim, esses dados sao armazenado em um dataframe e salve em um arquivo .csv com separador ';'
    # 6) Ao utilizar, modifique 'PATH_WEBDRIVE' e cogite alterar 'path_to_save_csv', 'num_pages_to_extract' ou 'tags_lista'
    # 7) acrescentar tratamento quando o numero de "num_pages_to_extract" for maior do que a quantidade disponivel no site


########### to do / problemas ###########
#1 - melhorar limpeza do corpo_noticia
#2 - acrescetar a limpeza do outro bloco "leia tambem:"
#3 - melhorar o tratamento dos casos em que a manchete 
    # nao tem subtitulo ou alterar a forma de coleta desse e dos outros dados que soa extraidos da mesma pagina
#4 - padronizar formato de data-hora conforme o padrao que sera usado por todos 
#5 - transformar primeira parte em funcao para generaliza a busca (possibilidade de usar tags variaveis)
#6 - analisar uso do separador ';' em "df.to_csv(path_to_save_csv, sep=';')"
#7 - [PRIORITARIO] alterar(/adicionar outro) momento de salvamento do dataframe para nao armazenar muitos dados em "todos_dados"
#8 - remover duplcates dict lista urls ou todos os dados, antes de coletar o corpo da noticia
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
# https://stackoverflow.com/questions/54501445/i-want-to-right-click-and-open-link-in-new-tab-using-selenium-with-python
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
import numpy as np

#https://stackoverflow.com/questions/37883759/errorssl-client-socket-openssl-cc1158-handshake-failed-with-chromedriver-chr
#https://stackoverflow.com/questions/69441767/error-using-selenium-chrome-webdriver-with-python
#https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#localizacao do webdriver
PATH_WEBDRIVER = 'C:/Users/wendel.DESKTOP-FE0U6IU/Documents/pangeia/montagem_datasets/chromedriver_win32/chromedriver.exe'
# numero de noticias que aparecem em cada pagina de busca 
  # modificar apenas se o objetivo for extrair menos noticias por pagina
NUM_NOTICIAS_POR_PAGE = 10

def tratamento_leia_tambem_1(corpo_noticia, qtd_leia_tambem):

    ############### #VISAO GERAL SOBRE A FUNCAO ############### 
    #pra que serve?
        #Função responsável por fazer o tratamento do trecho "Leia tambem"
        #Foram identificadas duas estrutura: 
            # na pimeira, aparentemente, aparece em uma única linha entre os paragrafos e podem conter um ou mais "leia tambem"; 
            # na segunda, as noticias do "leia tambem" aparecem em um unico bloco, sendo que cada bloco contem duas ou mais noticiais linkadas, apararentemente 
        # Possíveis exemplos:
            # Estrutura 1: https://www.cartacapital.com.br/justica/carta-aberta-ao-presidente-lula/
            # Estrutura 2: https://www.cartacapital.com.br/politica/vamos-ve-lo-presidente-novamente-diz-zapatero-a-lula-na-espanha/  
    
    #como funciona?
        #por enquanto, faz o tratamento apenas do segundo caso
        #identifica no corpo_noticia coletado a localizacao do trecho "leia tambem:\n" e salva a posição
        #a partir dessa posicao, é executado um while que so para quando encontrar o "\n" da ultima noticia linkada
        #neste laço, as posicoes de cada uma das palavras que aparecem no bloco "leia tambem" sao armazenadas na ista "indices_palavras_ignorar"
        #antes disso, para saber a quantidade de links, é coletada a quantidade da estrtura "driver.find_elements_by_class_name('box-news-thumb-text')" e armazenada em "qtd_leia_tambem"
        #por fim, é executado um for que, ao armazena as palavras do corpo_noticia coletado, ignora as palavras armazenada em "indices_palavras_ignorar"
    ###########################################################
        
    #faz a quebra do corpo_noticia coletado de acordo com os espaços entre as palavras
    corpo_noticia = corpo_noticia.split(' ')
    corpo_noticia_novo = ''
    
    indices_palavras_ignorar = []
    count = 0
    qtd_quebra_linha = 0

    #duas a duas palavras, o texto é percorrido 
    for palavra_atual, palavra_seguinte in zip(corpo_noticia, corpo_noticia[1:]):
        count +=2

        if ('Leia' in palavra_atual and 'também:\n' in palavra_seguinte) == True:

            count_2 = int((count-2)/2)

            indices_palavras_ignorar.append(count_2)
            count_2+=1

            while True:
                #roda da posicao do "leia também:\n" até o "\n" da ultima noticia linkada no bloco "Leia tambem"
                if qtd_quebra_linha > qtd_leia_tambem:

                    i = 0
                    for palavra in corpo_noticia:
                        #armazena a noticia coletada em "corpo_noticia_novo" ignorando as palavras
                            #nas posicoes armazenadas em "indices_palavras_ignorar"
                        if (i in indices_palavras_ignorar) == False:
                            corpo_noticia_novo = str(corpo_noticia_novo) + palavra +' '
                        i+=1

                    break 

                if '\n' in corpo_noticia[count_2]:
                    qtd_quebra_linha+=1

                indices_palavras_ignorar.append(count_2)
                count_2+=1
                
    return corpo_noticia_novo

def tratamento_receba_noticias(corpo_noticia):
    ############### #VISAO GERAL SOBRE A FUNCAO ############### 
    #pra que serve?
        #Função responsável por fazer o tratamento do trecho "RECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL"
        #Foram identificadas duas estrutura: na pimeira, apenas o titulo ("receba...") ficou visivel; na segunda, todo o conteudo do bloco foi coletado
        # Possíveis exemplos:
            # Estrutura 1: https://www.cartacapital.com.br/justica/carta-aberta-ao-presidente-lula/
            # Estrutura 2: https://www.cartacapital.com.br/politica/vamos-ve-lo-presidente-novamente-diz-zapatero-a-lula-na-espanha/  
    
    #como funciona?
        #Realiza o split em cima de cada um dos trechos visiveis, com isso sao removidos do trecho coeltado
        #O resultado do split é entao concatenado para unir os trechos originais da noticia
    ###########################################################

    if '\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL' in corpo_noticia:
        corpo_noticia = corpo_noticia.split('\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL')
        corpo_noticia = corpo_noticia[0] + corpo_noticia[1]
        
    elif '\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL\nOK\nAceito receber promoções e informações\nNão utilizamos seus dados para enviar nenhum tipo de spam.' in corpo_noticia:
        corpo_noticia = corpo_noticia.split('\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL\nOK\nAceito receber promoções e informações\nNão utilizamos seus dados para enviar nenhum tipo de spam.')
        corpo_noticia = corpo_noticia[0] + corpo_noticia[1]

    return corpo_noticia

def extracao_corpo_noticia_manchete(url, driver):
    ############### #VISAO GERAL SOBRE A FUNCAO ############### 
    # pra que serve?
        # extrair o corpo_noticia
    
    # como funciona?
        # é feita a extracao de todos os trechos <p> visiveis (que, aparentemente, englobam apenas o bloco de noticias)
        # é realizada tambem a limpeza do corpo_noticia (remocao de alguns blocos, exemplo "leita também:" e sobre assinatura da revista)
    ###########################################################
    driver.get(url)
    time.sleep(6)
  
    #Faz a extracao da noticia e alguns tratamentos para remoção de trechos irrelevantes (blocos de publicidades nao sao coletados)
    corpo_noticia = driver.find_element_by_class_name('eltdf-post-text-inner').text 

    #extrai a quantidade de noticias que estao likadas no bloco "leia tambem"
        # find_elements elementos retorna uma lista com todos os itens encontrado
        #a partir disso, é capturado o tamanho da lista
    qtd_leia_tambem = driver.find_elements_by_class_name('box-news-thumb-text')
    qtd_leia_tambem = len(qtd_leia_tambem)

    #remove texto que aparece junto ao reprodutor 
    corpo_noticia = corpo_noticia.split('ouça este conteúdo\nreadme.ai\nplay_circle_outline\n')[1]
    #revome bloco sobre assinatura e doação
    corpo_noticia = corpo_noticia.split('Um minuto, por favor...')[0]    

    #tratamento do bloco "RECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL"    
    corpo_noticia = tratamento_receba_noticias(corpo_noticia)

    #tratamento do bloco "leia tambem"
    if "leia também:\n" in corpo_noticia:
        corpo_noticia = tratamento_leia_tambem_1(corpo_noticia, qtd_leia_tambem)
    
    return corpo_noticia
 
def captura_dados_basicos_manchetes(num_pages_to_extract, tags_lista):

    ############### VISAO GERAL SOBRE A FUNCAO ############### 
    # pra que serve?
        # extrair dados basicos das noticias 
            #dados basicos = titulo, subtitulo, data, url
    
    # como funciona?
        # o script passa por todas as paginas que possui os resultados das buscas 
            #(exemplo https://www.cartacapital.com.br/page/1/?s=presidente+lula), conforme "num_pages_to_extract"
        # em cada uma dessas paginas, sao coletados os dados basicos
    ###########################################################
    
    urls_elements = []
    dados_basicos = []
    
    url_carta_capital = 'https://www.cartacapital.com.br/tag/'

    driver = webdriver.Chrome(executable_path = PATH_WEBDRIVER, options=options)
    print('\n\n\n---- EXTRAÇÃO DADOS BÁSICOS ----')
    for tag in tags_lista:
        print('############## Tag: ' + tag)
        for num_page in range(num_pages_to_extract):
            num_page+=1
            print('Página: {}/{}'.format(num_page, num_pages_to_extract))
            datas_manchetes = []
            subtitulos = []
            titulos = []
            urls_elements= []
          
            #formato da url = https://www.cartacapital.com.br/tag/jair-bolsonaro/page/3/
                            # https://www.cartacapital.com.br/tag/NOME_TAG/page/NUM_PAGE/
            url_completa = url_carta_capital+ tag +'/page/'+str(num_page)+'/' 
            driver.get(url_completa)
            time.sleep(6)  
            
            # NUM_NOTICIAS_POR_PAGE = 10 é o padrão
                # atualmente, cada pagina tem 10 manchete
            for num_artigo in range(1, NUM_NOTICIAS_POR_PAGE + 1):
        
                titulo_e_url = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div[1]/div[2]/div/div/div[1]/div/div[1]/article[{}]/div/h3/a'.format(num_artigo))
                titulo = titulo_e_url.get_attribute('innerHTML')
                url_noticia = titulo_e_url.get_attribute('href')
                
                # autoria = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div/div[1]/div/div[1]/article[{}]/div/div[3]/div[1]/div[2]/a[2]'.format(num_artigo))
                # autoria = autoria.get_attribute('innerHTML')

                try: 
                    data_manchete = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div/div[1]/div/div[1]/article[{}]/div/div[3]/div[1]/div[1]'.format(num_artigo)).text
                except NoSuchElementException:
                    data_manchete = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/div[2]/div/div/div[1]/div/div[1]/article[{}]/div/div[2]/div[1]/div[1]'.format(num_artigo)).text
                
                #algumas manchetes nao possuem subtitulo
                try:
                    subtitulo = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div[1]/div[2]/div/div/div[1]/div/div[1]/article[{}]/div/p'.format(num_artigo))
                    subtitulo = subtitulo.get_attribute('innerHTML')
                except IndexError:
                    subtitulo = None             

                coluna = url_noticia.split('/')[3]                  

                dados_basicos.append({
                                      'url_noticia': url_noticia, 
                                      'titulo': titulo, 
                                      'subtitulo': subtitulo, 
                                      'coluna': coluna,
                                      'data_manchete': data_manchete
                                      })
    
    driver.quit()
    return dados_basicos

def salva_dados(todos_dados, df, path_to_save_csv): 
    df = df.append(todos_dados, ignore_index=True)
    df.drop_duplicates(inplace=True)
    df.to_csv(path_to_save_csv, sep=';', index=False)

    return df

def main ():
    todos_dados = []
    todas_urls = []
    #definicao do dataframe que irá armazenado os dados coletados
    df = pd.DataFrame(columns=['site',  'url_noticia', 'titulo', 'subtitulo', 'coluna', 'corpo_noticia', 'data_noticia'])
    #local em que o csv com os dados do "df" serao salvos
    path_to_save_csv = 'cartaCapital.csv'
    #quantidade de paginas da seção de busca que devem ser acessadas
    num_pages_to_extract = 30
    # termos de buscas
    tags_lista = ['lula', 'jair-bolsonaro']

    #recebe dados basicos das noticias (titulo, subtitulo, data, url)
    dados_basicos = captura_dados_basicos_manchetes(num_pages_to_extract, tags_lista)
    # dados_basicos = list(np.unique(dados_basicos))

    driver = webdriver.Chrome(executable_path = PATH_WEBDRIVER, options=options)
    contador_noticias = 0

    print('\n\n\n---- EXTRAÇÃO CORPO NOTÍCIA ----')
    for dado in dados_basicos:
        print('Notícia: {}/{}'.format(contador_noticias+1, len(dados_basicos)))
        corpo_noticia = extracao_corpo_noticia_manchete(dado['url_noticia'], driver)
        
        todos_dados.append({'site':'CartaCapital', 
                            'url_noticia': dado['url_noticia'], 
                            'titulo': dado['titulo'], 
                            'subtitulo': dado['subtitulo'],
                            'coluna': dado['coluna'],
                            'data_noticia': dado['data_manchete'], 
                            'corpo_noticia': corpo_noticia})
        if contador_noticias%50 == 0:
            print('---- EXTRAÇÃO CORPO NOTÍCIA ----')
            df = salva_dados(todos_dados, df, path_to_save_csv)
        contador_noticias+=1

    driver.quit()
    salva_dados(todos_dados, df, path_to_save_csv)
    # print(df) 

if __name__ == "__main__":
    main()
 

 
