from typing import Any, Dict

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint
from grinning_cat_python_sdk.models.api.factories import (
    FactoryObjectSettingOutput,
    FactoryObjectSettingsOutput,
)


class IngestionEndpoint(AbstractEndpoint):
    def __init__(self, client: "GrinningCatClient"):
        super().__init__(client)
        self.prefix = "/ingestion"

    def get_ingestions_settings(self) -> FactoryObjectSettingsOutput:
        """
        Get all ingestion engine configurations for the system
        :return: FactoryObjectSettingsOutput, a list of ingestion engine settings
        """
        return self.get(
            self.format_url("/settings"),
            self.system_id,
            output_class=FactoryObjectSettingsOutput,
        )

    def get_ingestion_settings(self, ingestion: str) -> FactoryObjectSettingOutput:
        """
        Get ingestion engine settings for the system by configuration name
        :param ingestion: The ingestion configuration name
        :return: FactoryObjectSettingOutput, ingestion engine settings
        """
        return self.get(
            self.format_url(f"/settings/{ingestion}"),
            self.system_id,
            output_class=FactoryObjectSettingOutput,
        )

    def put_ingestion_settings(self, ingestion: str, values: Dict[str, Any]) -> FactoryObjectSettingOutput:
        """
        Update ingestion engine settings by configuration name
        :param ingestion: The ingestion configuration name
        :param values: The ingestion engine settings
        :return: FactoryObjectSettingOutput, ingestion engine settings
        """
        return self.put(
            self.format_url(f"/settings/{ingestion}"),
            self.system_id,
            output_class=FactoryObjectSettingOutput,
            payload=values,
        )
