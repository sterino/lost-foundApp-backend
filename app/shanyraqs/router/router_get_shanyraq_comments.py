from typing import Any, List

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetShanyraqCommentsOptions(AppModel):
    id: Any = Field(alias="_id")
    content: str
    created_at: str
    author_id: str


class GetShanyraqCommentsResponse(AppModel):
    comment: List[GetShanyraqCommentsOptions]


@router.get("/{id}/comments", response_model=GetShanyraqCommentsResponse)
def get_comments(
    id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    comment = svc.repository.get_shanyraq_comments(id)
    cm = []
    for com in comment:
        created_at = str(com["created_at"])
        person_id = str(com["person_id"])
        cm.append(
            GetShanyraqCommentsOptions(
                id=com["id"],
                content=com["content"],
                created_at=created_at,
                author_id=person_id,
            )
        )
    return GetShanyraqCommentsResponse(comment=cm)
