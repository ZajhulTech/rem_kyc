from typing import List
from fastapi import APIRouter, Depends
from app.models.response.customer_response import CustomerResponse
from app.userstorys.customer_story import CustomerStory
from app.interfaces.userstorys.customer_story import ICustomerStory
from app.infra.api.response_utils import get_response, get_custom_response
from app.infra.api.response import Response
from app.webapi.dependencies.mongo_dependencies import get_mongo_unit_of_work

router = APIRouter()
base = "/customer"
Tag = "Customers"

def get_user_story(uow = Depends(get_mongo_unit_of_work)) -> ICustomerStory:
    return CustomerStory(uow) # pyright: ignore[reportArgumentType]

##def get_user_repo():
##    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
##    return MongoUserRepository(client)

@router.get(base, response_model=Response[List[CustomerResponse]], tags=[Tag])
async def get_customer(user_story: ICustomerStory = Depends(get_user_story)):
    
    return await user_story.get_customer()