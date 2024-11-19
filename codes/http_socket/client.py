import socket
import struct
import time
import pickle  # Import pickle pro serializaci dat

SERVER_ADR = ('localhost', 12345)

def start_client(message):
    # Vytvoření socketu pro připojení k serveru
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADR)

    try:
        # Serializace zprávy pomocí pickle
        serialized_message = pickle.dumps(message)

        # Odeslání délky zprávy (v tomto případě je to délka ve formátu unsigned int)
        message_length = len(serialized_message)
        client_socket.sendall(struct.pack("I", message_length))  # Odeslání délky jako unsigned int (4 byty)

        # Odeslání samotné zprávy
        client_socket.sendall(serialized_message)

        # Přijmeme odpověď od serveru
        response_length = struct.unpack("I", client_socket.recv(4))[0]  # Nejprve přijmeme délku odpovědi
        response = pickle.loads(client_socket.recv(response_length))  # Poté odpověď samotnou
        print(f"Server odpověděl: {response}")

    except Exception as e:
        print(f"Chyba při komunikaci: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Zprávy mohou být nyní jakýkoliv Python objekt
    start_client(("Petr", "Novák", 45))  # Posíláme n-tici
    start_client(("Jana", "Nováková",33))  # Posíláme další n-tici
    time.sleep(2)
    start_client("!STOP")  # Posíláme příkaz k zastavení serveru
