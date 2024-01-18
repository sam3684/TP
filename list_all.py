import os

def list_all_files(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            print(os.path.join(root, file))

# Lancer la fonction
list_all_files('/')
