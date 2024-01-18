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
