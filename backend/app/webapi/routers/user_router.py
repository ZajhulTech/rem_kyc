from fastapi import APIRouter, Depends
from app.models.request.user_request import UserCreateRequest
from app.models.response.user_response import UserResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.userstorys.user_story import UserStory
#from app.infra.database.mongo_repository import MongoRepository
from app.infra.api.response_utils import get_response, get_custom_response
from app.infra.api.response import Response
from app.interfaces.userstorys.user_story import IUserStory

import os

router = APIRouter()
base = "/users"
Tag = "Users"

def get_user_story() -> IUserStory:
    return UserStory(None)

##def get_user_repo():
##    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
##    return MongoUserRepository(client)

@router.get("/users", response_model=Response[UserResponse], tags=[Tag])
async def get_user(user_story: IUserStory = Depends(get_user_story)):
    
    return await user_story.get_user()
 
@router.post(base, response_model=UserResponse, tags=[Tag])
async def create_user(user: UserCreateRequest):
    pass
   # use_case = CreateUser(repo)
   # return await use_case.execute(user)
