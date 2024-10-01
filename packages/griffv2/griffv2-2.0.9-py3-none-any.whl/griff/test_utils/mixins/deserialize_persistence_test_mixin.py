import copy
from typing import List, Any

from griff.services.json.json_service import JsonService


class DeserializePersistenceTestMixin:
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.json_service = cls.get_injected(JsonService)

    def deserialize(self, data: dict[str, Any] | List[dict[str, Any]] | None):
        def prepare(data):
            if "serialized" not in data:
                return data
            serialized = data.pop("serialized")
            return {**data, **self.json_service.load_from_str(serialized)}

        data_copy = copy.deepcopy(data)

        if isinstance(data_copy, list):
            return [prepare(d) for d in data_copy]
        return prepare(data_copy)
