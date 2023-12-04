import pika


def rabbitmq_producer():
    # Define camera monitoring signal
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", credentials=pika.PlainCredentials("user", "password"))
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

    return channel


def rabbitmq_consumer(binding_key):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", credentials=pika.PlainCredentials("user", "password"))
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")
    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange="topic_logs", queue=queue_name, routing_key=binding_key)

    return channel, queue_name
