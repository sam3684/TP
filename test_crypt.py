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
