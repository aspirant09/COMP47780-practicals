import pika
import json

def confirmation(ch, method, properties, body):
    try:
        message_body_string = body.decode('utf-8')
        assignment_data = json.loads(message_body_string)
        assignment_data['status']='confirmed'
        print("Module Coordinator changing status for user "+
            str(assignment_data['id'])+" to "+assignment_data['status'])
        print(assignment_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(e)

if __name__=='__main__':
    try:
        credentials = pika.PlainCredentials("guest","guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq",5672, "/",credentials))
        channel=connection.channel()


        channel.exchange_declare(exchange='Assignment', exchange_type='direct')
        channel.queue_declare(queue="Result queue")
        channel.queue_bind(exchange='Assignment', queue='Result queue',routing_key="confirmation")
        channel.basic_consume(queue='Result queue', on_message_callback=confirmation, auto_ack=False)
        channel.start_consuming()  
        connection.close()
    except Exception:
        pass
