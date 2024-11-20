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