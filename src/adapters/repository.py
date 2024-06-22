from domain import model
import abc

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch:model.Batch):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self, reference: str) -> model.Batch:
        raise NotImplementedError