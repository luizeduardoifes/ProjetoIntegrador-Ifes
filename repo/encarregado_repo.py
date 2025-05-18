from data.database import obter_conexao
from sql.encarregado_sql import *
from models.encarregado import Encarregado


def criar_tabela_encarregado():
    """Cria a tabela Remententes se ela não existir."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(CREATE_TABLE_ENCARREGADO)
    conexao.commit()
    conexao.close()