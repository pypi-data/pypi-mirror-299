from abc import ABC, abstractmethod
from typing import List, Any, Dict

QueryRowResult = Dict[str, Any]
QueryRowResults = List[QueryRowResult]
QueryResult = QueryRowResult | QueryRowResults


class DomainPersistence(ABC):  # pragma: no cover
    @abstractmethod
    async def insert(self, data: dict) -> None:
        ...

    @abstractmethod
    async def update(self, data: dict) -> None:
        ...

    @abstractmethod
    async def delete(self, persistence_id: str) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, persistence_id: str) -> QueryRowResult | None:
        ...

    @abstractmethod
    async def list_all(self) -> QueryRowResults:
        ...

    @abstractmethod
    async def run_query(self, query_name: str, **query_params) -> QueryResult:
        ...
