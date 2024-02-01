import pika
import teaching_assistant
import demonstrator_cc
import demonstrator_dm
import module_coordinator
import time

def cloud_computing(ch, method, properties, body):
    demonstrator_cc.cc(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def data_mining(ch, method, properties, body):
    demonstrator_dm.dm(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def validation(ch, method, properties, body): 
    teaching_assistant.validate(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def confirmation(ch, method, properties, body):
    module_coordinator.confirmation(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# task 1
# 1- Using Pika's syntax, declare the necessary queues/exchanges and their connections as shown in Figure 1
if __name__ == '__main__':
    channel = None
    connection = None
    credentials = None
    
    try:
        credentials = pika.PlainCredentials("guest", "guest")
        connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", 5672, "/", credentials))
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange='Assignment', exchange_type='direct')

        # Declare the queues
        channel.queue_declare(queue="Cloud Computing queue")
        channel.queue_declare(queue="Data Mining queue")
        channel.queue_declare(queue="Validation queue")
        channel.queue_declare(queue="Result queue")

        # Bind the queues to the exchange with routing keys
        channel.queue_bind(exchange='Assignment', queue='Cloud Computing queue', routing_key="CC")
        channel.queue_bind(exchange='Assignment', queue='Data Mining queue', routing_key="DM")
        channel.queue_bind(exchange='Assignment', queue='Validation queue', routing_key="validation")
        channel.queue_bind(exchange='Assignment', queue='Result queue',routing_key="confirmation")

        #callback for cloud computing queue
        channel.basic_consume(queue='Cloud Computing queue', on_message_callback=cloud_computing, auto_ack=False)
        #callback for cloud computing queue
        channel.basic_consume(queue='Data Mining queue', on_message_callback=data_mining, auto_ack=False)
        # TAs can listen to validation queue
        channel.basic_consume(queue='Validation queue', on_message_callback=validation, auto_ack=False)
        # Module coordinator can listen to result queue for confirmation
        channel.basic_consume(queue='Result queue', on_message_callback=confirmation, auto_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()  
        connection.close()
        
    except Exception as e:
        print (e)
