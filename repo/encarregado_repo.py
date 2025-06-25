from data.database import obter_conexao
from sql.encarregado_sql import *


def criar_tabela_encarregado():
    """Cria a tabela Encarregado se ela não existir."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(CREATE_TABLE_ENCARREGADO)
    conexao.commit()
    conexao.close()