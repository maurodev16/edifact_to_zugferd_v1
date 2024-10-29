from datetime import datetime
from pydantic import BaseModel
   
    
class InvoiceModel(BaseModel):
    message_type: str
    type_code: str
    issue_date_time: datetime
    # seller_order_issue_date_time:  datetime
    # buyer_order_issue_date_time: datetime
    # customer_order_issue_date_time: datetime
    # advance_payment_received_date: datetime
    invoice_number: str
    currency_code: str
    line_id: str
    payment_code:str