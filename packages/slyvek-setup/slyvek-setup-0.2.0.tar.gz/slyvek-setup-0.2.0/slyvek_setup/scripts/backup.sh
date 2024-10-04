#!/bin/bash

# Chemin de base pour tous les serveurs
BASE_PATH="/root/Slyvek"
BACKUP_DIR="/root/SlyvekBackup"

# Couleurs pour affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Pas de Couleur

# Fonction pour trouver le chemin du serveur
find_server_path() {
  SERVER_NAME=$1

  # Chercher dans le dossier Slyvek_GameServers
  if [ -d "$BASE_PATH/Slyvek_GameServers/$SERVER_NAME" ]; then
    echo "$BASE_PATH/Slyvek_GameServers/$SERVER_NAME"
    return 0
  fi

  # Chercher dans le dossier Slyvek_LoginServer
  if [ -d "$BASE_PATH/Slyvek_LoginServer/$SERVER_NAME" ]; then
    echo "$BASE_PATH/Slyvek_LoginServer/$SERVER_NAME"
    return 0
  fi

  # Si le serveur n'est trouvé dans aucun des répertoires
  echo ""
  return 1
}

# Fonction pour lister les backups disponibles pour un serveur donné
list_backups() {
  SERVER_NAME=$1

  # Trouver les backups qui commencent par le nom du serveur
  SERVER_BACKUP_LIST=$(find "$BACKUP_DIR" -type d -name "${SERVER_NAME}_backup_*" | sort -r)

  if [ -z "$SERVER_BACKUP_LIST" ]; then
    echo -e "${RED}Aucun backup trouvé pour le serveur $SERVER_NAME.${NC}"
    return 1
  fi

  echo -e "${YELLOW}Backups disponibles pour le serveur $SERVER_NAME :${NC}"
  
  # Imprimer l'en-tête du tableau
  printf "%-5s | %-25s | %-40s | %-15s\n" "ID" "Date de backup" "Chemin du backup" "Backup DB"
  printf "%-5s | %-25s | %-40s | %-15s\n" "----" "------------------------" "----------------------------------------" "-------------"

  # Parcourir les backups et assigner un identifiant
  ID=0
  for BACKUP_PATH in $SERVER_BACKUP_LIST; do
    # Extraire la date à partir du nom du dossier (dernière partie après _backup_)
    BACKUP_DATE=$(basename "$BACKUP_PATH" | awk -F'_backup_' '{print $2}')
    
    # Formater la date (du format YYYYMMDD_HHMMSS vers jj/mm/aaaa hh:mm)
    FORMATTED_DATE=$(date -d "${BACKUP_DATE:0:8} ${BACKUP_DATE:9:2}:${BACKUP_DATE:11:2}" +"%d/%m/%Y %H:%M")

    # Vérifier si un backup de la base de données est présent
    if [ -d "$BACKUP_PATH/Databases" ]; then
      DB_BACKUP="Oui"
    else
      DB_BACKUP="Non"
    fi

    # Tronquer le chemin si nécessaire
    TRUNCATED_PATH=$BACKUP_PATH
    if [ ${#BACKUP_PATH} -gt 40 ]; then
      TRUNCATED_PATH="...${BACKUP_PATH: -37}"
    fi

    # Imprimer la ligne du tableau avec l'ID
    printf "%-5s | %-25s | %-40s | %-15s\n" "$ID" "$FORMATTED_DATE" "$TRUNCATED_PATH" "$DB_BACKUP"
    
    # Incrémenter l'ID pour le prochain backup
    ID=$((ID + 1))
  done
}

# Fonction pour restaurer un backup spécifique (restaure les .json et Databases)
restore_backup() {
  SERVER_NAME=$1
  BACKUP_ID=$2
  SERVER_PATH=$(find_server_path "$SERVER_NAME")

  if [ -n "$SERVER_PATH" ]; then
    SERVER_BACKUP_LIST=$(find "$BACKUP_DIR" -type d -name "${SERVER_NAME}_backup_*" | sort -r)
    BACKUP_PATH=$(echo "$SERVER_BACKUP_LIST" | sed -n "$((BACKUP_ID + 1))p")

    if [ -n "$BACKUP_PATH" ]; then
      echo -e "${YELLOW}Restauration du backup ID $BACKUP_ID pour le serveur $SERVER_NAME...${NC}"
      find "$BACKUP_PATH" -type f -name "*.json" -exec cp {} "$SERVER_PATH" \;
      [ -d "$BACKUP_PATH/Databases" ] && cp -r "$BACKUP_PATH/Databases" "$SERVER_PATH"
      echo -e "${GREEN}Restauration réussie.${NC}"
    else
      echo -e "${RED}Erreur : Backup avec l'ID $BACKUP_ID non trouvé pour le serveur $SERVER_NAME.${NC}"
    fi
  else
    echo -e "${RED}Erreur : Le serveur $SERVER_NAME n'existe pas.${NC}"
  fi
}

# Fonction pour supprimer un backup spécifique ou tous les backups
delete_backups() {
  SERVER_NAME=$1
  BACKUP_ID=$2

  # Trouver le chemin du serveur
  SERVER_PATH=$(find_server_path "$SERVER_NAME")

  if [ -z "$SERVER_PATH" ]; then
    echo -e "${RED}Erreur : Le serveur $SERVER_NAME n'existe pas.${NC}"
    return 1
  fi

  # Lister tous les backups pour le serveur donné et les trier par date décroissante
  SERVER_BACKUP_LIST=$(find "$BACKUP_DIR" -type d -name "${SERVER_NAME}_backup_*" | sort -r)

  # Convertir la liste de backups en tableau
  BACKUP_ARRAY=($SERVER_BACKUP_LIST)

  # Si aucun backup trouvé
  if [ ${#BACKUP_ARRAY[@]} -eq 0 ]; then
    echo -e "${RED}Aucun backup trouvé pour le serveur $SERVER_NAME.${NC}"
    return 1
  fi

  # Vérifier si l'ID du backup est "all" pour tout supprimer
  if [ "$BACKUP_ID" == "all" ]; then
    echo -e "${YELLOW}Suppression de tous les backups pour le serveur $SERVER_NAME...${NC}"
    for BACKUP_PATH in "${BACKUP_ARRAY[@]}"; do
      rm -rf "$BACKUP_PATH"
    done
    echo -e "${GREEN}Tous les backups pour le serveur $SERVER_NAME ont été supprimés.${NC}"
  else
    # Vérifier si l'ID de backup est valide
    if [ "$BACKUP_ID" -ge 0 ] && [ "$BACKUP_ID" -lt ${#BACKUP_ARRAY[@]} ]; then
      BACKUP_PATH="${BACKUP_ARRAY[$BACKUP_ID]}"
      echo -e "${YELLOW}Suppression du backup ID $BACKUP_ID pour le serveur $SERVER_NAME : $BACKUP_PATH...${NC}"
      rm -rf "$BACKUP_PATH"
      echo -e "${GREEN}Le backup ID $BACKUP_ID pour le serveur $SERVER_NAME a été supprimé.${NC}"
    else
      echo -e "${RED}Erreur : L'ID $BACKUP_ID n'est pas valide.${NC}"
      return 1
    fi
  fi
}


# Fonction pour créer un nouveau backup (sauvegarde uniquement les .json et Databases)
create_backup() {
  SERVER_NAME=$1
  SERVER_PATH=$(find_server_path "$SERVER_NAME")

  if [ -z "$SERVER_PATH" ]; then
    echo -e "${RED}Erreur : Le serveur $SERVER_NAME n'existe pas.${NC}"
    return 1
  fi

  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  BACKUP_PATH="$BACKUP_DIR/${SERVER_NAME}_backup_$TIMESTAMP"

  echo -e "${YELLOW}Création d'un backup pour le serveur $SERVER_NAME...${NC}"

  # Créer le répertoire de sauvegarde
  mkdir -p "$BACKUP_PATH"
  
  # Sauvegarder les fichiers .json
  find "$SERVER_PATH" -type f -name "*.json" -exec cp {} "$BACKUP_PATH" \;

  # Sauvegarder le dossier Databases
  if [ -d "$SERVER_PATH/Databases" ]; then
    cp -r "$SERVER_PATH/Databases" "$BACKUP_PATH"
  fi

  echo -e "${GREEN}Backup réussi : $BACKUP_PATH${NC}"
}

# Affichage des options d'utilisation
usage() {
  echo -e "${YELLOW}Usage :${NC} backup <action> <nom_du_serveur> [id_backup]"
  echo -e ""
  echo -e "${YELLOW}Actions disponibles :${NC}"
  echo -e "  ${GREEN}-b|--backup        ${NC} : Créer un backup pour le serveur spécifié"
  echo -e "  ${GREEN}-rb|--restore      ${NC} : Restaurer un backup spécifique pour le serveur en utilisant l'ID du backup"
  echo -e "  ${GREEN}-lb|--list_backups ${NC} : Lister les backups disponibles pour le serveur, avec affichage de l'ID du backup"
  echo -e "  ${GREEN}-db|--delete_backup${NC} : Supprimer un backup spécifique (via ID) ou tous les backups (${YELLOW}all${NC}) pour le serveur"
  echo -e ""
  echo -e "${YELLOW}Exemples :${NC}"
  echo -e "  ${GREEN}backup --backup <nom_du_serveur>${NC}            : Crée un backup pour le serveur spécifié"
  echo -e "  ${GREEN}backup --list_backups <nom_du_serveur>${NC}      : Liste tous les backups disponibles avec leurs ID"
  echo -e "  ${GREEN}backup --restore <nom_du_serveur> <id_backup>${NC} : Restaure le backup spécifié pour le serveur"
  echo -e "  ${GREEN}backup --delete_backup <nom_du_serveur> all${NC} : Supprime tous les backups pour le serveur"
  echo -e "  ${GREEN}backup --delete_backup <nom_du_serveur> <id_backup>${NC} : Supprime un backup spécifique via l'ID"
  echo -e ""
  echo -e "${YELLOW}Remarques :${NC}"
  echo -e "  - L'ID de backup est généré à partir de l'ordre chronologique, le plus récent étant l'ID 0."
  echo -e "  - Utilisez ${YELLOW}list_backups${NC} pour afficher les IDs avant d'effectuer une restauration ou suppression."
}

# Analyse des arguments
case "$1" in
  -b|--backup)
    if [ -n "$2" ]; then
      create_backup "$2"
    else
      usage
    fi
    ;;
  -rb|--restore)
    if [ -n "$2" ] && [ -n "$3" ]; then
      restore_backup "$2" "$3"
    else
      usage
    fi
    ;;
  -lb|--list_backups)
    if [ -n "$2" ]; then
      list_backups "$2"
    else
      usage
    fi
    ;;
  -db|--delete_backup)
    if [ -n "$2" ]; then
      delete_backups "$2" "$3"
    else
      usage
    fi
    ;;
  *)
    usage
    ;;
esac
