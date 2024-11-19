from http.server import HTTPServer, BaseHTTPRequestHandler


# Jednoduchá databáze
database = {1: ["Karel", "Novy"], 2: ["Marek", "Modry"]}

def print_database() -> None:
    print("\n")
    print(f"{'ID':<5} | {'Name':<10} | {'Lastname':<10}")
    print("-" * 31)

    for key, value in database.items():
        print(f"{key:<5} | {value[0]:<10} | {value[1]:<10}")
    print("\n")

# Vlastní třída pro zpracování HTTP požadavků
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Zpracování požadavků na zobrazení databáze
        self.wfile.write(b"<h1>Database:</h1>")
        self.wfile.write(b"<table border='1'><tr><th>ID</th><th>Name</th><th>Lastname</th></tr>")
        for key, value in database.items():
            self.wfile.write(f"<tr><td>{key}</td><td>{value[0]}</td><td>{value[1]}</td></tr>".encode('utf-8'))
        self.wfile.write(b"</table>")

    def do_POST(self) -> None:

        # Získání délky těla požadavku (velikost dat)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Decoding a zpracování přijatých dat
        msg = post_data.decode('utf-8')
        print(f"Přijato: {msg}")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        #pro jednoduchost predpokladame ze zprava ma spravny format
        if msg not in [f"{value[0]} {value[1]}" for value in database.values()]:
                new_id = len(database) + 1
                first_name, last_name = msg.split(" ", 1)
                database[new_id] = [first_name, last_name]
                self.wfile.write(b"Data byla ulozena.")
        else:
            self.wfile.write(b"Jmeno je jiz v databazi.")

# Funkce pro spuštění serveru
def start_server():
    global server_running
    
    # Tisk databáze
    print_database()

    # Vytvoření HTTP serveru na localhostu a portu 8080
    server = HTTPServer(('localhost', 8080), MyHandler)
    print("Server běží na portu 8080...")
    server.serve_forever()

# Spuštění serveru
if __name__ == "__main__":
    start_server()