from typing import List

from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class DeleteShanyrakMediaRequest(AppModel):
    media: List[str]


@router.delete("/{id}/media", status_code=200)
def delete_media_shanyraq(
    id: str,
    input: DeleteShanyrakMediaRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyraq = svc.repository.get_shanyraq_id(id)

    if shanyraq is None:
        return Response(status_code=404)

    user_id = jwt_data.user_id

    if user_id != str(shanyraq["user_id"]):
        return Response(status_code=401)
    for image in input.media:
        svc.s3_service.delete_file(id, image)
        svc.repository.delete_shanyraq_media(id, image)

    return Response(status_code=200)
