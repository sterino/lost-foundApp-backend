from app.config import database

from .adapters.s3_service import S3Service
from .repository.repository import ShanyraqRepository


class Service:
    def __init__(
        self,
        repository: ShanyraqRepository(database),
        s3_service: S3Service(),
    ):
        self.repository = repository
        self.s3_service = s3_service


def get_service():
    repository = ShanyraqRepository(database)
    s3_service = S3Service()
    svc = Service(repository, s3_service)

    return svc
