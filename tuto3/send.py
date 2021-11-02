#!/usr/bin/env python
import pika
import sys

message = ' '.join(sys.argv[1:]) or "Chile"

#Conexión al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Creación de la cola
channel.queue_declare(queue='wiki')

#Publicación del mensaje
channel.basic_publish(exchange='',
                      routing_key='wiki',
                      body=message)

print(" [x] search %r in wikipedia"%message)

connection.close()

