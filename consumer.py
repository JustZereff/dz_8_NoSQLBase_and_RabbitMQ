import pika
import json
from models import Contact
from producer import URL_FOR_CLOUDAMQP

# Подключаемся к RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(URL_FOR_CLOUDAMQP))
channel = connection.channel()
channel.queue_declare(queue='contact_id')

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')
    
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()
        print(f'message_sent змінено на True у {contact.full_name}')
    else:
        print('Контактів не знайдено.')

channel.basic_consume(queue='contact_id', on_message_callback=callback, auto_ack=True)

channel.start_consuming()