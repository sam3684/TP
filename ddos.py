import socket
import threading
import time

def send_requests(target_ip, target_port, duration):
    timeout = time.time() + duration
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while time.time() < timeout:
        try:
            client.sendto(b"Request Data", (target_ip, target_port))
        except Exception as e:
            print(f"Erreur lors de l'envoi de la requête : {e}")
        time.sleep(0.01)  # Pour éviter une utilisation excessive des ressources

    client.close()

# Paramètres de la simulation
target_ip = "192.168.146.139"  # IP de la machine cible 
target_port = 80  # Port cible
duration = 60  # Durée de la simulation en secondes

# Démarrage de la simulation
thread = threading.Thread(target=send_requests, args=(target_ip, target_port, duration))
thread.start()
