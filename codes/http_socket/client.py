import socket
import struct
import time


SERVER_ADR = ('localhost', 12345)

def start_client(message:str):
    # Vytvoření socketu pro připojení k serveru
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADR)

    try:
        
        # Odeslání délky zprávy (v tomto případě je to délka ve formátu unsigned int)
        message_length = len(message)
        client_socket.sendall(struct.pack("I", message_length))  # Odeslání délky jako unsigned int (4 byty)

        # Odeslání samotné zprávy
        client_socket.sendall(message.encode('utf-8'))

        # Přijmeme odpověď od serveru
        response = client_socket.recv(1024)  # Předpokládáme, že odpověď bude do 1024 bytů
        print(f"Server odpověděl: {response.decode('utf-8')}")

    except Exception as e:
        print(f"Chyba při komunikaci: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client("Petr Novak")
    start_client("Jana Novakova")
    time.sleep(2)
    start_client("!STOP")