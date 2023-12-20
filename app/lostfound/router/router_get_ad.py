from fastapi import Depends

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from typing import Optional, Any

from pydantic import Field


class getPostResponse(AppModel):
    id: Any = Field(alias="_id")
    category: str
    type: int
    title: str
    description: str
    media: Optional[list]


@router.get("/{post_id}", status_code=200, response_model=getPostResponse)
def get_post(post_id: str, svc: Service = Depends(get_service)):
    post = svc.repository.get_ad_by_id(post_id)

    if not post:
        raise InvalidCredentialsException

    return post