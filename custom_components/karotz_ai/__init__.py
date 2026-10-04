"""Initialisation du composant Karotz AI."""

from __future__ import annotations

from aiohttp import web
from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_IP_ADDRESS, DOMAIN

PLATFORMS: list[str] = ["media_player", "light", "number"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration du Karotz à partir d'une entrée utilisateur."""
    hass.data.setdefault(DOMAIN, {})
    ip_address = entry.data[CONF_IP_ADDRESS]
    webhook_id = f"karotz_ai_rfid_{entry.entry_id}"

    hass.data[DOMAIN][entry.entry_id] = {
        CONF_IP_ADDRESS: ip_address,
        "webhook_id": webhook_id,
    }

    # Handler du Webhook RFID envoyé par OpenKarotz
    async def handle_rfid_webhook(hass: HomeAssistant, webhook_id: str, request: web.Request):
        """Déclenche un événement HA lors de la lecture d'un tag RFID."""
        data = await request.post() if request.method == "POST" else request.query
        tag_id = data.get("tag_id") or data.get("tag")

        if tag_id:
            # Émission de l'événement natif sur le bus de Home Assistant
            hass.bus.async_fire(
                "karotz_ai_rfid_scanned",
                {
                    "entry_id": entry.entry_id,
                    "ip_address": ip_address,
                    "tag_id": tag_id,
                },
            )
        return web.Response(text="OK", status=200)

    # Enregistrement du Webhook local dans Home Assistant
    webhook.async_register(
        hass,
        DOMAIN,
        "Karotz RFID Reader",
        webhook_id,
        handle_rfid_webhook,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Déchargement d'une entrée de configuration."""
    webhook_id = hass.data[DOMAIN][entry.entry_id].get("webhook_id")
    if webhook_id:
        webhook.async_unregister(hass, webhook_id)

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok