import socket
import threading
import sys

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print("[SERVER DISCONNECTED]")
                break
            print(message)
        except:
            print("[ERROR] Connection lost.")
            break

def send_messages(client):
    while True:
        try:
            message = sys.stdin.readline()
            if message:
                client.send(message.encode('utf-8'))
        except:
            print("[ERROR] Sending failed.")
            break

def start_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except:
        print("[ERROR] Unable to connect to server.")
        return

    print("[CONNECTED] You can now start chatting!")

    # Thread to receive messages
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    # Main thread handles sending
    send_messages(client)

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5556
    start_client(host, port)
