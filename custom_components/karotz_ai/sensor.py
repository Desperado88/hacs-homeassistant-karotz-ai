"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ATTR_RFID_TAGS

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([KarotzAIRfidTagsSensor(entry)])

class KarotzAIRfidTagsSensor(SensorEntity):
    """Representation of RFID tags list."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_rfid_tags"
        self._attr_name = f"{entry.title} - Tags RFID"
        self._attr_icon = "mdi:rfid"

    @property
    def native_value(self) -> int:
        """Return the number of RFID tags."""
        tags = self.hass.data.get(f"{DOMAIN}_rfid", {}).get(self._entry.entry_id, [])
        return len(tags)

    @property
    def extra_state_attributes(self) -> dict:
        """Return the list of RFID tags."""
        tags = self.hass.data.get(f"{DOMAIN}_rfid", {}).get(self._entry.entry_id, [])
        return {ATTR_RFID_TAGS: tags}