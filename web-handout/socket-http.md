# Modul `socket`
 - https://docs.python.org/3/library/socket.html
 - Modul `socket` je základní nástroj pro implementaci síťové komunikace. 
 - Je **nízkoúrovňový** - jsou na něm založeny všechny ostatní moduly Pythonu vyšší úrovně pro propojení v síti.
 - Podporuje většinu běžných protokolů, včetně TCP a UDP.
 - Data nejčastěji odesílány a přijímány jako bloky binárních dat.
	 - Je třeba určit jejich formu.

**Vytváření socketů**:
```python
import socket

socket = socket.socket(
	family=AF_INET,
	type=SOCK_STREAM
)
```

`family` - určuje, jaký protokol na síťové vrstvě bude socket používat.
- **`socket.AF_INET`**: Pro IPv4 adresy. 
- **`socket.AF_INET6`**: Pro IPv6 adresy.
- **`socket.AF_UNIX`**: Unixový socket (pro lokální komunikaci mezi procesy).
- `socket.AF_NETLINK`
`type` - určuje, jaký styl komunikace socket podporuje.
- **`socket.SOCK_STREAM`**:
    - Používá TCP (spolehlivý, orientovaný na připojení, přenos dat jako proud bajtů).
- **`socket.SOCK_DGRAM`**:
    - Používá UDP (nespolehlivý, bez připojení, přenos dat jako jednotlivé pakety).
- **`socket.SOCK_RAW`**:

**Odeslání zprávy**:
```python
s.connect(('localhost', 12345)) # navázání spojení
s.sendall(b'Ahoj!') #odešle všechna data
s.close() # ukončí socket s
```

 >[!note] socket.send a socket.sendall
 > - `sendall` - když se data nevlezou do bufferu automaticky je rozdělí a pošle
 >- `send` - pokud nemůže odeslat všechna data najednou (např. kvůli omezení bufferu), odešle jen část dat -> Ruční řízení odesílání.

**Poslouchání a přijímání dat**:
```python
addr = ('localhost', 12345) # adresa na které posloucháme
s.bind(addr) # přiřadí socket k adrese
s.listen() # umožňuje přijímat příchozí připojení
conn, addr = s.accept() # čeká se na příchozí připojení
print(f'Připojeno: {addr}')
data = conn.recv(1024) #přijme data, max. 1024B
conn.sendall(b'Ahoj!') # pošle odpověď
conn.close() # ukončí socket conn
s.close() # ukončí socket s
```
 - Co když data přesáhnou 1024B?
	 - Přijímací strana tohle nemá šanci zjistit.
	 - Použití ukončovacího znaku, první zpráva nese informaci kolik bytů má přijímací strana čekat....
**Výhody**:
- Přímá kontrola nad socketovou komunikací.
- Flexibilita pro implementaci vlastních protokolů.

**Nevýhody**:
- Vyžaduje znalosti síťových protokolů.
- Implementace složitější logiky (např. HTTPS) je náročnější.

---

# Modul `http`
 - https://docs.python.org/3/library/http.html
- Modul `http` v Pythonu poskytuje nástroje pro práci s protokolem HTTP.
- Je rozdělen na několik podmodulů:
	- `http.client`
	- `http.server`
	- `http.cookies`
	- `http.cookiejar`
	- `http.HTTPStatus`, `http.HTTPMethod`
- Využívá ho mnoho vyšších knihoven, jako je `requests` nebo `flask`.

**Výhody:**
- Vyšší úroveň abstrakce.
- Snazší implementace běžných HTTP funkcionalit.

 **Nevýhody:**
- Omezená flexibilita ve srovnání s nízkoúrovňovou komunikací pomocí `socket`.

## `http.server`
 - Tento modul definuje třídy pro implementaci HTTP serverů.
```python
from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):

	# Definujeme metodu pro zpracování GET požadavků
	def do_GET(self):
		# Odeslání odpovědi s kódem 200 (OK)
		self.send_response(200)
		# Nastavení hlavičky Content-Type pro HTML obsah
		self.send_header("Content-type", "text/html") 
		self.end_headers()
		# Odeslání těla odpovědi – text "Hello, World!"     
		self.wfile.write(b"Hello, World!")  


server = HTTPServer(("localhost", 8000), MyHandler)
print("Server bezi na portu 8000...")
server.serve_forever()
```
 - Dva typy:
	  - `http.server.HTTPServer(args)`
	 - `http.server.ThreadingHTTPServer(args)` identický předchozímu, používá však vlákna ke zpracování požadavků - použití vícenásobné dědičnosti `ThreadingMixIn`
- Argumenty `args`
	- `_server_address_` opět dvojice IP adresa (popř. localhost) a port
	- `_RequestHandlerClass_` - zpracovává příchozí HTTP požadavky (např. GET, POST) a definuje, jak server na tyto požadavky odpoví
		- `BaseHTTPRequestHandler` - Základní třída pro implementaci vlastního chování HTTP serveru.
		- `SimpleHTTPRequestHandler` - Automaticky obsluhuje `GET` a `HEAD` požadavky. Automaticky poskytuje statické soubory z určeného adresáře.
		- `CGIHTTPRequestHandler` - Rozšířená třída, která kromě statických souborů podporuje CGI (Common Gateway Interface) skripty.

---

# Související moduly
 - `socketserver`
	 - Návrh kódu pro tvorbu serverů bývá často podobný - proto je často vhodnější použít tento vysokoúrovňový modul.
	 - Stará se o všechny základní operace a nám už stačí přidat třídy obsluhující požadavky s metodou `handle()`.
	 - Řeší za nás komunikaci tím, že obslouží požadavek každého připojení, ať už sériově nebo předáním každého požadavku jeho vlastnímu samostatnému vláknu, či procesu.
	 - Více na https://docs.python.org/3/library/ssl.html.
 - `asyncore`
	 - Modul pro asynchronní I/O operace se sokety.
	 - Více na https://docs.python.org/3.11/library/asyncore.html.
 - `asynchat`
	 - Tento modul je nadstavbou nad `asyncore`, která usnadňuje práci s protokoly, které se skládají z několika zpráv (např. textové protokoly nebo protokoly, které očekávají více fragmentů dat).
	 - Více na https://docs.python.org/3.11/library/asynchat.html.
 - `ssl`
	 - Modul pro přidání SSL/TLS šifrování do soketové komunikace.
	 - Definuje třídu `ssl.SSLSocket` zděděná z `socket.Socket`.
	 - Více na https://docs.python.org/3/library/ssl.html.
 - `twisted` - komplexní síťový framework třetí strany
	 - Nabízí podporu pro širokou škálu síťových protokolů, jako jsou HTTP, SMTP, POP3, IMAP a další.
	 - Více na www.twistedmatrix.com.