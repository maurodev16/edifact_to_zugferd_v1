import json
import os
from typing import Any, Dict
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response, FileResponse
from edifact_file_parser import EDIFACTParser
from invoice_model import InvoiceModel
from invoice_xml_generator import InvoiceXMLGenerator
from invoice_pdf_generator import InvoicePDFGenerator
from mapper import EDIMapper

app = FastAPI()

@app.post("/parse-edifact", response_model=dict)
async def parse_edifact(file: UploadFile = File(...)) -> Dict[str, Any]:
    edifact_path = os.path.join("output", file.filename)
    
    try:
        # Salva o arquivo EDIFACT temporariamente
        with open(edifact_path, "wb") as f:
            f.write(await file.read())

        # Usa o parser para extrair os dados
        parsed_data = EDIFACTParser.parse_file(edifact_path)
        
        # Converte parsed_data para JSON string antes de retornar
        json_data = json.loads(json.dumps(parsed_data))  # json.loads converte de volta para um objeto dict
        print(f"Parsed EDIFACT data: {json_data}")
        
        return json_data 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao parsear arquivo EDIFACT: {e}")

    finally:
        # Remove o arquivo temporário
        if os.path.exists(edifact_path):
            os.remove(edifact_path)
            
@app.post("/convert_from_edifact_invoice_file_to_x-invoice_xml", response_class=Response)
async def generate_xml(file: UploadFile = File(...)):
    xml_path = os.path.join("output", file.filename)
    with open(xml_path, "wb") as f:
        f.write(await file.read())

    # Parse do arquivo EDIFACT e mapeamento para o modelo de fatura
    parsed_data = EDIFACTParser.parse_file(xml_path)
    print(f"Parsed file: {parsed_data}")
    mapper = EDIMapper()
    invoice_model = mapper.map_to_invoice(parsed_data)

    # Gera o X-Invoice XML da fatura
    invoice_generator = InvoiceXMLGenerator(invoice_model)
    xml_output = invoice_generator.generate_xml()

    # Salva o X-Invoice XML gerado em um arquivo
    output_file_path = invoice_generator.save_xml(xml_output, invoice_model.invoice_number)
    
    # Retorna o XML gerado como resposta
    return Response(content=xml_output.decode('utf-8'), media_type="application/xml")


@app.post("/generate_zugferd_pdf_from_x-invoice-xml", response_class=FileResponse)
async def generate_zugferd_pdf(file: UploadFile = File(...)):
    xml_path = os.path.join("output", file.filename)
    with open(xml_path, "wb") as f:
        f.write(await file.read())

    # Lê o XML
    with open(xml_path, "rb") as xml_file:
        xml_data = xml_file.read()
        print(xml_data)

    # Gera o PDF ZUGFeRD da fatura
    pdf_generator = InvoicePDFGenerator()
    pdf_path = f"output/invoice.pdf"

    # Gera o PDF ZUGFeRD com os dados
    pdf_generator.generate_zugferd_pdf(pdf_path, xml_data, level="BASIC")
    response = FileResponse(pdf_path, media_type="application/pdf", filename="invoice.pdf")
        
    # Retorna o PDF gerado como resposta
    return response



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
