import os

from fpdf import FPDF


from repo import registro_ponto_repo


PDF_DIR = "static/pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

def inserir_dados_ponto():
    obter_registros = registro_ponto_repo.obter_registros_ponto_por_pagina(12, 0)
    
    for registro in obter_registros:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Registro de Ponto ID: {registro.id}", ln=True)
        pdf.cell(200, 10, txt=f"Data: {registro.data}", ln=True)
        pdf.cell(200, 10, txt=f"Remetente: {registro.remetente}", ln=True)
        pdf.cell(200, 10, txt=f"Entrada: {registro.entrada}", ln=True)
        pdf.cell(200, 10, txt=f"Entrada Intervalo: {registro.entrada_intervalo}", ln=True)
        pdf.cell(200, 10, txt=f"Saída Intervalo: {registro.saida_intervalo}", ln=True)
        pdf.cell(200, 10, txt=f"Saída: {registro.saida}", ln=True)

        pdf_path = os.path.join(PDF_DIR, f"registro_{registro.id}.pdf")
        pdf.output(pdf_path)



def obter_pdf_path(id: int) -> str:
    """Obtém o caminho do PDF para um registro de ponto específico."""
    return os.path.join(PDF_DIR, f"registro_{id}.pdf")

    