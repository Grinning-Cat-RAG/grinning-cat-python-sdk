from typing import Dict, Any, List
from pydantic import BaseModel


class PropertySettingsOutput(BaseModel):
    default: Any
    title: str | None = None
    type: str | None = None
    # JSON-Schema metadata that Pydantic emits from model_json_schema().
    # Exposed explicitly so the admin UI can render hints/enum choosers and
    # mask password-like fields (they are silently dropped otherwise).
    description: str | None = None
    enum: List[Any] | None = None
    format: str | None = None
    extra: Dict[str, Any] | None = None


class PluginSchemaSettings(BaseModel):
    title: str
    type: str
    properties: Dict[str, PropertySettingsOutput]


class PluginSettingsOutput(BaseModel):
    name: str
    value: Dict[str, Any]
    scheme: PluginSchemaSettings | None = None

    def __init__(self, /, **data: Any) -> None:
        # if tags is a list, convert it to a comma-separated string
        if "scheme" in data and isinstance(data["scheme"], Dict) and not data["scheme"]:
            data["scheme"] = None
        super().__init__(**data)
