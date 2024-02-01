import pika

def correction(ch, method, properties, body):
    # doing nothing
    pass

def validation(ch, method, properties, body):
    pass

def confirmation(ch, method, properties, body):
    pass

# task 1
# 1- Using Pika's syntax, declare the necessary queues/exchanges and their connections as shown in Figure 1
if __name__ == '__main__':
    try:
        credentials = pika.PlainCredentials("guest", "guest")
        connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", 5672, "/", credentials))
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange='Assignment', exchange_type='direct')

        # Declare the queues
        channel.queue_declare(queue="Correction queue")
        channel.queue_declare(queue="Validation queue")
        channel.queue_declare(queue="Result queue")

        # Bind the queues to the exchange with routing keys
        channel.queue_bind(exchange='Assignment', queue='Correction queue', routing_key='correction')
        channel.queue_bind(exchange='Assignment', queue='Validation queue', routing_key='validation')
        channel.queue_bind(exchange='Assignment', queue='Result queue', routing_key='confirmation')

        '''task2 
        2-demonstrator subscribing to correction queue'''
        channel.basic_consume(queue='Correction queue', on_message_callback=correction, auto_ack=False)
        #TAs can listen to validation queue
        channel.basic_consume(queue='Validation queue', on_message_callback=validation, auto_ack=False)
        #Module coordinator can listen to result queue for confirmation
        channel.basic_consume(queue='Result queue', on_message_callback=confirmation, auto_ack=False)
        print(' [*] Waiting for messages. To exit press CTRL+C')
    except KeyboardInterrupt:
        print("Exiting")
