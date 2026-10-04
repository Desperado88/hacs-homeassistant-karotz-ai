"""Support pour le contrôle des oreilles du Karotz AI."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_IP_ADDRESS, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration de la plateforme number."""
    ip_address = entry.data[CONF_IP_ADDRESS]
    async_add_entities(
        [
            KarotzEarNumber(hass, entry.entry_id, ip_address, "left", "Oreille Gauche"),
            KarotzEarNumber(hass, entry.entry_id, ip_address, "right", "Oreille Droite"),
        ]
    )


class KarotzEarNumber(NumberEntity):
    """Représentation d'une oreille du Karotz."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry_id: str,
        ip_address: str,
        ear_side: str,
        name: str,
    ) -> None:
        """Initialisation de l'oreille."""
        self.hass = hass
        self._ip = ip_address
        self._side = ear_side
        self._attr_unique_id = f"{entry_id}_ear_{ear_side}"
        self._attr_name = f"Karotz {name}"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 15
        self._attr_native_step = 1
        self._attr_native_value = 0

    async def async_set_native_value(self, value: float) -> None:
        """Déplace l'oreille à la position demandée (0 à 15)."""
        position = int(value)
        self._attr_native_value = position
        
        # Récupération de la position actuelle de l'autre oreille
        left_pos = position if self._side == "left" else 0
        right_pos = position if self._side == "right" else 0

        session = async_get_clientsession(self.hass)
        url = f"http://{self._ip}/cgi-bin/ears?left={left_pos}&right={right_pos}&noreset=1"

        async with session.get(url):
            self.async_write_ha_state()