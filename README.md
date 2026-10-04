> **⚠️ Statut du projet : Abandonné mais fonctionnel**
> 
> Ce projet est **abandonné** et ne sera plus maintenu activement.
> Cependant, il est **fonctionnel en l'état** et peut être utilisé tel quel.
> N'hésitez pas à le forker et à contribuer si vous souhaitez poursuivre son développement.

---

# Karotz AI — Home Assistant Integration 🥕🤖

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/default)

Intégration Home Assistant permettant de ressusciter le **Karotz (OpenKarotz)** et de le connecter directement aux modèles de langage (Claude, OpenAI) via **Home Assistant Assist**.

## 🚀 Fonctionnalités

- **Lecteur Média (`media_player`)** : Synthèse vocale (TTS) native OpenKarotz, gestion du volume, mise en veille et réveil.
- **Contrôle LED (`light`)** : Gestion des couleurs RGB sur le ventre du Karotz pour indiquer le statut du LLM.
- **Gestion des Oreilles (`number`)** : Positionnement indépendant des oreilles gauche et droite (0 à 15).
- **Lecteur RFID (`event`)** : Capture en temps réel des puces RFID (Flatnanoz / badges) transmises sous forme d'événements natifs `karotz_ai_rfid_scanned`.
- **Blueprint LLM prêt à l'emploi** : Automatisation clé en main pour exécuter des promts vocaux Claude lors du passage d'un badge.

---

## 📋 Prérequis

1. Un **Karotz** fonctionnant sous **OpenKarotz** connecté à votre réseau local.
2. **Home Assistant** avec **HACS** installé.
3. Un agent de conversation configuré dans Home Assistant (*Paramètres > Assistants vocaux*, ex: Anthropic / Claude).

---

## 📦 Installation

### Via HACS (Dépôt personnalisé)

1. Ouvrez **HACS** > **Intégrations** dans Home Assistant.
2. Cliquez sur les **trois points** en haut à droite > **Dépôts personnalisés**.
3. Saisissez l'URL de ce dépôt : `https://github.com/votre_pseudo/hacs-homeassistant-karotz-ai` et choisissez la catégorie **Intégration**.
4. Cliquez sur **Télécharger**.
5. Redémarrez Home Assistant.

### Configuration initiale

1. Rendez-vous dans **Paramètres** > **Appareils et services** > **Ajouter une intégration**.
2. Recherchez **Karotz AI**.
3. Renseignez l'adresse IP locale de votre Karotz.

---

## 🏷️ Configuration des puces RFID sur OpenKarotz

Pour transmettre la lecture des badges à Home Assistant, configurez l'URL de destination des puces dans l'interface d'OpenKarotz :

- **URL à associer aux puces :**  
  `http://<IP_HOME_ASSISTANT>:8123/api/webhook/karotz_ai_rfid_<ENTRY_ID>?tag_id={{tag_id}}`

---

## 🪄 Utilisation du Blueprint LLM

Importez le blueprint situé dans `blueprints/automation/karotz_llm_rfid.yaml` :

1. Allez dans **Paramètres** > **Automatisations et scènes** > **Blueprints**.
2. Sélectionnez **Karotz AI - Interaction RFID & LLM**.
3. Choisissez votre Karotz, l'agent vocal Claude et le prompt désiré (ex: *"Fais un résumé de l'état de la maison"*).

---

## 📄 Licence

Ce projet est sous licence MIT.