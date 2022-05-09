import socket

HOST_IP = "127.0.0.1"
PORT = 32000
MAX_DATA_SIZE= 1024

def socket_receive_all_data(socket_p, data_len):
    current_data_len = 0
    total_data = None
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket_p.recv(MAX_DATA_SIZE)
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
    return total_data

def socket_send_command_and_receive_all_data(socket_p, command):
    if not command:
        return None
    socket_p.sendall(command.encode())

    header = socket_receive_all_data(socket_p, 13)
    longueur_data = int(header.decode())
    data_recues = socket_receive_all_data(socket_p, longueur_data)
    return data_recues

s = socket.socket()
s.bind((HOST_IP, PORT))
s.listen()
#blocage
print(f"Attente de connexion sur {HOST_IP}, port {PORT}...")
connection_socket, client_address = s.accept()
print(f"Connexion établie avec{connection_socket}")

while True:
    infos_data = socket_send_command_and_receive_all_data(connection_socket, "infos")
    if not infos_data:
        break
    commande = input(infos_data.decode() + " >")
    data_recues = socket_send_command_and_receive_all_data(connection_socket, commande)
    if not data_recues:
        break
    print(data_recues.decode())

s.close()