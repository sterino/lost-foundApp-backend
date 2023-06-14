
from fastapi import Depends
from ..service import Service, get_service
from . import router
from typing import List

from fastapi import UploadFile


@router.post("/{id}/file")
def add_Image(
    file: UploadFile,
    svc: Service = Depends(get_service),
):
    url = svc.s3_service.upload_file(file.file, file.filename)
    return {"msg": url}


@router.post("/files")
def upload_files(
    files: List[UploadFile],
    svc: Service = Depends(get_service),
):
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    return {"msg": files}
