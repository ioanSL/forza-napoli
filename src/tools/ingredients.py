from time import sleep
from broker import rabbitmq_producer


class IngredientsTool:
    def __init__(self, ingredients, coworker_communication):
        self.ingredients = ingredients
        self.coworker_communication = coworker_communication

    def ingredients_sequence(self):
        for ingredient in self.ingredients:
            print("Adding {} ...".format(ingredient))
            sleep(5)

    @staticmethod
    def callback(ch, method, properties, body, **args):
        print(" [x] %r:%r" % (method.routing_key, body))
        thisTool = args["args"]
        thisTool.ingredients_sequence()
        #thisTool.simulate_work_sequence()
        channel = rabbitmq_producer()
        for destination_route in thisTool.coworker_communication:
            message = b"Task successfully completed"

            channel.basic_publish(exchange="topic_logs", routing_key=destination_route, body=message)

    def __repr__(self):
        return "ingredients"


if __name__ == "__main__":
    IngredientTool = IngredientsTool(["tomatoes", "cheese"])
