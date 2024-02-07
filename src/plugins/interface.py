from abc import ABC, abstractmethod


class Plugin(ABC):

    def __init__(self, db):
        self.db = db

    @abstractmethod
    async def process_request(self, data):
        raise NotImplementedError()

    def _build_query(self, *args):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()