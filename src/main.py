#!/usr/bin/env python
import sys
import os
import ConfigParser
import json
import time
import threading
from distutils.core import setup

import pika
import boto
import pusherclient
from boto.sqs.message import RawMessage

# set defaults
channel = None
global pusher
config = ConfigParser.ConfigParser()


class MQServer(threading.Thread):
    """
    Message Queue Thread Listener (RabbitMQ, ZeroMQ, other MQs)
    """
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # get the items in the config
        endpoint = config.get('MQSERVER', 'endpoint')
        queue = config.get('MQSERVER', 'queue')


        # start the connection to the MQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=endpoint))
        channel = connection.channel()
        channel.basic_consume(self.callback,queue=queue,no_ack=True)
        print '[*] Waiting for queue messages'

        # start the consumer for the channel
        while True:
            channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print "[x] Received %r" % (body,)
        os.system(config.get('MQSERVER', 'command'))

class AmazonSQS(threading.Thread):
    """
    Amazon SQS Thread Listener
    """
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        # start the connection to the SQS endpoint
        sqs = boto.sqs.connect_to_region(config.get('AWSSQS', 'region'), aws_access_key_id=config.get('AWSSQS', 'key'), aws_secret_access_key=config.get('AWSSQS', 'secret'))
        q = sqs.lookup(config.get('AWSSQS', 'queue'))
        q.set_message_class(RawMessage)
        results = sqs.receive_message(q, number_messages=1)

        print '[*] Waiting for Amazon SQS messages'

        # loop and look for messages
        while True:
            # loop through the results
            for result in results:
                # You could set a command to do certain things based upon the config
                print str(result.get_body())

                # execute your command from the config
                os.system(config.get('AWSSQS', 'command'))

            # re-get the messages
            results = sqs.receive_message(q, number_messages=1)
            time.sleep(30) # at 30 seconds, it's guaranteed to get it at least once

class PusherWebSocket(threading.Thread):
    """
    Pusher websocket Thread Listener
    """
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # get the items in the config
        key = config.get('PUSHER', 'key')
        secret = config.get('PUSHER', 'secret')
        app_id = config.get('PUSHER', 'app_id')

        # start the connection to the Pusher client
        pusher = pusherclient.Pusher(key, secret=secret)
        pusher.connection.bind('pusher:connection_established', self.connect_handler)

        print '[*] Waiting for Pusher messages'

        while True:
            time.sleep(1)


    def connect_handler(self, data):
        channel = pusher.subscribe(config.get('PUSHER', 'channel'))
        channel.bind(config.get('PUSHER', 'event'), self.channel_callback)
        print '[-] Connected to Pusher'

    def channel_callback(self, data):
        # execute your command from the config
        os.system(config.get('PUSHER', 'command'))




def main():

    print 'Starting listeners...To exit press CTRL+C'

    # create a list of threads
    threads = []

    # open the config file
    config.readfp(open('deployer.cfg'))

    mq = MQServer()
    sqs = AmazonSQS()
    p = PusherWebSocket()

    try:

        if len(config.get('MQSERVER', 'endpoint')) > 1:
            mq.daemon = True  # daemonize the thread
            threads.append(mq)  # append the threads to the thread list
            mq.start() # start the thread

        if len(config.get('AWSSQS', 'key')) > 1:
            sqs.daemon = True  # daemonize the thread
            threads.append(sqs)  # append the threads to the thread list
            sqs.start() # start the thread

        if len(config.get('PUSHER', 'key')) > 1:
            p.daemon = True  # daemonize the thread
            threads.append(p)  # append the threads to the thread list
            p.start() # start the thread

        for thread in threads:
            # check to see the thread is still alive
            while thread.isAlive():
                thread.join(1)

    except (KeyboardInterrupt, SystemExit):
        print '\n!Received keyboard interrupt, quitting threads.\n'

if __name__ == '__main__':
    main()
