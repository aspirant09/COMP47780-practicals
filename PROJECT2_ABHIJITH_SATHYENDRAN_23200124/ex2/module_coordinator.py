import json
import pika



def confirmation(assignment):
    try:
        #print(assignment)
        credentials = pika.PlainCredentials("guest","guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq",5672, "/",credentials))
        channel=connection.channel()
    
        message_body_string = assignment.decode('utf-8')
        assignment_data = json.loads(message_body_string)
        if assignment_data['status']!='validated':
            #print("Skip processing by Module coordinator")
            return
        assignment_data['status']='confirmed'
        print("Module Coordinator changing status for user "+
            str(assignment_data['id'])+" to "+assignment_data['status'])
        print(assignment_data)
        channel.basic_publish(exchange="Assignment",routing_key='',
                              body=json.dumps(assignment_data))
    except Exception as e:
        print(e)
