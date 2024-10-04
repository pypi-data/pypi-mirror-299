import subprocess
import os
import sys
import shutil
import argparse

def run_command(command, shell=False):
    """Exécute une commande système."""
    print(f"Exécution de la commande : {' '.join(command) if isinstance(command, list) else command}")
    result = subprocess.run(command, shell=shell, check=True)
    return result

def clone_git_repo(username, password):
    """Clone le dépôt Git via HTTPS."""
    repo_url = f"https://{username}:{password}@github.com/Keksls/Slyvek_Server.git" 
    clone_dir = "/root/SlyvekVps"
    if not os.path.exists(clone_dir):
        print("Clonage du dépôt Git...")
        run_command(['git', 'clone', repo_url, clone_dir])
    else:
        print(f"Le répertoire {clone_dir} existe déjà. Le dépôt n'a pas été cloné.")

def create_directories():
    """Crée les dossiers requis."""
    directories = [
        "/root/SlyvekBackup/",
        "/root/Slyvek/Slyvek_GameServers/",
        "/root/Slyvek/Slyvek_LoginServer/",
        "/root/SlyvekVps/SlyvekApi/uploads",
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Dossier créé ou déjà existant : {directory}")
    
    with open('/root/SlyvekVps/SlyvekApi/api_key.txt', 'w') as file:
        print('api_key.txt créé.')
        pass

def generate_secret_key():
    """Génère une clé secrète pour JWT."""
    print("Génération de la clé secrète...")
    result = subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=subprocess.PIPE, check=True)
    secret_key = result.stdout.decode().strip()
    print(f'Clé secrète générée avec succès : {secret_key}')
    return secret_key

def get_api_key(api_key):
    try:
        print("Génération de la clé API...")
        command = ['python3', '/root/SlyvekVps/SlyvekApi/services/generate_key.py', '--api-key', api_key]

        result = subprocess.run(command, check=True, text=True, capture_output=True)

        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite lors de la génération de la clé API : {e}")
        print(e.output)

def setup_aliases_and_environment(secret_key, api_key):
    """Ajoute les alias et les variables d'environnement nécessaires."""
    bashrc_path = os.path.expanduser('~/.bashrc')
    with open(bashrc_path, 'a') as f:
        f.write("\n# Aliases ajoutés par Slyvek Setup\n")
        f.write("alias slyvek='/root/SlyvekVps/Scripts/slyvek.sh'\n")
        f.write("alias backup='/root/SlyvekVps/Scripts/backup.sh'\n")
        f.write(f"export SECRET_KEY={secret_key}\n")
        f.write(f"export API_KEY={api_key}\n")
    print(f"Les alias et variables d'environnement ont été ajoutés à {bashrc_path}.")

def generate_ssl_certificate(domain, email):
    """Génère un certificat SSL avec Certbot."""
    print("Génération du certificat SSL avec Certbot...")
    try:
        # Installer Certbot s'il n'est pas déjà installé
        run_command(['sudo', 'apt', 'install', '-y', 'certbot', 'python3-certbot-nginx'])
        # Générer le certificat SSL
        run_command(['sudo', 'certbot', '--nginx', '-d', domain, '-m', email, '--agree-tos', '-n'])
        print("Certificat SSL généré avec succès.")

        # Obtenez le chemin absolu du répertoire contenant ce script
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Chemin relatif vers le fichier de configuration Nginx
        source_conf = os.path.join(base_path, 'templates', 'nginx-backup.conf')
        dest_conf = '/etc/nginx/sites-available/default'

        # Copier le fichier de configuration
        shutil.copyfile(source_conf, dest_conf)
        print(f"Fichier de configuration Nginx copié de {source_conf} vers {dest_conf}.")

        # Tester et redémarrer Nginx
        try:
            run_command(['sudo', 'nginx', '-t'])
            run_command(['sudo', 'systemctl', 'restart', 'nginx'])
            print("Nginx configuré et redémarré avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du test ou du redémarrage de Nginx : {e}")
    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite lors de la génération du certificat SSL : {e}")
        sys.exit(1)

def install_system_packages():
    """Installe les paquets système requis."""
    packages = [
        'python3',
        'python3-pip',
        'python3-venv',
        'unzip',
        'mono-complete',
        'nginx',
        'git', 
        'openssl' 
    ]
    print("Mise à jour des paquets système...")
    run_command(['sudo', 'apt', 'update'])
    print("Installation des paquets système requis...")
    run_command(['sudo', 'apt', 'install', '-y'] + packages)

def setup_python_environment():
    """Configure l'environnement virtuel Python et installe les dépendances."""
    venv_path = '/root/SlyvekVps/SlyvekApi/venv'
    requirements_file = '/root/SlyvekVps/SlyvekApi/requirements.txt'
    pip_executable = os.path.join(venv_path, 'bin', 'pip')

    if not os.path.exists(venv_path):
        print("Création de l'environnement virtuel Python...")
        run_command(['python3', '-m', 'venv', venv_path])

    print("Activation de l'environnement virtuel et installation des dépendances...")
    run_command([pip_executable, 'install', '-r', requirements_file])

    print("Environnement Python configuré avec succès.")

def configure_nginx():
    """Configure Nginx avec les fichiers fournis."""
    print("Configuration de Nginx...")

    # Ajouter la configuration de limitation de connexion dans le bloc 'http' de nginx.conf
    nginx_conf = '/etc/nginx/nginx.conf'
    limit_conn_config = '       # Limitation des connexions\n       limit_conn_zone $binary_remote_addr zone=addr:10m;\n'

    # Lire le fichier nginx.conf
    with open(nginx_conf, 'r') as f:
        lines = f.readlines()

    # Trouver le début du bloc 'http {'
    for index, line in enumerate(lines):
        if 'http {' in line:
            # Trouver l'index de la ligne suivante
            insert_index = index + 1
            # Insérer la configuration après l'ouverture du bloc http
            lines.insert(insert_index, limit_conn_config)
            break
    else:
        print("Bloc 'http {' non trouvé dans nginx.conf. Impossible d'ajouter la configuration.")
        sys.exit(1)

    # Écrire les modifications dans nginx.conf
    with open(nginx_conf, 'w') as f:
        f.writelines(lines)

    print("Configuration de limitation de connexion ajoutée au bloc 'http' dans nginx.conf.")

    # Tester et redémarrer Nginx
    try:
        run_command(['sudo', 'nginx', '-t'])
        run_command(['sudo', 'systemctl', 'restart', 'nginx'])
        print("Nginx configuré et redémarré avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du test ou du redémarrage de Nginx : {e}")

def main():
    # Vérifier si le script est exécuté en tant que root
    if os.geteuid() != 0:
        print("Ce script doit être exécuté en tant que root. Veuillez réessayer avec 'sudo'.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Script de configuration du VPS avec Slyvek")
    parser.add_argument('--api-key', required=True, help='Clé API pour l\'application')
    parser.add_argument('--email', required=True, help='Adresse e-mail pour le certificat SSL')
    parser.add_argument('--domain', required=True, help='Nom de domaine pour le certificat SSL')
    parser.add_argument('--username', required=True, help='Nom d\'utilisateur pour le dépôt Git')
    parser.add_argument('--password', required=True, help='Mot de passe pour le dépôt Git')

    args = parser.parse_args()

    try:
        install_system_packages()
        clone_git_repo(args.username, args.password)
        create_directories()
        secret_key = generate_secret_key()
        get_api_key(args.api_key)
        setup_aliases_and_environment(secret_key, args.api_key)
        setup_python_environment()
        configure_nginx()
        generate_ssl_certificate(args.domain, args.email)
        print("Configuration complète du serveur terminée avec succès.")

        # Indiquer à l'utilisateur qu'il doit redémarrer son shell ou exécuter 'source ~/.bashrc'
        print("Veuillez exécuter 'source ~/.bashrc' ou redémarrer votre shell pour appliquer les changements.")

    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite lors de l'exécution : {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
