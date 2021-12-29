import os, time
import pika
import json
import requests


########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
#HOST = 'localhost'
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="donko-bot", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="donko-bot")


##########################################################


########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	arguments = body.decode("UTF-8").split(" ")

	if (arguments[0]=="!bored"):
		########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
		

		if arguments[1] == "random":
			api = "https://www.boredapi.com/api/activity"
		else:
			api = f"https://www.boredapi.com/api/activity?type=" + arguments[1]

		response = requests.get(api)
		content = response.json()
		result = content["activity"]
		print("send a new message to rabbitmq: "+result)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

	if (arguments[0]=="!ShowMeDogges"):
		api = "https://dog.ceo/api/breeds/image/random"
		response = requests.get(api)
		content = response.json()
		doggo = content["message"]
		print("send a new message to rabbitmq: "+ doggo)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=doggo)

	if (arguments[0]=="!ShibaInu"):
		api = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true"
		response = requests.get(api)
		content = response.json()
		shiba = content[0]
		print("send a new message to rabbitmq: "+ shiba)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=shiba)




channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()



#######################