from typing import Tuple
import psycopg2

caminho_db = 'postgresql://postgres:123159@localhost/eiprice'

""" sql_criar_banco
-- Database: eiprice
-- DROP DATABASE IF EXISTS eiprice;

CREATE DATABASE eiprice
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;"
    
"""



def conectar():
  conexao_pg = psycopg2.connect(host='localhost', user='postgres', password='123159', database='eiprice', port=5432)  
  return conexao_pg


def aplicar_banco(sql: str) -> None:
  try:
    conexao_pg = conectar()
    cursor = conexao_pg.cursor()
    cursor.execute(sql)
    conexao_pg.commit()
  except (Exception, psycopg2.DatabaseError) as e:
    # print("Error: %s" % e)
    conexao_pg.rollback()
    cursor.close()
    return 1
  conexao_pg.close()


def consultar(sql: str) -> Tuple:
  try:
    conexao_pg = conectar()
    cursor = conexao_pg.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    return row
  except (Exception, psycopg2.DatabaseError) as e:
    print("Error: %s" % e)
    conexao_pg.rollback()
    cursor.close()
    return None
  finally:
    conexao_pg.close()
  
  
    