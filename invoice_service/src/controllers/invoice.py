from typing import List
from sqlalchemy.orm import Session
from src.controllers.base import BaseController
import src.models as models
import src.schemas as schemas
from src.utils import Singleton

"""
This class is a CRUD class for the invoice table.
"""

class InvoiceCRUD(
    
    BaseController[schemas.Invoice, schemas.InvoiceCreate, schemas.InvoiceUpdate],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models.Invoice)   
   

    def invoice_informations(self, db: Session, request: List[str]):
        """
        Get invoice information, and all its associated information such as events, senders and recipients..
        :param db: Database session
        :param cufes: List of the cufe
        :return: Dict related invoice information
        """
        response = {}

        # Consultar la base de datos para obtener información de las facturas
        invoices = db.query(self.model_cls).filter(self.model_cls.number_invoice.in_(request.cufes)).all()

        events_by_invoice = {}
        for invoice in invoices:
            # Consultar los eventos asociados a la factura actual
            events = db.query(models.Event).filter(models.Event.invoice_id == invoice.id).all()
            events_by_invoice[invoice.id] = events
        
        for invoice in invoices:
           
            invoice_info = {
                "date_issued": invoice.date_issued,
                "series": invoice.series,
                "folio": invoice.folio,
                "total": invoice.total,
                "iva": invoice.tax,
                "linkGraphicRepresentation": invoice.pdf_url,
                "sellerInformation": {
                    "document_number": invoice.emitter.document_number,
                    "name": invoice.emitter.name
                },
                "receiverInformation":{
                    "document_number": invoice.receiver.document_number,
                    "name": invoice.receiver.name
                }
            }

            # Obtener los eventos asociados a esta factura
            events = events_by_invoice.get(invoice.id, [])
            
            # Construir la lista de eventos para esta factura
            events_info = []
            for event in events:
                event_info = {
                    "code": event.code,
                    "description": event.description,
                    "date_event": event.date_event
                }
                events_info.append(event_info)

            # Agregar los eventos a la información de la factura
            invoice_info["events"] = events_info

            response[invoice.number_invoice] = invoice_info

        return response
                          
# Create a singleton instance of the NpsCRUD class
invoice = InvoiceCRUD()