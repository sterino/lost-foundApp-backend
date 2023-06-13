from fastapi import Depends
from pydantic import BaseModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class ChangeUserDataRequest(BaseModel):
    phone: str = ""
    name: str = ""
    city: str = ""


@router.patch("/users/me", response_model=ChangeUserDataRequest)
def update_my_account(
    input: ChangeUserDataRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    print(jwt_data.user_id)
    svc.repository.update_user(jwt_data.user_id, input.dict())
    return input
