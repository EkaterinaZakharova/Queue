import pika
import uuid
import sys
class request:
    idc=1
    text=""

def on_response(ch, methon, properties, body):
	print(body)
	channel.close()

req = request()
client_id = str(uuid.uuid1())
req.idc = client_id
filename = input("enter filename")
f = open(filename, "r")
req.text = f.read()

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.exchange_declare(exchange = 'request', type = 'direct')
channel.basic_publish(exchange = 'request', routing_key = '', body = str(req))
connection.close()
connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.exchange_declare(exchange = 'response', type = 'direct')
result = channel.queue_declare(exclusive = True)
queue_name = result.method.queue
channel.queue_bind(exchange = 'response', queue = queue_name, routing_key = client_id)
channel.basic_consume(on_response, queue = queue_name)
channel.start_consuming()
