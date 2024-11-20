---
title: Komunikace pomocí soketů a HTTP
---

# Modul `socket`
 - https://docs.python.org/3/library/socket.html
 - Modul `socket` je základní nástroj pro implementaci síťové komunikace. 
 - Je **nízkoúrovňový** - jsou na něm založeny všechny ostatní moduly Pythonu vyšší úrovně pro propojení v síti.
 - Podporuje většinu běžných protokolů, včetně TCP a UDP.
 - Data nejčastěji odesílány a přijímány jako bloky binárních dat.
	 - Je třeba určit jejich formu.
	 - Nabízí se modul `pickle` - jedná se o modul v Pythonu, který  umožňuje převádět objekty do binárního formátu (serializace) a zpět (deserializace), což je užitečné pro ukládání dat nebo jejich přenos po síti.

## Vytváření socketů:
```python
import socket

socket = socket.socket(
	family=AF_INET,
	type=SOCK_STREAM
)
```

Při vytváření socketů specifikujeme protokoly, které bude socket používat. Dva základní parametry: `family` a `type`.

`family` - určuje, jaký protokol na síťové vrstvě bude socket používat.
- `socket.AF_INET`: Pro IPv4 adresy. 
- `socket.AF_INET6`: Pro IPv6 adresy.
- `socket.AF_UNIX`: Unixový socket (pro lokální komunikaci mezi procesy).
- `socket.AF_NETLINK`

`type` - určuje, jaký styl komunikace socket podporuje.
- `socket.SOCK_STREAM`:
    - Používá TCP (spolehlivý, orientovaný na připojení, přenos dat jako proud bajtů).
- `socket.SOCK_DGRAM`:
    - Používá UDP (nespolehlivý, bez připojení, přenos dat jako jednotlivé pakety).
- `socket.SOCK_RAW`

 >[!note] Výchozí hodnoty
 >Výchozí hodnota při vytváření socketu pro parametr `family` je `socket.AF_INET` a pro parametr `type` `socket.SOCK_STREAM`. 

## Odeslání zprávy:
```python
s.connect(('localhost', 12345)) # navázání spojení
s.sendall(b'Ahoj!') #odešle všechna data
s.close() # ukončí socket s
```

 Při odesílání zprávy musíme znát adresu příjemce. Ta je určena dvojicí `(host, port)`:
  - `host` je adresa příjemce na síťové vrstvě - ta je daná podle zvolené `family`
	 - Pro simulaci na lokálním počítači lze využít `localhost`
 - `port` je to číslo v rozsahu 1–65535, které specifikuje konkrétní aplikaci nebo službu na zařízení příjemce.
 
 Následně data pošleme pomocí `socket.send()`, nebo `socket.sendall()`
  - `sendall` - když se data nevlezou do bufferu, automaticky je rozdělí a pošle
  - `send` - pokud nemůže odeslat všechna data najednou (např. kvůli omezení bufferu), odešle jen část dat -> Ruční řízení odesílání.

## Poslouchání a přijímání dat:
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
 Pro příjem zpráv je nutné přiřadit socketu adresu, na kterou můžou odesílatelé zasílat zprávy. Toho dosáhneme pomocí příkazu `socket.bind(addr)`. Následně socket přepneme do tzv. poslouchacího módu pomocí `socket.listen()`. Pak můžeme čekat než obdržíme zprávu přes `socket.accept()`. `socket.accept()` po obdržení dat vrátí socket `conn` určený pro komunikaci s odesílatelem a adresu odesílatele `addr`. Samotnou zprávu pak dostaneme zadáním `socket.recv(buffer_size)`. Parametr `buffer_size` udává maximální počet bajtů, které se mají přečíst při jednom volání metody.
 - Co když data přesáhnou 1024B?
	 - Přijímací strana tohle nemá šanci zjistit.
	 - Řešení: Použití ukončovacího znaku, první zpráva nese informaci kolik bytů má přijímací strana čekat....
## Výhody:
- Přímá kontrola nad socketovou komunikací.
- Flexibilita pro implementaci vlastních protokolů.
## Nevýhody:
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
		pass

server = HTTPServer(("localhost", 8000), MyHandler)
print("Server bezi na portu 8000...")
server.serve_forever()
```
 Dva typy:
- `http.server.HTTPServer(args)`
 - `http.server.ThreadingHTTPServer(args)` identický předchozímu, používá však vlákna ke zpracování požadavků - použití vícenásobné dědičnosti `ThreadingMixIn`
Argumenty `args`
- `_server_address_` opět dvojice `host` a `port`
- `_RequestHandlerClass_` - zpracovává příchozí HTTP požadavky (např. GET, POST) a definuje, jak server na tyto požadavky odpoví
	- `BaseHTTPRequestHandler` - Základní třída pro implementaci vlastního chování HTTP serveru.
	- `SimpleHTTPRequestHandler` - Automaticky obsluhuje `GET` a `HEAD` požadavky. Automaticky poskytuje statické soubory z určeného adresáře.
	- `CGIHTTPRequestHandler` - Rozšířená třída, která kromě statických souborů podporuje CGI (Common Gateway Interface) skripty.
Metoda `serve_forever()` spustí server, aby neustále naslouchal na příchozí HTTP požadavky a obsluhoval je. Tento proces běží, dokud server není ukončen.

## Ukázka metody pro zpracování GET

```python
def do_GET(self):
	# Odeslání odpovědi s kódem 200 (OK)
	self.send_response(200)
	# Nastavení hlavičky Content-Type pro HTML obsah
	self.send_header("Content-type", "text/html") 
	self.end_headers()
	# Odeslání těla odpovědi – text "Hello, World!"     
	self.wfile.write(b"Hello, World!") 
```

Pomocí metody `send_response(status_code)` server pošle stavový kód, který signalizuje výsledek požadavku.
Metoda `send_header(key, value)`:
 - `key`: Klíč hlavičky (string) – specifikuje název hlavičky.
 - `value`: Hodnota hlavičky (string) – obsah hlavičky.
Pro nastavení více hlaviček stačí `send_header` zavolat vícekrát před zavoláním `end_headers()`. Které specifikaci hlaviček ukončí.

Pro odesílání těla HTTP odpovědi se zavolá `wfile.write(content)`. Tato metoda vyžaduje binární data. Lze opět poslat více než jedno tělo zprávy opakovaným zasláním této metody.
  
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