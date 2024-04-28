# Подключаем необходимые модули
from faker import Faker
from mongoengine import connect
import pika
from models import Contact
import json

# Открываем файлы с паролями
with open('password.txt', 'r') as file_pass:
    password = file_pass.read()
    
with open('password_from_CloudAMQP.txt', 'r') as file_pass_cloudamqp:
    password_from_CloudAMQP = file_pass_cloudamqp.read()

# Формируем URL для подключения к MongoDB и RabbitMQ
URL = f'mongodb+srv://tapxyh1445:{password}@nosqlbase.zekqidk.mongodb.net/'
URL_FOR_CLOUDAMQP = f'amqps://fbvnpspi:{password_from_CloudAMQP}@sparrow.rmq.cloudamqp.com/fbvnpspi'

# Подключаемся к MongoDB
connect(host=URL)

# Подключаемся к RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(URL_FOR_CLOUDAMQP))
channel = connection.channel()
channel.queue_declare(queue='contact_id')

# Генерируем контакты 
def generate_contacts():
    fake = Faker()
    for _ in range(50):
        author = Contact(
            full_name=fake.name(),
            email=fake.email(),
            user_password=fake.password(),
            message_sent=False
        )
        author.save()
        # Отправляем сообщение с ObjectID в очередь RabbitMQ
        message = {'contact_id': str(author.id)}  # Преобразуем ObjectID в строку для JSON
        channel.basic_publish(exchange='', routing_key='contact_id', body=json.dumps(message))
    print('Контакти створені та відправлені до RebbitMQ')
generate_contacts()
