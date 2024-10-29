from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, FileResponse
import os
from edifact_file_parser import EDIFACTParser
from invoice_model import InvoiceModel
from invoice_xml_generator import InvoiceXMLGenerator
from invoice_pdf_generator import InvoicePDFGenerator
from mapper import EDIMapper
from drafthorse.models.document import Document
from drafthorse.models.tradelines import LineItem

app = FastAPI()

@app.post("/generate_xml", response_class=Response)
async def generate_xml(file: UploadFile = File(...)):
    xml_path = os.path.join("output", file.filename)
    with open(xml_path, "wb") as f:
        f.write(await file.read())

    # Parse do arquivo EDIFACT e mapeamento para o modelo de fatura
    parsed_data = EDIFACTParser.parse_file(xml_path)
    mapper = EDIMapper()
    invoice_model = mapper.map_to_invoice(parsed_data)

    # Gera o XML da fatura
    invoice_generator = InvoiceXMLGenerator(invoice_model)
    xml_output = invoice_generator.generate_xml()

    # Salva o XML gerado em um arquivo
    output_file_path = invoice_generator.save_xml(xml_output, invoice_model.invoice_number)
    
    # Retorna o XML gerado como resposta
    return Response(content=xml_output.decode('utf-8'), media_type="application/xml")


@app.post("/generate_zugferd_pdf", response_class=FileResponse)
async def generate_zugferd_pdf(file: UploadFile = File(...)):
    xml_path = os.path.join("output", file.filename)
    with open(xml_path, "wb") as f:
        f.write(await file.read())

    # Lê o XML e faz o parsing usando a classe Document
    with open(xml_path, "rb") as xml_file:
        samplexml = xml_file.read()
        doc = Document.parse(samplexml)

    # Agora você pode acessar os dados da fatura através do objeto `doc`
    
        # Define os detalhes do item
        li = LineItem()

    # Você pode mapear os dados da fatura para o modelo de fatura aqui
    invoice_model = InvoiceModel(
        type_code = doc.header.type_code,
        message_type =  doc.header.name,
        issue_date_time= doc.header.issue_date_time,
        invoice_number= doc.header.id,
        currency_code = doc.trade.settlement.currency_code,
        line_id=  li.document.line_id,
        payment_code = doc.trade.settlement.payment_means.type_code,
      
    )

    # Gera o PDF ZUGFeRD da fatura
    pdf_generator = InvoicePDFGenerator(invoice_model)
    pdf_path = f"output/invoice_{invoice_model.invoice_number}.pdf"

    # Metadados para o PDF
    metadata = {
        'author': 'Company Name Here',
        'keywords': 'Factur-X, Invoice',
        'title': f'Company Name: Invoice {invoice_model.invoice_number}',
        'subject': f'Fatura Factur-X Number {invoice_model.invoice_number}'
    }

    # Gera o PDF ZUGFeRD com os dados
    pdf_generator.generate_zugferd_pdf(pdf_path, samplexml, metadata=metadata, level="BASIC")

    # Retorna o PDF gerado como resposta
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"invoice_{invoice_model.invoice_number}.pdf")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
