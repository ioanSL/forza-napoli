from time import sleep
from broker import rabbitmq_producer


class Camera:
    def __init__(self, name, route_destination, number_signals, signals_initial_state):
        self.name = name
        self.channel = rabbitmq_producer()
        self.routing_key = route_destination
        self.signals = [signals_initial_state for _ in range(number_signals)]
        self.simulate_trigger_signal()

    def simulate_trigger_signal(self):
        while True:
            for i in range(len(self.signals)):
                if self.signals[i]:
                    message = "{}:{}:{}".format(self.name, i, self.signals[i])
                    self.signals[i] = not self.signals[i]
                    self.channel.basic_publish(exchange="topic_logs", routing_key=self.routing_key, body=message)
                    print(" [x] %s Sent %r:%r" % (self.name, self.routing_key, message))
                    sleep(5)


if __name__ == "__main__":
    # Example of the ingredients quality camera
    C_ingredient_quality = Camera(
        name="ingredients_monitoring",
        route_destination="ingredients.chef.robot",
        number_signals=1,
        signals_initial_state=True,
    )

    C_shelf_monitor = Camera(
        name="shelf_monitoring",
        route_destination="delivery.prod.robot",
        number_signals=8,
        signals_initial_state=True,
    )

    C_oven_monitor = Camera(
        name="oven_monitoring",
        route_destination="delivery.prod.robot",
        number_signals=1,
        signals_initial_state=True,
    )
