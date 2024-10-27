from datetime import datetime
from invoice_model import InvoiceModel

class EDIMapper:
    
    def map_to_invoice(self, parsed_data) -> InvoiceModel:
        # Obter o código da fatura e o número da fatura
        invoice_type_code = parsed_data.get("BGM", [None])[0]  # Código da fatura "380"
        print("Invoice Type Code:", invoice_type_code)
        
        invoice_number = parsed_data.get("BGM", [None, None])[1]  # Número da fatura "IN432097"
        print("Invoice Number:", invoice_number)
        
        
        # Obter a data da fatura e a moeda
        invoice_date = parsed_data.get("DTM", [[None]])[0][1]
        print("Invoice Date:", invoice_date)
        
        currency_code = parsed_data.get("CUX", [[None]])[0][1]
        print("currency_code :", currency_code)
        

        # Mapeamento do cabeçalho para obter "INVOIC" do campo UNB
        header_name = parsed_data.get("UNB", [])[6]  # Pegando "INVOIC" na posição correta
        print("Header name :", header_name)
        
        # Criação do objeto da fatura completa
        invoice = InvoiceModel(
            header_name=header_name,
            type_code=invoice_type_code,  # Usando o código da fatura
            issue_date_time=invoice_date,
            invoice_number=invoice_number,
            currency_code=currency_code,
        )
        print("Invoice::", invoice)
        return invoice
