from fastapi import Depends, Response, status

from app.utils import BaseModel

from ..service import Service, get_service
from . import router


class PatchShanyraqsResponseById(BaseModel):
    type: str
    price: str
    address: str
    area: str
    rooms_count: str
    description: str


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PatchShanyraqsResponseById,
)
def update_shanyraq_by_user_id(
    id: str,
    input: PatchShanyraqsResponseById,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.update_shanyraq_by_id(id, input.dict())
    return Response(status_code=200)
