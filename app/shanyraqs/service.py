from app.config import database

from .repository.repository import ShanyraqRepository


class Service:
    def __init__(
        self,
        repository: ShanyraqRepository,
    ):
        self.repository = repository


def get_service():
    repository = ShanyraqRepository(database)

    svc = Service(repository)
    return svc
