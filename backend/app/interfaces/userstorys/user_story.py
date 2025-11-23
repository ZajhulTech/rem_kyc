from abc import ABC, abstractmethod
from app.models.request.user_request import UserCreateRequest
from app.models.response.user_response import UserResponse
from app.infra.api.response import Response

class IUserStory(ABC):
    @abstractmethod
    async def get_user(self) -> Response[UserResponse]:
        pass
    @abstractmethod
    async def create_user(self, user: UserCreateRequest) -> UserResponse:
        pass
