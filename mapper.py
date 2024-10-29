from datetime import datetime
from invoice_model import InvoiceModel

class EDIMapper:
    
    def map_to_invoice(self, parsed_data) -> InvoiceModel:
        invoice_number = parsed_data.get("BGM", [None, None])[1]  # Número da fatura "IN432097"
        print("Invoice Number:", invoice_number)
        # Obter o código da fatura e o número da fatura
        invoice_type_code = parsed_data.get("BGM", [None])[0]  # Código da fatura "380"
        print("Invoice Type Code:", invoice_type_code)
        
        # Mapeamento do cabeçalho para obter "INVOIC" do campo UNB
        unh_segment = parsed_data.get("UNH", [None, []])
        message_id = unh_segment[0]  # 'ME000001'
        message_type = unh_segment[1][0]  # 'INVOIC'
        print("Header name :", message_type)
        
        # DTM
        dtm_data = parsed_data.get("DTM", [])
        
        # Inicializa as listas para as datas
        invoice_dates = []
        
        # Verifica se o DTM contém dados
        if dtm_data:
            # Extrai a primeira data obrigatória
            first_entry = dtm_data[0]  # Pegamos o primeiro elemento da lista principal
            if isinstance(first_entry, list) and len(first_entry) >= 3:
                # Extraímos a data do primeiro subarray (ex: ['137', '20020308', '102'])
                issue_date_str = first_entry[1]  # Pegando a segunda posição que contém a data
                invoice_dates.append(issue_date_str)
        
        # Extrai todas as demais datas (se existirem)
        for entry in dtm_data[1:]:  # Começa do segundo elemento
            if isinstance(entry, list) and len(entry) >= 3:
                # Cada entrada deve ser um array com pelo menos 3 elementos
                date_str = entry[1]  # Pegando a segunda posição que contém a data
                invoice_dates.append(date_str)
        
        # Converte a primeira data para o formato desejado
        if invoice_dates:
            # Converte a primeira data para objeto datetime
            issue_date_time = datetime.strptime(invoice_dates[0], "%Y%m%d").strftime("%Y-%m-%d")
            print("Invoice Date:", issue_date_time)
        else:
            print("Data de emissão não encontrada.")
        
        # Exibe todas as datas extraídas
        for date_str in invoice_dates:
            formatted_date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
            print("Other Date:", formatted_date)
        
        currency_code = parsed_data.get("CUX", [[None]])[0][1]
        print("Currency Code:", currency_code)
        
        line_id = parsed_data.get("LIN", [['', '', []]])[0][0]
        payment_code = parsed_data.get("PAI", [['', '', '']])[0][2]
        print("Payment Code:", payment_code)


        
        # Criação do objeto da fatura completa
        invoice = InvoiceModel(
            message_type=message_type,
            type_code=invoice_type_code,  # Usando o código da fatura
            issue_date_time=issue_date_time,  # A primeira data obrigatória
            invoice_number=invoice_number,
            currency_code=currency_code,
            line_id=line_id,
            payment_code=payment_code,
        )
        
        
        print("Invoice::", invoice)
        return invoice     
        # percentage_data = []
        # pcd_data = parsed_data.get("PCD", [])
        # for pct in pcd_data:
        #     percentage_data.append({"qualifier": pct[0], "percentage": pct[1]})
        # print("Percentage Data:", percentage_data)
                
        #         references = []
        # rff_data = parsed_data.get("RFF", [])
        # for ref in rff_data:
        #     reference_type = ref[0]
        #     reference_value = ref[1]
        #     references.append({"type": reference_type, "value": reference_value})
        # print("References:", references)
        
        # parties = []
        # nad_data = parsed_data.get("NAD", [])
        # for party in nad_data:
        #     party_qualifier = party[0]
        #     party_id = party[1][0] if len(party) > 1 and party[1] else None
        #     parties.append({"qualifier": party_qualifier, "id": party_id})
        # print("Parties:", parties)
                
        # payment_terms = []
        # pat_data = parsed_data.get("PAT", [])
        # for term in pat_data[2:]:  # Ignora os primeiros elementos fixos
        #     payment_terms.append({"type": term[0], "detail": term[1]})
        # print("Payment Terms:", payment_terms)
                
        # monetary_amounts = []
        # moa_data = parsed_data.get("MOA", [])
        # for amount in moa_data:
        #     amount_qualifier = amount[0]
        #     amount_value = amount[1]
        #     monetary_amounts.append({"qualifier": amount_qualifier, "value": amount_value})
        # print("Monetary Amounts:", monetary_amounts)
        
        # tax_data = []
        # tax_segments = parsed_data.get("TAX", [])
        # for tax in tax_segments:
        #     tax_type = tax[1]
        #     tax_rate = tax[4][3] if len(tax) > 4 and len(tax[4]) > 3 else None
        #     tax_data.append({"type": tax_type, "rate": tax_rate})
        # print("Tax Data:", tax_data)
                
        # line_items = []
        # lin_data = parsed_data.get("LIN", [])
        # for line in lin_data:
        #     item_id = line[2][0] if len(line) > 2 else None
        #     line_items.append({"item_id": item_id})
        # print("Line Items:", line_items)
                
        # unt_segment = parsed_data.get("UNT", [])
        # unz_segment = parsed_data.get("UNZ", [])
        # print("UNT Segment:", unt_segment)
        # print("UNZ Segment:", unz_segment)
        
        

        