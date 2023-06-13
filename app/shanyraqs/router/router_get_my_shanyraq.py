from typing import Any, List

from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetMyShanyraqRequest(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: str
    address: str
    area: str
    rooms_count: str
    description: str


class GetMyShanyraqResponse(AppModel):
    shanyraqs: List[GetMyShanyraqRequest]


@router.get("/", response_model=GetMyShanyraqResponse)
def get_my_shanyraq(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    shanyraqs = svc.repository.get_shanyraq_by_user_id(user_id)

    resp = {"shanyraqs": shanyraqs}

    return resp
