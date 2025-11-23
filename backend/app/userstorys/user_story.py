from app.interfaces.userstorys.user_story import IUserStory
from app.models.request.user_request import UserCreateRequest
from app.models.response.user_response import UserResponse
from app.infra.api.response import Response
from uuid import uuid4
#from app.infra.database.mongo_repository import MongoRepository
from app.interfaces.database.base_repository import IBaseRepository
from typing import Optional

class UserStory(IUserStory):
    def __init__(self, repo: IBaseRepository):
       pass
       #self.repo = repo
       # self.customer_repo = MongoRepository(self.repo.collection, CustomerModel)
    
    async def get_user(self, user_id: Optional[str] = None) -> Response[UserResponse]:
        #print("llegue a get_user")
        # customer = await self.customer_repo.find_one({"_id": user_id}) if user_id else None
       
        data = UserResponse(
            id=uuid4(),
            name="Juan Pérez",
            email="juan@example.com"
        )
        result = Response.with_data(data)
        return result

    async def create_user(self, user_data: UserCreateRequest) -> UserResponse:
        pass
        #return await self.user_repository.create_user(user_data)