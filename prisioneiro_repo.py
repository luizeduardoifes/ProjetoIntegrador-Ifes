from database import obter_conexao
from sql import *
from prisioneiro import Remetente

def criar_tabela():
    """Cria a tabela Remententes se ela não existir."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(CREATE_TABLE_REMENTENTES)
    conexao.commit()
    conexao.close()

def inserir_produto(remetente: Remetente) -> Remetente:
    """Insere um novo rementente no banco de dados."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(INSERT_REMETENTES, 
        (remetente.prisioneiro, remetente.idade, remetente.crime, remetente.tempo_sentenca, remetente.cela, remetente.comportamento))
    remetente.id = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return remetente

def atualizar_produto(rementente: Remetente) -> bool:
    """Atualiza um remetente existente no banco de dados."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(UPDATE_REMETENTES, 
        ())
    conexao.commit()
    conexao.close()
    return (cursor.rowcount > 0)

def excluir_produto(id: int) -> bool:
    """Exclui um rementente do banco de dados pelo ID."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(DELETE_REMETENTES, (id,))
    conexao.commit()
    conexao.close()
    return (cursor.rowcount > 0)

def obter_produto_por_id(id: int) -> Remetente:
    """Obtém um rementente pelo ID."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(GET_REMETENTES_BY_ID, (id,))
    resultado = cursor.fetchone()
    conexao.close()
    if resultado:
        return Remetente(
            id=resultado[0],
            prisioneiro=resultado[1],
            idade=resultado[2],
            crime=resultado[3],
            tempo_sentenca=resultado[4],
            cela=resultado[5],
            comportamento=resultado[6]
            
        )
    return None

def obter_produtos_por_pagina(limite: int, offset: int) -> list[Remetente]:
    """Obtém uma lista de remetentes com paginação."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(GET_REMETENTES_BY_ID, (limite, offset))
    resultados = cursor.fetchall()
    conexao.close()
    return [Remetente(
        id=resultado[0],
        prisioneiro=resultado[1],   
        idade=resultado[2],
        crime=resultado[3],
        tempo_sentenca=resultado[4],
        cela=resultado[5],
        comportamento=resultado[6]
    ) for resultado in resultados]