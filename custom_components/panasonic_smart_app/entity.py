from abc import ABC, abstractmethod
import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .model_type import find_model_commands
from .smartApp import SmartApp

_LOGGER = logging.getLogger(__package__)


class PanasonicBaseEntity(CoordinatorEntity, ABC):
    def __init__(
        self,
        coordinator,
        index,
        client,
        device,
    ):
        super().__init__(coordinator)
        self.client: SmartApp = client
        self.device = device
        self.index = index

    @property
    @abstractmethod
    def label(self) -> str:
        """Label to use for name and unique id."""
        ...

    @property
    def current_device_info(self) -> dict:
        return self.device

    @property
    def nickname(self) -> str:
        return self.current_device_info["NickName"]

    @property
    def model(self) -> str:
        return self.current_device_info["Model"]

    @property
    def commands(self) -> list:
        command_list = self.client.get_commands()
        current_model_type = self.current_device_info["ModelType"]
        commands = find_model_commands(command_list, current_model_type)

        if not commands:
            _LOGGER.warning(
                "No command metadata found for %s (ModelType: %s)",
                self.nickname,
                current_model_type,
            )
            return []

        return commands[0]["JSON"][0]["list"]

    @property
    def name(self) -> str:
        return self.label

    @property
    def auth(self) -> str:
        return self.device["Auth"]

    @property
    def unique_id(self) -> str:
        return self.auth + self.label

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self.auth)},
            "name": self.nickname,
            "manufacturer": MANUFACTURER,
            "model": self.model,
        }
