""" Створення моделей. """

from mongoengine import Document, StringField, EmailField, BooleanField

class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    user_password = StringField()
    message_sent = BooleanField(default=False)