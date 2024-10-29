from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from invoice_model import InvoiceModel
from drafthorse.pdf import attach_xml

class InvoicePDFGenerator:
    def __init__(self, invoice: InvoiceModel):
        self.invoice = invoice
        
    def format_date(self, date):
        """Formata a data para uma string padrão."""
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y%m%d')
        return date.strftime('%Y-%m-%d')
    
    def generate_pdf(self, pdf_path):
        """Cria o arquivo PDF básico com as informações da fatura."""
        pdf_canvas = canvas.Canvas(pdf_path, pagesize=A4)
        pdf_canvas.drawString(100, 750, f"Invoice Number: {self.invoice.invoice_number}")
        pdf_canvas.drawString(100, 735, f"Invoice Date: {self.format_date(self.invoice.issue_date_time)}")
        pdf_canvas.save()
    
    def generate_zugferd_pdf(self, pdf_path, xml_data, metadata=None, level="BASIC", lang="de-DE"):
     try:
         self.generate_pdf(pdf_path)
 
         with open(pdf_path, "rb") as pdf_file:
             original_pdf = pdf_file.read()
         
         zugferd_pdf = attach_xml(
             original_pdf=original_pdf,
             xml_data=xml_data,
             level=level,
             metadata=metadata,
             lang=lang
         )
 
         with open(pdf_path, "wb") as pdf_file:
             pdf_file.write(zugferd_pdf)
         print(f"PDF ZUGFeRD gerado em: {pdf_path}")
 
     except Exception as e:
         print(f"Erro ao gerar o PDF ZUGFeRD: {str(e)}")

