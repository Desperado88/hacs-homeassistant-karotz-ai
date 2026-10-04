"""Support pour l'entité Light Karotz AI."""

from __future__ import annotations

from typing import Any
from homeassistant.components.light import (
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import color as color_util

from .const import CONF_IP_ADDRESS, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration de la plateforme light."""
    ip_address = entry.data[CONF_IP_ADDRESS]
    async_add_entities([KarotzLight(hass, entry.entry_id, ip_address)])


class KarotzLight(LightEntity):
    """Représentation de la LED du Karotz."""

    def __init__(self, hass: HomeAssistant, entry_id: str, ip_address: str) -> None:
        """Initialisation de la LED."""
        self.hass = hass
        self._ip = ip_address
        self._attr_unique_id = f"{entry_id}_led"
        self._attr_name = "Karotz AI LED"
        self._attr_supported_color_modes = {ColorMode.RGB}
        self._attr_color_mode = ColorMode.RGB
        self._attr_rgb_color = (0, 255, 0)
        self._attr_is_on = True

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Allume la LED ou change sa couleur."""
        session = async_get_clientsession(self.hass)

        if ATTR_RGB_COLOR in kwargs:
            self._attr_rgb_color = kwargs[ATTR_RGB_COLOR]

        hex_color = color_util.color_rgb_to_hex(*self._attr_rgb_color)
        url = f"http://{self._ip}/cgi-bin/leds?pulse=0&color={hex_color}"

        async with session.get(url):
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Éteint la LED."""
        session = async_get_clientsession(self.hass)
        url = f"http://{self._ip}/cgi-bin/leds?pulse=0&color=000000"

        async with session.get(url):
            self._attr_is_on = False
            self.async_write_ha_state()