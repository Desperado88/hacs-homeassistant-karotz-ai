"""Constantes pour l'intégration Karotz AI."""
from homeassistant.const import Platform

DOMAIN = "karotz_ai"
CONF_IP_ADDRESS = "ip_address"
DEFAULT_NAME = "Karotz"

# RFID
ATTR_RFID_TAGS = "rfid_tags"
SERVICE_ASSIGN_RFID_TAG = "assign_rfid_tag"
SERVICE_DELETE_RFID_TAG = "delete_rfid_tag"