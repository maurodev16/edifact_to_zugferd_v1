from datetime import datetime
from pydantic import BaseModel
   
    
class InvoiceModel(BaseModel):
    header_name: str
    type_code: str
    issue_date_time: datetime
    invoice_number: str
    currency_code: str