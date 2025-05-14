from dataclasses import dataclass

@dataclass
class Remetente:
    id: int
    prisioneiro: str
    idade: int
    crime: str
    tempo_sentenca: int
    cela: str
    comportamento: str