import json
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        # BlockingConnection for simple, non-async queue
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    # send a message
    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                    routing_key=self.queue_name,
                                    body=json.dumps(message))
        # print ("[AMQP] message sent to %s:%s" % (self.queue_name, message))

    # get a message
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            # print ("[AMQP] message receieved from %s:%s" % (self.queue_name, body))
            return json.loads(body.decode('utf-8'))
        else:
            print ("[%s] is empty" % self.queue_name)
            return None
    # a safer way to sleep than calling time.sleep()
    def sleep(self, seconds):
        self.connection.sleep(seconds)
