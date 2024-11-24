import threading
from elevator import Elevator
from request_generator import generate_random_requests
import config
import time


def run_simulation():
    elevator = Elevator(total_floors=config.TOTAL_FLOORS)

    request_thread = threading.Thread(
        target=generate_random_requests,
        args=(elevator, config.SIMULATION_TIME, config.REQUEST_INTERVAL),
        daemon=True
    )
    request_thread.start()

    start_time = time.time()
    while time.time() - start_time < config.SIMULATION_TIME:
        elevator.process_requests()

    print("Simulation ended. Final state:")
    print(f"Elevator on floor {elevator.current_floor}, direction: {elevator.direction}")


if __name__ == "__main__":
    run_simulation()
