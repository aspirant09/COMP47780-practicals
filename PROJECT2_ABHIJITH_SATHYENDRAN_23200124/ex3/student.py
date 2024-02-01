import pika
import json


credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost",5672, "/",credentials))
channel=connection.channel()


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

publish()