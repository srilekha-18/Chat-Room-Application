import socket
import threading

clients = []

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"[{addr}] {message.decode('utf-8')}")
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            print(f"[DISCONNECTED] {addr} left.")
            break

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"[SERVER STARTED] Listening on {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    host = '127.0.0.1'  # Localhost
    port = 5556
    start_server(host, port)
