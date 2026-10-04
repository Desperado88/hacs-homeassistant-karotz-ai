"""Support pour l'entité Media Player Karotz AI."""

from __future__ import annotations

import urllib.parse
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaType,
)
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
    """Configuration de la plateforme media_player."""
    ip_address = entry.data[CONF_IP_ADDRESS]
    async_add_entities([KarotzMediaPlayer(hass, entry.entry_id, ip_address)])


class KarotzMediaPlayer(MediaPlayerEntity):
    """Représentation du Karotz en tant que Media Player."""

    def __init__(self, hass: HomeAssistant, entry_id: str, ip_address: str) -> None:
        """Initialisation du lecteur média."""
        self.hass = hass
        self._ip = ip_address
        self._attr_unique_id = f"{entry_id}_media_player"
        self._attr_name = "Karotz AI Speaker"
        self._attr_supported_features = (
            MediaPlayerEntityFeature.VOLUME_SET
            | MediaPlayerEntityFeature.PLAY_MEDIA
            | MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.TURN_OFF
        )
        self._attr_volume_level = 0.5
        self._attr_is_on = True

    async def async_turn_on(self) -> None:
        """Réveille le Karotz."""
        session = async_get_clientsession(self.hass)
        async with session.get(f"http://{self._ip}/cgi-bin/wakeup?silent=1"):
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Endort le Karotz."""
        session = async_get_clientsession(self.hass)
        async with session.get(f"http://{self._ip}/cgi-bin/sleep"):
            self._attr_is_on = False
            self.async_write_ha_state()

    async def async_set_volume_level(self, volume: float) -> None:
        """Définit le volume (0.0 à 1.0)."""
        level = int(volume * 100)
        session = async_get_clientsession(self.hass)
        async with session.get(
            f"http://{self._ip}/cgi-bin/volume?level={level}"
        ):
            self._attr_volume_level = volume
            self.async_write_ha_state()

    async def async_play_media(
        self, media_type: MediaType | str, media_id: str, **kwargs
    ) -> None:
        """Lit un texte via le TTS OpenKarotz ou joue un son."""
        session = async_get_clientsession(self.hass)
        encoded_text = urllib.parse.quote(media_id)

        # Envoi de la requête TTS à OpenKarotz
        url = f"http://{self._ip}/cgi-bin/tts?voice=2&text={encoded_text}&nocache=1"
        async with session.get(url):
            pass