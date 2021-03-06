from datetime import datetime
from app.controller.obter_pagina import acessar_conteudo
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app.controller.eiprice_db import aplicar_banco
import time
"""
    Realiza a leitura da pagina após a autenticar
"""

driver: str = None

def obter_categorias(nome_categoria: str, usuario: str, senha: str):
    """Função para obter todas as sub-categorias

    Args:
        nome_categoria (str): _Nome da categoria para scraping _

    Returns:
        dict: _Dicionario contendo a chave como o nome da sub-categoria e o valor o link do acesso_
    """
    categorias: dict = {}
    
    # Instancia para receber a Class Selenium Driver autenticada
    global driver
    driver = acessar_conteudo("https://landing.shopper.com.br/", usuario, senha)
    
    # Realiza a espera do elementos enquanto carrega
    aguardar_elemento = WebDriverWait(driver, timeout=10)

    # Realiza o scraping com base no nome do departamento recebido no parametro
    departamento = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, f"//li[@department='{nome_categoria}']")))
    
    # O scraping retornar uma lista com todas as sub-categorias
    # Realiza o laço pulando sempre a primeira recebida, pois é um link para sub-categoria -> Todos
    # Utiliza um enumerate para poder realizar a separação da primeira sub-categoria -> Todos.
    for id, lista in enumerate(departamento.find_elements(By.TAG_NAME, "li")):
        if id > 0:
            sub_categoria = lista.find_element(By.TAG_NAME, "a")
            categorias[sub_categoria.get_attribute("text")] = sub_categoria.get_attribute("href")
    
    return categorias

# Essa função necessita ser refatorada
def extrair_dados(categoria) -> dict:
    """Função para obter as sub_categorias

    Args:
        categoria (_dict_): _Recebe um dicionario contendo como chave o nome da categoria para
        e o valor o link da categoria_
     Returns:
        _list_: _Retorna uma lista com os produtos percorrido_
    """
    print("Scraping...")
    for chave_categoria in categoria:
       
        """ Acessa a pagina da sub_categoria e cria um dicionario tendo como chave
        o nome do produto e valor o link.
        """
        
        driver.get(categoria[chave_categoria])
        
        # Aguarda a pagina carregar os elementos
        aguardar_elemento = WebDriverWait(driver, timeout=2)
        
        # Chama a função rolar_pagina passando como parametro o driver e a quantidade de vezes para repetir o precionar da tecla.
        rolar_pagina(driver)
        
        # Obtem todos os produtos listado na pagina
        lista_produtos: list = []
        lista_produtos = aguardar_elemento.until(expected_conditions.visibility_of_all_elements_located((By.XPATH, "//div[@id='subcategory']/div/div[3]/div/div")))
        # Recupera o nome da categoria em processo
        nome_categoria = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='subcategory']/div/div[1]/div[1]/p[1]"))).text
        
        print(nome_categoria)
        # Recupera o nome da sub-categoria em processo
        nome_sub_categoria = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='subcategory']/div/div[1]/div[1]/p[2]"))).text
        
        
        # Cria a tabela sub_categoria no banco de dados e gravar OBS: Realizar o relacionamentos
        aplicar_banco(f"CREATE TABLE sub_categoria (id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 42 CYCLE), id_categoria int NOT NULL, nome varchar, primary key (id), foreign key (id_categoria) references categoria (id) ON DELETE CASCADE ON UPDATE CASCADE)")
        aplicar_banco(f"INSERT INTO sub_categoria (nome, id_categoria) SELECT '{nome_sub_categoria}', (select id from categoria where nome = '{nome_categoria.lower()}') WHERE NOT EXISTS (SELECT * FROM sub_categoria WHERE nome = '{nome_sub_categoria}')")
        
        print(len(lista_produtos))
        
        for id,  lista in enumerate(lista_produtos):
            if id <= len(lista_produtos) - 2:
                try:
                    lista.find_element(By.TAG_NAME, "button").click()
                except:
                    print("Proxima categoria!")
                # Obter data hora
                dt = datetime.now()
                # Converter timestamp para gravar no banco
                ts = datetime.timestamp(dt)
                dt_hora = datetime.timestamp(dt)
                try:
                    nome_produto = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='react-root']/div[2]/div[2]/div/div/div/div[2]/div[2]/h2"))).text
                except:
                    nome_produto = None
                try:
                    imagen_produto = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='react-root']/div[2]/div[2]/div/div/div/div[2]/div/div/figure/img"))).get_attribute("src")
                except:
                    imagen_produto = None
                try:
                    valor_produto = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='react-root']/div[2]/div[2]/div/div/div/div[2]/div[2]/div/span[2]"))).text
                except:
                    valor_produto = 0
                try:
                    valor_medio = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='react-root']/div[2]/div[2]/div/div/div/div[3]/div[2]/span"))).text
                    valor_medio = valor_medio.replace("R$", "")
                    valor_medio.strip()
                except:
                    valor_medio = 0
                try:
                    desconto = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='react-root']/div[2]/div[2]/div/div/div/div[3]/div[3]/span"))).text
                except:
                    desconto = 0
                try: 
                    descricao = aguardar_elemento.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id='react-root']/div[2]/div[2]/div/div/div/p"))).text
                except:
                    descricao = None
            
                lista_valores_mercados: dict = {}
                # Realiza a coleta dos dados dos valores dos outros mercados
                for iten in range(1,4):
                    try:
                        valor_mercado = lista.find_element(By.XPATH, f"//div[@id='react-root']/div[2]/div[2]/div/div/div/div[3]/div/div[{iten}]")
                        lista_valores_mercados[obter_nome_mercados((valor_mercado.find_element(By.TAG_NAME, "img").get_attribute("src")))] = str(valor_mercado.find_element(By.TAG_NAME, "span").text).replace("R$", "").strip()
                    except:
                        pass
                
                # Tratando as variaveis antes de enviar para o banco.
                imagen: str = str(imagen_produto).strip()
                valor: str = str(valor_produto).strip()
                valor = valor.replace(",", ".")
                avg: str = str(valor_medio).strip()
                avg = avg.replace(",", ".")
                desconto: int = str(desconto).strip()
                desconto = desconto.replace("%", "")
                descricao: str =  str(descricao)
                
 
                # Criar tabela produto e cadastrar produtos no banco de dados
                aplicar_banco(f"CREATE TABLE produto (id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 101 CYCLE), nome varchar, primary key (id), img varchar, valor decimal, avg decimal, desconto int, descricao varchar, dt_hora varchar, id_sub_categoria int NOT NULL, foreign key (id_sub_categoria) references sub_categoria (id) ON DELETE CASCADE ON UPDATE CASCADE)")
                aplicar_banco(f"INSERT INTO produto (nome, img, valor, avg, desconto, descricao, dt_hora, id_sub_categoria) SELECT '{nome_produto}', '{imagen}', '{valor}', '{avg}', '{desconto}', '{descricao}', '{dt_hora}', (select id from sub_categoria where nome = '{nome_sub_categoria}') WHERE NOT EXISTS (SELECT * FROM produto WHERE nome = '{nome_produto}')")

                # Criar tabela outro e cadastrar os valores no banco de dados
                aplicar_banco(f"CREATE TABLE outro (id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 81 CYCLE), nome varchar, primary key (id), valor decimal, id_produto int NOT NULL, foreign key (id_produto) references produto (id) ON DELETE CASCADE ON UPDATE CASCADE)")
                
                # Loop para percorer o dicionario dos valores obtidos dos concorrentes
                for iten in lista_valores_mercados:
                    valor_outro: str = str(lista_valores_mercados[iten])
                    valor_outro: str = valor_outro.replace(",", "")
                    valor_outro: str = valor_outro.strip()
                # Inseri o item extraido no banco de dados
                    aplicar_banco(f"INSERT INTO outro (nome, valor, id_produto) values ('{iten}', '{valor_outro}', (select id from produto where nome = '{nome_produto}'))")
                
                
                # Fecha a tela de detalhes dos produtos aberta
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
        
        

#def rolar_pagina(driver: str, qtd: int):
def rolar_pagina(driver: str):
    """Função para rolar a pagina pausadamente e carregar os conteudos dinamicos.

    Args:
        driver (str): _Recebe a pagina_
        qtd (int): _Recebe a quantidade que o loop vai percorre a pagina_
    """
    # for x in range(0,qtd):
    for x in range(0, 30):
        time.sleep(0.3)
        driver.execute_script('window.scrollBy(0, 1200)')
        
    # for x in range(0,qtd):
    for x in range(0, 30):
        time.sleep(0.3)
        ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
        

def obter_nome_mercados(url_logo: str) -> str:
    """Função para poder comparar as url das imagens e definir o nome do mercado conforme a url

    Args:
        url_logo (str): _Recebe a url da logo_

    Returns:
        _str_: _Retorna o nome do mercado_
    """
    switch={
        "https://d2om08pcbtz1n1.cloudfront.net/media/mercados/supermercados_1458250868_TS7N1fZCCWs11L31Ge31cpGtR9tJ0r.png": "sonda",
        "https://d2om08pcbtz1n1.cloudfront.net/media/mercados/supermercados_1434573567_Nz0N8kcVQn1572z0DZLhLd8VhmkFS6.png": "extra",
        "https://d2om08pcbtz1n1.cloudfront.net/media/mercados/supermercados_1438477076_J2F57cSBn5wV9jjUJ7I9EZXX1gM2m6.jpg": "pa"
    }
    return switch.get(url_logo)