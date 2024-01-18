# TP
TP Groupe Samy Elandaloussi Diouma Diack

J'ai d'abord créé un script qui liste tous les fichiers de mon système 
qui se nomme en pièce joint list_all.py


Puis pour pouvoir savoir le faire j'ai exclu certains fichiers de la liste en l'occurence le dossier /home avec le script suivant list_all_exclued_home.py


Mon serveur est sur l'IP 192.168.146.138 , pour faire des tests j'ai créé une autre machine ubuntu cliente sur l'IP 192.168.146.139

J'ai commencé par vouloir chiffrer un fichier spécifique sur ma machine cliente , /home/crypt_socket/sam_decrypted et dans ce cas spécifique j'ai crée deux scripts sockets qui me permettent de chiffrer en rsa le fichier sam et d'envoyer la clef privée qui me servira au déchiffrement ainsi que le fichier déchiffré sur ma machine serveur , voici les deux scripts sockets , d'abord côté serveur test_crypt.py

Ensuite après avoir lancé ce script côté serveur à l'aide de la commande python3 test_crypt.py , je lance côté client le script suivant test2crypt.py , les indications dans le script indique ses actions : 

Voilà j'obtiens bien sur ma machine serveur le fichier sam_decrypted et ma clef  private_key.pem , et le fichier sam sur ma machine cliente est illisible 

Maintenant je vais effectuer la démarche de ne plus chiffrer uniquement un fichier sam mais chiffrer des élèments essentiels à ma machine cliente en l'occurence le dossier /home et le dossier /var , mon script côté serveur se nomme cryptentier.py

Mon script côté client  cryptentier_client.py


J'ai maintenant les dossiers /home et /var entièrement chiffrés avec la clef privée uniquement sur mon serveur : 

Pour pouvoir déchiffrer ma machine et dans l'hypothèse ou je le souhaite je peux transférer à mon client ma clef privée en scp /home/crypt_socket/private_key.pem sam@192.168.146.139:/home/sam
et j'informe mon client d'éxecuter le script suivant decrypt.py : 


Mes données sur ma machine cliente sont entièrement déchiffrées après l'exécution de ce script 

