from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import os
from edifact_file_parser import EDIFACTParser
from file_generator import structure
from mapper import EDIMapper

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Domínio do frontend em desenvolvimento
        "https://seu-dominio-frontend.com"  # Domínio do frontend em produção, se houver
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

@app.post("/generate_xml", response_class=Response)
async def generate_xml(file: UploadFile = File(...)):
    # Salva o arquivo temporariamente
    temp_file_path = os.path.join("output", file.filename)
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    # Parse o arquivo EDIFACT
    parsed_data = EDIFACTParser.parse_file(temp_file_path)

    # Mapeia os dados para um modelo de fatura
    mapper = EDIMapper()
    invoice_model = mapper.map_to_invoice(parsed_data)

    # Gera a estrutura do XML usando a fatura mapeada
    invoice_structure = structure(invoice_model)

    # Gera o XML
    xml_output = invoice_structure.generate_xml()

    # Retorna o XML gerado como resposta
    return Response(content=xml_output.decode('utf-8'))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
