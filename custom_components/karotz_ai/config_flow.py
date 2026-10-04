"""Config flow pour l'intégration Karotz AI."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import CONF_IP_ADDRESS, DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
    }
)


class KarotzAIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gère le flux de configuration du Karotz AI."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Étape d'initialisation par l'utilisateur."""
        errors = {}

        if user_input is not None:
            # On vérifie si cet identifiant/IP est déjà configuré
            await self.async_set_unique_id(user_input[CONF_IP_ADDRESS])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Karotz ({user_input[CONF_IP_ADDRESS]})",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )