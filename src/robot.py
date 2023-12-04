from broker import rabbitmq_consumer
from tools import *
import functools


class Robot:
    def __init__(self, role, tool):
        self.role = role
        self.tool = tool
        self._set_binding_key()
        self._robot_connect()
        self._robot_consume()

    def _robot_connect(self):
        self.channel, self.queue_name = rabbitmq_consumer(self.binding_key)

    def _robot_consume(self):
        on_message_callback = functools.partial(self.tool.callback, args=self.tool)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=on_message_callback, auto_ack=False)
        self.channel.start_consuming()

    def _set_binding_key(self):
        self.binding_key = "{}.{}.robot".format(self.tool, self.role)


if __name__ == "__main__":
    Rci = Robot("chef", ingredients.IngredientsTool(["tomatoes", "cheese"], ["pick.chef.robot"]))
    Rcp = Robot("chef", pick.PickTool(["ingredients.chef.robot"]))

    Rpd = Robot("prod", delivery.DeliveryTool(["slicer.prod.robot"]))
    Rps = Robot("prod", slicer.SliceTool(["delivery.prod.robot"]))
