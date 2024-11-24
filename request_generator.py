import time
import random


def generate_random_requests(elevator, duration, interval=3):
    start_time = time.time()
    while time.time() - start_time < duration:
        random_floor = random.randint(1, elevator.total_floors)
        elevator.add_request(random_floor)
        time.sleep(random.uniform(1, interval))
