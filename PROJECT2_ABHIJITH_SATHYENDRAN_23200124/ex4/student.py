import pika
import json
import logging
import sys


credentials =None
channel= None
credentials=None


def publish():
    assignment= json.dumps({
        'id': 1,
        'title': "CC",
        'status': "submitted"  # Assuming Status is an Enum
    })
    channel.basic_publish(exchange="Assignment",routing_key='CC',body=assignment)
    assignment= json.dumps({
        'id': 2,
        'title': "DM",
        'status': "submitted"  # Assuming Status is an Enum
    })
    channel.basic_publish(exchange="Assignment",routing_key='DM',body=assignment)



if __name__=='__main__':
    try:
        credentials = pika.PlainCredentials("guest","guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq",5672, "/",credentials))
        channel=connection.channel()
        channel.exchange_declare(exchange='Assignment', exchange_type='direct')

        # Declare the queues
        channel.queue_declare(queue="Cloud Computing queue")
        channel.queue_declare(queue="Data Mining queue")
        channel.queue_bind(exchange='Assignment', queue='Cloud Computing queue', routing_key="CC")
        channel.queue_bind(exchange='Assignment', queue='Data Mining queue', routing_key="DM")
        
        # channel.start_consuming()  
        
        print("STUDENT ABOUT TO PUBLISH!!",file=sys.stderr)
        sys.stdout.flush()
        publish()
        sys.stdout.flush()
        connection.close()
    except Exception as e:
        logging.info("fuck it")
        print(e)