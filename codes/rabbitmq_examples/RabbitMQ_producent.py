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