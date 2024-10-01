from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from injector import inject

from griff.domain.common_types import Aggregate
from griff.infra.mixin.serialized_mixin import SerializedMixin
from griff.infra.persistence.domain_persistence import (
    DomainPersistence,
)
from griff.infra.repository.repository import Repository
from griff.services.date.date_service import DateService
from griff.services.json.json_service import JsonService

A = TypeVar("A", bound=Aggregate)


class SerializedRepository(SerializedMixin, Generic[A], Repository[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        persistence: DomainPersistence,
        date_service: DateService,
        json_service: JsonService,
    ):
        super().__init__(persistence, date_service)
        self.json_service = json_service

    def _serialize_for_persistence(self, aggregate: A) -> dict:
        return {
            "entity_id": aggregate.entity_id,
            "serialized": self._serialize(aggregate),
        }

    def _convert_to_hydratation_dict(self, result: dict) -> dict:
        return self._deserialize(result["serialized"])
