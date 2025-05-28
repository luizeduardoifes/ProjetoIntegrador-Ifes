
from dataclasses import dataclass
from datetime import date, time

from sqlalchemy import ForeignKey

from models.remetente import Remetente


@dataclass
class RegistroPonto(Remetente):
    id: int
    remetente: Remetente = ForeignKey('Remetente.id', ondelete='CASCADE')
    data: date
    entrada: time
    entrada_intervalo: time
    saida_intervalo: time
    saida: time
    horas_trabalhadas: float
    