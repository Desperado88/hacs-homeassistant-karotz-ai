"""Initialisation du composant Karotz AI."""

from __future__ import annotations

from aiohttp import web
import voluptuous as vol
from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_component

from .const import (
    ATTR_RFID_TAGS,
    CONF_IP_ADDRESS,
    DOMAIN,
    SERVICE_ASSIGN_RFID_TAG,
    SERVICE_DELETE_RFID_TAG,
)

PLATFORMS: list[str] = ["media_player", "light", "number", "sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration du Karotz à partir d'une entrée utilisateur."""
    # Initialisation des données de base
    hass.data.setdefault(DOMAIN, {})
    hass.data.setdefault(f"{DOMAIN}_rfid", {})

    ip_address = entry.data[CONF_IP_ADDRESS]
    webhook_id = f"karotz_ai_rfid_{entry.entry_id}"

    hass.data[DOMAIN][entry.entry_id] = {
        CONF_IP_ADDRESS: ip_address,
        "webhook_id": webhook_id,
    }

    # Initialiser la liste des tags RFID pour cette entrée
    if entry.entry_id not in hass.data[f"{DOMAIN}_rfid"]:
        hass.data[f"{DOMAIN}_rfid"][entry.entry_id] = []

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

    # ===== SERVICES RFID =====
    # Service : Assigner un tag RFID
    async def handle_assign_rfid_tag(call: ServiceCall) -> None:
        """Associe un tag RFID à une action."""
        entry_id = call.data.get("entry_id")
        tag_id = call.data.get("tag_id")
        tag_name = call.data.get("tag_name", "")
        action = call.data.get("action", "")

        if not entry_id or not tag_id:
            return

        # Initialiser la liste si elle n'existe pas
        if entry_id not in hass.data[f"{DOMAIN}_rfid"]:
            hass.data[f"{DOMAIN}_rfid"][entry_id] = []

        # Vérifier si le tag existe déjà
        existing_tags = hass.data[f"{DOMAIN}_rfid"][entry_id]
        tag_found = False
        for tag in existing_tags:
            if tag["id"] == tag_id:
                # Mettre à jour le tag existant
                tag.update({"name": tag_name, "action": action})
                tag_found = True
                break

        if not tag_found:
            # Ajouter un nouveau tag
            existing_tags.append({"id": tag_id, "name": tag_name, "action": action})

        # Mettre à jour le sensor
        await entity_component.async_update_entity(
            hass, f"sensor.{DOMAIN}_{entry_id}_rfid_tags"
        )

    # Service : Supprimer un tag RFID
    async def handle_delete_rfid_tag(call: ServiceCall) -> None:
        """Supprime un tag RFID."""
        entry_id = call.data.get("entry_id")
        tag_id = call.data.get("tag_id")

        if not entry_id or not tag_id:
            return

        if entry_id in hass.data[f"{DOMAIN}_rfid"]:
            # Filtrer pour supprimer le tag
            hass.data[f"{DOMAIN}_rfid"][entry_id] = [
                tag for tag in hass.data[f"{DOMAIN}_rfid"][entry_id]
                if tag["id"] != tag_id
            ]
            # Mettre à jour le sensor
            await entity_component.async_update_entity(
                hass, f"sensor.{DOMAIN}_{entry_id}_rfid_tags"
            )

    # Enregistrer les services
    hass.services.async_register(
        DOMAIN,
        SERVICE_ASSIGN_RFID_TAG,
        handle_assign_rfid_tag,
        schema=vol.Schema({
            vol.Required("entry_id"): str,
            vol.Required("tag_id"): str,
            vol.Optional("tag_name"): str,
            vol.Optional("action"): str,
        }),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_RFID_TAG,
        handle_delete_rfid_tag,
        schema=vol.Schema({
            vol.Required("entry_id"): str,
            vol.Required("tag_id"): str,
        }),
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Déchargement d'une entrée de configuration."""
    webhook_id = hass.data[DOMAIN][entry.entry_id].get("webhook_id")
    if webhook_id:
        webhook.async_unregister(hass, webhook_id)

    # Nettoyer les données RFID
    if entry.entry_id in hass.data.get(f"{DOMAIN}_rfid", {}):
        hass.data[f"{DOMAIN}_rfid"][entry.entry_id] = []

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok