from datetime import datetime, timedelta
from main import entrada, entrada_intervalo, saida_intervalo, saida

def calcular_dias_remidos(entrada, entrada_intervalo, saida_intervalo, saida, jornada_padrao=8):
    # Converte strings de horário para objetos datetime
    formato = "%H:%M"
    entrada = datetime.strptime(entrada, formato)
    entrada_intervalo = datetime.strptime(entrada_intervalo, formato)
    saida_intervalo = datetime.strptime(saida_intervalo, formato)
    saida = datetime.strptime(saida, formato)

    # Calcula o tempo trabalhado antes e depois do intervalo
    periodo1 = entrada_intervalo - entrada
    periodo2 = saida - saida_intervalo

    # Soma os dois períodos
    total_trabalhado = periodo1 + periodo2

    # Total de horas e minutos
    total_horas = total_trabalhado.total_seconds() / 3600  # converte para horas

    # Calcula dias remidos
    dias_remidos = total_horas / jornada_padrao

    return round(dias_remidos, 2)  # Arredonda para 2 casas decimais

# Exemplo de uso
entrada = entrada
entrada_intervalo = entrada_intervalo
saida_intervalo = saida_intervalo
saida = saida

dias = calcular_dias_remidos(entrada, entrada_intervalo, saida_intervalo, saida)
print("Dias remidos:", dias)
