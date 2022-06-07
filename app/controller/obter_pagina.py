from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

"""
    Autenticar na pagina
"""

def acessar_conteudo(link_pagina: str, usuario: str, senha: str) -> None: 
    
    """
        Função para acessar e logar na pagina, recebe como um paramento o link.
    Args:
        link_pagina (str): _Endereço do link_

    Returns:
        _dict_: _Class Selenium Driver_
    """
    try:
        driver: str = None
    
        endereco = link_pagina
    
        # ChromeOptions para passar argumentos ao abrir o navegador, neste caso ocultar o navegador.
        opcoes_navegador =  ChromeOptions()

        # Abrir o navegador em modo headless, ou seja oculto sem utilizar rescursos graficos
        opcoes_navegador.add_argument("--headless")
    
        opcoes_navegador.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Passa o paramento ocultar_navegador quando instanciar o Chrome(ocultar_navegador)
        driver = Chrome(options=opcoes_navegador)
    
        driver.maximize_window()

        # Abrir endereco do paramentro
        driver.get(endereco)

        # Aguarda os elemento carregar para poder dar sequencia.
        driver_wait = WebDriverWait(driver, timeout=10)
    
        # Localiza o botão de entrar e clica
        botao_entrar = driver_wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='benefits']/div/div[1]/span/a")))
        botao_entrar.click()
    
    
        # Realiza a buscar do campo email
        entrada_email = driver_wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "[name='email']")))
        entrada_email.send_keys(usuario)

        # Realiza a buscar do campo senha e dar enter para entrar logar
        driver.find_element(By.CSS_SELECTOR, "[name='senha']").send_keys(senha + Keys.RETURN)

        return driver
        
    except:
        print("elemento não localizado")
      
    