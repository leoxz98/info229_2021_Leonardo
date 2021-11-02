#!/usr/bin/env python
import pika, sys, os
import wikipedia
import pageviewapi
import pageviewapi.period

#ejem ejecucion: python3 send.py Bolivia

def main():   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='wiki')


    def callback(ch, method, properties, body):
        p = body.decode("utf-8")
        print(" [x] search %r" % p)
        #print(p)
        nv=pageviewapi.period.avg_last('en.wikipedia',p, last=30)
        print("vistas del mes: ")
        print(nv)
        #aqui

    channel.basic_consume(queue='wiki', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for instructions. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
