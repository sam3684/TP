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
