from time import sleep

from broker import rabbitmq_producer


class DeliveryTool:
    def __init__(self, coworker_communication):
        self.coworker_communication = coworker_communication

    def deliver_pizza_box(self, shelf_position):
        print("Pack pizza and put it into shelf position {}".format(shelf_position))
        # Here there should be placed a communication with the robot to trigger the sequence. Serial port maybe?
        # This applies for all sequences
        sleep(5)

    def pick_pizza_oven_sequence(self, oven):
        # Perform some accion
        print("Picking the pizza from the oven {} and placing it in the box".format(oven))
        sleep(5)

    @staticmethod
    def callback(ch, method, properties, body, **args):
        print(" [x] %r:%r" % (method.routing_key, body))
        thisTool = args["args"]
        list_body = str(body).split(":")
        channel = rabbitmq_producer()

        if "shelf_monitoring" in list_body:
            thisTool.deliver_pizza_box(shelf_position=list_body[1])
        elif "oven_monitoring" in list_body:
            thisTool.pick_pizza_oven_sequence(oven=list_body[1])
        # Else: raise some error or just skip

        for destination_route in thisTool.coworker_communication:
            message = b"Task successfully completed"

            channel.basic_publish(exchange="topic_logs", routing_key=destination_route, body=message)

    def __repr__(self):
        return "delivery"
