from typing import List

from fastapi import Depends, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.post("/{id}/file")
def add_Image(
    sh_id: str,
    file: UploadFile,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    sh = svc.repository.get_shanyraq_id(sh_id)
    if sh is None:
        return Response(status_code=404)
    user_id = jwt_data.user_id
    if user_id != str(sh["user_id"]):
        return Response(status_code=401)

    url = svc.s3_service.upload_file(file.file, sh_id, file.filename)
    svc.repository.add_shanyraq_media(sh_id, url)
    return {"msg": url}


@router.post("/files")
def upload_files(
    sh_id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    sh = svc.repository.get_shanyraq_id(sh_id)
    if sh is None:
        return Response(status_code=404)
    user_id = jwt_data.user_id
    if user_id != str(sh("user_id ")):
        return Response(status_code=404)

    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, sh_id, file.filename)
        svc.repository.add_shanyraq_media(sh_id, url)
        result.append(url)
    return {"msg": url}
