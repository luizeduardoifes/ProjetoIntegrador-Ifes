from dataclasses import dataclass
from datetime import date

@dataclass
class Remetente:
    id: int
    remetente: str
    data_nascimento: date
    artigo: int
    tempo_sentenca: str
    cela: str
    comportamento: str
    