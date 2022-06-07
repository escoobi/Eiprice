from app.controller.scraping import extrair_dados, obter_categorias
from app.controller.eiprice_db import aplicar_banco, consultar
from fastapi import FastAPI
from typing import Union
import pandas as pd


# Cria a tabela e adiciona a categoria.
aplicar_banco(f"CREATE TABLE categoria (id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 42 CYCLE), nome varchar, primary key (id))")
aplicar_banco(f"INSERT INTO categoria (nome) SELECT 'alimentos' WHERE NOT EXISTS (SELECT * FROM categoria WHERE nome = 'alimentos')")


# Chama a função para realizar o scraping e armazenas no banco de dados
extrair_dados(obter_categorias("alimentos", "gustavo.euguga@gmail.com", "Es05727143.."))

app = FastAPI()

@app.get("/")
async def root():
    df = pd.DataFrame(consultar("select categoria.nome, sub_categoria.nome, produto.id, produto.nome, produto.img, produto.valor, produto.desconto, produto.dt_hora from produto inner join sub_categoria on sub_categoria.id = produto.id_sub_categoria inner join categoria on categoria.id = sub_categoria.id_categoria"), columns =['categoria', 'departamento', 'id', 'nome', 'img', 'valor', 'desconto', 'data_hora'])
    df.to_csv('assortment.csv')
    return df.to_dict()

@app.get("/seller")
async def seller():
    df = pd.DataFrame(consultar("select categoria.nome, sub_categoria.nome, produto.id, produto.nome, produto.img, produto.valor, produto.desconto, produto.dt_hora from produto inner join sub_categoria on sub_categoria.id = produto.id_sub_categoria inner join categoria on categoria.id = sub_categoria.id_categoria"), columns =['categoria', 'departamento', 'id', 'nome', 'img', 'valor', 'desconto', 'data_hora'])
    df.to_csv('seller.csv')
    return df.to_dict()

@app.get("/categoria/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

