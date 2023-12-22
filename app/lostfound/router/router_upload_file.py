from fastapi import Depends, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
import os


@router.post("/{post_id}/media/", status_code=200)
def set_ads_image(
    file: UploadFile,
    ad_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    if file.filename is None:
        file.filename = os.path.basename(file)
        
    user_id = jwt_data.user_id

    post = svc.repository.get_ad_by_id(ad_id)

    if str(post["user_id"]) != user_id:
        raise Response(status_code=404)

    url = svc.s3_service.upload_file(file.file, file.filename)

    svc.repository.add_ads_media(ad_id, url)

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
