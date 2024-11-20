---
title: Práce s RabbitMQ
---

## Co je RabbitMQ?
RabbitMQ je message broker implementující protokol AMQP (Advanced Message Queuing Protocol). Umožňuje komunikaci mezi aplikacemi nebo jejich komponentami. RabbitMQ umožňuje oddělení producentů a konzumentů, což podporuje asynchronní komunikaci.

### Hlavní pojmy
- **Message Broker**: Implementuje systém front zpráv.
- **Exchanges** (výměníky): Komponenty odpovědné za směrování zpráv do správných front.
- **Binding**: Spojení mezi výměníkem a frontou, identifikován pomocí **binding key**.
- **Routing key**: Identifikace jednotlivých zpráv.

### Příklad: Posílání zprávy (producent)
```python
import pika

# Navázání spojení s RabbitMQ serverem
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Deklarace fronty
channel.queue_declare(queue='hello')

# Odeslání zprávy
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello, RabbitMQ!')

print(" [x] Zpráva 'Hello, RabbitMQ!' byla odeslána.")

# Uzavření spojení
connection.close()
```

### Příklad: Příjem zprávy (konzument)
```python
import pika

def callback(ch, method, properties, body):
    print(f" [x] Přijatá zpráva: {body}")

# Navázání spojení s RabbitMQ serverem
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Deklarace fronty
channel.queue_declare(queue='hello')

# Přihlášení ke zprávám z fronty
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Čekám na zprávy. Pro ukončení stiskněte CTRL+C')
channel.start_consuming()
```
## Výhody RabbitMQ
Mezi hlavní výhody RabbitMQ patří:
- **Oddělení** (decoupling): Producenti nemusí čekat na zpracování zpráv, což umožňuje asynchronní provádění úloh.
- **Škálování**: RabbitMQ usnadňuje přidávání nových producentů nebo konzumentů, což podporuje horizontální škálování.
- **Výkon**: Broker může běžet na samostatném zařízení, což zlepšuje výkon.

## Typy výměníků (Exchanges)
Výměníky definují, jakým způsobem jsou zprávy směrovány do front:
- **Direct**: Směřuje zprávy do konkrétní fronty na základě **kompletní** shody **binding key** a **routing key**.
- **Fanout**: Rozesílá všechny zprávy do všech front napojených na výměník.
- **Topic**: Směruje zprávy do front na základě **částečné** shody mezi **binding key** a **routing key** (pattern matching).
- **Header**: Směruje zprávy podle hodnot v hlavičkách zpráv.

### Příklad: Implementace Fanout Exchange
```python
import pika

# Navázání spojení s RabbitMQ serverem
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Deklarace výměníku typu fanout
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Deklarace fronty
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# Přiřazení fronty k výměníku
channel.queue_bind(exchange='logs', queue=queue_name)

# Callback pro zpracování přijatých zpráv
def callback(ch, method, properties, body):
    print(f" [x] Přijatý log: {body}")

# Přihlášení ke zprávám
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Čekám na logy. Pro ukončení stiskněte CTRL+C')
channel.start_consuming()
```

## Funkce a vlastnosti
- **Spolehlivost**: Možnost zajištění, že se zprávy neztratí ani při výpadcích.
- **Flexibilita**: Podpora více protokolů, například AMQP, MQTT nebo STOMP.
- **Škálovatelnost**: Jednoduché přidávání producentů, konzumentů nebo zvýšení výkonu systému.
- **Pluggability**: Možnost snadného rozšíření funkcionality pomocí pluginů.
- 
### Příklad: Spolehlivost zpráv
```python
import pika

# Navázání spojení s RabbitMQ serverem
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Deklarace fronty s povolením trvalosti (durable)
channel.queue_declare(queue='task_queue', durable=True)

# Publikování zprávy s potvrzením
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body='Úkol 1',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # Zpráva je trvalá
                      ))

print(" [x] Zpráva 'Úkol 1' byla odeslána.")

# Uzavření spojení
connection.close()
```

## Využití RabbitMQ
RabbitMQ nachází využití v různých scénářích:
- **Asynchronní zpracování úloh**: Oddělení umožňuje producentům odesílat úlohy bez čekání na jejich dokončení, což dovoluje zpracovávání úloh, které jsou časově náročné nebo nevyžadují okamžité zpracování.
- **Load balancing**: Rozložení zátěže mezi více konzumentů.
- **Zpracování dat v reálném čase**: Užitečné pro monitoring, logování a další.
 ### Příklad: Zpracování logů v reálném čase
```python
import pika

# Navázání spojení s RabbitMQ serverem
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Deklarace výměníku typu fanout pro logy
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Deklarace fronty pro příjem logů
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# Přiřazení fronty k výměníku
channel.queue_bind(exchange='logs', queue=queue_name)

# Callback pro zpracování logů
def callback(ch, method, properties, body):
    print(f" [x] Přijatý log: {body}")

# Přihlášení ke zprávám
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Čekám na logy. Pro ukončení stiskněte CTRL+C')
channel.start_consuming()
```

