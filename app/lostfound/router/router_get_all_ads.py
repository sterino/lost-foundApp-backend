from typing import Any, List, Optional

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Ads(AppModel):
    id: Any = Field(alias="_id")
    type: int
    title: str
    description: str
    media: str


class GetAdsResponse(AppModel):
    total: int
    ads: List[Ads]


@router.get("/getads", response_model=GetAdsResponse)
def get_posts(
    type: Optional[int] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_ads(
        type,
        category,
    )
    return result
