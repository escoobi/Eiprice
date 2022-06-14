import requests


def obter_dados() -> list:
    """Função para realizar a raspagem do dados

    Returns:
        list: _Lista contendo dos os dicionarios extraido do site_
    """
    #Lista para retontar os dicionarios
    dados_coletados: list = []
    #Url da base Json
    base_url = "https://siteapi.shopper.com.br/catalog"
    # Coletear o valor no site
    bearer = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjo5ODEwOTUsImRldmljZVVVSUQiOiJiNGU0OTAwYS0zNDE2LTQ2NmMtODYyOS03ZjIxYjQxNGNjMzciLCJpYXQiOjE2NTUxNDE2NDd9.D7earQVzuWpJCHRoliYNlfsnhKfXGGRO7ZLRp9dJlxM"
    #Formular cabeçalho
    header = {'Authorization': bearer}
    response = requests.get(url=f"{base_url}/departments", headers=header)
    data = response.json()
    dados: dict = {}
    dados = data
    
    #List Comprehensions no departamento de Alimentos
    departments = [lista for lista in dados["departments"] if lista["name"] == "Alimentos"]
    
    #Laço para formular e extrair dos dicionarios obtidos
    for lista in departments:
        #Laço dentro do deparamento para coletar os sub-departamentos
        for subcategoria in lista["subdepartments"]:
            page = 0
            last = False
            while not last:
                page += 1
                #Montagem da url para solicitar o request passando como paramentro o cabeçalho montado.
                url = f"{base_url}/products?department={lista['id']}&subdepartment={subcategoria['id']}&page={page}&size=20&"
                response = requests.get(url, headers=header)
                data = response.json()
                #dados: dict = {}
                #dados = data
                dados_coletados.append(data["products"])
                last = data["last"]
    
    return dados_coletados