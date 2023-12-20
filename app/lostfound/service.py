from app.config import database

from .adapters.s3_service import S3Service
from .repository.repository import AdsRepository


class Service:
    def __init__(self):
        self.repository = AdsRepository(database)
        self.s3_service = S3Service()


def get_service():
    svc = Service()
    return svc
