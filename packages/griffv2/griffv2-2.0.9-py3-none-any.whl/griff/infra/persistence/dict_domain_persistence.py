import copy
import re
from typing import Dict, List, Callable, Coroutine, Any

from griff.infra.persistence.domain_persistence import (
    DomainPersistence,
    QueryRowResult,
    QueryResult,
    QueryRowResults,
)
from griff.services.json.json_service import JsonService

QueryName = str
QueryCallable = Callable[..., Coroutine[Any, Any, QueryResult]]


class DictDomainPersistence(DomainPersistence):
    def __init__(self, initial_data: List[Dict] | None = None):
        self._internal_storage: Dict[str, Dict] = {}
        self.reset(initial_data)

    async def insert(self, data: dict) -> None:
        if data["entity_id"] not in self._internal_storage:
            self._internal_storage[data["entity_id"]] = data
            return None
        raise ValueError(f"id '{data['entity_id']}' already exists")

    async def update(self, data: dict) -> None:
        if data["entity_id"] in self._internal_storage:
            self._internal_storage[data["entity_id"]] = data
            return None
        raise ValueError(f"id '{data['entity_id']}' does not exists")

    async def delete(self, persistence_id: str) -> None:
        if persistence_id in self._internal_storage:
            self._internal_storage.pop(persistence_id)
            return None
        raise ValueError(f"id '{persistence_id}' does not exists")

    async def get_by_id(self, persistence_id: str) -> QueryRowResult:
        if persistence_id in self._internal_storage:
            return self._internal_storage[persistence_id]
        raise ValueError(f"id '{persistence_id}' not found")

    async def list_all(self) -> QueryRowResults:
        return list(self._internal_storage.values())

    async def run_query(self, query_name: str, **query_params) -> QueryResult:
        if self._has_custom_queries(query_name):
            return await self._run_custom_queries(query_name, **query_params)
        result = self._try_get_by_query(query_name, **query_params)
        if result is not False:
            return result
        raise RuntimeError(f"Query {query_name} not found")

    def reset(self, initial_data: List[Dict] | None = None):
        if initial_data is None:
            self._internal_storage = {}
            return None
        self._internal_storage = {e["entity_id"]: e for e in initial_data}

    @property
    def _queries(self) -> Dict[QueryName, QueryCallable]:
        return {}

    def _has_custom_queries(self, query_name: str) -> bool:
        return query_name in self._queries

    async def _run_custom_queries(self, query_name: str, **query_params):
        return await self._queries[query_name](**query_params)

    def _try_get_by_query(self, query_name: str, **query_params):
        pattern = r"^get_by_([a-z_]+)$"
        match = re.match(pattern, query_name)
        if not match:
            return False
        attr_name = match.group(1)
        search = query_params.get(attr_name)
        for e in self._searchable_internal_storage():
            if e.get(attr_name) == search:
                return self._internal_storage[e["entity_id"]]
        return None

    def _searchable_internal_storage(self):
        return list(self._internal_storage.values())


class SerializedDictDomainPersistence(DictDomainPersistence):
    def __init__(self, initial_data: List[Dict] | None = None):
        super().__init__(initial_data)
        self.json_service = JsonService()

    def _searchable_internal_storage(self):
        return [self._deserialize(d) for d in self._internal_storage.values()]

    def _deserialize(self, data):
        data_copy = copy.deepcopy(data)
        serialized = data_copy.pop("serialized")
        return {**data_copy, **self.json_service.load_from_str(serialized)}
