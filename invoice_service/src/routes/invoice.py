from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from src.adapters.mysql_adapter import get_db
from src.utils.logger import logger
import src.controllers as controller
import src.schemas as schemas

router = InferringRouter()

@cbv(router)
class InvoiceRouter:
    # dependency injection
    db: Session = Depends(get_db)


    @router.post("/consult_invoice_information")
    def get_information(self, request: schemas.InvoiceRequest) -> Dict[str, Any]:
        """
        register a nps
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