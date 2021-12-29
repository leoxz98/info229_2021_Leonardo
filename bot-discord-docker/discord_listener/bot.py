import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import threading
import pika


############ CONEXION RABBITMQ ##############
#
HOST = os.environ['RABBITMQ_HOST']
#HOST = 'localhost'
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channelMQ = connection.channel()

#Creamos el exchange 'cartero' de tipo 'fanout'
channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)



#############################################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    for channel in bot.get_all_channels():
        print(channel)
        print(channel.id)

    channel = bot.get_channel(913706828502814760)
    #await channel.send('¡Hola!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'test':
        response = "rs: "+ message.content+"!"
        await message.channel.send(response)

    await bot.process_commands(message)

@bot.command(name='bored', help='Muestra una actividad ya sea random o por categoria: ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"] ')
async def aburrido(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)

    channelMQ.basic_publish(exchange='cartero', routing_key="donko-bot", body=message)


@bot.command(name='ShowMeDogges', help='muesta un dogge random')
async def aburrido(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)

    channelMQ.basic_publish(exchange='cartero', routing_key="donko-bot", body=message)


@bot.command(name='ShibaInu', help='muesta un dogge shibainu')
async def aburrido(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)

    channelMQ.basic_publish(exchange='cartero', routing_key="donko-bot", body=message)



############ CONSUMER ###############

import threading
import asyncio

def writer(bot):
    """thread worker function"""
    print('Worker')

    HOST = os.environ['RABBITMQ_HOST']
    #HOST = 'localhost'

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channelMQ = connection.channel()

    #Creamos el exchange 'cartero' de tipo 'fanout'
    channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

    #Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
    result = channelMQ.queue_declare(queue="discord_writer", exclusive=True, durable=True)
    queue_name = result.method.queue

    #La cola se asigna a un 'exchange'
    channelMQ.queue_bind(exchange='cartero', queue=queue_name, routing_key="discord_writer")


    print(' [*] Waiting for messages. To exit press CTRL+C')

    async def write(message):
        channel = bot.get_channel(908505071887732768)#913706828502814760
        await channel.send(message)

    def callback(ch, method, properties, body):
        message=body.decode("UTF-8")
        print(message)

        bot.loop.create_task(write(message))

    channelMQ.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channelMQ.start_consuming()

t = threading.Thread(target=writer, args=[bot])
t.start()

########################################
bot.run(TOKEN)