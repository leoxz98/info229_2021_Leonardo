#!/usr/bin/env python
import pika, sys, os
import wikipedia

#ejem ejecucion: python3 send.py Bolivia

def main():
       
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    
    channel.queue_declare(queue='wiki')


    def callback(ch, method, properties, body):
        p = body.decode("utf-8")
        #print(p)
        print(" [x] search %r" % p)
        print(wikipedia.summary(p, sentences=3))

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

