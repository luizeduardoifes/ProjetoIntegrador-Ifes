from models.registro_ponto import RegistroPonto
from sql.registro_ponto_sql import *
from data.database import obter_conexao

def criar_tabela_registro_ponto():
    """Cria a tabela de registro de ponto no banco de dados."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(CREATE_TABLE_REGISTRO_PONTO)
    conexao.commit()
    conexao.close()
    
def inserir_registro_ponto(registro: RegistroPonto) -> RegistroPonto:
    """Insere um novo registro de ponto no banco de dados."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(INSERT_REGISTRO_PONTO, 
        (registro.data, registro.remetente, registro.entrada, registro.entrada_intervalo, registro.saida_intervalo, registro.saida, registro.dias_remidos))
    registro.id = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return registro

def atualizar_registro_ponto(registro: RegistroPonto) -> bool:
    """Atualiza um registro de ponto existente no banco de dados."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(UPDATE_REGISTRO_PONTO, 
        (registro.data, registro.remetente, registro.entrada, registro.entrada_intervalo, registro.saida_intervalo, registro.saida,registro.dias_remidos, registro.id))
    conexao.commit()
    conexao.close()
    return (cursor.rowcount > 0)

def excluir_registro_ponto() -> bool:
    """Exclui todos os registros de ponto do banco de dados."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(DELETE_REGISTRO_PONTO)
    conexao.commit()
    conexao.close()
    return (cursor.rowcount > 0)

def obter_registros_ponto_por_pagina(limite:int, offset:int) -> list[RegistroPonto]:
    """Obtém registros de ponto com paginação."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(GET_REGISTRO_PONTO_BY_PAGE, (limite, offset))
    resultados = cursor.fetchall()
    conexao.close()
    
    return [RegistroPonto(
        id=resultado[0],
        data=resultado[1],
        remetente=resultado[2],
        entrada=resultado[3],
        entrada_intervalo=resultado[4],
        saida_intervalo=resultado[5],
        saida=resultado[6],
        dias_remidos=resultado[7]
    ) for resultado in resultados]
    
    
def obter_registro_ponto_por_id(id: int) -> RegistroPonto:
    """Obtém um registro de ponto pelo ID."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(GET_REGISTRO_PONTO_BY_ID, (id,))
    resultado = cursor.fetchone()
    conexao.close()
    
    if resultado:
        return RegistroPonto(
            id=resultado[0],
            data=resultado[1],
            remetente=resultado[2],
            entrada=resultado[3],
            entrada_intervalo=resultado[4],
            saida_intervalo=resultado[5],
            saida=resultado[6],
            dias_remidos=resultado[7]
        )
    return None

def obter_registros_por_remetente(remetente: str) -> list[RegistroPonto]:
    """Obtém todos os registros de ponto para um remetente específico."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(GET_REGISTRO_PONTO_BY_REMETENTE, (remetente,))
    resultados = cursor.fetchall()
    conexao.close()
    
    return [RegistroPonto(
        id=resultado[0],
        data=resultado[1],
        remetente=resultado[2],
        entrada=resultado[3],
        entrada_intervalo=resultado[4],
        saida_intervalo=resultado[5],
        saida=resultado[6],
        dias_remidos=resultado[7]
    ) for resultado in resultados] 