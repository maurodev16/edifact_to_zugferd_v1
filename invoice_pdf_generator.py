from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from invoice_model import InvoiceModel
from drafthorse.models.document import Document
from drafthorse.models.tradelines import LineItem
from drafthorse.pdf import attach_xml

class InvoicePDFGenerator:
    def __init__(self):
        self.invoice = None
        
    def format_date(self, date):
        """Formata a data para uma string padrão."""
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y%m%d')
        return date.strftime('%Y-%m-%d')
    
    def map_invoice_data(self, samplexml):
        """Mapeia os dados da fatura para o modelo de fatura."""
        doc = Document.parse(samplexml)
        li = LineItem()
        self.invoice = InvoiceModel(
            type_code= str(doc.header.type_code),
            message_type= str(doc.header.name),
            issue_date_time= str(doc.header.issue_date_time),
            invoice_number= str(doc.header.id),
            currency_code= str(doc.trade.settlement.currency_code),
            line_id= str(li.document.line_id),
            payment_code= str(doc.trade.settlement.payment_means.type_code),
        )
    
    def generate_pdf(self, pdf_path):
        """Cria o arquivo PDF básico com as informações da fatura."""
        pdf_canvas = canvas.Canvas(pdf_path, pagesize=A4)
        pdf_canvas.drawString(100, 760, f"Invoice Number: {self.invoice.invoice_number}")
        pdf_canvas.drawString(100, 755, f"Invoice Date: {self.format_date(self.invoice.issue_date_time)}")
        pdf_canvas.drawString(100, 745, f"Type Code: {self.invoice.type_code}")
        pdf_canvas.drawString(100, 735, f"Currency Code: {self.invoice.currency_code}")
        pdf_canvas.drawString(100, 725, f"Line ID: {self.invoice.line_id}")
        pdf_canvas.save()
    
    def generate_zugferd_pdf(self, pdf_path, xml_data, metadata=None, level="BASIC", lang="de-DE"):
        try:
            self.map_invoice_data(xml_data)
            
            # Define os metadados para o PDF
            metadata = metadata or {
                'author': 'Company Name Here',
                'keywords': 'Factur-X, Invoice',
                'title': f'Company Name: Invoice {self.invoice.invoice_number}',
                'subject': f'Fatura Factur-X Number {self.invoice.invoice_number}'
            }

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
