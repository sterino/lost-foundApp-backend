from fastapi import Depends, Response, status

from ..service import Service, get_service
from . import router


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_shanyraq_by_user_id(
    id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.delete_shanyraq_by_id(id)

    return Response(status_code=200)
