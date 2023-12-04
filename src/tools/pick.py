from time import sleep
from broker import rabbitmq_producer


class PickTool:
    def __init__(self, coworker_communication):
        self.coworker_communication = coworker_communication

    def put_pizza_into_oven_sequence(self, oven):
        print("Placing pizza in the oven {}...".format(oven))
        sleep(3)

    def pick_pizza_sequence(self):
        print("Picking the pizza and place it on the work desk...")
        sleep(3)

    @staticmethod
    def callback(ch, method, properties, body, **args):
        print(" [x] %r:%r" % (method.routing_key, body))
        thisTool = args["args"]
        list_body = str(body).split(":")
        channel = rabbitmq_producer()

        if "fridge_monitoring" in list_body[0]:
            thisTool.deliver_pizza_box(shelf_position=list_body[1])
        elif "oven_monitoring" in list_body[0]:
            thisTool.pick_pizza_ove_sequence(oven=list_body[1])
        # Else: raise some error or just skip

        for destination_route in thisTool.coworker_communication:
            message = b"Task successfully completed"

            channel.basic_publish(exchange="topic_logs", routing_key=destination_route, body=message)

    def __repr__(self):
        return "pick"
