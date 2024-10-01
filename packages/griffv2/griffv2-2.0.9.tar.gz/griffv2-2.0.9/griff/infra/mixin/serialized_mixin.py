from pydantic import BaseModel

from griff.services.json.json_service import JsonService

Deserialized = BaseModel
Serialized = str


class SerializedMixin:
    json_service: JsonService

    def _serialize(self, deserialized: Deserialized) -> str:
        json_prepared = self.json_service.to_json_dumpable(deserialized.model_dump())
        return self.json_service.dump(json_prepared)

    def _deserialize(self, serialized: Serialized) -> dict:
        return self.json_service.load_from_str(serialized)
