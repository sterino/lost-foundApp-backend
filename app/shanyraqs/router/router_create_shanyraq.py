from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateShanyrakRequest(AppModel):
    type: str
    price: str
    address: str
    area: str
    rooms_count: str
    description: str


@router.post("/")
def create_shanyraq(
    input: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    svc.repository.create_shanyraq(
        {
            "user_id": user_id,
            "type": input.type,
            "price": input.price,
            "address": input.address,
            "area": input.area,
            "rooms_count": input.rooms_count,
            "description": input.description,
        }
    )

    return Response(status_code=200)
