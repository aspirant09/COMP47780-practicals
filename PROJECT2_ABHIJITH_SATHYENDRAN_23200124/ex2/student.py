import pika
import json


credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost",5672, "/",credentials))
channel=connection.channel()


def publish():
    assignment= json.dumps({
        'id': 1,
        'title': "testing",
        'status': "submitted"  # Assuming Status is an Enum
    })
    channel.basic_publish(exchange="Assignment",routing_key='',body=assignment)

publish()