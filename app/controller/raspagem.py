import requests
from app.models.assortment import Assortment
from datetime import datetime


#Criar instancia do objeto
assortment = Assortment

def obter_dados() -> Assortment:
    """Função para realizar a raspagem do dados

    Returns:
        list: _Lista contendo dos os dicionarios extraido do site_
    """
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
            print(subcategoria['name'])
            while not last:
                page += 1
                #Montagem da url para solicitar o request passando como paramentro o cabeçalho montado.
                url = f"{base_url}/products?department={lista['id']}&subdepartment={subcategoria['id']}&page={page}&size=20&"
                response = requests.get(url, headers=header)
                data = response.json()
                
                for contador in range(0,len(data['products'])):
                    assortment.sku = data["products"][contador]["id"]
                    assortment.url = data["products"][contador]["url"]
                    assortment.name = data["products"][contador]["name"]
                    assortment.image = data["products"][contador]["image"]
                    assortment.price_to = data["products"][contador]["price"]
                    assortment.discount = data["products"][contador]["savingPercentage"]
                    assortment.department = data["products"][contador]["metadata"]["department_url"]
                    assortment.category = data["products"][contador]["metadata"]["subdepartment_url"]
                    assortment.available = data["products"][contador]["paused"]
                    assortment.stock_qty = data["products"][contador]["maxCartQuantity"]
                    assortment.created_at = datetime.today().strftime("%Y-%m-%d")
                    assortment.hour = datetime.today().strftime("%H:%M:%S")
                    last = data["last"]
                
    return assortment