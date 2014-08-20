# Deployer

Auto-Scaling Continuous Deployment Helper


 * Easily notify machines that builds are ready to be deployed
 * Configuration for multiple methods to notify your machines
 * Works across auto scaling methodologies


## Configuration

There is a configuration file called deployer.cfg . This file holds all of the keys and endpoints needed for connecting to your system

 * Messaging Queues (RabbitMQ, ZeroMQ, etc...)
 * Amazon SQS
 * Pusher (Websocket)

And here's some code!

```python
[MQSERVER]
endpoint = mq.endpoint.io
queue = deploy
command = echo $PATH

[AWSSQS]
endpoint = mq.endpoint.io
queue = deployer
region = us-west-2
key = AWSKEY
secret = AWSECRET
command = echo $HOME

[PUSHER]
app_id = 00000
key = xxxxxxxxxxxxxxxxxxxxxxxx
secret = xxxxxxxxxxxxxxxxxxxxxxxx
channel = deployer
event = deploy
command = echo $PATH
```

The command key is the important part. You can run any script or bash command. For example:
```bash
source /home/env/myapp/bin/activate && cd /home/apps/myapp/ && fab production >> /var/log/fabric/cron.log 2>&1
```

## How to Run
```bash
$ virtualenv deployer # or use virtualenvwrapper
$ source deployer/bin/activate
$ pip install -r requirements.txt
$ nohup python main.py &> /path/to/log/deployer.out
```

## Running Tests
You need to make a copy of the `src/tests/test_config_example.py` and add correct values for the variables.

```
$ make test
```

This code is very much an __alpha__ version. Please test and integrate properly before you integrate this into your production systems. 

If anyone would like to help out with this project, please feel free to fork it!

### Python Libraries Used

 * [boto](https://github.com/boto/boto) for Amazon SQS
 * [pika](https://github.com/pika/pika) for MQ connection
 * [pusher-client](https://github.com/ekulyk/PythonPusherClient) for Pusher client connection
 * [websocket-client](https://github.com/liris/websocket-client) used by the Pusher client
