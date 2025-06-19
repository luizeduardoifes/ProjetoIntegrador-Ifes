from dataclasses import dataclass
from datetime import date, time


@dataclass
class RegistroPonto:
    id: int
    data: date
    remetente: str
    entrada: time
    entrada_intervalo: time
    saida_intervalo: time
    saida: time
    dias_remidos: float 
