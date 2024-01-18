import os

def list_all_files_exclude_home(start_path):
    for root, dirs, files in os.walk(start_path):
        # Ignorer le répertoire /home et ses sous-dossiers
        if '/home' in root:
            continue

        for file in files:
            print(os.path.join(root, file))

# Lancer la fonction
list_all_files_exclude_home('/')
