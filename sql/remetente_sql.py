# Constante para criar a tabela Remetentes
CREATE_TABLE_REMENTENTES = """
CREATE TABLE IF NOT EXISTS Prisioneiros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prisioneiro TEXT NOT NULL,
    data_nascimento DATE NOT NULL,
    crime TEXT NOT NULL,
    tempo_sentenca TEXT NOT NULL,
    cela TEXT NOT NULL,
    comportamento TEXT NOT NULL
);
"""

# Constante para inserir um novo remetente
INSERT_REMETENTES = """
INSERT INTO Remetentes (prisioneiro, data_nascimento, crime, tempo_sentenca, cela, comportamento) 
VALUES (?, ?, ?, ?, ?, ?);
"""

# Constante para atualizar um remetente existente
UPDATE_REMETENTES = """
UPDATE Remetentes 
SET prisioneiro = ?, data_nascimento = ?, crime = ?, tempo_sentenca = ?, cela = ?, comportamento = ?
WHERE id = ?;
"""


# Constante para excluir um remetente pelo ID
DELETE_REMETENTES = """
DELETE FROM Remetentes 
WHERE id = ?;
"""

# Constante para obter um remetente pelo ID
GET_REMETENTES_BY_ID = """
SELECT id, prisioneiro, data_nascimento, crime, tempo_sentenca, cela, comportamento
FROM Remetentes 
WHERE id = ?;
"""

# Constante para obter remetentes por página (com paginação)
GET_REMETENTES_BY_PAGE = """
SELECT id, prisioneiro, data_nascimento, crime, tempo_sentenca, cela, comportamento
FROM Remetentes
ORDER BY nome ASC 
LIMIT ? OFFSET ?;
"""
