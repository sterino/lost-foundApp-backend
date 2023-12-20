from fastapi import Depends

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class createPostRequest(AppModel):
    type: int
    title: str
    description: str
    category: str


class createPostResponse(AppModel):
    new_post_id: str


@router.post("/", status_code=200)
def create_post(
    input: createPostRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id

    id_post = svc.repository.create_ad(user_id, input.dict())

    return createPostResponse(new_post_id=str(id_post))