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