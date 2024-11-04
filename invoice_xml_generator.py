import os
from datetime import datetime, timezone
from decimal import Decimal
from drafthorse.utils import validate_xml
from drafthorse.models.accounting import ApplicableTradeTax
from drafthorse.models.document import Document
from drafthorse.models.note import IncludedNote
from drafthorse.models.tradelines import LineItem
from invoice_model import InvoiceModel

class InvoiceXMLGenerator:
    def __init__(self, invoice: InvoiceModel):
        self.invoice = invoice

    def generate_xml(self):   
        doc = Document()
        note = IncludedNote()

        # Define os parâmetros do documento
        doc.context.guideline_parameter.id = "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
        doc.header.id = self.invoice.invoice_number
        doc.header.type_code = self.invoice.type_code
        doc.header.name = self.invoice.message_type
        doc.header.issue_date_time = self.invoice.issue_date_time
        doc.header.languages.add("de")

        note.content.add("Test Note 1")
        doc.header.notes.add(note)

        # Define os dados do fornecedor e cliente
        doc.trade.agreement.seller.name = "Lieferant GmbH"
        doc.trade.settlement.payee.name = "Kunde GmbH"
        doc.trade.agreement.buyer.name = "Kunde GmbH"
        doc.trade.settlement.invoicee.name = "Kunde GmbH"
        doc.trade.settlement.currency_code = self.invoice.currency_code
        doc.trade.settlement.payment_means.type_code = self.invoice.payment_code

        # Configura o endereço e informações adicionais
        doc.trade.agreement.seller.address.country_id = "DE"
        doc.trade.agreement.seller.address.country_subdivision = "Bayern"
        doc.trade.agreement.seller_order.issue_date_time = datetime.now(timezone.utc)
        doc.trade.agreement.buyer_order.issue_date_time = datetime.now(timezone.utc)
        doc.trade.settlement.advance_payment.received_date = datetime.now(timezone.utc)
        doc.trade.agreement.customer_order.issue_date_time = datetime.now(timezone.utc)

        # Define os detalhes do item
        li = LineItem()
        li.document.line_id = self.invoice.line_id
        li.product.name = "Rainbow"
        li.agreement.gross.amount = Decimal("999.00")
        li.agreement.gross.basis_quantity = (Decimal("1.0000"), "C62")  # C62 == unidades
        li.agreement.net.amount = Decimal("999.00")
        li.agreement.net.basis_quantity = (Decimal("999.00"), "EUR")
        li.delivery.billed_quantity = (Decimal("1.0000"), "C62")
        li.settlement.trade_tax.type_code = "VAT"
        li.settlement.trade_tax.category_code = "E"
        li.settlement.trade_tax.rate_applicable_percent = Decimal("0.00")
        li.settlement.monetary_summation.total_amount = Decimal("999.00")
        doc.trade.items.add(li)

        # Define o imposto comercial aplicável
        trade_tax = ApplicableTradeTax()
        trade_tax.calculated_amount = Decimal("0.00")
        trade_tax.basis_amount = Decimal("999.00")
        trade_tax.type_code = "VAT"
        trade_tax.category_code = "AE"
        trade_tax.exemption_reason_code = 'VATEX-EU-AE'
        trade_tax.rate_applicable_percent = Decimal("0.00")
        doc.trade.settlement.trade_tax.add(trade_tax)

        # Define o total monetário
        doc.trade.settlement.monetary_summation.line_total = Decimal("999.00")
        doc.trade.settlement.monetary_summation.charge_total = Decimal("0.00")
        doc.trade.settlement.monetary_summation.allowance_total = Decimal("0.00")
        doc.trade.settlement.monetary_summation.tax_basis_total = Decimal("999.00")
        doc.trade.settlement.monetary_summation.tax_total = Decimal("0.00")
        doc.trade.settlement.monetary_summation.grand_total = Decimal("999.00")
        doc.trade.settlement.monetary_summation.due_amount = Decimal("999.00")

        # Generate and Validate XML X-Rechnung
        xml = doc.serialize(schema="FACTUR-X_EXTENDED")
        validate_xml(xml, schema="FACTUR-X_EXTENDED")

        return xml

    def save_xml(self, xml: bytes, invoice_number: str):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, f"X-Rechnung-{invoice_number}.xml")

        with open(output_file_path, "wb") as file:
            file.write(xml)

        print(f"XML Savad in: {output_file_path}")
        return output_file_path
