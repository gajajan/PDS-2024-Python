import socket
import threading
import struct
import time
from typing import Tuple


#jednoduchá databáze
database = {1:["Karel", "Novy"], 2:["Marek", "Modry"]}

# Globální proměnná pro kontrolu, zda má server běžet
server_running = True

def print_database():
    print("\n")
    print(f"{'ID':<5} | {'Name':<10} | {'Lastname':<10}")
    print("-" * 31)

    for key, value in database.items():
        print(f"{key:<5} | {value[0]:<10} | {value[1]:<10}")
    print("\n")

# Funkce pro obsluhu každého klienta
def handle_client(client_socket: socket.socket, client_address: Tuple[str,int]) -> None:
    global server_running
    
    try:
        # Přijme 4 byty, které určují velikost dat (formát je "I", což je unsigned int)
        data_length = struct.unpack("I", client_socket.recv(4))[0]  # Očekáváme velikost zprávy jako unsigned int
        print(f"Čekám {data_length} bytů od {client_address}")

        # Přijme požadovaná data (data_length bytů)
        data = client_socket.recv(data_length)
        msg = data.decode('utf-8')
        print(f"Přijato: {msg}")

        # Odeslání odpovědi zpět klientovi
        client_socket.sendall(b"Data prijata!")

        # Zpracování zprávy
        if msg == '!STOP':
            print("Příkaz pro zastavení serveru přijat.")
            server_running = False
        elif msg not in database.items():
            database[len(database)+1] = msg.split(" ",1)

    except Exception as e:
        print(f"Chyba při zpracování klienta {client_address}: {e}")
    finally:
        client_socket.close()

# server
def start_server() -> None:
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    print("Server běží na portu 12345...")
    print_database()

    while server_running:
        try:
            # Zkontrolujeme, zda je nějaký klient připraven na připojení
            client_socket, client_address = server_socket.accept()
            print(f"Připojen klient: {client_address}")

            # Vytvoření vlákna pro obsluhu klienta
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

        except BlockingIOError:
            # Pokud žádný klient není připraven, pokračujeme dál
            pass

        # Zkontrolujeme, zda má server běžet nebo zastavit
        if not server_running:
            print("Server je zastaven.")
            break

        time.sleep(1)  # Na chvili spime

    # Zastavení serveru
    print("Server byl zastaven.")
    server_socket.close()
    print_database()

if __name__ == "__main__":
    start_server()