from app.controller.scraping import extrair_dados, obter_categorias
from app.controller.eiprice_db import aplicar_banco, consultar
from fastapi import FastAPI
import pandas as pd


# Cria a tabela e adiciona a categoria.
#aplicar_banco(f"CREATE TABLE categoria (id INTEGER GENERATED BY DEFAULT AS IDENTITY (START WITH 42 CYCLE), nome varchar, primary key (id))")
#aplicar_banco(f"INSERT INTO categoria (nome) SELECT 'alimentos' WHERE NOT EXISTS (SELECT * FROM categoria WHERE nome = 'alimentos')")


# Chama a função para realizar o scraping e armazenas no banco de dados
#extrair_dados(obter_categorias("alimentos", "*", "*"))

app = FastAPI()

@app.get("/")
async def root():
    return "Teste Eiprice para backend."


@app.get("/categoria/")
async def read_categoria():
    """Rota para lista todas as categorias cadastradas

    Returns:
        _dict_: _Retorna um dicionario com todas as categoria cadastrada no banco de dados_
    """
    dados_recebido = consultar(f"select id, nome from categoria")
    df = pd.DataFrame(dados_recebido, columns=['id', 'nome'])
    dd = df.set_index("id").T.to_dict("dict")
    return dd


@app.get("/categoria/{id_categoria}")
async def read_categoria_id(id_categoria: str):
    """Rota para consultar a categoria cadastra

    Args:
        id_categoria (str): _recebe um valor inteiro referente ao id cadastrado no banco de dados da categoria_

    Returns:
        _dicr_: _Retorna um dicionario contendo o id e nome da categoria seleciona_
    """
    dados_recebido = consultar(f"select id, distinct(nome) from categoria where id = '{id_categoria}'")
    df = pd.DataFrame(dados_recebido, columns=['id', 'nome'])
    dd = df.set_index("id").T.to_dict("dict")
    return dd


@app.get("/categoria/departamento/")
async def read_departamento():
    """Rota para listar todos os departamento cadastrado no banco de dados

    Returns:
        _dict_: _Retorna um dicionario contendo o id e nome dos departamento cadastrado_
    """
    dados_recebido = consultar(f"select id, nome from sub_categoria")
    df = pd.DataFrame(dados_recebido, columns=['id','nome'])
    dd = df.set_index("id").T.to_dict("dict")
    return dd

@app.get("/categoria/departamento/{id_departamento}")
async def read_departamento_id(id_departamento: str):
    """Rota para consulta do departamento

    Args:
        id_departamento (str): _Passa como paramentro o numero referente ao id cadastrado do departamento no banco de dados_

    Returns:
        _dict_: _Retorna um dicionario contendo id e nome do departamento selecionado_
    """
    dados_recebido = consultar(f"select id, nome from sub_categoria where id = '{id_departamento}'")
    df = pd.DataFrame(dados_recebido, columns=['id', 'nome'])
    dd = df.set_index("id").T.to_dict("dict")
    return dd

@app.get("/{id_categoria}/{id_departamento}/{id_produto}")
async def read_departamento_id(id_categoria, id_departamento, id_produto: str):
    """Rota para consulta de produtos

    Args:
        id_categoria (_int_): _Recebe um atributo inteiro referente ao id da categoria cadastra para consulta_
        id_departamento (_int_): _Recebe um atributo inteiro referente ao id da departamento cadastra para consulta_
        id_produto (int): _Recebe um atributo inteiro referente ao id da produto cadastra para consulta_

    Returns:
        _dict_: _Retorna um dicionario contendo os dados cadastrado do produto extraido no scraping, contendo os dados como "nome", "img"
        "valor", "avg-> Média de preço", "desconto", "descrição do produto", "dt_hora no formato timestamp", "categoria", "departamento", 
        "e valores ofertado em outros estabelecimentos"
    """
    dados_recebido = consultar(f'select produto.nome, produto.img, produto.valor, produto.avg, produto.desconto, produto.descricao, produto.dt_hora, categoria.nome as "categoria", sub_categoria.nome as "departamento" from produto inner join sub_categoria on sub_categoria.id = produto.id_sub_categoria inner join categoria on categoria.id = sub_categoria.id_categoria where produto.id = {id_produto} and sub_categoria.id = {id_departamento} and categoria.id = {id_categoria}')
    df_produto = pd.DataFrame(dados_recebido, columns=['nome', 'img', 'valor', 'avg', 'desconto', 'descricao', 'dt_hora', 'categoria', 'departamento'])
    tabela_produto = df_produto.set_index("categoria").T.to_dict("dict")
    dados_recebido = consultar(f'select outro.nome, outro.valor from outro where id_produto = {id_produto}')
    df_outro = pd.DataFrame(dados_recebido, columns=['nome', 'valor'])
    tabela_outro = df_outro.set_index("nome").to_dict("dict")
    tabela_produto.update(tabela_outro)
    return tabela_produto

