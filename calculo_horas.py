from datetime import datetime


def calcular_dias_remidos(entrada, entrada_intervalo, saida_intervalo, saida, jornada_padrao=8):
        formato = "%H:%M"
        entrada = datetime.strptime(entrada, formato)
        entrada_intervalo = datetime.strptime(entrada_intervalo, formato)
        saida_intervalo = datetime.strptime(saida_intervalo, formato)
        saida = datetime.strptime(saida, formato)

        periodo1 = entrada_intervalo - entrada
        periodo2 = saida - saida_intervalo

        total_trabalhado = periodo1 + periodo2
        total_horas = total_trabalhado.total_seconds() / 3600

        dias_remidos = total_horas / jornada_padrao
        return round(dias_remidos, 2)