CREATE_TABLE_REGISTRO_PONTO = """
CREATE TABLE IF NOT EXISTS registro_ponto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    remetente TEXT NOT NULL,
    entrada TIME NOT NULL,
    entrada_intervalo TIME NOT NULL,
    saida_intervalo TIME NOT NULL,
    saida TIME NOT NULL,
    dias_remidos REAL NOT NULL
);
"""

INSERT_REGISTRO_PONTO = """
INSERT INTO registro_ponto (data, remetente, entrada, entrada_intervalo, saida_intervalo, saida, dias_remidos)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

UPDATE_REGISTRO_PONTO = """
UPDATE registro_ponto
SET data = ? remetente = ? entrada = ?, entrada_intervalo = ?, saida_intervalo = ?, saida = ?, dias_remidos = ?
WHERE id = ?;
"""

DELETE_REGISTRO_PONTO = """
DELETE FROM registro_ponto
WHERE id = ?;
"""

GET_REGISTRO_PONTO_BY_ID = """
SELECT id, data, remetente, entrada, entrada_intervalo, saida_intervalo, saida, dias_remidos
FROM registro_ponto
WHERE id = ?;
"""

GET_REGISTRO_PONTO_BY_PAGE = """
SELECT id, data, remetente, entrada, entrada_intervalo, saida_intervalo, saida, dias_remidos
FROM registro_ponto
ORDER BY data DESC
LIMIT ? OFFSET ?;
"""

GET_REGISTRO_PONTO_BY_REMETENTE = """
SELECT id, data, remetente, entrada, entrada_intervalo, saida_intervalo, saida, dias_remidos
FROM registro_ponto
WHERE remetente = ?
ORDER BY data DESC
LIMIT ? OFFSET ?;
"""