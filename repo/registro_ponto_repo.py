from database import obter_conexao
from sql.registro_ponto_sql import *
from models.registro_ponto import RegistroPonto


def criar_tabela_registro_ponto():
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(CREATE_TABLE_REGISTRO_PONTO)
        conexao.commit()

def inserir_registro_ponto(registro: RegistroPonto):
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_REGISTRO_PONTO, (
            registro.remetente,
            registro.data,
            registro.entrada,
            registro.saida,
            registro.horas_trabalhadas
        ))
        conexao.commit()

def atualizar_registro_ponto(registro: RegistroPonto):
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_REGISTRO_PONTO, (
            registro.remetente,
            registro.data,
            registro.entrada,
            registro.saida,
            registro.horas_trabalhadas,
            registro.id
        ))
        conexao.commit()

def excluir_registro_ponto(id: int):
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_REGISTRO_PONTO, (id,))
        conexao.commit()

def obter_registro_ponto_por_id(id: int) -> RegistroPonto:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_REGISTRO_PONTO_BY_ID, (id,))
        row = cursor.fetchone()
        if row:
            return RegistroPonto(
                id=row[0],
                remetente=row[1],
                data=row[2],
                entrada=row[3],
                saida=row[4],
                horas_trabalhadas=row[5]
            )
        return None
    
def obter_registro_ponto_por_pagina(pagina: int, limite: int) -> list[RegistroPonto]:
    offset = (pagina - 1) * limite
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_REGISTRO_PONTO_BY_PAGE, (limite, offset))
        rows = cursor.fetchall()
        registros = []
        for row in rows:
            registros.append(RegistroPonto(
                id=row[0],
                remetente=row[1],
                data=row[2],
                entrada=row[3],
                saida=row[4],
                horas_trabalhadas=row[5]
            ))
        return registros