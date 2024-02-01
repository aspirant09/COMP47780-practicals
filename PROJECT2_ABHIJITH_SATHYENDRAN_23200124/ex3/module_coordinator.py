import json
import pika



def confirmation(assignment):
    try:
        credentials = pika.PlainCredentials("guest","guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq",5672, "/",credentials))
        channel=connection.channel()
    
        message_body_string = assignment.decode('utf-8')
        assignment_data = json.loads(message_body_string)
        assignment_data['status']='confirmed'
        print("Module Coordinator changing status for user "+
            str(assignment_data['id'])+" to "+assignment_data['status'])
        print(assignment_data)
    except Exception as e:
        print(e)
