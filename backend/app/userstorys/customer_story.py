from fastapi import HTTPException

from app.models.response.card_response import CardResponse
from app.models.response.customer_response import CustomerResponse
from app.infra.api.response import Response
from app.interfaces.database.unit_of_work import IUnitOfWork
from app.interfaces.userstorys.customer_story import ICustomerStory
from typing import List, Optional

from app.infra.mongodb.mongo_base_repository import MongoBaseRepository
from app.models.atlasdb.customer_model import CustomerModel

class CustomerStory(ICustomerStory):
   def __init__(self, unit_of_work: IUnitOfWork):
      self._uow = unit_of_work
    
   async def get_customer(self, phone: Optional[str] = None) -> Response[List[CustomerResponse]]:
      
      customerRepo: MongoBaseRepository[CustomerModel] = self._uow.get_repository(CustomerModel)
      customers = await customerRepo.find_all()

      try:

         customer_response_list = [CustomerStory.to_customer_response(c) for c in customers]

      except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error al mapear datos: {str(e)}")

      return Response.with_data(customer_response_list)


   # HELPERS
   @staticmethod
   def to_customer_response(customer: CustomerModel) -> CustomerResponse:
      return CustomerResponse(
         id=str(getattr(customer, "id", customer.id)),  # Asegura compatibilidad
         whatsapp_number=customer.whatsapp_number,
         email=customer.email,
         name=customer.name,
         last_name=customer.last_name,
         birthdate=customer.birthdate,
         gender=customer.gender,
         status=customer.status,
         brand=customer.brand,
         card=[
            CardResponse(
                  card_number=card.card_number,
                  level=card.level,
                  points=card.points,
                  expiration_date=card.expiration_date,
                  is_enabled=card.is_enabled
            )
            for card in customer.card or []
         ],
         created=customer.created
      )