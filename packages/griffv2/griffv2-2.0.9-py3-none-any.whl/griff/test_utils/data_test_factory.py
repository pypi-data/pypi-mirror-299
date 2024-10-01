import inspect
import random
from abc import ABC
from decimal import Decimal
from typing import Self

from griff.domain.common_types import Entity
from griff.infra.repository.repository import Repository
from griff.services.date.fake_date_service import FakeDateService
from griff.services.uniqid.generator.fake_uniqid_generator import FakeUniqIdGenerator
from griff.services.uniqid.uniqid_service import UniqIdService
from griff.utils.async_utils import AsyncUtils


class DataTestFactory(ABC):
    def __init__(self, start_id=1):
        self.uniqid_service = UniqIdService(FakeUniqIdGenerator(start_id))
        self.date_service = FakeDateService()
        self._sequence = {}
        random.seed(42)
        self._random_state = random.getstate()

    def reset(self, start_id=1):
        self.uniqid_service.reset(start_id)

    async def persist(
        self, repository: Repository, data: list[Entity] | Entity
    ) -> Self:
        if isinstance(data, list) is False:
            await repository.save(data)
            return self

        for a in data:
            await repository.save(a)
        return self

    def sync_persist(self, repository: Repository, data: list[Entity] | Entity) -> Self:
        AsyncUtils.async_to_sync(self.persist, [repository, data])
        return self

    def _random_decimal(self, min, max) -> Decimal:
        random.setstate(self._random_state)
        min = float(min) * 100
        max = float(max) * 100
        val = Decimal(random.uniform(min, max)) / 100
        self._random_state = random.getstate()
        return val

    def _random_int(self, min, max) -> int:
        random.setstate(self._random_state)
        val = random.randrange(min, max)
        self._random_state = random.getstate()
        return val

    def _next_sequence(self):
        current_frame = inspect.currentframe()
        calling_frame = inspect.getouterframes(current_frame, 2)
        caller = calling_frame[1][3]
        if caller not in self._sequence:
            self._sequence[caller] = 0
        self._sequence[caller] += 1
        # self.uniqid_service.reset(self._sequence[caller])
        return self._sequence[caller]
