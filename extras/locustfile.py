import random

from locust import TaskSet, HttpLocust, task
from urllib.parse import urlencode


class ApiClientBehavior(TaskSet):
    """
    The @task decorator declares a locust task.
    The argument passed the task decorator determines
    the relative frequency with which the task
    will be spawned within a swarm. For example
    a task with a relative frequency of 1 will be
    spawned half as often as a task with a
    relative frequency of 2.
    """

    @task(1)
    def quick_check(self):
        self.client.get("/", name='/', headers={"Accept": "application/json"})

    @task(2)
    def get_current(self):
        self.client.get("/current", name='/current', headers={"Accept": "application/json"})

    @task(3)
    def predict_from_city_linear(self):
        cities = ["paris,fr", "london,uk", "berlin,de", "beijing,cn", "stockholm,se"]
        params = urlencode({'model': 'linear', 'city': random.choice(cities)})
        self.client.get("/predict_from_city?" + params,
            name='/predict_from_city',
            headers={"Accept": "application/json"})

    @task(4)
    def predict_from_values_linear(self):
        params = urlencode({
            'model': 'linear',
            'temp_max': round(random.uniform(0.0, 100.0), 2),
            'temp_min': round(random.uniform(0.0, 100.0), 2),
            'pressure': round(random.uniform(0.0, 100.0), 2),
            'humidity': round(random.uniform(0.0, 100.0), 2)
        })
        self.client.get("/predict_from_values?" + params,
            name='/predict_from_values',
            headers={"Accept": "application/json"})

    @task(5)
    def predict_from_city_dnn(self):
        cities = ["paris,fr", "london,uk", "berlin,de", "beijing,cn", "stockholm,se"]
        params = urlencode({'model': 'dnn', 'city': random.choice(cities)})
        self.client.get("/predict_from_city?" + params,
            name='/predict_from_city',
            headers={"Accept": "application/json"})

    @task(6)
    def predict_from_values_dnn(self):
        params = urlencode({
            'model': 'dnn',
            'temp_max': round(random.uniform(0.0, 100.0), 2),
            'temp_min': round(random.uniform(0.0, 100.0), 2),
            'pressure': round(random.uniform(0.0, 100.0), 2),
            'humidity': round(random.uniform(0.0, 100.0), 2)
        })
        self.client.get("/predict_from_values?" + params,
            name='/predict_from_values',
            headers={"Accept": "application/json"})


class ApiClient(HttpLocust):
    task_set = ApiClientBehavior

    # How long should a task wait after the batch
    # member is spawned before executing. This creates
    # randomness in the traffic patterns rather than
    # having every member of the batch try to execute
    # at once.
    min_wait = 1000
    max_wait = 5000
