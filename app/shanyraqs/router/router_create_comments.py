from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class content(AppModel):
    comment: str


@router.post("/{id}/comments")
def create_comments(
    id: str,
    input: content,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    if user_id is None:
        return Response(status_code=404)

    result = svc.repository.create_shanyraq_comment(user_id, id, input.comment)
    if result is None:
        return Response(status_code=403)
    return Response(status_code=200)
