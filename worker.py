import pika
import sys
import time
import subprocess
class request:
    idc = 1
    text=""

def on_request(ch, method, properties, body):
	req = request()
	req.ParseFromString(body)
	client_id = req.idc
	content = req.text.encode()
	echo_pr = subprocess.Popen(['echo', content], stdout = subprocess.PIPE)
	result_pr = subprocess.Popen(['mystem', '-gnid'], stdin = echo_pr.stdout, stdout = subprocess.PIPE)
	result = result_pr.communicate()[0]
	channel.basic_publish(exchange = 'response', routing_key = client_id, body = result)

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.exchange_declare(exchange = 'request', type = 'direct')
request_queue = channel.queue_declare(queue = 'request_queue')
channel.queue_bind(exchange = 'request', queue = 'request_queue', routing_key = '')
channel.exchange_declare(exchange = 'response', type = 'direct')
channel.basic_consume(on_request, queue = 'request_queue')
channel.start_consuming()
