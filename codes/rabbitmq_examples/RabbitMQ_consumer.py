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