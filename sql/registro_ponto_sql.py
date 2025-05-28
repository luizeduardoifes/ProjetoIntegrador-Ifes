CREATE_TABLE_REGISTRO_PONTO = """
CREATE TABLE IF NOT EXISTS RegistroPonto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remetente TEXT NOT NULL,
    data DATE NOT NULL,
    entrada TIME NOT NULL,
    entrada_intervalo TIME NOT NULL,
    saida_intervalo TIME NOT NULL,
    saida TIME NOT NULL,
    horas_trabalhadas REAL NOT NULL
);
"""

