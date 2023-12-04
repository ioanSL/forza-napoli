from time import sleep
from broker import rabbitmq_producer


class SliceTool:
    def __init__(self, coworker_communication):
        self.coworker_communication = coworker_communication

    def slice_sequence(self):
        # Perform some accion
        print("Slicing pizza into beautiful pieces...")
        sleep(10)

    @staticmethod
    def callback(ch, method, properties, body, **args):
        print(" [x] %r:%r" % (method.routing_key, body))
        thisTool = args["args"]
        thisTool.simulate_work_sequence()
        channel = rabbitmq_producer()
        for destination_route in thisTool.coworker_communication:
            message = b"Task successfully completed"

            channel.basic_publish(exchange="topic_logs", routing_key=destination_route, body=message)

    def __repr__(self):
        return "slice"
