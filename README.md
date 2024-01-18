# TP
TP Groupe Samy Elandaloussi Diouma Diack

J'ai d'abord créé un script qui liste tous les fichiers de mon système 
'''
import os

def list_all_files(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            print(os.path.join(root, file))

# Lancer la fonction
list_all_files('/')



Puis pour pouvoir savoir le faire j'ai exclu certains fichiers de la liste en l'occurence le dossier /home avec le script suivant : 

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


