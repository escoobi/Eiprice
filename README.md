Python >= 3.9
Postgres >= 11

Libs utilizadas:
Selenium
Pandas
FastApi
psycopg2


Observação: 
1 - Cadastrar no https://shopper.com.br e adicionar o email e senha em main.py na chamada de função "extrair_dados"
2 - Criar um banco de dados no postgres com o nome "eiprice" e passar o usuário e senha de acesso ao banco na variavel caminho_db no arquivo eiprice_db.py
3 - Apos o scraping iniciar o serviço da API com o comando: uvicorn main:app --reload
