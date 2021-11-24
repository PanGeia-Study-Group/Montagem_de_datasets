########### Visão geral do scritp e estrutura do site ###########
# O scripts acessa as páginas da Revista Carta Capital.
# Apenas acessadas são desse tipo https://www.cartacapital.com.br/page/1/?s=presidente+lula
# Cada página dessa possui 10 manchetes.
# Os termos de busca são pré-definidos em "termos_busca"
# O número de páginas é definido em "num_pages_to_extract"
# Então, o número de notícias a ser coletadas é definida por:
    # num_pages_to_extract*qtd_conjunto_termos_busca*10 = num_pages_to_extract*qtd_conjunto_termos_busca*num_manchetes
    
########### Funcionamento ###########    
    # 1) Acessa www.cartacapital.com.br/page/NUM_PAGINA/?s=TERMOS_BUSCA
    # 2) Coleta todos os titulos, subtitulos, datas e urls das noticiais
    # 3) Os passos anteriores são executados de acordo com o número de páginas estabelecido (num_pages_to_extract)
    # 4) Após essa coleta, cada um dos links das noticias sao acessados e o corpo da noticia (texto) é extraido
    # 5) Por fim, esses dados sao armazenado em um dataframe e salve em um arquivo .csv com separador ';'
    # 6) Ao utilizar, modifique 'PATH_WEBDRIVE' e cogite alterar 'path_to_save_csv', 'num_pages_to_extract' ou 'termos_busca'
                

########### to do / problemas ###########
#1 -  melhorar limpeza do texto
#2 - acrescetar a limpeza do outro bloco "leia tambem:"
#3 - melhorar o tratamento dos casos em que a manchete 
    # nao tem subtitulo ou alterar a forma de coleta desse e dos outros dados que soa extraidos da mesma pagina
#4 - padroniza formato de data-hora conforme o padrao que sera usado por todos 
#5 - transforma primeira parte em funcao para generaliza a busca (possibilidade de usar de termos de busca variaveis)
#6 - analisar uso do separador ';' em "df.to_csv(path_to_save_csv, sep=';')"
#7 - [PRIORITARIO] alterar(/adicionar outro) momento de salvamento do dataframe para nao armazenar muitos dados em "todos_dados"
#8 - acrescentar tratamento quando o numero de "num_pages_to_extract" for maior do que a quantidade disponivel no site


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
import numpy as np

#localizacao do webdriver
PATH_WEBDRIVER = 'PATH/chromedriver_win32/chromedriver.exe'
# numero de noticias que aparecem em cada pagina de busca 
  # modificar apenas se o objetivo for extrair menos noticias por pagina
NUM_NOTICIAS_POR_PAGE = 10

def tratamento_leia_tambem_1(texto, qtd_leia_tambem):

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
        #identifica no texto coletado a localizacao do trecho "leia tambem:\n" e salva a posição
        #a partir dessa posicao, é executado um while que so para quando encontrar o "\n" da ultima noticia linkada
        #neste laço, as posicoes de cada uma das palavras que aparecem no bloco "leia tambem" sao armazenadas na ista "indices_palavras_ignorar"
        #antes disso, para saber a quantidade de links, é coletada a quantidade da estrtura "driver.find_elements_by_class_name('box-news-thumb-text')" e armazenada em "qtd_leia_tambem"
        #por fim, é executado um for que, ao armazena as palavras do texto coletado, ignora as palavras armazenada em "indices_palavras_ignorar"
    ###########################################################
        
    #faz a quebra do texto coletado de acordo com os espaços entre as palavras
    texto = texto.split(' ')
    texto_novo = ''
    
    indices_palavras_ignorar = []
    count = 0
    qtd_quebra_linha = 0

    #duas a duas palavras, o texto é percorrido 
    for palavra_atual, palavra_seguinte in zip(texto, texto[1:]):
        count +=2

        if ('Leia' in palavra_atual and 'também:\n' in palavra_seguinte) == True:

            count_2 = int((count-2)/2)

            indices_palavras_ignorar.append(count_2)
            count_2+=1

            while True:
                #roda da posicao do "leia também:\n" até o "\n" da ultima noticia linkada no bloco "Leia tambem"
                if qtd_quebra_linha > qtd_leia_tambem:

                    i = 0
                    for palavra in texto:
                        #armazena a noticia coletada em "texto_novo" ignorando as palavras
                            #nas posicoes armazenadas em "indices_palavras_ignorar"
                        if (i in indices_palavras_ignorar) == False:
                            texto_novo = str(texto_novo) + palavra +' '
                        i+=1

                    break 

                if '\n' in texto[count_2]:
                    qtd_quebra_linha+=1

                indices_palavras_ignorar.append(count_2)
                count_2+=1
                
    return texto_novo

def tratamento_receba_noticias(texto):
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

    if '\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL' in texto:
        texto = texto.split('\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL')
        texto = texto[0] + texto[1]
        
    elif '\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL\nOK\nAceito receber promoções e informações\nNão utilizamos seus dados para enviar nenhum tipo de spam.' in texto:
        texto = texto.split('\nRECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL\nOK\nAceito receber promoções e informações\nNão utilizamos seus dados para enviar nenhum tipo de spam.')
        texto = texto[0] + texto[1]

    return texto

def extracao_texto_manchete(url, driver):
    ############### #VISAO GERAL SOBRE A FUNCAO ############### 
    # pra que serve?
        # extrair o texto da noticia 
    
    # como funciona?
        # é feita a extracao de todos os trechos <p> visiveis (que, aparentemente, englobam apenas o bloco de noticias)
        # é realizada tambem a limpeza do texto (remocao de alguns blocos, exemplo "leita também:" e sobre assinatura da revista)
    ###########################################################
    driver.get(url)
    time.sleep(7)
  
    #Faz a extracao da noticia e alguns tratamentos para remoção de trechos irrelevantes (blocos de publicidades nao sao coletados)
    texto = driver.find_element_by_class_name('eltdf-post-text-inner').text 

    #extrai a quantidade de noticias que estao likadas no bloco "leia tambem"
        # find_elements elementos retorna uma lista com todos os itens encontrado
        #a partir disso, é capturado o tamanho da lista
    qtd_leia_tambem = driver.find_elements_by_class_name('box-news-thumb-text')
    qtd_leia_tambem = len(qtd_leia_tambem)

    #remove texto que aparece junto ao reprodutor 
    texto = texto.split('ouça este conteúdo\nreadme.ai\nplay_circle_outline\n')[1]
    #revome bloco sobre assinatura e doação
    texto = texto.split('Um minuto, por favor...')[0]    

    #tratamento do bloco "RECEBA AS NOTÍCIAS DE CARTACAPITAL TODOS OS DIAS NO SEU E-MAIL"    
    texto = tratamento_receba_noticias(texto)

    #tratamento do bloco "leia tambem"
    if "leia também:\n" in texto:
        texto = tratamento_leia_tambem_1(texto, qtd_leia_tambem)
    
    return texto
 
def captura_dados_basicos_manchetes(num_pages_to_extract, termos_busca):

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
    
    #Formato da url https://www.cartacapital.com.br/page/NUM_PAGE/?s=presidente+NOME_PRESIDENTE
    url_carta_capital = 'https://www.cartacapital.com.br/page/'


    driver = webdriver.Chrome(executable_path = PATH_WEBDRIVER)
    for termos in termos_busca:
        for num_page in range(num_pages_to_extract):
            datas_manchetes = []
            subtitulos = []
            titulos = []
            urls_elements= []
          
            url_completa = url_carta_capital+str(num_page+1)+termos 
            driver.get(url_completa)
            time.sleep(7)  
            
            # coleta os WebElements
            urls_elements = driver.find_elements_by_class_name('eltdf-pt-link')
            titulos = driver.find_elements_by_class_name('eltdf-pt-link') 
            subtitulos = driver.find_elements_by_class_name('eltdf-post-excerpt')                                        
            datas = driver.find_elements_by_class_name('eltdf-post-info-date')                           

            # extra o valor de WebElement (textos e links)
            for aux_2 in range(10):
            
                url = urls_elements[aux_2].get_attribute('href')
                titulo = titulos[aux_2].get_attribute('innerHTML')
                
                #usado por causa de manchetes que nao possuem subtitulo
                try:
                    subtitulo = subtitulos[aux_2].get_attribute('innerHTML')
                except IndexError:
                    subtitulo = 'sem_subtitulo'
                    
                data_manchete = datas[aux_2].get_attribute('innerHTML')
                data_manchete = data_manchete.split('/">\n')[1]
                data_manchete = data_manchete.split(' </a>\n')[0]

                dados_basicos.append({'titulo': titulo, 'subtitulo': subtitulo, 
                                        'url': url, 'data_manchete': data_manchete})
    
    driver.quit()
    return dados_basicos

def main ():
    todos_dados = []
    todas_urls = []
    #definicao do dataframe que irá armazenado os dados coletados
    df = pd.DataFrame(columns=['titulo', 'subtitulo', 'data_noticia', 'texto', 'url'])
    #local em que o csv com os dados do "df" serao salvos
    path_to_save_csv = 'cartaCapital.csv'
    #quantidade de paginas da seção de busca que devem ser acessadas
    num_pages_to_extract = 1
    # termos de buscas
    termos_busca = ['/?s=presidente+lula', '/?s=presidente+bolsonaro']

    #recebe dados basicos das noticias (titulo, subtitulo, data, url)
    dados_basicos = captura_dados_basicos_manchetes(num_pages_to_extract, termos_busca)
    # dados_basicos = list(np.unique(dados_basicos))

    driver = webdriver.Chrome(executable_path = PATH_WEBDRIVER)
    for dado in dados_basicos:
        texto = extracao_texto_manchete(dado['url'], driver)
        print(dado['titulo'])
        todos_dados.append({'titulo': dado['titulo'], 'subtitulo': dado['subtitulo'], 
                            'data_noticia': dado['data_manchete'], 'texto': texto, 'url': dado['url']})

    driver.quit()
    df = df.append(todos_dados, ignore_index=True)
    df.drop_duplicates(inplace=True)
    df.to_csv(path_to_save_csv, sep=';')
    print(df)    

if __name__ == "__main__":
    main()