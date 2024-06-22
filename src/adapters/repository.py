from domain import model

from typing import List
from sqlalchemy.orm import session, sessionmaker
import abc

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self, reference: str) -> model.Batch:
        raise NotImplementedError
    
class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: session) -> None:
        self.session = session

    def add(self, batch: model.Batch):
        return session.add(batch)
    
    def get(self, reference: str) -> model.Batch:
        return self.session.query(model.Batch).filter_by(reference).first()
    
    def list(self) -> List[model.Batch]:
        return self.session.query(model.Batch).all()

class FakeRepository(AbstractRepository):
    def __init__(self, batches) -> None:
        self._batches = set(batches)

    def add(self, batch: model.Batch):
        self._batches.add(batch)

    def get(self, reference: str) -> model.Batch:
        return next(batch for batch in self._batches if batch.reference == reference)
    
    def list(self):
        return list(self._batches)