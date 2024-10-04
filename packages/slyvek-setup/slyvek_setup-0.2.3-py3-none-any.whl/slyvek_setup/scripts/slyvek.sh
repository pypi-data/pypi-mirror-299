#!/bin/bash
# Script pour gérer le loginserver et gameservers

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Pas de Couleur

# Chemins de base pour les serveurs de jeu et de login
GAMESERVERS_PATH="/root/Slyvek/Slyvek_GameServers"
LOGINSERVERS_PATH="/root/Slyvek/Slyvek_LoginServer"

API_URL="http://127.0.0.1:5000"  # L'URL de l'API Flask
API_KEY=$API_KEY  # La clé API à utiliser pour l'authentification

# Fonction pour afficher les messages
display_message() {
  COLOR=$1
  MESSAGE=$2
  echo -e "${COLOR}${MESSAGE}${NC}"
}

# Fonction pour vérifier si `screen` est installé
check_screen_installed() {
  if ! command -v screen &> /dev/null; then
    display_message "$RED" "Erreur : L'utilitaire 'screen' n'est pas installé. Veuillez l'installer et réessayer."
    exit 1
  fi
}

# Vérifier si le serveur Flask API est déjà en cours d'exécution dans une session screen
is_api_running() {
  screen -list | grep -q "api"
}

# Démarrer le serveur Flask API dans une session screen
start_api() {
  if is_api_running; then
    display_message "$YELLOW" "Le serveur API est déjà en cours d'exécution."
  else
    display_message "$GREEN" "Démarrage du serveur API..."
    screen -dmS api bash -c "cd /root/SlyvekVps/SlyvekApi && source venv/bin/activate && flask run"
    display_message "$GREEN" "Serveur API démarré."
  fi
}

# Se connecter à la session screen du serveur Flask API
connect_api() {
  if is_api_running; then
    display_message "$YELLOW" "Connexion à la session screen du serveur API..."
    screen -x api
  else
    display_message "$RED" "Erreur : Le serveur API n'est pas en cours d'exécution."
  fi
}

# Arrêter la session screen du serveur Flask API
kill_api() {
  if is_api_running; then
    display_message "$RED" "Arrêt du serveur API..."
    screen -S api -X quit
    display_message "$GREEN" "Serveur API arrêté."
  else
    display_message "$YELLOW" "Le serveur API n'est pas en cours d'exécution."
  fi
}
# Vérifier si le serveur est déjà en cours d'exécution dans une session screen
is_server_running() {
  SERVER_NAME=$1
  screen -list | grep -q "$SERVER_NAME"
}

# Trouver le chemin du serveur donné (login ou jeu)
find_server_path() {
  SERVER_NAME=$1
  SERVER_PATH=""

  if [ -d "$GAMESERVERS_PATH/$SERVER_NAME" ]; then
    SERVER_PATH="$GAMESERVERS_PATH/$SERVER_NAME"
  elif [ -d "$LOGINSERVERS_PATH/$SERVER_NAME" ]; then
    SERVER_PATH="$LOGINSERVERS_PATH/$SERVER_NAME"
  fi

  echo "$SERVER_PATH"
}

# Fonction pour démarrer un serveur
start_server() {
  SERVER_NAME=$1
  curl -X POST "$API_URL/start_server" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    -d "{\"server_name\": \"$SERVER_NAME\"}"
}

# Fonction pour arrêter un serveur
stop_server() {
  SERVER_NAME=$1
  curl -X POST "$API_URL/stop_server" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    -d "{\"server_name\": \"$SERVER_NAME\"}"
}

# Fonction pour effacer la base de données d'un serveur
clear_db() {
  SERVER_NAME=$1
  curl -X POST "$API_URL/clear_db" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $API_KEY" \
    -d "{\"server_name\": \"$SERVER_NAME\"}"
}

# Fonction pour se connecter à un serveur en cours d'exécution
connect_server() {
  SERVER_NAME=$1

  if is_server_running "$SERVER_NAME"; then
    display_message "$YELLOW" "Connexion au serveur $SERVER_NAME..."
    screen -x "$SERVER_NAME"
  else
    display_message "$RED" "Erreur : Le serveur $SERVER_NAME n'est pas en cours d'exécution."
  fi
}

# Fonction pour redémarrer un serveur
restart_server() {
  SERVER_NAME=$1
  stop_server "$SERVER_NAME"
  start_server "$SERVER_NAME"
}

# Fonction pour generer un clef d'api
genrate_key() {
  python3 /root/SlyvekVps/SlyvekApi/services/generate_key.py
}

# Vérifier si screen est installé
check_screen_installed

usage() {
  echo -e "${YELLOW}Slyvek Server Management Script${NC}"
  echo -e ""
  echo -e "${GREEN}Description :${NC} Utilisez ce script pour gérer vos serveurs de jeu, de login, ainsi que l'API Flask à travers les actions démarrer, arrêter, redémarrer, se connecter et nettoyer les bases de données."
  echo -e ""
  echo -e "${YELLOW}Usage :${NC} slyvek <action> <nom_du_serveur>"
  echo -e ""
  echo -e "${YELLOW}Actions disponibles :${NC}"
  echo -e "  ${GREEN}-s|--start        ${NC} : Démarrer le serveur spécifié"
  echo -e "  ${GREEN}-k|--kill         ${NC} : Arrêter le serveur spécifié"
  echo -e "  ${GREEN}-c|--connect      ${NC} : Se connecter à une session screen d'un serveur en cours d'exécution"
  echo -e "  ${GREEN}-r|--restart      ${NC} : Redémarrer le serveur spécifié"
  echo -e "  ${GREEN}-ls|--list        ${NC} : Lister toutes les sessions screen en cours d'exécution"
  echo -e "  ${GREEN}-cd|--clear_db    ${NC} : Effacer la base de données d'un serveur spécifié"
  echo -e "  ${GREEN}-gk|--generate_key${NC} : Générer et stocker une clé API pour la gestion sécurisée des serveurs"
  echo -e "  ${GREEN}-api-start        ${NC} : Démarrer l'API Flask dans une session screen"
  echo -e "  ${GREEN}-api-stop         ${NC} : Arrêter la session screen de l'API Flask"
  echo -e "  ${GREEN}-api-connect      ${NC} : Se connecter à la session screen de l'API Flask"
  echo -e ""
  echo -e "${YELLOW}Exemples :${NC}"
  echo -e "  ${GREEN}slyvek -s <nom_du_serveur>${NC}            : Démarrer un serveur de jeu ou de login"
  echo -e "  ${GREEN}slyvek -k <nom_du_serveur>${NC}            : Arrêter le serveur spécifié"
  echo -e "  ${GREEN}slyvek -c <nom_du_serveur>${NC}            : Se connecter à un serveur en cours d'exécution"
  echo -e "  ${GREEN}slyvek -r <nom_du_serveur>${NC}            : Redémarrer un serveur"
  echo -e "  ${GREEN}slyvek -ls${NC}                           : Lister toutes les sessions screen en cours"
  echo -e "  ${GREEN}slyvek -cd <nom_du_serveur>${NC}           : Effacer la base de données d'un serveur"
  echo -e "  ${GREEN}slyvek -gk${NC}                            : Générer une nouvelle clé API sécurisée"
  echo -e "  ${GREEN}slyvek -api-start${NC}                      : Démarrer l'API Flask"
  echo -e "  ${GREEN}slyvek -api-stop${NC}                       : Arrêter l'API Flask"
  echo -e "  ${GREEN}slyvek -api-connect${NC}                    : Se connecter à la session screen de l'API Flask"
  echo -e ""
  echo -e "${YELLOW}Gestion des clés API :${NC} Ce script prend en charge la génération et la gestion sécurisée des clés API."
  echo -e "  ${GREEN}Vous pouvez utiliser la commande ${YELLOW}'slyvek -gk'${NC} pour générer une nouvelle clé API hachée et sécurisée."
  echo -e "  ${YELLOW}Remarque :${NC} L'API Flask est utilisée pour démarrer, arrêter et nettoyer les serveurs. Assurez-vous que l'API est en ligne et que la clé API est correcte."
}


# Analyse des arguments
case "$1" in
  -s|--start)
    if [ -n "$2" ]; then
      start_server "$2"
    else
      display_message "$YELLOW" "Usage: slyvek -s <nom_du_serveur>"
    fi
    ;;
  -c|--connect)
    if [ -n "$2" ]; then
      connect_server "$2"
    else
      display_message "$YELLOW" "Usage: slyvek -c <nom_du_serveur>"
    fi
    ;;
  -k|--kill)
    if [ -n "$2" ]; then
      stop_server "$2"
    else
      display_message "$YELLOW" "Usage: slyvek -k <nom_du_serveur>"
    fi
    ;;
  -r|--restart)
    if [ -n "$2" ]; then
      restart_server "$2"
    else
      display_message "$YELLOW" "Usage: slyvek -r <nom_du_serveur>"
    fi
    ;;
  -ls|--list)
    screen -ls
    ;;
  -cd|--clear_db)
    if [ -n "$2" ]; then
      clear_db "$2"
    else
      display_message "$YELLOW" "Usage: slyvek -cd <nom_du_serveur>"
    fi
    ;;
  -gk|--generate_key)
    genrate_key
    ;;
  -api-start)
    start_api
    ;;
  -api-connect)
    connect_api
    ;;
  -api-stop)
    kill_api
    ;;
  *)
    usage
    ;;
esac
