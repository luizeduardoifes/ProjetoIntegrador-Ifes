from database import obter_conexao
from encarregado_sql import *
from encarregado import Encarregado


def criar_tabela():
    """Cria a tabela Remententes se ela não existir."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(CREATE_TABLE_ENCARREGADO)
    conexao.commit()
    conexao.close()