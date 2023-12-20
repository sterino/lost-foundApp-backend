from typing import List

from fastapi import Depends, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.post("/{ad_id}/media", status_code=200)
def set_ads_image(
    files: List[UploadFile],
    ad_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id

    post = svc.repository.get_ad_by_id(ad_id)

    if str(post["user_id"]) != user_id:
        raise Response(status_code=404)

    result_links = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result_links.append(url)

    svc.repository.change_post_image(ad_id, result_links)

    return 200


# @router.post("/file")
# def upload_file(
#     file: UploadFile,
#     svc: Service = Depends(get_service),
# ):
#     """
#     file.filename: str - Название файла
#     file.file: BytesIO - Содержимое файла
#     """
#     url = svc.s3_service.upload_file(file.file, file.filename)

#     return {"msg": url}


# @router.post("/files")
# def upload_files(
#     files: List[UploadFile],
#     svc: Service = Depends(get_service),
# ):
#     """
#     file.filename: str - Название файла
#     file.file: BytesIO - Содержимое файла
#     """

#     result = []
#     for file in files:
#         url = svc.s3_service.upload_file(file.file, file.filename)
#         result.append(url)

# return {"msg": files}
