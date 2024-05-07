import src.controllers as controller
import src.schemas as schemas
from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.adapters.mysql_adapter import get_db
from src.utils.logger import logger
from src.services.scrapper import call_scrapper

router = InferringRouter()

@cbv(router)
class InvoiceRouter:
    # dependency injection
    db: Session = Depends(get_db)


    @router.post("/consult_invoice_information")
    def get_information(self, request: schemas.InvoiceRequest) -> Dict[str, Any]:
        """
        get information cufes
        :return:
        """
        try:
                    
            logger.info("consult invoice information process started")
            response = controller.invoice.invoice_informations(self.db, request)
            return {
                "type": "success",
                "message": "Success Operation",
                "data": response
            }
               
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=str(e))
        
    @router.post("/process_invoice_information")
    def process_information(self, request: schemas.ProcessInvoiceRequest) -> Dict[str, Any]:
        """
        register a cufe
        :return:
        """
        try:
                    
            logger.info("process invoice information process started")
            call_scrapper(request.cufe)
            return {
                "type": "success",
                "message": "Success Operation",
                "data": []
            }
               
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=str(e))